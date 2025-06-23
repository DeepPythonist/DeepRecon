import requests
import socket
import dns.resolver
from typing import List, Dict, Union
from .utils.validator import validate_domain, validate_ip, normalize_domain
from .config import HTTP_TIMEOUT, DEFAULT_USER_AGENT, BLACKLIST_PROVIDERS, WAF_SIGNATURES
from .availability import get_response_headers

def is_filtered(target: str, test_ports: List[int] = None) -> Union[bool, None]:
    ip_valid, _ = validate_ip(target)
    domain_valid, _ = validate_domain(target)
    
    if not (ip_valid or domain_valid):
        return None
    
    if domain_valid:
        target = normalize_domain(target)
    
    if test_ports is None:
        test_ports = [80, 443]
    
    filtered_count = 0
    
    for port in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            if domain_valid:
                ip = socket.gethostbyname(target)
            else:
                ip = target
            
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result != 0:
                filtered_count += 1
        except:
            filtered_count += 1
    
    return filtered_count == len(test_ports)

def check_blacklists(target: str) -> Dict[str, bool]:
    ip_valid, _ = validate_ip(target)
    domain_valid, _ = validate_domain(target)
    
    if not (ip_valid or domain_valid):
        return {}
    
    if domain_valid:
        try:
            target = socket.gethostbyname(normalize_domain(target))
        except:
            return {}
    
    octets = target.split('.')
    reversed_ip = '.'.join(reversed(octets))
    
    results = {}
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2
    
    for blacklist in BLACKLIST_PROVIDERS:
        query = f"{reversed_ip}.{blacklist}"
        try:
            resolver.resolve(query, 'A')
            results[blacklist] = True
        except:
            results[blacklist] = False
    
    return results

def is_cloudflare_protected(domain: str) -> bool:
    valid, error = validate_domain(domain)
    if not valid:
        return False
    
    domain = normalize_domain(domain)
    
    try:
        headers = get_response_headers(domain)
        
        cf_headers = ['CF-RAY', 'CF-Cache-Status', 'cf-request-id']
        for header in cf_headers:
            if header in headers:
                return True
        
        if headers.get('Server', '').lower() == 'cloudflare':
            return True
        
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, 'A')
        
        for rdata in answers:
            ip = str(rdata)
            try:
                ptr = socket.gethostbyaddr(ip)[0]
                if 'cloudflare' in ptr.lower():
                    return True
            except:
                pass
    
    except:
        pass
    
    return False

def has_waf(domain: str) -> Union[str, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    
    try:
        headers = get_response_headers(domain)
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        
        for waf_name, signatures in WAF_SIGNATURES.items():
            for signature in signatures:
                if signature.lower() in str(headers_lower):
                    return waf_name
        
        response = requests.get(
            f'https://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT}
        )
        
        page_content = response.text.lower()
        
        waf_patterns = {
            'cloudflare': ['cloudflare', 'cf-ray'],
            'akamai': ['akamai', 'akamaighost'],
            'incapsula': ['incapsula', 'incap_ses'],
            'aws': ['awselb', 'amazonws'],
            'sucuri': ['sucuri', 'x-sucuri'],
            'barracuda': ['barracuda', 'barra'],
            'f5': ['f5-bigip', 'x-waf-status'],
            'fortinet': ['fortigate', 'fortiweb'],
            'modsecurity': ['mod_security', 'modsecurity']
        }
        
        for waf_name, patterns in waf_patterns.items():
            for pattern in patterns:
                if pattern in page_content:
                    return waf_name
    
    except:
        pass
    
    return None

def is_https_forced(domain: str) -> bool:
    valid, error = validate_domain(domain)
    if not valid:
        return False
    
    domain = normalize_domain(domain)
    
    try:
        response = requests.get(
            f'http://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT},
            allow_redirects=False
        )
        
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '')
            if location.startswith('https://'):
                return True
        
        hsts_header = response.headers.get('Strict-Transport-Security')
        if hsts_header:
            return True
    
    except:
        pass
    
    return False

def check_security_headers(domain: str) -> Dict[str, bool]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    
    security_headers = {
        'Strict-Transport-Security': False,
        'X-Frame-Options': False,
        'X-Content-Type-Options': False,
        'X-XSS-Protection': False,
        'Content-Security-Policy': False,
        'Referrer-Policy': False,
        'Permissions-Policy': False
    }
    
    try:
        headers = get_response_headers(domain, https=True)
        
        for header in security_headers:
            if header in headers:
                security_headers[header] = True
    
    except:
        pass
    
    return security_headers

def get_security_score(domain: str) -> int:
    score = 0
    
    if is_https_forced(domain):
        score += 20
    
    if is_cloudflare_protected(domain) or has_waf(domain):
        score += 20
    
    headers = check_security_headers(domain)
    header_score = sum(1 for enabled in headers.values() if enabled)
    score += header_score * 8
    
    try:
        from .ssl import check_ssl_validity, ssl_grade
        
        if check_ssl_validity(domain):
            score += 10
        
        grade = ssl_grade(domain)
        if grade:
            grade_scores = {'A+': 10, 'A': 8, 'B': 6, 'C': 4, 'D': 2, 'F': 0}
            score += grade_scores.get(grade, 0)
    except:
        pass
    
    return min(score, 100)
