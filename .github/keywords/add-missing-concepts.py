#!/usr/bin/env python3
"""
Script to add missing icon concepts to icons-keywords.json

This script:
1. Scans all SVG files in the icons/ directory
2. Extracts concepts by removing style suffixes (-regular, -light, -filled)
3. Identifies missing concepts not present in icons-keywords.json
4. Adds them to the JSON with empty keywords and category arrays
"""

import json
import os
import re
from pathlib import Path

def get_all_svg_files(icons_dir):
    """Get all SVG files from the icons directory recursively"""
    svg_files = []
    for root, dirs, files in os.walk(icons_dir):
        for file in files:
            if file.endswith('.svg'):
                svg_files.append(file)
    return svg_files

def extract_concept_from_filename(filename):
    """Extract concept name by removing style suffixes and .svg extension"""
    # Remove .svg extension
    name = filename.replace('.svg', '')
    
    # Remove style suffixes
    concept = re.sub(r'-(?:regular|light|filled)$', '', name)
    
    return concept

def get_unique_concepts(svg_files):
    """Get unique concepts from list of SVG files"""
    concepts = set()
    
    for filename in svg_files:
        concept = extract_concept_from_filename(filename)
        if concept:  # Only add non-empty concepts
            concepts.add(concept)
    
    return sorted(list(concepts))

def load_keywords_json(json_path):
    """Load the current icons-keywords.json file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def find_missing_concepts(all_concepts, existing_data):
    """Find concepts that are missing from the JSON"""
    existing_concepts = set(existing_data.keys())
    missing_concepts = [concept for concept in all_concepts if concept not in existing_concepts]
    return sorted(missing_concepts)

def add_missing_concepts_to_json(missing_concepts, existing_data):
    """Add missing concepts to the JSON data with default empty values"""
    for concept in missing_concepts:
        existing_data[concept] = {
            "keywords": [],
            "category": []
        }
    
    return existing_data

def save_keywords_json(json_path, data):
    """Save the updated JSON data back to file with sorted keys"""
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def format_with_prettier(json_path):
    """Format the JSON file with prettier"""
    import subprocess
    
    try:
        result = subprocess.run(
            ['prettier', '--write', str(json_path)],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running prettier: {e}")
        print(f"Prettier stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Warning: prettier not found. Install it with: npm install -g prettier")
        return False

def main():
    # Define paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    icons_dir = repo_root / "icons"
    keywords_json_path = repo_root / "icons" / "icons-keywords.json"
    
    print("🔍 Scanning for SVG files...")
    
    # Get all SVG files
    svg_files = get_all_svg_files(icons_dir)
    print(f"Found {len(svg_files)} SVG files")
    
    # Extract unique concepts
    all_concepts = get_unique_concepts(svg_files)
    print(f"Found {len(all_concepts)} unique concepts")
    
    # Load existing keywords JSON
    print("📖 Loading icons-keywords.json...")
    existing_data = load_keywords_json(keywords_json_path)
    if existing_data is None:
        return 1
    
    # Find missing concepts
    missing_concepts = find_missing_concepts(all_concepts, existing_data)
    
    # Check if keys are sorted
    current_keys = list(existing_data.keys())
    sorted_keys = sorted(current_keys)
    keys_need_sorting = current_keys != sorted_keys
    
    if not missing_concepts and not keys_need_sorting:
        print("✅ All concepts are already present and keys are sorted in icons-keywords.json!")
        return 0
    
    if missing_concepts:
        print(f"\n📝 Found {len(missing_concepts)} missing concepts:")
        for concept in missing_concepts:
            print(f"  + {concept}")
    
    if keys_need_sorting:
        print("🔄 Keys need to be sorted alphabetically")
    
    # Add missing concepts
    if missing_concepts:
        print(f"\n🔄 Adding {len(missing_concepts)} missing concepts...")
        updated_data = add_missing_concepts_to_json(missing_concepts, existing_data)
    else:
        updated_data = existing_data
    
    # Save updated JSON
    print("💾 Saving updated icons-keywords.json...")
    if save_keywords_json(keywords_json_path, updated_data):
        print("✅ Successfully saved icons-keywords.json!")
        
        # Format with prettier
        print("🎨 Formatting with prettier...")
        if format_with_prettier(keywords_json_path):
            print("✅ Successfully formatted with prettier!")
        else:
            print("⚠️  Prettier formatting failed, but JSON was saved successfully")
        
        if missing_concepts:
            print(f"Added concepts: {', '.join(missing_concepts)}")
        if keys_need_sorting:
            print("Sorted keys alphabetically")
        return 0
    else:
        print("❌ Failed to save updated JSON!")
        return 1

if __name__ == "__main__":
    exit(main())