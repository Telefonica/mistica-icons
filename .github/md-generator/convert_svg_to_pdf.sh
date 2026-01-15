#!/bin/bash

# Script to convert SVG files to PDF with reproducible checksums
set -e

echo "Installing required dependencies..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y libimage-exiftool-perl librsvg2-bin qpdf
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install exiftool librsvg qpdf
fi

QPDF_BIN=$(command -v qpdf)
if [[ -z "$QPDF_BIN" ]]; then
    echo "Error: qpdf not found."
    exit 1
fi

echo "Setting up reproducible build environment..."
export SOURCE_DATE_EPOCH=0

echo "Converting SVG files to PDF..."

tmp_dir=$(mktemp -d)
cleanup() {
    rm -rf "$tmp_dir"
}
trap cleanup EXIT

# Usamos process substitution para evitar subshells
while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    
    # 1. Archivos temporales separados (evita problemas de lock o corrupción)
    raw_pdf=$(mktemp "${tmp_dir}/raw-XXXXXX.pdf")
    clean_pdf=$(mktemp "${tmp_dir}/clean-XXXXXX.pdf")

    echo "Converting: $svg -> $target_pdf"
    
    # 2. Generar el PDF "crudo" con rsvg
    if ! rsvg-convert -f pdf -o "$raw_pdf" "$svg"; then
        echo "Error: rsvg-convert failed for $svg"
        exit 1
    fi

    # 3. Limpiar metadatos en el PDF crudo
    exiftool -overwrite_original_in_place \
        -all:all= \
        -Creator= \
        -Producer= \
        -CreationDate= \
        -ModDate= \
        -Title= \
        -Subject= \
        -Keywords= \
        "$raw_pdf" > /dev/null 2>&1

    # 4. QPDF: De Raw a Clean (Sin --replace-input)
    # Usamos "|| true" para capturar el código después sin que set -e nos mate
    qpdf_exit_code=0
    "$QPDF_BIN" "$raw_pdf" "$clean_pdf" \
        --object-streams=preserve \
        --stream-data=preserve \
        --deterministic-id \
        --static-id \
        > /dev/null 2>&1 || qpdf_exit_code=$?

    # Manejo del código de salida
    if [[ $qpdf_exit_code -ne 0 ]]; then
        if [[ $qpdf_exit_code -eq 3 ]]; then
            # Código 3 es Warning. Verificamos que el archivo de salida exista.
            if [[ -f "$clean_pdf" ]]; then
                echo "Warning: qpdf found issues in structure but fixed them (code 3)."
            else
                echo "Error: qpdf returned code 3 but output file is missing."
                exit 1
            fi
        else
            echo "Critical Error: qpdf failed with code $qpdf_exit_code"
            exit $qpdf_exit_code
        fi
    fi

    # 5. Establecer timestamps fijos en el archivo limpio
    touch -t 197001010000.00 "$clean_pdf"

    # 6. Comparar y mover
    if [[ -f "$target_pdf" ]] && cmp -s "$clean_pdf" "$target_pdf"; then
        echo "No changes detected for $target_pdf"
    else
        echo "Updating $target_pdf"
        mv "$clean_pdf" "$target_pdf"
    fi
    
    # Limpieza inmediata de temporales de esta iteración
    rm -f "$raw_pdf" "$clean_pdf"

done < <(find icons -type f -name "*.svg" -print0 2>/dev/null)

echo "--------------------------------"
echo "Conversion completed successfully!"
exit 0