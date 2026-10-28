# Electronic Circuit Simulations (LTspice & MCP)

A modular, automated analog and mixed-signal electronic circuit simulation repository powered by **LTspice 26** and the official **LTspice Model Context Protocol (MCP) Bridge**.

Designed to support scalable component-by-component library expansion, providing SPICE netlists, visual `.asc` schematics, automated validation scripts, waveform extractors, and publication-ready plots.

---

## Repository Structure

```
circuits-simulations/
├── .agents/
│   └── mcp_config.json              # Workspace LTspice MCP bridge configuration
├── opamps/                          # Operational Amplifier Simulation Suite
│   ├── 01_inverting_amplifier/      # V_o = -(R2/R1) * V_i
│   ├── 02_non_inverting_amplifier/  # V_o = (1 + R2/R1) * V_i
│   ├── 03_voltage_follower/         # V_o = V_i (Unity buffer)
│   ├── 04_summing_amplifier/        # V_o = -Rf * sum(Vk / Rk)
│   ├── 05_difference_amplifier/     # V_o = (R2/R1) * (V2 - V1)
│   ├── 06_integrator/               # V_o = -(1/RC) * integral(Vi dt)
│   ├── 07_differentiator/           # V_o = -RC * (dVi/dt)
│   ├── plots/                       # High-res waveform plots & summary dashboard
│   ├── simulation_results.json      # Verified metrics & error table
│   ├── run_simulations.py           # Sub-suite runner
│   └── README.md                    # Op-Amp technical derivations & analysis
├── ltspice_mcp_client.py            # Reusable JSON-RPC client for LTspice MCP bridge
├── run_all_simulations.py           # Master automated verification runner
├── plot_all_waveforms.py            # Master waveform visualization engine
├── .gitignore                       # Git ignore for temporary SPICE artifacts (.raw, .log, .db)
└── README.md                        # Master repository documentation
```

### Planned Future Component Modules
- `diodes/`: Rectifiers, Zener regulators, clippers, clampers, small-signal models.
- `bjt/`: Common-emitter, common-collector (emitter follower), common-base amplifiers.
- `mosfets/`: CMOS inverters, current mirrors, differential pairs, switching stages.
- `filters/`: Sallen-Key active filters, Butterworth, Chebyshev, notch filters.
- `timers_555/`: Astable and monostable multivibrators.
- `power/`: Buck/boost converters, LDO regulators, flyback converters.

---

## LTspice MCP Integration

The workspace includes configuration for the official **`ltspice-mcp-bridge.exe`** allowing AI agents and external tools to interact directly with LTspice.

### Configuration (`.agents/mcp_config.json`):
```json
{
  "mcpServers": {
    "ltspice": {
      "command": "C:\\Program Files\\ADI\\LTspice\\ltspice-mcp-bridge.exe",
      "args": [],
      "env": {
        "LTSPICE_INSTALL_DIR": "C:\\Program Files\\ADI\\LTspice"
      }
    }
  }
}
```

The bridge provides 18 tools enabling:
- Opening, inspecting, and editing `.asc` schematic files.
- Launching headless or GUI batch simulations.
- Reading binary waveform data directly into structured arrays.
- Accessing official ADI reference documentation.

---

## Active Component Suite: Operational Amplifiers (`opamps/`)

The op-amp suite implements and verifies the seven classical topologies:

| # | Topology | Transfer Function | Components | Theory | Simulated | Error (%) | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Inverting Amp** | $V_o/V_i = -R_2/R_1$ | $R_1=10\text{k}, R_2=50\text{k}$ | $-5.000\text{ V/V}$ | $4.9997\text{ V/V}$ | $0.0061\%$ | **PASS** |
| 2 | **Non-Inverting Amp** | $V_o/V_i = 1 + R_2/R_1$ | $R_1=10\text{k}, R_2=30\text{k}$ | $+4.000\text{ V/V}$ | $3.9998\text{ V/V}$ | $0.0039\%$ | **PASS** |
| 3 | **Voltage Follower** | $V_o = V_i$ | Direct feedback, $R_L=1\text{k}$ | $1.0000\text{ V/V}$ | $1.0000\text{ V/V}$ | $0.0010\%$ | **PASS** |
| 4 | **Summing Amp** | $V_o = -R_f \sum \frac{V_k}{R_k}$ | $R_f=20\text{k}, R_1=20\text{k}, R_2=10\text{k}, R_3=40\text{k}$ | $V_{DC} = -0.5000\text{ V}$ | $-0.5000\text{ V}$ | $0.0045\%$ | **PASS** |
| 5 | **Difference Amp** | $V_o = \frac{R_2}{R_1}(V_2 - V_1)$ | $R_1=10\text{k}, R_2=20\text{k}, R_3=10\text{k}, R_4=20\text{k}$ | $2.000\cdot(V_2 - V_1)$ | $1.9999\text{ V/V}$ | $0.0029\%$ | **PASS** |
| 6 | **Integrator** | $V_o = -\frac{1}{RC}\int V_i dt$ | $R=10\text{k}, C=100\text{nF}$ ($\tau=1\text{ms}$) | $0.15915\text{ Vpk}$ | $0.15915\text{ Vpk}$ | $0.0016\%$ | **PASS** |
| 7 | **Differentiator** | $V_o = -RC\frac{dV_i}{dt}$ | $C=100\text{nF}, R_f=10\text{k}, R_{in}=220\Omega$ | $\pm 1.0000\text{ V}$ | $\pm 1.0000\text{ V}$ | $0.0040\%$ | **PASS** |

See the detailed mathematical derivations, schematics, and waveforms in [opamps/README.md](opamps/README.md).

---

## Quickstart

### 1. Run Automated Simulation & Verification
```powershell
python run_all_simulations.py
```

### 2. Generate / Refresh Plots
```powershell
python plot_all_waveforms.py
```

### 3. Open Interactively in LTspice GUI
Double-click any `.asc` schematic file inside the subdirectories (e.g. `opamps\01_inverting_amplifier\01_inverting_amplifier.asc`) to inspect the schematic, modify parameters, and run simulations with LTspice's built-in interactive probe viewer.
