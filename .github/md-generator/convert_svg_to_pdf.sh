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
    brew install exiftool librsvg qpdf
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (Ubuntu/Debian)
    sudo apt-get update
    sudo apt-get install -y libimage-exiftool-perl librsvg2-bin qpdf
    
else
    echo "Error: Unsupported operating system"
    exit 1
fi

# Ensure qpdf is reachable and prepared to downgrade warnings to exit code 0.
QPDF_BIN=$(command -v qpdf || true)
if [[ -z "$QPDF_BIN" ]]; then
    echo "Error: qpdf binary not found"
    exit 1
fi
QPDF_CMD=("$QPDF_BIN" --warning-exit-0)

echo "Setting up reproducible build environment..."

# Set reproducible timestamp
export SOURCE_DATE_EPOCH=0

echo "Converting SVG files to PDF..."

tmp_dir=$(mktemp -d)
cleanup() {
    rm -rf "$tmp_dir"
}
trap cleanup EXIT

find icons -type f -name "*.svg" -print0 2>/dev/null | while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    tmp_pdf=$(mktemp "${tmp_dir}/pdf-XXXXXX.pdf")

    echo "Converting: $svg -> $target_pdf"
    rsvg-convert -f pdf -o "$tmp_pdf" "$svg"

    # Strip metadata before diffing to avoid spurious git changes
    exiftool -overwrite_original_in_place \
        -all:all= \
        -Creator= \
        -Producer= \
        -CreationDate= \
        -ModDate= \
        -Title= \
        -Subject= \
        -Keywords= \
        "$tmp_pdf" > /dev/null 2>&1

    # Normalize trailer IDs for reproducibility
    "${QPDF_CMD[@]}" --replace-input --object-streams=preserve --stream-data=preserve --deterministic-id --static-id "$tmp_pdf"

    # Set fixed timestamps so identical PDFs stay untouched
    touch -t 197001010000.00 "$tmp_pdf"

    if [[ -f "$target_pdf" ]] && cmp -s "$tmp_pdf" "$target_pdf"; then
        echo "No changes detected for $target_pdf"
        rm "$tmp_pdf"
    else
        mv "$tmp_pdf" "$target_pdf"
    fi
done

echo "Conversion completed successfully!"
echo "PDF files only update when their SVG source actually changes."
