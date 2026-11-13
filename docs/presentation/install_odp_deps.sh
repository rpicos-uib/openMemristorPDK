#!/usr/bin/env bash
# Installs the real Python libraries build_odp.py needs to regenerate
# memristor_walkthrough.odp: odfpy (writes the real .odp/OpenDocument
# XML) and Pillow (reads each real screenshot's own pixel dimensions,
# so every image lands on its slide at the correct aspect ratio).
#
# Run on the host (not inside the IIC-OSIC-TOOLS container -- these
# are unrelated to the EDA toolchain, just for building this one
# presentation).
#
# Real, found-live PEP 668 handling, same as ../../install_deps.sh:
# a real, externally-managed system Python refuses a plain `pip
# install`, even with `--user`, with "error: externally-managed-
# environment" -- confirmed real on a real such host, not guessed.
# Rather than pass `--break-system-packages`, this script tries the
# real, plain install first and only on that real, specific failure
# falls back to a real, isolated virtualenv at .venv/.
#
#   bash install_odp_deps.sh
set -euo pipefail
cd "$(dirname "$0")"

VENV_DIR=".venv"
PYTHON=python3

echo "Installing: $(tr '\n' ' ' < requirements-odp.txt)"
if python3 -m pip install --user -r requirements-odp.txt 2>/tmp/install_odp_deps_pip_err.$$; then
    :
elif grep -q "externally-managed-environment" /tmp/install_odp_deps_pip_err.$$; then
    echo
    echo "This Python is externally managed (PEP 668) -- falling back"
    echo "to a real, isolated virtual environment at $VENV_DIR/ ..."
    rm -f /tmp/install_odp_deps_pip_err.$$
    [ -d "$VENV_DIR" ] || python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -r requirements-odp.txt
    PYTHON="$VENV_DIR/bin/python3"
else
    cat /tmp/install_odp_deps_pip_err.$$ >&2
    rm -f /tmp/install_odp_deps_pip_err.$$
    exit 1
fi
rm -f /tmp/install_odp_deps_pip_err.$$

echo
echo "Verifying the real imports resolve (using $PYTHON)..."
"$PYTHON" -c "import odf, PIL; print('odfpy', odf.__version__ if hasattr(odf, \"__version__\") else \"(ok)\"); print('Pillow', PIL.__version__)"

echo
if [ "$PYTHON" = "python3" ]; then
    echo "Ready -- run: python3 build_odp.py"
else
    echo "Ready -- since .venv/ was used, run: $VENV_DIR/bin/python3 build_odp.py"
fi
