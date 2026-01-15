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

PROGRESS_ACTIVE=0
CURRENT_PROGRESS=0
TOTAL_PROGRESS=0

log_msg() {
    if [[ ${PROGRESS_ACTIVE:-0} -eq 1 ]]; then
        printf '\r\033[K'
        PROGRESS_ACTIVE=0
    fi
    echo "$@"
    if [[ ${TOTAL_PROGRESS:-0} -gt 0 ]]; then
        render_progress_bar "$CURRENT_PROGRESS" "$TOTAL_PROGRESS"
    fi
}

finalize_progress_bar() {
    if [[ ${PROGRESS_ACTIVE:-0} -eq 1 ]]; then
        printf "\n"
        PROGRESS_ACTIVE=0
    fi
}

render_progress_bar() {
    local current=$1
    local total=$2
    local width=40
    local percent=$(( current * 100 / total ))
    local filled=$(( percent * width / 100 ))
    local empty=$(( width - filled ))
    local bar_filled bar_empty

    printf -v bar_filled '%*s' "$filled" ''
    bar_filled=${bar_filled// /#}
    printf -v bar_empty '%*s' "$empty" ''
    bar_empty=${bar_empty// /-}

    CURRENT_PROGRESS=$current
    TOTAL_PROGRESS=$total
    printf "\rProgress: [%s%s] %3d%% (%d/%d)" "$bar_filled" "$bar_empty" "$percent" "$current" "$total"
    PROGRESS_ACTIVE=1
}

QPDF_BIN=$(command -v qpdf)
export SOURCE_DATE_EPOCH=0
echo "Setting up reproducible build environment..."

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

echo "Converting SVG files to PDF..."

total_svgs=$(find icons -type f -name "*.svg" 2>/dev/null | wc -l | tr -d ' ')
if [[ -z "$total_svgs" || "$total_svgs" -eq 0 ]]; then
    echo "No SVG files found under icons/. Nothing to convert."
    exit 0
fi

processed_svgs=0
render_progress_bar 0 "$total_svgs"

# Buscamos archivos y procesamos
while IFS= read -r -d '' svg; do
    target_pdf="${svg%.*}.pdf"
    tmp_pdf=$(mktemp "${tmp_dir}/pdf-XXXXXX.pdf")

    log_msg "Converting: $svg -> $target_pdf"
    
    # RSVG (si falla aquí, el script muere)
    rsvg-convert -f pdf -o "$tmp_pdf" "$svg"

    # EXIFTOOL
    exiftool -overwrite_original_in_place -all:all= "$tmp_pdf" > /dev/null 2>&1

    # --- QPDF NUCLEAR FIX ---
    # Usamos un subshell ( ) y capturamos el resultado manualmente para que NADA
    # pueda hacer que el script principal vea un código 3.
    log_msg "Optimizing with qpdf..."
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
        log_msg "No changes for $target_pdf"
        rm "$tmp_pdf"
    else
        log_msg "Updating $target_pdf"
        mv "$tmp_pdf" "$target_pdf"
    fi

    ((processed_svgs++))
    render_progress_bar "$processed_svgs" "$total_svgs"

done < <(find icons -type f -name "*.svg" -print0 2>/dev/null)

finalize_progress_bar
log_msg "Process finished successfully!"
exit 0