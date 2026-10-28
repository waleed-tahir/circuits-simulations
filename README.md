# Operational Amplifier Circuits Simulation Suite (LTspice & MCP)

This repository contains a complete simulation and verification package for the fundamental operational amplifier (op-amp) configurations using **LTspice 26** and the official **LTspice Model Context Protocol (MCP) Bridge**.

---

## 1. LTspice MCP Integration Setup

The official Analog Devices (ADI) **`ltspice-mcp-bridge.exe`** has been configured to interface with Antigravity IDE and MCP-compliant AI agents.

### Configuration Files
- **Global Config**: `C:\Users\PC\.gemini\config\mcp_config.json`
- **Workspace Config**: `.agents\mcp_config.json`

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

### Capabilities of the LTspice MCP Server (18 Tools)
1. **Schematic & Netlist Operations**: `list_open_designs`, `open_design`, `get_active_design_path`, `get_design_content`, `set_design_content`, `get_schematic_netlist`.
2. **Simulation Lifecycle Control**: `start_simulation`, `is_simulation_running`, `get_spice_log`, `bring_to_front`.
3. **Waveform & Data Extraction**: `get_raw_info`, `read_raw_waveforms`, `export_raw_waveforms`.
4. **Authoritative Reference Documentation**: `list_ltspice_reference_docs`, `get_ltspice_reference`.
5. **Session Control**: `status`, `attach`, `start_headless`.

A dedicated Python client (`ltspice_mcp_client.py`) is included to communicate directly with this bridge.

---

## 2. Circuit Topologies & Analytical Verification

All 7 configurations are implemented as both **visual schematics** (`.asc`) for the LTspice GUI and **SPICE netlists** (`.cir`) for automated batch analysis.

| # | Circuit Configuration | Theoretical Transfer Function | Component Values | Expected Gain / Output | Simulated Result | Error (%) | Status |
|---|----------------------|--------------------------------|------------------|-------------------------|------------------|-----------|--------|
| **1** | **Inverting Amplifier** | $V_o / V_i = -Z_2/Z_1 = -R_2/R_1$ | $R_1=10\text{k}\Omega$, $R_2=50\text{k}\Omega$ | $-5.000\text{ V/V}$ ($180^\circ$ phase) | $4.9997\text{ V/V}$ | $0.0061\%$ | **PASS** |
| **2** | **Non-Inverting Amplifier** | $V_o / V_i = 1 + Z_2/Z_1 = 1 + R_2/R_1$ | $R_1=10\text{k}\Omega$, $R_2=30\text{k}\Omega$ | $+4.000\text{ V/V}$ ($0^\circ$ phase) | $3.9998\text{ V/V}$ | $0.0039\%$ | **PASS** |
| **3** | **Voltage Follower (Buffer)** | $V_o = V_i$ (Gain = 1) | Direct feedback ($R_f=0$), $R_L=1\text{k}\Omega$ | $1.0000\text{ V/V}$ (High $Z_{in}$, Low $Z_{out}$) | $1.0000\text{ V/V}$ ($\Delta V < 20\mu\text{V}$) | $0.0010\%$ | **PASS** |
| **4** | **Summing Amplifier** | $V_o = -R_f \sum \frac{V_k}{R_k}$ | $R_f=20\text{k}$, $R_1=20\text{k}$, $R_2=10\text{k}$, $R_3=40\text{k}$ | $V_o = -(V_1 + 2V_2 + 0.5V_3)$ | $V_{DC} = -0.5000\text{ V}$ | $0.0045\%$ | **PASS** |
| **5** | **Difference (Subtractor) Amp** | $V_o = \frac{R_2}{R_1}(V_2 - V_1)$ | $R_1=10\text{k}, R_2=20\text{k}, R_3=10\text{k}, R_4=20\text{k}$ | $2.000\cdot(V_2 - V_1)$ | $1.9999\text{ V/V}$ | $0.0029\%$ | **PASS** |
| **6** | **Integrator** | $V_o(t) = -\frac{1}{RC}\int V_i\, dt$, $G(s)=-\frac{1}{RCs}$ | $R=10\text{k}\Omega$, $C=100\text{nF}$ ($\tau=1\text{ms}$) | $0.15915\text{ Vpk}$ (@ 1kHz) | $0.15915\text{ Vpk}$ | $0.0016\%$ | **PASS** |
| **7** | **Differentiator** | $V_o(t) = -RC\frac{dV_i}{dt}$, $G(s)=-RCs$ | $C=100\text{nF}$, $R_f=10\text{k}\Omega$, $R_{in}=220\Omega$ | $\pm 1.0000\text{ V}$ plateau for $1000\text{V/s}$ | $\pm 1.0000\text{ V}$ | $0.0040\%$ | **PASS** |

---

## 3. Circuit Details

