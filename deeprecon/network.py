import socket
import subprocess
import platform
import threading
import time
import struct
from typing import Dict, List, Union, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils.validator import validate_ip, validate_domain, normalize_domain, is_valid_port
from .config import NETWORK_SCAN_TIMEOUT, NETWORK_DISCOVERY_TIMEOUT, PORT_SCAN_TIMEOUT, PING_COUNT, MAX_THREADS

try:
    import psutil
    import netifaces
    HAS_PSUTIL = True
    HAS_NETIFACES = True
except ImportError:
    HAS_PSUTIL = False
    HAS_NETIFACES = False

try:
    import nmap
    HAS_NMAP = False
except ImportError:
    HAS_NMAP = False

def get_network_interfaces() -> Dict[str, Dict]:
    interfaces = {}
    
    if HAS_NETIFACES:
        for interface in netifaces.interfaces():
            if interface == 'lo':
                continue
                
            interface_info = {}
            addrs = netifaces.ifaddresses(interface)
            
            if netifaces.AF_INET in addrs:
                ipv4 = addrs[netifaces.AF_INET][0]
                interface_info.update({
                    'ip': ipv4.get('addr'),
                    'netmask': ipv4.get('netmask'),
                    'broadcast': ipv4.get('broadcast')
                })
            
            if netifaces.AF_LINK in addrs:
                mac_info = addrs[netifaces.AF_LINK][0]
                interface_info['mac'] = mac_info.get('addr')
            
            interface_info['status'] = 'up' if interface_info.get('ip') else 'down'
            interfaces[interface] = interface_info
    
    elif HAS_PSUTIL:
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for interface, addrs in net_if_addrs.items():
            if interface == 'lo':
                continue
                
            interface_info = {'status': 'down'}
            
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    interface_info.update({
                        'ip': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast,
                        'status': 'up'
                    })
                elif addr.family == psutil.AF_LINK:
                    interface_info['mac'] = addr.address
            
            if interface in net_if_stats:
                stats = net_if_stats[interface]
                interface_info['speed'] = f"{stats.speed} Mbps" if stats.speed > 0 else "Unknown"
            
            interfaces[interface] = interface_info
    
    return interfaces

def _ping_host(ip: str) -> Tuple[bool, float]:
    try:
        if platform.system().lower() == 'windows':
            cmd = ['ping', '-n', '1', '-w', '1000', ip]
        else:
            cmd = ['ping', '-c', '1', '-W', '1', ip]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, timeout=3)
        end_time = time.time()
        
        if result.returncode == 0:
            return True, (end_time - start_time) * 1000
        return False, 0
    except:
        return False, 0

def _get_mac_from_arp(ip: str) -> Union[str, None]:
    try:
        if platform.system().lower() == 'windows':
            cmd = ['arp', '-a', ip]
        else:
            cmd = ['arp', '-n', ip]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if ip in line:
                    parts = line.split()
                    for part in parts:
                        if ':' in part and len(part) == 17:
                            return part.lower()
                        elif '-' in part and len(part) == 17:
                            return part.replace('-', ':').lower()
        return None
    except:
        return None

def scan_network_devices(subnet: str = None) -> List[Dict]:
    devices = []
    
    if not subnet:
        interfaces = get_network_interfaces()
        for interface_info in interfaces.values():
            if interface_info.get('ip') and interface_info.get('netmask'):
                ip = interface_info['ip']
                netmask = interface_info['netmask']
                subnet = f"{'.'.join(ip.split('.')[:-1])}.0/24"
                break
    
    if not subnet:
        return devices
    
    network_base = subnet.split('/')[0]
    base_parts = network_base.split('.')
    
    def scan_ip(i):
        ip = f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{i}"
        is_alive, response_time = _ping_host(ip)
        
        if is_alive:
            device_info = {
                'ip': ip,
                'response_time': round(response_time, 2),
                'mac': _get_mac_from_arp(ip),
                'hostname': None,
                'vendor': None
            }
            
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                device_info['hostname'] = hostname
            except:
                pass
            
            return device_info
        return None
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_ip, i): i for i in range(1, 255)}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                devices.append(result)
    
    return sorted(devices, key=lambda x: int(x['ip'].split('.')[-1]))

