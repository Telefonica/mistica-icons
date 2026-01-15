#!/bin/bash

# Script to convert SVG files to PDF with reproducible checksums
set -e

echo "Installing required dependencies..."

# Detectar OS e instalar dependencias
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y libimage-exiftool-perl librsvg2-bin qpdf
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install exiftool librsvg qpdf
fi

# Verificar qpdf
QPDF_BIN=$(command -v qpdf)
if [[ -z "$QPDF_BIN" ]]; then
    echo "Error: qpdf not found."
    exit 1
fi

echo "Setting up reproducible build environment..."
export SOURCE_DATE_EPOCH=0

echo "Converting SVG files to PDF..."

find icons -type f -name "*.svg" -print0 2>/dev/null | while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    echo "Converting: $svg -> $target_pdf"

    if ! rsvg-convert -f pdf -o "$target_pdf" "$svg"; then
        echo "Error: rsvg-convert failed for $svg"
        exit 1
    fi
done

echo "Cleaning metadata and normalizing PDFs..."

find icons -type f -name "*.pdf" -print0 2>/dev/null | while IFS= read -r -d '' file; do
    echo "Processing $file"

    # Remove variable metadata that would otherwise produce diff noise
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

    # Normalize trailer IDs so the binary stays deterministic
    qpdf_exit_code=0
    "$QPDF_BIN" --replace-input --object-streams=preserve --stream-data=preserve --deterministic-id --static-id "$file" || qpdf_exit_code=$?

    if [[ $qpdf_exit_code -ne 0 ]]; then
        if [[ $qpdf_exit_code -eq 3 ]]; then
            echo "Aviso: qpdf terminó con warnings (código 3). Continuando."
            rm -f "${file}.~qpdf-orig"
        else
            echo "Error Crítico: qpdf falló con código $qpdf_exit_code"
            exit $qpdf_exit_code
        fi
    fi

    touch -t 197001010000.00 "$file"
done

echo "--------------------------------"
echo "Conversion completed successfully!"
exit 0