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

# Crear directorio temporal
tmp_dir=$(mktemp -d)
cleanup() {
    rm -rf "$tmp_dir"
}
trap cleanup EXIT

# Usamos process substitution para evitar subshells
while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    tmp_pdf=$(mktemp "${tmp_dir}/pdf-XXXXXX.pdf")

    echo "Converting: $svg -> $target_pdf"
    
    # 1. Convertir SVG a PDF
    if ! rsvg-convert -f pdf -o "$tmp_pdf" "$svg"; then
        echo "Error: rsvg-convert failed for $svg"
        exit 1
    fi

    # 2. Limpiar Metadatos
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

    # 3. Normalizar con qpdf (SOLUCIÓN DEFINITIVA AL ERROR 3)
    # Al poner el comando dentro del 'if', Bash NO aborta el script aunque devuelva error (set -e se pausa)
    if ! "$QPDF_BIN" --replace-input --object-streams=preserve --stream-data=preserve --deterministic-id --static-id "$tmp_pdf"; then
        qpdf_status=$?
        
        # El código 3 significa "Warnings" (éxito parcial). Lo aceptamos.
        if [[ $qpdf_status -eq 3 ]]; then
            echo "Aviso: qpdf completó con advertencias (exit code 3). Continuando..."
            # qpdf suele dejar un archivo .~qpdf-orig cuando da warnings, lo borramos
            rm -f "${tmp_pdf}.~qpdf-orig"
        else
            # Cualquier otro código es un error real
            echo "Error Crítico: qpdf falló con código $qpdf_status"
            exit $qpdf_status
        fi
    fi

    # 4. Establecer fecha fija para reproducibilidad
    touch -t 197001010000.00 "$tmp_pdf"

    # 5. Comparar y mover si es necesario
    if [[ -f "$target_pdf" ]] && cmp -s "$tmp_pdf" "$target_pdf"; then
        echo "No changes detected for $target_pdf"
        rm "$tmp_pdf"
    else
        echo "Updating $target_pdf"
        mv "$tmp_pdf" "$target_pdf"
    fi

done < <(find icons -type f -name "*.svg" -print0 2>/dev/null)

echo "--------------------------------"
echo "Conversion completed successfully!"
# Forzamos un exit 0 limpio al final
exit 0