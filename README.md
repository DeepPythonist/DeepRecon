# 🔍 DeepRecon

<div align="center">

![DeepRecon Logo](https://img.shields.io/badge/DeepRecon-Domain%20%26%20IP%20Analysis-blue?style=for-the-badge&logo=python)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/deeprecon?style=flat-square)](https://pypi.org/project/deeprecon/)
[![Downloads](https://img.shields.io/pypi/dm/deeprecon?style=flat-square)](https://pypi.org/project/deeprecon/)
[![GitHub Stars](https://img.shields.io/github/stars/DeepPythonist/DeepRecon?style=flat-square)](https://github.com/DeepPythonist/DeepRecon)

**A powerful, modular Python library for comprehensive domain and IP analysis**

[🚀 Installation](#installation) •
[📖 Documentation](#documentation) •
[💡 Examples](#examples) •
[🤝 Contributing](#contributing)

</div>

---

## ✨ Features

DeepRecon provides a comprehensive suite of tools for analyzing domains and IP addresses with ease:

### 🎯 Core Analysis
- **DNS Resolution**: Convert domains to IPs and vice versa
- **DNS Records**: Fetch A, AAAA, MX, NS, TXT, CNAME, SOA records
- **WHOIS Information**: Domain registration details and IP ownership
- **Geolocation**: IP-based geographical information with ISP details

### 🔒 Security Analysis  
- **SSL/TLS Certificates**: Certificate validation, expiry checking, and grading
- **Security Headers**: HSTS, CSP, X-Frame-Options analysis
- **WAF Detection**: Identify Web Application Firewalls
- **Blacklist Checking**: Multi-provider blacklist verification

### 🌐 Connectivity & Performance
- **Availability Testing**: Ping, HTTP status, response time measurement
- **Port Scanning**: TCP port connectivity testing
- **Traceroute**: Network path analysis
- **Response Analysis**: HTTP headers and redirect chain tracking

### 💻 Technology Detection
- **Web Technologies**: CMS, frameworks, analytics tools detection
- **Server Identification**: Web server and proxy detection
- **Meta Information**: Page titles, meta tags extraction

### 🌍 Multi-language Support
- **English** and **Persian (فارسی)** interface
- **Internationalization**: Easy to extend for more languages

### 📊 Flexible Output
- **JSON**: Machine-readable structured data
- **CSV**: Spreadsheet-compatible format  
- **Pretty Print**: Human-readable console output
- **CLI Interface**: Command-line tool with rich options

---

## 🚀 Installation

### Using pip (Recommended)

```bash
pip install deeprecon
```

### From source

```bash
git clone https://github.com/DeepPythonist/DeepRecon.git
cd DeepRecon
pip install -e .
```

### Dependencies

DeepRecon automatically installs these required packages:
- `requests` - HTTP client library
- `dnspython` - DNS toolkit
- `python-whois` - WHOIS client
- `ipwhois` - IP WHOIS client  
- `pyOpenSSL` - SSL/TLS toolkit
- `beautifulsoup4` - HTML parser
- `lxml` - XML/HTML parser

---

## 💡 Quick Start

### CLI Usage

```bash
# Analyze a domain with all modules
deeprecon google.com

# Specific analysis modules
deeprecon github.com --modules resolve dns ssl

# Output in JSON format
deeprecon example.com --output json

# Save results to file
deeprecon stackoverflow.com --file results.json

# Use Persian language
deeprecon google.com --language fa

# Quiet mode (results only)
deeprecon google.com --quiet
```

### Python API Usage

```python
from deeprecon import resolve, dns, geoip, ssl

# Basic domain to IP resolution
ip = resolve.get_ip('google.com')
print(f"Google IP: {ip}")

# Get all DNS records
dns_records = dns.get_dns_records('github.com')
print(f"DNS Records: {dns_records}")

# IP geolocation
location = geoip.geoip('8.8.8.8')
print(f"Location: {location['city']}, {location['country']}")

# SSL certificate information
ssl_info = ssl.get_ssl_info('github.com')
print(f"SSL Issuer: {ssl_info['issuer']['organizationName']}")
```

---

## 📖 Documentation

### Command Line Interface

#### Basic Syntax
```bash
deeprecon <target> [options]
```

#### Options
- `--modules, -m`: Specify analysis modules
  - Available: `resolve`, `dns`, `whois`, `geoip`, `ssl`, `availability`, `security`, `tech`
- `--output, -o`: Output format (`json`, `csv`, `pretty`)
- `--file, -f`: Save output to file
- `--language, -l`: Interface language (`en`, `fa`)
- `--quiet, -q`: Quiet mode

#### Examples
```bash
# Domain analysis
deeprecon example.com

# IP analysis  
deeprecon 8.8.8.8

# Custom modules
deeprecon google.com -m resolve dns ssl

# JSON output to file
deeprecon github.com -o json -f analysis.json
```

### Python API Reference

#### Resolve Module
```python
from deeprecon.resolve import get_ip, get_ips, get_domain, resolve_all

# Convert domain to IP
ip = get_ip('example.com')

# Get all IPs for domain
ips = get_ips('example.com')

# Reverse DNS lookup
domain = get_domain('8.8.8.8')

# Complete resolution analysis
result = resolve_all('example.com')
```

#### DNS Module
```python
from deeprecon.dns import get_dns_records, get_ns_records, get_mx_records

# Get all DNS records
records = get_dns_records('example.com')

# Get name servers
nameservers = get_ns_records('example.com')

# Get MX records
mx_records = get_mx_records('example.com')
```

#### GeoIP Module
```python
from deeprecon.geoip import geoip, get_country, get_asn

# Complete geolocation data
geo_data = geoip('8.8.8.8')

# Get specific information
country = get_country('8.8.8.8')
asn = get_asn('8.8.8.8')
```

#### SSL Module
```python
from deeprecon.ssl import get_ssl_info, check_ssl_validity, ssl_grade

# Get SSL certificate information
ssl_data = get_ssl_info('example.com')

# Check if certificate is valid
is_valid = check_ssl_validity('example.com')

# Get SSL grade
grade = ssl_grade('example.com')
```

#### Security Module
```python
from deeprecon.security import is_filtered, has_waf, get_security_score

# Check if domain/IP is filtered
filtered = is_filtered('example.com')

# Detect WAF protection
waf = has_waf('example.com')

# Get overall security score
score = get_security_score('example.com')
```

---

## 🏗️ Architecture

DeepRecon follows a modular architecture:

```
deeprecon/
├── config.py          # Configuration and constants
├── resolve.py          # Domain ↔ IP resolution
├── dns.py             # DNS record analysis
├── whois.py           # WHOIS information
├── geoip.py           # Geographic location
├── ssl.py             # SSL/TLS analysis
├── availability.py    # Connectivity testing
├── security.py        # Security analysis
├── tech_detect.py     # Technology detection
├── utils/
│   ├── validator.py   # Input validation
│   └── formatter.py   # Output formatting
└── locales/           # Internationalization
    ├── en.json
    └── fa.json
```

---

## 🎯 Use Cases

### Security Research
- **Domain reconnaissance** for penetration testing
- **SSL/TLS analysis** for security audits
- **Blacklist monitoring** for threat intelligence
- **WAF detection** for security assessment

### DevOps & Monitoring
- **Infrastructure monitoring** with availability checks
- **DNS monitoring** for domain management
- **Performance analysis** with response time measurement
- **Certificate monitoring** for SSL expiry tracking

### Network Analysis
- **Network path analysis** with traceroute
- **Port scanning** for connectivity testing
- **Geolocation analysis** for CDN optimization
- **Technology stack identification**

### Research & Analytics
- **Domain analysis** for market research
- **Technology trends** analysis
- **Geographic distribution** of services
- **Compliance checking** for regulations

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/DeepPythonist/DeepRecon.git
   cd DeepRecon
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

### Contribution Guidelines

- **Code Style**: Follow PEP 8 standards
- **Documentation**: Update docstrings and README
- **Testing**: Add tests for new features
- **Commits**: Use clear, descriptive commit messages

### Areas for Contribution

- 🌐 **Additional language support**
- 🔧 **New analysis modules**
- 📊 **Enhanced output formats**
- 🚀 **Performance optimizations**
- 🐛 **Bug fixes and improvements**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mohammad Rasol Esfandiari**
- GitHub: [@DeepPythonist](https://github.com/DeepPythonist)
- Email: mrasolesfandiari@gmail.com

---

## 🙏 Acknowledgments

- Thanks to all contributors who helped make this project better
- Special thanks to the open-source community for the amazing libraries
- Inspired by the need for comprehensive domain and IP analysis tools

---

## ⭐ Star History

If you find DeepRecon useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=DeepPythonist/DeepRecon&type=Date)](https://star-history.com/#DeepPythonist/DeepRecon&Date)

---

<div align="center">

**Made with ❤️ by [Mohammad Rasol Esfandiari](https://github.com/DeepPythonist)**

</div> 