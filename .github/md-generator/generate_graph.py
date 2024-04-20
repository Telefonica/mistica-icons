import os

brands = ["telefonica", "o2", "vivo-new", "blau"]

def preprocess_filename(filename):
    """Normalize filenames by removing specific substrings."""
    return filename.replace("-filled", "").replace("-light", "").replace("-regular", "")

def list_svg_files(folder):
    """List all .svg files in the directory, including subdirectories."""
    svg_files = []
    for root, dirs, files in os.walk(folder):
        svg_files.extend(os.path.join(root, file) for file in files if file.endswith('.svg') and not file.startswith('.'))
    return svg_files

def process_icon_sets(folders, all_concepts):
    """Process each icon set to compute various metrics."""
    data = {}

    # Collect all icons and their processed names in each folder
    for folder in folders:
        files = list_svg_files(folder)
        icons = {os.path.basename(file): file for file in files}
        processed_names = {preprocess_filename(os.path.basename(file)): file for file in files}
        data[folder] = {
            "total": len(files),
            "icons": set(icons.keys()),
            "processed_names": set(processed_names.keys())
        }
        all_concepts.update(data[folder]["processed_names"])
    
    # Calculate metrics related to equivalence and uniqueness
    for folder in folders:
        current_processed_names = data[folder]["processed_names"]
        data[folder]["unique"] = current_processed_names - set.union(*(data[f]["processed_names"] for f in folders if f != folder))
        data[folder]["all_equivalence"] = set.intersection(*(data[f]["processed_names"] for f in folders))
        data[folder]["some_equivalence"] = set()
        
        for other_folder in folders:
            if other_folder != folder:
                data[folder]["some_equivalence"].update(current_processed_names & data[other_folder]["processed_names"])
        data[folder]["some_equivalence"] -= data[folder]["all_equivalence"]
        
        # Adjusted calculation for Missing
        data[folder]["missing"] = all_concepts - (data[folder]["unique"] | data[folder]["all_equivalence"] | data[folder]["some_equivalence"])

    return data

def generate_markdown_table(data, folders, all_concepts):
    """Generate markdown table representation of the data."""
    markdown = "| Icon Set | Concepts | Total | Unique (%) | All Equivalence (%) | Some Equivalence (%) | Missing (%) |\n"
    markdown += "| --------- | -------- | ----- | ---------- | ------------------- | ------------------- | ------------ |\n"
    
    for folder in folders:
        folder_name = os.path.basename(folder)
        folder_data = data[folder]
        total_concepts = len(all_concepts)  # Total concepts across all folders
        unique_count = len(folder_data['unique'])
        unique_percent = f"{unique_count} ({unique_count / total_concepts * 100:.1f}%)" if total_concepts > 0 else "0 (0%)"
        all_equivalence_count = len(folder_data['all_equivalence'])
        all_equivalence_percent = f"{all_equivalence_count} ({all_equivalence_count / total_concepts * 100:.1f}%)" if total_concepts > 0 else "0 (0%)"
        some_equivalence_count = len(folder_data['some_equivalence'])
        some_equivalence_percent = f"{some_equivalence_count} ({some_equivalence_count / total_concepts * 100:.1f}%)" if total_concepts > 0 else "0 (0%)"
        missing_count = len(folder_data['missing'])
        missing_percent = f"{missing_count} ({missing_count / total_concepts * 100:.1f}%)" if total_concepts > 0 else "0 (0%)"
        
        markdown += f"| {folder_name} | {len(folder_data['processed_names'])} | {folder_data['total']} | {unique_percent} | {all_equivalence_percent} | {some_equivalence_percent} | {missing_percent} |\n"
    
    return markdown

def main(root_folder):
    """Main function to orchestrate the icon analysis and reporting."""
    folders = [os.path.join(root_folder, brand) for brand in brands]
    all_concepts = set()  # Define all_concepts here to be used globally
    try:
        icon_data = process_icon_sets(folders, all_concepts)
        print(generate_markdown_table(icon_data, folders, all_concepts))
    except Exception as e:
        print(f"Error processing icon sets: {str(e)}")

if __name__ == "__main__":
    root_folder = "icons"
    main(root_folder)
