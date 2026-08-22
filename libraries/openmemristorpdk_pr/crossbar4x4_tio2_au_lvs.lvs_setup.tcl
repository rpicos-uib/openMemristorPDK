# Real, minimal netgen LVS setup. No real transistor/resistor/
# capacitor device *classes* are registered here -- a from-scratch
# project with no such real devices in its own Magic tech file yet
# doesn't need any (a real, fuller PDK's own libs.tech/netgen/
# setup.tcl -- e.g. SkyWater sky130A's own real, ~500-line file --
# adds one real `lappend devices ...`/permute/property block per
# real device class it needs LVS to treat specially).
permute default
property default
property parallel none
