#!/usr/bin/env python3
"""
Script para actualizar el archivo icons-keywords.json con información de marcas.
Analiza todos los iconos SVG en las carpetas de marcas y añade una clave 'brands'
a cada entrada del JSON indicando en qué marcas está disponible cada icono.

Uso: python3 update_icon_brands.py
"""

import os
import json
import re
import subprocess
from collections import defaultdict

def extract_icon_name(filepath):
    """Extract the base icon name from a file path, removing style suffixes"""
    filename = os.path.basename(filepath)
    # Remove .svg extension
    name = filename.replace('.svg', '')
    # Remove style suffixes (-filled, -regular, -light)
    name = re.sub(r'-(filled|regular|light)$', '', name)
    return name

def scan_brand_icons():
    """Scan all brand folders and collect icon information"""
    icons_dir = './icons'
    
    # Automatically detect brand folders
    brands = []
    if os.path.exists(icons_dir):
        for item in os.listdir(icons_dir):
            item_path = os.path.join(icons_dir, item)
            # Only include directories (excluding files like icons-keywords.json)
            if os.path.isdir(item_path):
                brands.append(item)
    
    brands = sorted(brands)  # Sort for consistency
    print(f"Detected brands: {brands}")
    
    # Dictionary to store icon -> brands mapping
    icon_brands = defaultdict(set)
    
    for brand in brands:
        brand_path = os.path.join(icons_dir, brand)
        if not os.path.exists(brand_path):
            print(f"Warning: Brand folder '{brand}' not found at {brand_path}")
            continue
            
        # Walk through all subdirectories (filled, regular, light)
        for root, dirs, files in os.walk(brand_path):
            for file in files:
                if file.endswith('.svg'):
                    filepath = os.path.join(root, file)
                    icon_name = extract_icon_name(filepath)
                    icon_brands[icon_name].add(brand)
    
    # Convert sets to sorted lists for consistency
    icon_brands_dict = {icon: sorted(list(brands)) for icon, brands in icon_brands.items()}
    
    return icon_brands_dict

def load_keywords_json():
    """Load the current icons-keywords.json file"""
    keywords_path = './icons/icons-keywords.json'
    
    if not os.path.exists(keywords_path):
        raise FileNotFoundError(f"File not found: {keywords_path}")
    
    with open(keywords_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_prettier(file_path):
    """Run Prettier on the specified file"""
    try:
        result = subprocess.run(['npx', 'prettier', '--write', file_path], 
                              capture_output=True, text=True, check=True)
        print(f"Prettier applied to {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Warning: Prettier failed on {file_path}: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Warning: Prettier not found. Make sure it's installed (npm install -g prettier or use npx)")
        return False

def update_keywords_with_brands():
    """Update the keywords JSON with brand information"""
    
    # Get icon-brands mapping
    print("Scanning brand folders for icons...")
    icon_brands = scan_brand_icons()
    print(f"Found {len(icon_brands)} unique icons across all brands")
    
    # Load current keywords
    print("Loading keywords file...")
    keywords_data = load_keywords_json()
    
    # Update each icon entry with brand information
    updated_count = 0
    missing_icons = []
    
    for icon_name in keywords_data:
        if icon_name in icon_brands:
            keywords_data[icon_name]['brands'] = icon_brands[icon_name]
            updated_count += 1
        else:
            missing_icons.append(icon_name)
    
    # Report statistics
    print(f"\n=== UPDATE SUMMARY ===")
    print(f"Updated {updated_count} icons with brand information")
    
    if missing_icons:
        print(f"Found {len(missing_icons)} icons in keywords that don't exist in brand folders:")
        for icon in missing_icons[:10]:  # Show first 10
            print(f"  - {icon}")
        if len(missing_icons) > 10:
            print(f"  ... and {len(missing_icons) - 10} more")
    
    # Check for icons that exist in brands but not in keywords
    all_keywords_icons = set(keywords_data.keys())
    all_brand_icons = set(icon_brands.keys())
    icons_without_keywords = all_brand_icons - all_keywords_icons
    
    if icons_without_keywords:
        print(f"\nFound {len(icons_without_keywords)} icons in brands that don't have keywords:")
        for icon in sorted(list(icons_without_keywords))[:10]:  # Show first 10
            print(f"  - {icon}")
        if len(icons_without_keywords) > 10:
            print(f"  ... and {len(icons_without_keywords) - 10} more")
    
    # Save updated file
    keywords_path = './icons/icons-keywords.json'
    with open(keywords_path, 'w', encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated file saved: {keywords_path}")
    
    # Apply Prettier formatting
    print("Applying Prettier formatting...")
    run_prettier(keywords_path)
    
    print("=== COMPLETE ===")
    
    return keywords_data, icon_brands

def show_brand_statistics():
    """Show statistics about icon distribution across brands"""
    icon_brands = scan_brand_icons()
    
    # Count icons per brand
    brand_counts = defaultdict(int)
    for icon, brands in icon_brands.items():
        for brand in brands:
            brand_counts[brand] += 1
    
    print("\n=== BRAND STATISTICS ===")
    print("Icons per brand:")
    for brand in sorted(brand_counts.keys()):
        print(f"  {brand}: {brand_counts[brand]} icons")
    
    # Count how many brands each icon appears in
    brand_coverage = defaultdict(int)
    for icon, brands in icon_brands.items():
        brand_coverage[len(brands)] += 1
    
    print("\nIcon brand coverage:")
    for num_brands in sorted(brand_coverage.keys()):
        print(f"  {brand_coverage[num_brands]} icons appear in {num_brands} brand(s)")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        show_brand_statistics()
    else:
        update_keywords_with_brands()