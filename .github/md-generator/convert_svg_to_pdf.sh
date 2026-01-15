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

# Ensure qpdf is reachable
QPDF_BIN=$(command -v qpdf || true)
if [[ -z "$QPDF_BIN" ]]; then
    echo "Error: qpdf binary not found"
    exit 1
fi

# Note: We handle the exit code 3 manually in the loop logic
QPDF_CMD=("$QPDF_BIN")

echo "Setting up reproducible build environment..."

# Set reproducible timestamp
export SOURCE_DATE_EPOCH=0

echo "Converting SVG files to PDF..."

tmp_dir=$(mktemp -d)
cleanup() {
    rm -rf "$tmp_dir"
}
trap cleanup EXIT

# We use process substitution < <(find...) to avoid subshell issues with 'exit' and 'set -e'
while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    tmp_pdf=$(mktemp "${tmp_dir}/pdf-XXXXXX.pdf")

    echo "Converting: $svg -> $target_pdf"
    
    if ! rsvg-convert -f pdf -o "$tmp_pdf" "$svg"; then
        echo "Error: rsvg-convert failed for $svg"
        exit 1
    fi

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

    # --- CAMBIO CRÍTICO AQUÍ ---
    # Ejecutamos qpdf directamente en el IF. 
    # Bash no activará 'set -e' si el comando es parte de una condición.
    if "${QPDF_BIN}" --replace-input --object-streams=preserve --stream-data=preserve --deterministic-id --static-id "$tmp_pdf"; then
        echo "qpdf: success"
    else
        qpdf_status=$?
        if [[ $qpdf_status -eq 3 ]]; then
            echo "qpdf: finished with warnings (code 3), continuing as it is acceptable."
        else
            echo "Error: qpdf failed with critical exit code $qpdf_status"
            exit $qpdf_status
        fi
    fi
    # ---------------------------

    touch -t 197001010000.00 "$tmp_pdf"

    if [[ -f "$target_pdf" ]] && cmp -s "$tmp_pdf" "$target_pdf"; then
        echo "No changes detected for $target_pdf"
        rm "$tmp_pdf"
    else
        echo "Updating $target_pdf"
        mv "$tmp_pdf" "$target_pdf"
    fi

done < <(find icons -type f -name "*.svg" -print0 2>/dev/null)

echo "---"
echo "Conversion completed successfully!"