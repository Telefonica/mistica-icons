import os

brands = ["telefonica", "o2", "vivo-new", "blau"]

colors = {
    "unique": "59C2C9",
    "all_equivalence": "0066FF",
    "some_equivalence": "EAC344",
    "missing": "D1D5E4"
}

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
    """Process each icon set to compute various metrics, update all_concepts with unique processed names."""
    data = {}
    for folder in folders:
        files = list_svg_files(folder)
        icons = {os.path.basename(file): file for file in files}
        processed_names = {preprocess_filename(os.path.basename(file)): file for file in files}
        data[folder] = {
            "total": len(files),
            "icons": set(icons.keys()),
            "processed_names": set(processed_names.keys()),
            "unique": set(),
            "all_equivalence": set(),
            "some_equivalence": set(),
            "missing": set()
        }
        all_concepts.update(data[folder]["processed_names"])

    for folder in folders:
        current_processed_names = data[folder]["processed_names"]
        data[folder]["unique"] = current_processed_names - set.union(*(data[f]["processed_names"] for f in folders if f != folder))
        data[folder]["all_equivalence"] = set.intersection(*(data[f]["processed_names"] for f in folders))
        for other_folder in folders:
            if other_folder != folder:
                data[folder]["some_equivalence"].update(current_processed_names & data[other_folder]["processed_names"])
        data[folder]["some_equivalence"] -= data[folder]["all_equivalence"]
        data[folder]["missing"] = all_concepts - (data[folder]["unique"] | data[folder]["all_equivalence"] | data[folder]["some_equivalence"])

    return data

def generate_bar_representation(data, all_concepts, total_width=200):
    """Generate a color-coded bar representation for each icon set based on percentage data."""
    bar_output = []
    for folder, metrics in data.items():
        total_concepts = len(all_concepts)
        unique_width = max(1, int(len(metrics['unique']) / total_concepts * total_width)) if len(metrics['unique']) / total_concepts * total_width > 0 else 0
        all_equiv_width = max(1, int(len(metrics['all_equivalence']) / total_concepts * total_width)) if len(metrics['all_equivalence']) / total_concepts * total_width > 0 else 0
        some_equiv_width = max(1, int(len(metrics['some_equivalence']) / total_concepts * total_width)) if len(metrics['some_equivalence']) / total_concepts * total_width > 0 else 0
        missing_width = max(1, total_width - (unique_width + all_equiv_width + some_equiv_width)) if total_width - (unique_width + all_equiv_width + some_equiv_width) > 0 else 0
        bar_parts = []
        if unique_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{unique_width}x20/{colors['unique']}/000&text=+' alt='Unique'>")
        if all_equiv_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{all_equiv_width}x20/{colors['all_equivalence']}/000&text=+' alt='All Equivalence'>")
        if some_equiv_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{some_equiv_width}x20/{colors['some_equivalence']}/000&text=+' alt='Some Equivalence'>")
        if missing_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{missing_width}x20/{colors['missing']}/000&text=+' alt='Missing'>")
        
        bar_representation = f"{os.path.basename(folder)}\n" + "".join(bar_parts) + "\n"
        bar_output.append(bar_representation)
    return bar_output

def generate_markdown_table(data, folders, all_concepts):
    """Generate markdown table representation of the data."""
    markdown = "| Icon Set | Concepts | Total | Unique (%) | All Equivalence (%) | Some Equivalence (%) | Missing (%) |\n"
    markdown += "| --------- | -------- | ----- | ---------- | ------------------- | ------------------- | ------------ |\n"
    
    for folder in folders:
        folder_name = os.path.basename(folder)
        folder_data = data[folder]
        total_concepts = len(all_concepts)
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
    all_concepts = set()
    icon_data = process_icon_sets(folders, all_concepts)
    bars = generate_bar_representation(icon_data, all_concepts)
    for bar in bars:
        print(bar)
    print(generate_markdown_table(icon_data, folders, all_concepts))

if __name__ == "__main__":
    root_folder = "icons"
    main(root_folder)
