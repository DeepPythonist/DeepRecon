import requests
from typing import Dict, Union
from .utils.validator import validate_ip
from .config import DEFAULT_TIMEOUT

def geoip(ip: str) -> Dict[str, Union[str, float, None]]:
    valid, error = validate_ip(ip)
    if not valid:
        return {}
    
    try:
        response = requests.get(
            f'http://ip-api.com/json/{ip}',
            timeout=DEFAULT_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'ip': data.get('query'),
                    'country': data.get('country'),
                    'country_code': data.get('countryCode'),
                    'region': data.get('regionName'),
                    'region_code': data.get('region'),
                    'city': data.get('city'),
                    'zip': data.get('zip'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'as': data.get('as')
                }
    except Exception:
        pass
    
    return {}

def get_asn(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    as_info = geo_info.get('as')
    
    if as_info:
        parts = as_info.split(' ', 1)
        if parts:
            return parts[0]
    
    return None

def get_org(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    return geo_info.get('org')

def get_timezone(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    return geo_info.get('timezone')

def get_location_flag(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    country_code = geo_info.get('country_code')
    
    if country_code:
        return f'https://flagcdn.com/w320/{country_code.lower()}.png'
    
    return None

def get_coordinates(ip: str) -> Dict[str, Union[float, None]]:
    geo_info = geoip(ip)
    return {
        'latitude': geo_info.get('lat'),
        'longitude': geo_info.get('lon')
    }

def get_country(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    return geo_info.get('country')

def get_city(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    return geo_info.get('city')

def get_isp(ip: str) -> Union[str, None]:
    geo_info = geoip(ip)
    return geo_info.get('isp')
