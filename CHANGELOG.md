# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Deprecated
- Nothing yet

### Removed
- Nothing yet

### Fixed
- Nothing yet

### Security
- Nothing yet

## [1.1.0] - 2024-12-24

### Added
- 🌐 **Network Analysis Module**
  - Network interface discovery and monitoring
  - Network device scanning and identification
  - Advanced port scanning with multi-threading
  - Network performance analysis and metrics
  - Network security scanning and assessment
  - Real-time network topology mapping

- 🔧 **Network Utility Functions**
  - Subnet calculation and network analysis
  - MAC address vendor identification
  - ARP table parsing and analysis
  - Routing table extraction
  - Network speed testing integration
  - Port knocking functionality
  - Public IP address detection

- 🚀 **Performance Enhancements**
  - Multi-threaded network scanning (up to 50 concurrent connections)
  - Optimized network discovery algorithms
  - Cross-platform network interface support
  - Enhanced timeout management for network operations

- 📊 **Extended CLI Support**
  - New `network` module option for CLI
  - Comprehensive network analysis output formats
  - Integration with existing output formats (JSON, CSV, pretty print)

### Changed
- Enhanced error handling for network operations
- Improved cross-platform compatibility (Windows, macOS, Linux)
- Updated CLI help messages for new network module

### Dependencies
- Added `psutil>=5.9.0` for system and network monitoring
- Added `netifaces>=0.11.0` for network interface management
- Added `speedtest-cli>=2.1.3` for network speed testing

### Technical Improvements
- Thread-safe network operations
- Memory-efficient network scanning
- Graceful degradation when dependencies are missing
- Comprehensive input validation for network functions

## [1.0.0] - 2024-06-24

### Added
- 🎯 **Core Analysis Modules**
  - DNS resolution and reverse DNS lookup
  - Comprehensive DNS records fetching (A, AAAA, MX, NS, TXT, CNAME, SOA)
  - WHOIS information for domains and IP addresses
  - IP geolocation with detailed geographic information

- 🔒 **Security Analysis**
  - SSL/TLS certificate validation and grading
  - Security headers analysis (HSTS, CSP, X-Frame-Options, etc.)
  - WAF detection for multiple providers
  - Multi-provider blacklist checking
  - Overall security scoring system

- 🌐 **Connectivity & Performance**
  - Ping functionality for domains and IPs
  - HTTP status code checking
  - Response time measurement
  - TCP port connectivity testing
  - Network traceroute analysis
  - HTTP headers and redirect chain analysis

- 💻 **Technology Detection**
  - Web technology stack identification
  - CMS detection (WordPress, Joomla, Drupal, etc.)
  - JavaScript framework detection
  - Analytics tools identification
  - CDN detection
  - Web server identification

- 🌍 **Multi-language Support**
  - English and Persian (فارسی) interface
  - Internationalization framework
  - Localized error messages and UI text

- 📊 **Flexible Output Formats**
  - JSON structured output
  - CSV export functionality
  - Human-readable pretty print
  - Command-line interface with rich options

- 🛠️ **Developer Features**
  - Modular architecture for easy extension
  - Comprehensive input validation
  - Type hints throughout codebase
  - Configurable timeouts and settings
  - Error handling and graceful degradation

- 📱 **Command Line Interface**
  - Full-featured CLI with argument parsing
  - Module selection capability
  - Output format selection
  - File export functionality
  - Quiet mode support
  - Language selection

### Technical Features
- Python 3.8+ compatibility
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive error handling
- Timeout management
- Input validation and sanitization
- Caching support for improved performance
- Clean separation of concerns
- Extensive configuration options

### Dependencies
- `requests` - HTTP client library
- `dnspython` - DNS toolkit
- `python-whois` - WHOIS client
- `ipwhois` - IP WHOIS client
- `pyOpenSSL` - SSL/TLS toolkit
- `beautifulsoup4` - HTML parser
- `lxml` - XML/HTML parser

## [0.1.0] - 2024-06-20

### Added
- Initial project structure
- Basic domain resolution functionality
- Core utility functions

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities 