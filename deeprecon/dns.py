import dns.resolver
import dns.reversename
from typing import List, Dict, Union
from .utils.validator import validate_domain, validate_ip, normalize_domain
from .config import DNS_TIMEOUT, DEFAULT_DNS_SERVERS

def _get_resolver():
    resolver = dns.resolver.Resolver()
    resolver.nameservers = DEFAULT_DNS_SERVERS
    resolver.timeout = DNS_TIMEOUT
    resolver.lifetime = DNS_TIMEOUT
    return resolver

def get_dns_records(domain: str) -> Dict[str, List[str]]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    resolver = _get_resolver()
    records = {}
    
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
    
    for record_type in record_types:
        try:
            answers = resolver.resolve(domain, record_type)
            records[record_type] = []
            for rdata in answers:
                if record_type == 'MX':
                    records[record_type].append(f"{rdata.preference} {rdata.exchange}")
                elif record_type == 'SOA':
                    records[record_type].append(f"{rdata.mname} {rdata.rname}")
                else:
                    records[record_type].append(str(rdata))
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
            pass
    
    return records

def get_ns_records(domain: str) -> List[str]:
    valid, error = validate_domain(domain)
    if not valid:
        return []
    
    domain = normalize_domain(domain)
    resolver = _get_resolver()
    
    try:
        answers = resolver.resolve(domain, 'NS')
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
        return []

def get_cname(domain: str) -> Union[str, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    resolver = _get_resolver()
    
    try:
        answers = resolver.resolve(domain, 'CNAME')
        for rdata in answers:
            return str(rdata)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
        return None

def get_ptr(ip: str) -> Union[str, None]:
    valid, error = validate_ip(ip)
    if not valid:
        return None
    
    resolver = _get_resolver()
    
    try:
        rev_name = dns.reversename.from_address(ip)
        answers = resolver.resolve(rev_name, 'PTR')
        for rdata in answers:
            return str(rdata)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
        return None

def get_mx_records(domain: str) -> List[Dict[str, Union[str, int]]]:
    valid, error = validate_domain(domain)
    if not valid:
        return []
    
    domain = normalize_domain(domain)
    resolver = _get_resolver()
    
    try:
        answers = resolver.resolve(domain, 'MX')
        mx_records = []
        for rdata in answers:
            mx_records.append({
                'priority': rdata.preference,
                'host': str(rdata.exchange)
            })
        return sorted(mx_records, key=lambda x: x['priority'])
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
        return []
