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

# Installs a missing host-side command via the system package manager
# (apt-get on Debian/Ubuntu, dnf on Fedora/RHEL/Rocky) if it isn't on
# PATH already. Only ever used for $CONTAINER_ENGINE itself below --
# everything else this script needs (python3, pgrep, ...) runs inside
# the already-provisioned IIC-OSIC-TOOLS container, not on the host.
ensure_installed() {
    local cmd="$1" pkg="${2:-$1}"
    command -v "$cmd" >/dev/null 2>&1 && return 0
    echo "[INFO] '$cmd' not found on this host -- installing '$pkg' ..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y "$pkg"
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y "$pkg"
    else
        echo "[ERROR] Neither apt-get nor dnf found -- install '$cmd' manually." >&2
        exit 1
    fi
}

ensure_installed "${CONTAINER_ENGINE}"

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
