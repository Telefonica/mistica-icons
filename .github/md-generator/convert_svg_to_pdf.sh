#!/bin/bash

# Script to convert SVG files to PDF with reproducible checksums
# Usage: ./convert_svg_to_pdf.sh

set -e

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

# Convert all SVG files to PDF
for i in $(find icons -type f -name "*.svg" 2>/dev/null); do 
    echo "Converting: $i -> ${i%.*}.pdf"
    rsvg-convert -f pdf -o "${i%.*}.pdf" "$i"
done

echo "Cleaning metadata from PDF files..."

# Clean metadata from all PDF files
find icons -type f -name "*.pdf" 2>/dev/null | while IFS= read -r file; do
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
