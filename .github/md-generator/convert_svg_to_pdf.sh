#!/bin/bash

# 1. Desactivamos el error inmediato para el arranque
set +e

echo "Installing required dependencies..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update && sudo apt-get install -y libimage-exiftool-perl librsvg2-bin qpdf
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install exiftool librsvg qpdf
fi

# Volvemos a activar set -e pero con cuidado
set -e

QPDF_BIN=$(command -v qpdf)
export SOURCE_DATE_EPOCH=0
echo "Setting up reproducible build environment..."

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

echo "Converting SVG files to PDF..."

# Buscamos archivos y procesamos
while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    tmp_pdf=$(mktemp "${tmp_dir}/pdf-XXXXXX.pdf")

    echo "Converting: $svg -> $target_pdf"
    
    # RSVG (si falla aquí, el script muere)
    rsvg-convert -f pdf -o "$tmp_pdf" "$svg"

    # EXIFTOOL
    exiftool -overwrite_original_in_place -all:all= "$tmp_pdf" > /dev/null 2>&1

    # --- QPDF NUCLEAR FIX ---
    # Usamos un subshell ( ) y capturamos el resultado manualmente para que NADA
    # pueda hacer que el script principal vea un código 3.
    echo "Optimizing with qpdf..."
    (
        set +e
        "$QPDF_BIN" --replace-input --object-streams=preserve --stream-data=preserve --deterministic-id --static-id "$tmp_pdf" > /dev/null 2>&1
        exit 0
    )
    # Limpiamos posibles basuras de qpdf
    rm -f "${tmp_pdf}.~qpdf-orig"

    # Timestamps
    touch -t 197001010000.00 "$tmp_pdf"

    # Comparar y mover
    if [[ -f "$target_pdf" ]] && cmp -s "$tmp_pdf" "$target_pdf"; then
        echo "No changes for $target_pdf"
        rm "$tmp_pdf"
    else
        echo "Updating $target_pdf"
        mv "$tmp_pdf" "$target_pdf"
    fi

done < <(find icons -type f -name "*.svg" -print0 2>/dev/null)

echo "Process finished successfully!"
exit 0