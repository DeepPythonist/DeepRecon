import re
import requests
from typing import List, Dict, Union
from .utils.validator import validate_domain, normalize_domain
from .config import HTTP_TIMEOUT, DEFAULT_USER_AGENT, TECH_PATTERNS, MAX_REDIRECT_CHAIN
from .availability import get_response_headers

def detect_technologies(domain: str) -> Dict[str, List[str]]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    
    technologies = {
        'server': [],
        'frameworks': [],
        'cms': [],
        'analytics': [],
        'cdn': [],
        'programming_languages': [],
        'javascript_libraries': []
    }
    
    try:
        headers = get_response_headers(domain, https=True)
        if not headers:
            headers = get_response_headers(domain, https=False)
        
        server_header = headers.get('Server', '').lower()
        for tech, pattern in TECH_PATTERNS.items():
            if re.search(pattern, server_header, re.IGNORECASE):
                technologies['server'].append(tech)
        
        x_powered_by = headers.get('X-Powered-By', '').lower()
        if 'php' in x_powered_by:
            technologies['programming_languages'].append('PHP')
        if 'asp.net' in x_powered_by:
            technologies['programming_languages'].append('ASP.NET')
        if 'express' in x_powered_by:
            technologies['frameworks'].append('Express.js')
        
        response = requests.get(
            f'https://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT}
        )
        
        content = response.text.lower()
        
        cms_patterns = {
            'WordPress': ['/wp-content/', '/wp-includes/', 'wp-json'],
            'Joomla': ['/components/com_', 'joomla', 'option=com_'],
            'Drupal': ['/sites/default/', 'drupal', '/node/'],
            'Magento': ['/skin/frontend/', 'magento', 'mage/'],
            'Shopify': ['shopify', 'myshopify.com', 'cdn.shopify.com'],
            'Wix': ['wix.com', 'parastorage.com', 'wixsite.com'],
            'Squarespace': ['squarespace', 'sqsp.net'],
            'PrestaShop': ['prestashop', '/modules/'],
            'Laravel': ['laravel', 'laravel_session']
        }
        
        for cms, patterns in cms_patterns.items():
            for pattern in patterns:
                if pattern in content:
                    technologies['cms'].append(cms)
                    break
        
        js_patterns = {
            'jQuery': [r'jquery[\.-][\d\.]+', 'jquery.com'],
            'React': ['react', 'reactjs', '__react'],
            'Angular': ['angular', 'ng-version'],
            'Vue.js': ['vue', 'v-if', 'v-for', 'v-model'],
            'Bootstrap': ['bootstrap', 'getbootstrap.com']
        }
        
        for lib, patterns in js_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    technologies['javascript_libraries'].append(lib)
                    break
        
        analytics_patterns = {
            'Google Analytics': ['google-analytics.com', 'ga.js', 'gtag', '_gaq'],
            'Google Tag Manager': ['googletagmanager.com', 'gtm.js'],
            'Facebook Pixel': ['connect.facebook.net', 'fbevents.js'],
            'Matomo': ['matomo', 'piwik'],
            'Hotjar': ['hotjar.com', '_hjSettings']
        }
        
        for analytics, patterns in analytics_patterns.items():
            for pattern in patterns:
                if pattern in content:
                    technologies['analytics'].append(analytics)
                    break
        
        cdn_patterns = {
            'Cloudflare': ['cloudflare', 'cf-ray'],
            'Fastly': ['fastly', 'fastly.net'],
            'Akamai': ['akamai', 'akamaihd.net'],
            'CloudFront': ['cloudfront.net', 'x-amz-cf-id'],
            'MaxCDN': ['maxcdn', 'netdna-cdn.com']
        }
        
        for cdn, patterns in cdn_patterns.items():
            for pattern in patterns:
                if pattern in content or pattern in str(headers).lower():
                    technologies['cdn'].append(cdn)
                    break
    
    except:
        pass
    
    for category in technologies:
        technologies[category] = list(set(technologies[category]))
    
    return {k: v for k, v in technologies.items() if v}

def get_server_header(domain: str) -> Union[str, None]:
    headers = get_response_headers(domain)
    return headers.get('Server')

def get_redirect_chain(domain: str) -> List[str]:
    valid, error = validate_domain(domain)
    if not valid:
        return []
    
    domain = normalize_domain(domain)
    redirect_chain = []
    
    try:
        current_url = f'https://{domain}'
        session = requests.Session()
        session.max_redirects = MAX_REDIRECT_CHAIN
        
        for _ in range(MAX_REDIRECT_CHAIN):
            response = session.get(
                current_url,
                timeout=HTTP_TIMEOUT,
                headers={'User-Agent': DEFAULT_USER_AGENT},
                allow_redirects=False
            )
            
            redirect_chain.append({
                'url': current_url,
                'status_code': response.status_code
            })
            
            if response.status_code not in [301, 302, 303, 307, 308]:
                break
            
            location = response.headers.get('Location')
            if not location:
                break
            
            if not location.startswith('http'):
                from urllib.parse import urljoin
                location = urljoin(current_url, location)
            
            current_url = location
    
    except:
        pass
    
    return redirect_chain

def is_using_proxy(domain: str) -> bool:
    valid, error = validate_domain(domain)
    if not valid:
        return False
    
    domain = normalize_domain(domain)
    
    try:
        headers = get_response_headers(domain)
        
        proxy_headers = [
            'X-Forwarded-For',
            'X-Forwarded-Host',
            'X-Forwarded-Proto',
            'X-Real-IP',
            'Via',
            'Forwarded'
        ]
        
        for header in proxy_headers:
            if header in headers:
                return True
        
        server = headers.get('Server', '').lower()
        proxy_servers = ['nginx', 'apache', 'haproxy', 'varnish', 'squid']
        
        for proxy in proxy_servers:
            if proxy in server:
                return True
    
    except:
        pass
    
    return False

def get_meta_tags(domain: str) -> Dict[str, str]:
    valid, error = validate_domain(domain)
    if not valid:
        return {}
    
    domain = normalize_domain(domain)
    meta_tags = {}
    
    try:
        response = requests.get(
            f'https://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT}
        )
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            
            if name and content:
                meta_tags[name] = content
    
    except:
        pass
    
    return meta_tags

def get_page_title(domain: str) -> Union[str, None]:
    valid, error = validate_domain(domain)
    if not valid:
        return None
    
    domain = normalize_domain(domain)
    
    try:
        response = requests.get(
            f'https://{domain}',
            timeout=HTTP_TIMEOUT,
            headers={'User-Agent': DEFAULT_USER_AGENT}
        )
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip()
    
    except:
        pass
    
    return None
