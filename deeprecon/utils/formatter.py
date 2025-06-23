import json
import csv
from datetime import datetime
from typing import Any, Dict, List
from io import StringIO

def to_json(data: Any, indent: int = 2) -> str:
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)
    
    return json.dumps(data, indent=indent, default=json_serializer, ensure_ascii=False)

def to_dict(data: Any) -> Dict:
    if isinstance(data, dict):
        return data
    elif hasattr(data, '__dict__'):
        return data.__dict__
    else:
        return {'data': data}

def export_to_csv(results: List[Dict], filename: str = None) -> str:
    if not results:
        return ""
    
    output = StringIO()
    
    # Flatten all results first to get all possible keys
    flat_results = [flatten_dict(result) for result in results]
    
    all_keys = set()
    for flat_result in flat_results:
        all_keys.update(flat_result.keys())
    
    fieldnames = sorted(all_keys)
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for flat_result in flat_results:
        writer.writerow(flat_result)
    
    csv_content = output.getvalue()
    
    if filename:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_content)
    
    return csv_content

def flatten_dict(data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    items = []
    
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            items.append((new_key, ', '.join(str(v) for v in value)))
        elif isinstance(value, datetime):
            items.append((new_key, value.isoformat()))
        else:
            items.append((new_key, value))
    
    return dict(items)

def format_size(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f}h"
    else:
        days = seconds / 86400
        return f"{days:.2f}d"

def sanitize_filename(filename: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def create_summary(data: Dict) -> Dict:
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_items': len(data) if isinstance(data, (list, dict)) else 1
    }
    
    if isinstance(data, dict):
        summary['keys'] = list(data.keys())
    
    return summary
