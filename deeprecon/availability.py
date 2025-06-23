import subprocess
import platform
import requests
import socket
import time
from typing import Dict, Union, List, Tuple
from .utils.validator import validate_domain, validate_ip, normalize_domain, is_valid_port
from .config import PING_TIMEOUT, HTTP_TIMEOUT, DEFAULT_USER_AGENT

def ping(target: str, count: int = 4) -> Dict[str, Union[bool, float, int, str]]:
    ip_valid, _ = validate_ip(target)
    domain_valid, _ = validate_domain(target)
    
    if not (ip_valid or domain_valid):
        return {'success': False, 'error': 'invalid_target'}
    
    if domain_valid:
        target = normalize_domain(target)
    
    try:
        if platform.system().lower() == 'windows':
            cmd = ['ping', '-n', str(count), target]
        else:
            cmd = ['ping', '-c', str(count), '-W', str(PING_TIMEOUT), target]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=PING_TIMEOUT * count)
        
        if result.returncode == 0:
            output = result.stdout
            
            if 'min/avg/max' in output:
                times = output.split('min/avg/max')[1].split('=')[1].strip().split('/')[1]
                avg_time = float(times.split()[0])
            else:
                lines = output.split('\n')
                total_time = 0
                successful_pings = 0
                
                for line in lines:
                    if 'time=' in line:
                        time_str = line.split('time=')[1].split()[0]
                        total_time += float(time_str.replace('ms', ''))
                        successful_pings += 1
                
                avg_time = total_time / successful_pings if successful_pings > 0 else 0
            
            return {
                'success': True,
                'average_time': avg_time,
                'packet_loss': 0
            }
    
    except Exception:
        pass
    
    return {'success': False, 'average_time': None, 'packet_loss': 100}

def is_up(domain: str) -> bool:
    valid, error = validate_domain(domain)
    if not valid:
        return False
    
    domain = normalize_domain(domain)
    
    try:
        socket.setdefaulttimeout(PING_TIMEOUT)
        socket.gethostbyname(domain)
        return True
    except:
        return False

def get_http_status(domain: str, https: bool = True) -> Union[int, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    protocol = 'https' if https else 'http'
    
    try:
        response = requests.head(
            f'{protocol}://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT},
            allow_redirects=True
        )
        return response.status_code
    except:
        return None

def traceroute(target: str, max_hops: int = 30) -> List[Dict[str, Union[str, float, int]]]:
    ip_valid, _ = validate_ip(target)
    domain_valid, _ = validate_domain(target)
    
    if not (ip_valid or domain_valid):
        return []
    
    if domain_valid:
        target = normalize_domain(target)
    
    hops = []
    
    try:
        if platform.system().lower() == 'windows':
            cmd = ['tracert', '-h', str(max_hops), '-w', str(PING_TIMEOUT * 1000), target]
        else:
            cmd = ['traceroute', '-m', str(max_hops), '-w', str(PING_TIMEOUT), target]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=max_hops * PING_TIMEOUT)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')[1:]
            
            for line in lines:
                if line.strip() and not line.startswith('traceroute'):
                    parts = line.split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        hop_num = int(parts[0])
                        
                        if '(' in line and ')' in line:
                            ip = line.split('(')[1].split(')')[0]
                            hostname = parts[1]
                        else:
                            ip = parts[1] if len(parts) > 1 else None
                            hostname = None
                        
                        hops.append({
                            'hop': hop_num,
                            'ip': ip,
                            'hostname': hostname
                        })
    
    except Exception:
        pass
    
    return hops

def tcp_port_check(ip: str, port: int) -> bool:
    valid, error = validate_ip(ip)
    if not valid or not is_valid_port(port):
        return False
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(PING_TIMEOUT)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def get_response_headers(domain: str, https: bool = True) -> Dict[str, str]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    protocol = 'https' if https else 'http'
    
    try:
        response = requests.head(
            f'{protocol}://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT},
            allow_redirects=False
        )
        return dict(response.headers)
    except:
        return {}

def check_port_range(ip: str, start_port: int = 1, end_port: int = 1000) -> List[int]:
    valid, error = validate_ip(ip)
    if not valid:
        return []
    
    open_ports = []
    
    for port in range(start_port, min(end_port + 1, 65536)):
        if tcp_port_check(ip, port):
            open_ports.append(port)
    
    return open_ports

def measure_response_time(domain: str, https: bool = True) -> Union[float, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    protocol = 'https' if https else 'http'
    
    try:
        start_time = time.time()
        response = requests.get(
            f'{protocol}://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT}
        )
        end_time = time.time()
        
        if response.status_code < 400:
            return (end_time - start_time) * 1000
    except:
        pass
    
    return None
