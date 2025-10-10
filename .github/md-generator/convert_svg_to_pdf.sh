#!/bin/bash

# Script to convert SVG files to PDF with reproducible checksums
# Usage: ./convert_svg_to_pdf.sh [-f|--folder FOLDER]
# Options:
#   -f, --folder FOLDER    Specify subfolder within icons/ to convert (e.g., blau, o2, etc.)
#                         If not specified, converts all folders in icons/

set -e

# Default values
FOLDER=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--folder)
            FOLDER="$2"
            shift # past argument
            shift # past value
            ;;
        -h|--help)
            echo "Usage: $0 [-f|--folder FOLDER]"
            echo "Options:"
            echo "  -f, --folder FOLDER    Specify subfolder within icons/ to convert"
            echo "  -h, --help            Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo "Installing required dependencies..."

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Error: Homebrew is required on macOS"
        echo "Install it from: https://brew.sh"
        exit 1
    fi
    
    # Install dependencies
    brew install exiftool librsvg
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (Ubuntu/Debian)
    sudo apt-get update
    sudo apt-get install -y libimage-exiftool-perl librsvg2-bin
    
else
    echo "Error: Unsupported operating system"
    exit 1
fi

echo "Setting up reproducible build environment..."

# Set reproducible timestamp
export SOURCE_DATE_EPOCH=0

echo "Converting SVG files to PDF..."

# Determine the target directory
if [[ -n "$FOLDER" ]]; then
    TARGET_DIR="icons/$FOLDER"
    if [[ ! -d "$TARGET_DIR" ]]; then
        echo "Error: Directory '$TARGET_DIR' does not exist"
        exit 1
    fi
    echo "Converting SVG files in: $TARGET_DIR"
else
    TARGET_DIR="icons"
    echo "Converting all SVG files in: $TARGET_DIR"
fi

# Convert all SVG files to PDF
for i in $(find "$TARGET_DIR" -type f -name "*.svg" 2>/dev/null); do 
    echo "Converting: $i -> ${i%.*}.pdf"
    rsvg-convert -f pdf -o "${i%.*}.pdf" "$i"
done

echo "Cleaning metadata from PDF files..."

# Clean metadata from all PDF files in the target directory
find "$TARGET_DIR" -type f -name "*.pdf" 2>/dev/null | while IFS= read -r file; do
    echo "Cleaning metadata from $file"
    
    # Remove all metadata including creation/modification dates
    exiftool -overwrite_original_in_place \
        -all:all= \
        -Creator= \
        -Producer= \
        -CreationDate= \
        -ModDate= \
        -Title= \
        -Subject= \
        -Keywords= \
        "$file" > /dev/null 2>&1
    
    # Set fixed timestamps for reproducibility
    touch -t 197001010000.00 "$file"
done

echo "Conversion completed successfully!"
echo "All PDF files now have reproducible checksums."
