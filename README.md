# openMemristorPDK

A bare-minimum, multi-material memristor PDK built from scratch with
[openPDKcreator](https://github.com/rpicos-uib/openpdkcreator-toolkit)'s own GUI.
It is a teaching PDK: the materials, layers and parameters are illustrative,
not a qualified process.

- **Devices:** Au/TiO₂/Au, Au/TiO₂/Ti and Au/HfO₂/Al memristors, plus 2×2 and
  4×4 crossbars.
- **Layers:** a 6-layer stack (bottom electrode, switching oxide, top
  electrode) with its own KLayout layer file and technology
  (`openmemristorpdk.lyp` / `.lyt`), Magic tech file and DRC rules.
- **Models:** Verilog-A compact models (HP linear ion drift for TiO₂, a
  threshold-switching model for HfO₂), compiled to OSDI for ngspice
  automatically when openPDKcreator starts.
- **Views:** LEF, xschem symbols and schematics, Magic layouts, GDS, CDL/SPICE,
  Verilog and Liberty, plus TT/FF/SS corners.

## Beginner guide

[`docs/for_dummies/index.html`](docs/for_dummies/index.html) is a step-by-step
guide with a real screenshot for every click: installing everything on a new
computer, starting the tools, simulating a memristor's pinched hysteresis loop
and looking at its layout. Open it in a browser.

Example of the guide published online:
<http://memristors.uib.es:8081/memristorPDK/for_dummies/>

## Using it

This repository holds the PDK and its project data only. openPDKcreator itself
comes from the [openpdkcreator-toolkit](https://github.com/rpicos-uib/openpdkcreator-toolkit)
checkout this project lives inside:

```
git clone https://github.com/rpicos-uib/openpdkcreator-toolkit.git openPDKcreator
cd openPDKcreator
git clone https://github.com/rpicos-uib/openMemristorPDK.git
./start_eda_container.sh --gui-memristor
```

The last command starts the IIC-OSIC-TOOLS container (it needs
[IIC-OSIC-TOOLS](https://github.com/iic-jku/IIC-OSIC-TOOLS) cloned in
`~/eda/IIC-OSIC-TOOLS`) and opens the GUI inside it. It runs

```
main.py --project-root openMemristorPDK --pdk-root openMemristorPDK/data/openmemristorpdk gui
```

The beginner guide's Part 0 covers the full first-time setup.

## Layout

| Path | Contents |
|---|---|
| `data/openmemristorpdk/` | The editable PDK tree (`libs.tech/`, `libs.ref/`) |
| `export/openmemristorpdk/` | open_pdks-format output exported from the GUI |
| `libraries/openmemristorpdk_pr/` | Cell views: schematics, layouts, GDS, netlists |
| `user_models/` | Verilog and Verilog-A models (`.osdi` files are built automatically) |
| `saves/` | openPDKcreator's saved edits for this PDK |
| `docs/` | The beginner guide, presentations and simulation scripts |

## License

Apache License 2.0, see [LICENSE](LICENSE).
