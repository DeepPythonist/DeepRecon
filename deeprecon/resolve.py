import socket
from typing import List, Union, Dict
from .utils.validator import validate_ip, validate_domain, normalize_domain
from .config import DEFAULT_TIMEOUT

def get_ip(domain: str) -> Union[str, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    
    try:
        socket.setdefaulttimeout(DEFAULT_TIMEOUT)
        ip = socket.gethostbyname(domain)
        return ip
    except (socket.gaierror, socket.timeout):
        return None

def get_ips(domain: str) -> List[str]:
    valid, error = validate_domain(domain)
    if not valid:
        return []
    
    domain = normalize_domain(domain)
    
    try:
        socket.setdefaulttimeout(DEFAULT_TIMEOUT)
        host_info = socket.getaddrinfo(domain, None)
        ips = list(set([info[4][0] for info in host_info]))
        return ips
    except (socket.gaierror, socket.timeout):
        return []

def get_domain(ip: str) -> Union[str, None]:
    valid, error = validate_ip(ip)
    if not valid:
        return None
    
    try:
        socket.setdefaulttimeout(DEFAULT_TIMEOUT)
        domain, _, _ = socket.gethostbyaddr(ip)
        return domain
    except (socket.herror, socket.timeout):
        return None

def resolve_all(target: str) -> Dict[str, Union[str, List[str], None]]:
    result = {
        'input': target,
        'type': None,
        'ip': None,
        'ips': [],
        'domain': None
    }
    
    ip_valid, _ = validate_ip(target)
    domain_valid, _ = validate_domain(target)
    
    if ip_valid:
        result['type'] = 'ip'
        result['ip'] = target
        result['domain'] = get_domain(target)
    elif domain_valid:
        result['type'] = 'domain'
        result['domain'] = normalize_domain(target)
        result['ip'] = get_ip(target)
        result['ips'] = get_ips(target)
    
    return result
