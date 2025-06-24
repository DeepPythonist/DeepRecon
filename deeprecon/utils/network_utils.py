import re
import socket
import struct
import subprocess
import platform
import requests
from typing import Dict, List, Union, Tuple
from ..config import DEFAULT_TIMEOUT

def calculate_subnet(ip: str, netmask: str) -> Dict:
    try:
        ip_int = struct.unpack("!I", socket.inet_aton(ip))[0]
        netmask_int = struct.unpack("!I", socket.inet_aton(netmask))[0]
        
        network_int = ip_int & netmask_int
        broadcast_int = network_int | (~netmask_int & 0xffffffff)
        
        network = socket.inet_ntoa(struct.pack("!I", network_int))
        broadcast = socket.inet_ntoa(struct.pack("!I", broadcast_int))
        
        cidr = bin(netmask_int).count('1')
        
        return {
            'network': network,
            'broadcast': broadcast,
            'netmask': netmask,
            'cidr': cidr,
            'subnet': f"{network}/{cidr}",
            'host_count': (2 ** (32 - cidr)) - 2
        }
    except:
        return {}

def mac_vendor_lookup(mac: str) -> str:
    try:
        mac_clean = mac.replace(':', '').replace('-', '').upper()
        if len(mac_clean) >= 6:
            oui = mac_clean[:6]
            
            oui_database = {
                '000C29': 'VMware',
                '080027': 'VirtualBox',
                '525400': 'QEMU',
                '000569': 'VMware',
                '001C42': 'Parallels',
                '001B21': 'Intel',
                '00A0C6': 'Qualcomm',
                '001DD8': 'Apple',
                '8CF8C5': 'Apple',
                'F0F61C': 'Apple',
                '28F076': 'Apple',
                '78CA39': 'Apple'
            }
            
            return oui_database.get(oui, 'Unknown')
    except:
        pass
    
    return 'Unknown'

def parse_arp_table() -> List[Dict]:
    arp_entries = []
    
    try:
        if platform.system().lower() == 'windows':
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if '(' in line and ')' in line:
                    parts = line.split()
                    ip_match = re.search(r'\(([\d.]+)\)', line)
                    mac_match = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', line)
                    
                    if ip_match and mac_match:
                        ip = ip_match.group(1)
                        mac = mac_match.group(0).lower()
                        
                        arp_entries.append({
                            'ip': ip,
                            'mac': mac,
                            'vendor': mac_vendor_lookup(mac)
                        })
    except:
        pass
    
    return arp_entries

def get_routing_table() -> List[Dict]:
    routes = []
    
    try:
        if platform.system().lower() == 'windows':
            result = subprocess.run(['route', 'print'], capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(['route', '-n'], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if '0.0.0.0' in line or 'default' in line or re.match(r'^\d+\.\d+\.\d+\.\d+', line.strip()):
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            if platform.system().lower() == 'windows':
                                if len(parts) >= 4:
                                    routes.append({
                                        'destination': parts[0],
                                        'netmask': parts[1],
                                        'gateway': parts[2],
                                        'interface': parts[3] if len(parts) > 3 else '',
                                        'metric': parts[4] if len(parts) > 4 else '0'
                                    })
                            else:
                                routes.append({
                                    'destination': parts[0],
                                    'gateway': parts[1],
                                    'netmask': parts[2] if len(parts) > 2 else '',
                                    'interface': parts[-1],
                                    'metric': '0'
                                })
                        except:
                            continue
    except:
        pass
    
    return routes

def network_speed_test() -> Dict:
    speed_data = {
        'download': 0,
        'upload': 0,
        'ping': 0,
        'server': 'Unknown'
    }
    
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        
        speed_data['download'] = round(st.download() / 1024 / 1024, 2)
        speed_data['upload'] = round(st.upload() / 1024 / 1024, 2)
        speed_data['ping'] = round(st.results.ping, 2)
        speed_data['server'] = st.results.server.get('sponsor', 'Unknown')
        
    except ImportError:
        pass
    except:
        pass
    
    return speed_data

def port_knock(target: str, ports: List[int], delay: float = 0.5) -> bool:
    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect_ex((target, port))
            sock.close()
            
            import time
            time.sleep(delay)
        
        return True
    except:
        return False

def get_public_ip() -> Union[str, None]:
    services = [
        'https://api.ipify.org',
        'https://icanhazip.com',
        'https://ident.me',
        'https://ipecho.net/plain'
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                ip = response.text.strip()
                if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip):
                    return ip
        except:
            continue
    
    return None

def is_port_open(ip: str, port: int, timeout: int = 3) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False