def _scan_port(ip: str, port: int, timeout: int = 1) -> Dict:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            service = socket.getservbyport(port, 'tcp') if port < 65536 else 'unknown'
            return {
                'port': port,
                'state': 'open',
                'service': service
            }
    except:
        pass
    
    return None

def advanced_port_scan(target: str, port_range: str = '1-1000') -> Dict:
    ip_valid, _ = validate_ip(target)
    domain_valid, _ = validate_domain(target)
    
    if not (ip_valid or domain_valid):
        return {}
    
    if domain_valid:
        try:
            target = socket.gethostbyname(normalize_domain(target))
        except:
            return {}
    
    ports_to_scan = []
    
    if '-' in port_range:
        start, end = map(int, port_range.split('-'))
        ports_to_scan = list(range(start, end + 1))
    elif ',' in port_range:
        ports_to_scan = [int(p.strip()) for p in port_range.split(',')]
    else:
        ports_to_scan = [int(port_range)]
    
    open_ports = []
    
    def scan_port_worker(port):
        return _scan_port(target, port)
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(scan_port_worker, port): port for port in ports_to_scan}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    
    return {
        'target': target,
        'total_ports_scanned': len(ports_to_scan),
        'open_ports': sorted(open_ports, key=lambda x: x['port']),
        'open_count': len(open_ports),
        'closed_count': len(ports_to_scan) - len(open_ports)
    }

def network_performance() -> Dict:
    performance_data = {}
    
    if HAS_PSUTIL:
        net_io = psutil.net_io_counters()
        performance_data['interface_stats'] = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout,
            'dropin': net_io.dropin,
            'dropout': net_io.dropout
        }
        
        per_nic = psutil.net_io_counters(pernic=True)
        performance_data['per_interface'] = {}
        
        for interface, stats in per_nic.items():
            if interface != 'lo':
                performance_data['per_interface'][interface] = {
                    'bytes_sent': stats.bytes_sent,
                    'bytes_recv': stats.bytes_recv,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv
                }
    
    gateways = []
    try:
        if platform.system().lower() == 'windows':
            result = subprocess.run(['route', 'print', '0.0.0.0'], capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(['route', '-n'], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if '0.0.0.0' in line or 'default' in line:
                    parts = line.split()
                    for part in parts:
                        if validate_ip(part)[0]:
                            gateways.append(part)
                            break
    except:
        pass
    
    gateway_latency = {}
    for gateway in set(gateways):
        is_alive, latency = _ping_host(gateway)
        if is_alive:
            gateway_latency[gateway] = round(latency, 2)
    
    performance_data['gateways'] = gateway_latency
    
    return performance_data

def network_security_scan() -> Dict:
    security_data = {
        'open_services': [],
        'suspicious_ports': [],
        'network_shares': [],
        'security_score': 100
    }
    
    interfaces = get_network_interfaces()
    local_ips = [info.get('ip') for info in interfaces.values() if info.get('ip')]
    
    suspicious_ports = [21, 23, 135, 139, 445, 1433, 3389, 5900]
    
    for ip in local_ips:
        if ip and not ip.startswith('127.'):
            for port in suspicious_ports:
                port_result = _scan_port(ip, port, timeout=2)
                if port_result:
                    security_data['suspicious_ports'].append({
                        'ip': ip,
                        'port': port,
                        'service': port_result.get('service', 'unknown'),
                        'risk': 'high' if port in [21, 23, 135] else 'medium'
                    })
    
    if platform.system().lower() == 'windows':
        try:
            result = subprocess.run(['net', 'share'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if '$' not in line and 'Share name' not in line and line.strip():
                        parts = line.split()
                        if parts:
                            security_data['network_shares'].append(parts[0])
        except:
            pass
    else:
        try:
            result = subprocess.run(['showmount', '-e', 'localhost'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.split('\n')[1:]
                for line in lines:
                    if line.strip():
                        security_data['network_shares'].append(line.split()[0])
        except:
            pass
    
    score_deduction = 0
    score_deduction += len(security_data['suspicious_ports']) * 10
    score_deduction += len(security_data['network_shares']) * 5
    
    security_data['security_score'] = max(0, 100 - score_deduction)
    
    return security_data 