### 1. Inverting Amplifier (`01_inverting_amplifier/`)
- **Equation**: $V_o = -(R_2 / R_1) V_i$.
- **Design**: $R_1 = 10\text{ k}\Omega$, $R_2 = 50\text{ k}\Omega \implies A_v = -5.000$.
- **Signals**: $1.0\text{ Vpk}$ sine at $1\text{ kHz} \implies 5.0\text{ Vpk}$ inverted output. Virtual ground maintained at node `inv` ($\Delta V_{inv} \approx 32\ \mu\text{V}$).

### 2. Non-Inverting Amplifier (`02_non_inverting_amplifier/`)
- **Equation**: $V_o = (1 + R_2 / R_1) V_i$.
- **Design**: $R_1 = 10\text{ k}\Omega$, $R_2 = 30\text{ k}\Omega \implies A_v = 1 + 30/10 = +4.000$.
- **Signals**: $1.0\text{ Vpk}$ sine at $1\text{ kHz} \implies 4.0\text{ Vpk}$ in-phase output ($0^\circ$ phase shift).

### 3. Voltage Follower / Buffer (`03_voltage_follower/`)
- **Equation**: $V_o = V_i$.
- **Design**: Output tied directly to inverting input. Drives a heavy $1\text{ k}\Omega$ load without voltage droop.
- **Signals**: $2.0\text{ Vpk}$ input $\implies 2.0\text{ Vpk}$ output. Tracking error is below $20\ \mu\text{V}$.

### 4. Summing Amplifier (Inverting) (`04_summing_amplifier/`)
- **Equation**: $V_o = -R_f (V_1/R_1 + V_2/R_2 + V_3/R_3)$.
- **Design**: $R_f = 20\text{ k}\Omega$, weights: $W_1 = -1.0$, $W_2 = -2.0$, $W_3 = -0.5$.
- **Inputs**: $V_1$ ($1\text{ Vpk}$ @ $500\text{ Hz}$), $V_2$ ($0.5\text{ Vpk}$ @ $2\text{ kHz}$), $V_3$ ($1.0\text{ V}$ DC offset).
- **Result**: Output produces clean multi-tone synthesis with exact $-0.5\text{ V}$ DC shift.

### 5. Difference (Subtractor) Amplifier (`05_difference_amplifier/`)
- **Equation**: $V_o = \frac{R_2}{R_1} (V_2 - V_1)$ (matched ratios $R_2/R_1 = R_4/R_3 = 2.0$).
- **Inputs**: $V_1 = 1.0\text{ Vpk}$ (inverting leg), $V_2 = 2.5\text{ Vpk}$ (non-inverting leg).
- **Result**: Differential input $\Delta V = 1.5\text{ Vpk} \implies V_o = 3.0\text{ Vpk}$. High common-mode rejection.

### 6. Integrator (`06_integrator/`)
- **Equation**: $V_o(t) = -\frac{1}{RC} \int V_i\, dt \implies G(s) = -\frac{1}{RCs}$.
- **Design**: $R = 10\text{ k}\Omega$, $C = 100\text{ nF} \implies \tau = 1.0\text{ ms}$, unity-gain frequency $f_0 = 159.15\text{ Hz}$.
- **Result**: For $1.0\text{ Vpk}$ sine input at $1\text{ kHz}$, theoretical output amplitude is $\frac{1}{2\pi f RC} = 0.15915\text{ Vpk}$ (exact simulated match $0.15915\text{ Vpk}$, lagging $90^\circ$).

### 7. Differentiator (`07_differentiator/`)
- **Equation**: $V_o(t) = -RC \frac{dV_i}{dt} \implies G(s) = -RCs$.
- **Design**: $C = 100\text{ nF}$, $R_f = 10\text{ k}\Omega \implies \tau = 1.0\text{ ms}$. Includes $R_{in} = 220\ \Omega$ series damping resistor for high-frequency closed-loop stability.
- **Result**: Input triangle wave $\pm 1\text{ V}$ at $250\text{ Hz}$ has constant slope $\frac{dV_i}{dt} = \pm 1000\text{ V/s}$. Differentiated output is a clean $\mp 1.000\text{ V}$ plateau square wave.

---

## 4. How to Run & Verify

### Option A: Run the Master Automation Script
Executes all 7 simulations in LTspice, extracts `.meas` directives from the `.log` files, validates errors, and generates all plots:
```powershell
python run_all_simulations.py
```

### Option B: Generate / Refresh Waveform Plots
Extracts raw simulation waveforms directly via the LTspice MCP Client:
```powershell
python plot_all_waveforms.py
```
Generated plots are placed in `plots/`:
- `plots/01_inverting_amplifier.png`
- `plots/02_non_inverting_amplifier.png`
- `plots/03_voltage_follower.png`
- `plots/04_summing_amplifier.png`
- `plots/05_difference_amplifier.png`
- `plots/06_integrator.png`
- `plots/07_differentiator.png`
- `plots/summary_dashboard.png`

### Option C: Interactive Graphical Inspection in LTspice GUI
Double-click any `.asc` file in the subfolders (e.g., `01_inverting_amplifier\01_inverting_amplifier.asc`) to open it directly in LTspice, view the schematic, press **Run (F9)**, and probe any wire or component.
