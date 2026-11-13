#!/usr/bin/env bash
# Launches main.py gui for THIS project's PDK (data/openmemristorpdk),
# not the ihp-sg13g2 default main.py --pdk-root falls back to.
#
# Needs the IIC-OSIC-TOOLS container the outer openPDKcreator repo's
# own start_eda_container.sh provides (real X11/Xvnc display -- main.py
# gui will never show a window run directly on this host). That script
# mounts the outer repo root at /foss/designs inside the container, so
# this project is reachable in there at /foss/designs/openMemristorPDK
# -- confirmed by reading that script directly, not guessed.
#
#   bash start_gui.sh
set -euo pipefail
cd "$(dirname "$0")"

OUTER_REPO="$(cd .. && pwd)"
CONTAINER_ENGINE="${CONTAINER_ENGINE:-podman}"
CONTAINER_NAME="${CONTAINER_NAME:-iic-osic-tools_openpdkcreator_uid_$(id -u)}"

# Starts (or reattaches to) the shared container; prints its VNC URL.
# Deliberately run WITHOUT --gui -- that flag launches the outer
# repo's own main.py gui against ihp-sg13g2, not this PDK.
"$OUTER_REPO/start_eda_container.sh"

if "${CONTAINER_ENGINE}" exec "${CONTAINER_NAME}" pgrep -f "main.py --pdk-root data/openmemristorpdk gui" > /dev/null 2>&1; then
    echo "[INFO] main.py gui is already running against data/openmemristorpdk."
else
    echo "[INFO] Launching main.py gui against data/openmemristorpdk ..."
    "${CONTAINER_ENGINE}" exec -d -e DISPLAY=:1 -w /foss/designs/openMemristorPDK "${CONTAINER_NAME}" \
        python3 main.py --pdk-root data/openmemristorpdk gui
fi
