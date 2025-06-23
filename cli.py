#!/usr/bin/env python3

import argparse
import sys
from deeprecon import set_language, get_message
from deeprecon.resolve import resolve_all
from deeprecon.dns import get_dns_records
from deeprecon.whois import whois_domain, whois_ip
from deeprecon.geoip import geoip
from deeprecon.ssl import get_ssl_info, ssl_grade
from deeprecon.availability import ping, get_http_status
from deeprecon.security import is_filtered, has_waf, get_security_score
from deeprecon.tech_detect import detect_technologies
from deeprecon.utils.formatter import to_json, export_to_csv
from deeprecon.utils.validator import validate_domain, validate_ip

def main():
    parser = argparse.ArgumentParser(
        description='DeepRecon - Domain and IP Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'target',
        help='Domain or IP address to analyze'
    )
    
    parser.add_argument(
        '-m', '--modules',
        nargs='+',
        choices=['resolve', 'dns', 'whois', 'geoip', 'ssl', 'availability', 'security', 'tech'],
        default=['resolve', 'dns', 'whois', 'geoip', 'ssl', 'availability', 'security', 'tech'],
        help='Modules to run (default: all)'
    )
    
    parser.add_argument(
        '-o', '--output',
        choices=['json', 'csv', 'pretty'],
        default='pretty',
        help='Output format (default: pretty)'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Save output to file'
    )
    
    parser.add_argument(
        '-l', '--language',
        choices=['en', 'fa'],
        default='en',
        help='Output language (default: en)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode - only show results'
    )
    
    args = parser.parse_args()
    
    set_language(args.language)
    
    target = args.target
    results = {}
    
    is_domain, _ = validate_domain(target)
    is_ip, _ = validate_ip(target)
    
    if not (is_domain or is_ip):
        print(get_message('errors.invalid_domain'))
        sys.exit(1)
    
    if not args.quiet:
        print(f"{get_message('messages.checking_domain')}: {target}\n")
    
    if 'resolve' in args.modules:
        if not args.quiet:
            print(get_message('messages.resolving_ip'))
        results['resolve'] = resolve_all(target)
    
    if 'dns' in args.modules and is_domain:
        if not args.quiet:
            print(get_message('messages.fetching_dns'))
        results['dns'] = get_dns_records(target)
    
    if 'whois' in args.modules:
        if not args.quiet:
            print(get_message('messages.performing_whois'))
        if is_domain:
            results['whois'] = whois_domain(target)
        else:
            results['whois'] = whois_ip(target)
    
    if 'geoip' in args.modules:
        if not args.quiet:
            print(get_message('messages.locating_ip'))
        if is_ip:
            results['geoip'] = geoip(target)
        elif 'resolve' in results and results['resolve'].get('ip'):
            results['geoip'] = geoip(results['resolve']['ip'])
    
    if 'ssl' in args.modules and is_domain:
        if not args.quiet:
            print(get_message('messages.checking_ssl'))
        results['ssl'] = {
            'info': get_ssl_info(target),
            'grade': ssl_grade(target)
        }
    
    if 'availability' in args.modules:
        if not args.quiet:
            print(get_message('messages.checking_availability'))
        results['availability'] = {
            'ping': ping(target),
            'http_status': get_http_status(target) if is_domain else None
        }
    
    if 'security' in args.modules:
        if not args.quiet:
            print(get_message('messages.scanning_security'))
        results['security'] = {
            'filtered': is_filtered(target),
            'waf': has_waf(target) if is_domain else None,
            'score': get_security_score(target) if is_domain else None
        }
    
    if 'tech' in args.modules and is_domain:
        if not args.quiet:
            print(get_message('messages.detecting_tech'))
        results['tech'] = detect_technologies(target)
    
    if not args.quiet:
        print(f"\n{get_message('messages.complete')}\n")
    
    if args.output == 'json':
        output = to_json(results)
    elif args.output == 'csv':
        flat_results = [{'target': target, **results}]
        output = export_to_csv(flat_results)
    else:
        output = format_pretty(results)
    
    if args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(output)
        if not args.quiet:
            print(f"Output saved to: {args.file}")
    else:
        print(output)

def format_pretty(results: dict) -> str:
    output = []
    
    for module, data in results.items():
        output.append(f"\n=== {module.upper()} ===")
        output.append(format_dict(data, indent=2))
    
    return '\n'.join(output)

def format_dict(data, indent=0):
    lines = []
    prefix = ' ' * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(format_dict(value, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(format_dict(item, indent))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}{data}")
    
    return '\n'.join(lines)

if __name__ == '__main__':
    main()
