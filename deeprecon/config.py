DEFAULT_LANGUAGE = 'en'
SUPPORTED_LANGUAGES = ['en', 'fa']

DEFAULT_TIMEOUT = 10
DNS_TIMEOUT = 5
HTTP_TIMEOUT = 15
SSL_TIMEOUT = 10
PING_TIMEOUT = 5

DEFAULT_USER_AGENT = 'DeepRecon/1.0'
MAX_REDIRECT_CHAIN = 10
MAX_RETRIES = 3
RETRY_DELAY = 1

DEFAULT_DNS_SERVERS = ['8.8.8.8', '1.1.1.1']
DEFAULT_PORTS = [80, 443, 21, 22, 25, 3306, 8080]

SSL_GRADES = {
    'A+': 95,
    'A': 90,
    'B': 80,
    'C': 70,
    'D': 60,
    'F': 0
}

BLACKLIST_PROVIDERS = [
    'zen.spamhaus.org',
    'bl.spamcop.net',
    'b.barracudacentral.org',
    'dnsbl.sorbs.net'
]

WAF_SIGNATURES = {
    'cloudflare': ['CF-RAY', '__cfduid', 'cf-request-id'],
    'akamai': ['AkamaiGHost', 'akamai.net'],
    'incapsula': ['incap_ses', 'visid_incap'],
    'aws': ['AWSALB', 'AWSALBCORS', 'X-Amz']
}

TECH_PATTERNS = {
    'nginx': r'nginx/[\d.]+',
    'apache': r'Apache/[\d.]+',
    'iis': r'Microsoft-IIS/[\d.]+',
    'cloudflare': r'cloudflare',
    'litespeed': r'LiteSpeed'
}

CACHE_ENABLED = True
CACHE_TTL = 3600
MAX_CACHE_SIZE = 1000

NETWORK_SCAN_TIMEOUT = 30
NETWORK_DISCOVERY_TIMEOUT = 60
PORT_SCAN_TIMEOUT = 120
PING_COUNT = 4
MAX_THREADS = 50

SCAN_COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
FULL_PORT_RANGE = range(1, 65536)

BANDWIDTH_TEST_SERVERS = [
    'speedtest.net',
    'fast.com',
    'testmy.net'
]

NETWORK_INTERFACE_TYPES = {
    'ethernet': ['eth', 'ens', 'enp'],
    'wireless': ['wlan', 'wlp'],
    'loopback': ['lo'],
    'virtual': ['docker', 'br-', 'veth', 'tun', 'tap']
}
