import re
import ipaddress
from typing import Union, Tuple

def validate_ip(ip: str) -> Tuple[bool, Union[str, None]]:
    try:
        ipaddress.ip_address(ip)
        return True, None
    except ValueError:
        return False, "invalid_ip"

def validate_domain(domain: str) -> Tuple[bool, Union[str, None]]:
    domain = domain.lower().strip()
    if not domain:
        return False, "invalid_domain"
    
    domain_pattern = re.compile(
        r'^(([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)*'
        r'[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)$'
    )
    
    if domain_pattern.match(domain):
        return True, None
    return False, "invalid_domain"

def is_private_ip(ip: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

def normalize_domain(domain: str) -> str:
    domain = domain.lower().strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    domain = domain.split('/')[0]
    domain = domain.split(':')[0]
    return domain

def extract_domain_from_url(url: str) -> str:
    url = url.lower().strip()
    url = re.sub(r'^https?://', '', url)
    return url.split('/')[0]

def is_valid_port(port: int) -> bool:
    return 0 < port <= 65535

def get_ip_version(ip: str) -> Union[int, None]:
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.version
    except ValueError:
        return None
