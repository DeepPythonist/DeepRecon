import whois
from datetime import datetime
from typing import Dict, Union
from .utils.validator import validate_domain, validate_ip, normalize_domain
from .config import DEFAULT_TIMEOUT

def whois_domain(domain: str) -> Dict[str, Union[str, list, datetime, None]]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    
    try:
        w = whois.whois(domain)
        
        result = {
            'domain_name': w.domain_name,
            'registrar': w.registrar,
            'whois_server': w.whois_server,
            'referral_url': w.referral_url,
            'creation_date': w.creation_date,
            'expiration_date': w.expiration_date,
            'updated_date': w.updated_date,
            'name_servers': w.name_servers,
            'status': w.status,
            'emails': w.emails,
            'dnssec': w.dnssec,
            'name': w.name,
            'org': w.org,
            'address': w.address,
            'city': w.city,
            'state': w.state,
            'zipcode': w.zipcode,
            'country': w.country
        }
        
        for key, value in result.items():
            if isinstance(value, list) and len(value) == 1:
                result[key] = value[0]
        
        return {k: v for k, v in result.items() if v is not None}
    
    except Exception:
        return {}

def whois_ip(ip: str) -> Dict[str, Union[str, list, None]]:
    valid, error = validate_ip(ip)
    if not valid:
        return {}
    
    try:
        import ipwhois
        obj = ipwhois.IPWhois(ip)
        results = obj.lookup_rdap(depth=1)
        
        return {
            'asn': results.get('asn'),
            'asn_cidr': results.get('asn_cidr'),
            'asn_country_code': results.get('asn_country_code'),
            'asn_date': results.get('asn_date'),
            'asn_description': results.get('asn_description'),
            'asn_registry': results.get('asn_registry'),
            'network': {
                'cidr': results.get('network', {}).get('cidr'),
                'name': results.get('network', {}).get('name'),
                'country': results.get('network', {}).get('country'),
                'start_address': results.get('network', {}).get('start_address'),
                'end_address': results.get('network', {}).get('end_address')
            }
        }
    
    except Exception:
        return {}

def get_creation_date(domain: str) -> Union[datetime, None]:
    whois_info = whois_domain(domain)
    creation_date = whois_info.get('creation_date')
    
    if isinstance(creation_date, list):
        return creation_date[0] if creation_date else None
    return creation_date

def get_expiry_date(domain: str) -> Union[datetime, None]:
    whois_info = whois_domain(domain)
    expiry_date = whois_info.get('expiration_date')
    
    if isinstance(expiry_date, list):
        return expiry_date[0] if expiry_date else None
    return expiry_date

def get_domain_age(domain: str) -> Union[int, None]:
    creation_date = get_creation_date(domain)
    
    if creation_date:
        if isinstance(creation_date, datetime):
            age = datetime.now() - creation_date
            return age.days
    
    return None

def get_registrar(domain: str) -> Union[str, None]:
    whois_info = whois_domain(domain)
    return whois_info.get('registrar')

def is_domain_expired(domain: str) -> Union[bool, None]:
    expiry_date = get_expiry_date(domain)
    
    if expiry_date:
        if isinstance(expiry_date, datetime):
            return datetime.now() > expiry_date
    
    return None
