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

    # 3. Normalizar con qpdf
    # Inicializamos la variable de estado en 0
    qpdf_exit_code=0
    
    # ESTA ES LA CLAVE:
    # Usamos "|| qpdf_exit_code=$?"
    # Esto evita que 'set -e' mate el script inmediatamente si qpdf devuelve 3.
    "$QPDF_BIN" --replace-input --object-streams=preserve --stream-data=preserve --deterministic-id --static-id "$tmp_pdf" || qpdf_exit_code=$?

    if [[ $qpdf_exit_code -ne 0 ]]; then
        if [[ $qpdf_exit_code -eq 3 ]]; then
            echo "Aviso: qpdf terminó con advertencias (código 3). Esto es aceptable."
            # Borramos el backup que genera qpdf cuando hay warnings
            rm -f "${tmp_pdf}.~qpdf-orig"
        else
            echo "Error Crítico: qpdf falló con código $qpdf_exit_code"
            exit $qpdf_exit_code
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
exit 0