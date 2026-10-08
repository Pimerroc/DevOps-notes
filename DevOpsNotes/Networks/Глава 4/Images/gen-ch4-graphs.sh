#!/usr/bin/env bash
# Перегенерировать ВСЕ графики главы 4 одним запуском.
#   bash gen-ch4-graphs.sh
# Зависимости: graphviz (dot) и rsvg-convert — оба есть в системе по умолчанию.
set -euo pipefail
cd "$(dirname "$0")"
echo "== графики главы 4 =="
python3 gen-ch4-plots.py .
bash gen-ch4-diagrams.sh .
echo
echo "Готово:"
ls -1 ch4-*.png