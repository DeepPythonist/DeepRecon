import ssl
import socket
import OpenSSL
from datetime import datetime
from typing import Dict, Union, List
from .utils.validator import validate_domain, normalize_domain
from .config import SSL_TIMEOUT, SSL_GRADES

def get_ssl_info(domain: str) -> Dict[str, Union[str, datetime, List[str], None]]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    
    try:
        context = ssl.create_default_context()
        
        with socket.create_connection((domain, 443), timeout=SSL_TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                
                return {
                    'subject': dict(x[0] for x in cert.get('subject', [])),
                    'issuer': dict(x[0] for x in cert.get('issuer', [])),
                    'version': cert.get('version'),
                    'serialNumber': cert.get('serialNumber'),
                    'notBefore': not_before,
                    'notAfter': not_after,
                    'subjectAltName': [x[1] for x in cert.get('subjectAltName', [])],
                    'OCSP': cert.get('OCSP'),
                    'caIssuers': cert.get('caIssuers'),
                    'crlDistributionPoints': cert.get('crlDistributionPoints')
                }
    
    except Exception:
        return {}

def check_ssl_validity(domain: str) -> Union[bool, None]:
    ssl_info = get_ssl_info(domain)
    
    if ssl_info and 'notBefore' in ssl_info and 'notAfter' in ssl_info:
        now = datetime.now()
        return ssl_info['notBefore'] <= now <= ssl_info['notAfter']
    
    return None

def check_ssl_expiry(domain: str) -> Union[int, None]:
    ssl_info = get_ssl_info(domain)
    
    if ssl_info and 'notAfter' in ssl_info:
        days_left = (ssl_info['notAfter'] - datetime.now()).days
        return days_left
    
    return None

def is_self_signed_ssl(domain: str) -> Union[bool, None]:
    ssl_info = get_ssl_info(domain)
    
    if ssl_info:
        subject = ssl_info.get('subject', {})
        issuer = ssl_info.get('issuer', {})
        
        if subject and issuer:
            return subject == issuer
    
    return None

def ssl_grade(domain: str) -> Union[str, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    
    try:
        context = ssl.create_default_context()
        
        with socket.create_connection((domain, 443), timeout=SSL_TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cipher = ssock.cipher()
                protocol = ssock.version()
                
                if protocol == 'TLSv1.3':
                    return 'A+'
                elif protocol == 'TLSv1.2':
                    if cipher and 'AES' in cipher[0] and 'GCM' in cipher[0]:
                        return 'A'
                    return 'B'
                elif protocol == 'TLSv1.1':
                    return 'C'
                elif protocol == 'TLSv1.0':
                    return 'D'
                else:
                    return 'F'
    
    except Exception:
        return None

def get_certificate_chain(domain: str) -> List[Dict[str, str]]:
    valid, error = validate_domain(domain)
    if not valid:
        return []
    
    domain = normalize_domain(domain)
    
    try:
        cert_pem = ssl.get_server_certificate((domain, 443))
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_pem)
        
        chain = [{
            'subject': str(cert.get_subject()),
            'issuer': str(cert.get_issuer()),
            'serial': str(cert.get_serial_number()),
            'signature_algorithm': cert.get_signature_algorithm().decode('utf-8')
        }]
        
        return chain
    
    except Exception:
        return []
