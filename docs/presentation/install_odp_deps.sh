#!/usr/bin/env bash
# Installs the real Python libraries build_odp.py needs to regenerate
# memristor_walkthrough.odp: odfpy (writes the real .odp/OpenDocument
# XML) and Pillow (reads each real screenshot's own pixel dimensions,
# so every image lands on its slide at the correct aspect ratio).
#
# Run on the host (not inside the IIC-OSIC-TOOLS container -- these
# are unrelated to the EDA toolchain, just for building this one
# presentation):
#
#   bash install_odp_deps.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "Installing: $(tr '\n' ' ' < requirements-odp.txt)"
python3 -m pip install --user -r requirements-odp.txt

echo "Done. Verifying the real imports resolve..."
python3 -c "import odf, PIL; print('odfpy', odf.__version__ if hasattr(odf, \"__version__\") else \"(ok)\"); print('Pillow', PIL.__version__)"

echo "Ready -- run: python3 build_odp.py"
