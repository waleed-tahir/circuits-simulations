"""
Master Simulation Automation & Verification Script
--------------------------------------------------
Runs all operational amplifier circuits under opamps/ in LTspice, extracts and verifies
all simulation metrics against their analytical textbook equations, and
outputs a formatted summary comparison report.
"""

import json
import os
import re
import subprocess
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPAMPS_DIR = os.path.join(BASE_DIR, "opamps")
LTSPICE_EXE = r"C:\Program Files\ADI\LTspice\LTspice.exe"

CIRCUITS = [
    {
        "id": "01_inverting_amplifier",
        "name": "Inverting Amplifier",
        "formula": "V_o/V_i = -R2/R1",
        "components": "R1=10k, R2=50k",
        "theoretical_gain": -5.000,
        "gain_metric": "gain_mag",
        "expected_value": 5.000,
        "unit": "V/V (magnitude)"
    },
    {
        "id": "02_non_inverting_amplifier",
        "name": "Non-Inverting Amplifier",
        "formula": "V_o/V_i = 1 + R2/R1",
        "components": "R1=10k, R2=30k",
        "theoretical_gain": 4.000,
        "gain_metric": "gain_mag",
        "expected_value": 4.000,
        "unit": "V/V"
    },
    {
        "id": "03_voltage_follower",
        "name": "Voltage Follower (Buffer)",
        "formula": "V_o = V_i",
        "components": "Direct feedback, RL=1k",
        "theoretical_gain": 1.000,
        "gain_metric": "gain",
        "expected_value": 1.000,
        "unit": "V/V"
    },
    {
        "id": "04_summing_amplifier",
        "name": "Summing Amplifier (Inverting)",
        "formula": "V_o = -Rf*(V1/R1 + V2/R2 + V3/R3)",
        "components": "Rf=20k, R1=20k, R2=10k, R3=40k",
        "theoretical_gain": -0.500,  # DC component from 1V DC
        "gain_metric": "vout_dc",
        "expected_value": -0.500,
        "unit": "V (DC offset)"
    },
    {
        "id": "05_difference_amplifier",
        "name": "Difference (Subtractor) Amp",
        "formula": "V_o = (R2/R1)*(V2 - V1)",
        "components": "R1=10k, R2=20k, R3=10k, R4=20k",
        "theoretical_gain": 2.000,
        "gain_metric": "diff_gain",
        "expected_value": 2.000,
        "unit": "V/V"
    },
    {
        "id": "06_integrator",
        "name": "Integrator",
        "formula": "V_o = -(1/RC) * integral(V_i dt)",
        "components": "R=10k, C=100nF (tau=1ms)",
        "theoretical_gain": 0.159155,  # 1/(2*pi*f*RC) at 1kHz
        "gain_metric": "sim_gain",
        "expected_value": 0.159155,
        "unit": "Vpk/Vpk @ 1kHz"
    },
    {
        "id": "07_differentiator",
        "name": "Differentiator",
        "formula": "V_o = -RC * (dVi/dt)",
        "components": "C=100nF, Rf=10k, Rin=220",
        "theoretical_gain": 1.000,  # plateau level for 1000V/s triangle
        "gain_metric": "vout_plateau_pos",
        "expected_value": 1.000,
        "unit": "V (Square plateau)"
    }
]


def parse_meas_from_log(log_path):
    measurements = {}
    if not os.path.exists(log_path):
        return measurements
    
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            m = re.match(r"^([a-zA-Z0-9_]+):.*=\s*([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)", line)
            if m:
                var_name = m.group(1).lower()
                val = float(m.group(2))
                measurements[var_name] = val
    return measurements


def main():
    print("=" * 80)
    print("LTspice Op-Amp Basic Configurations — Automated Simulation & Verification")
    print("=" * 80)
    print(f"Simulator Engine: {LTSPICE_EXE}")
    print(f"Base Directory:   {BASE_DIR}")
    print(f"Op-Amps Folder:   {OPAMPS_DIR}\n")

    results = []

    for item in CIRCUITS:
        cid = item["id"]
        cname = item["name"]
        asc_path = os.path.join(OPAMPS_DIR, cid, f"{cid}.asc")
        log_path = os.path.join(OPAMPS_DIR, cid, f"{cid}.log")

        print(f"Running simulation for: {cname}...")
        cmd = [LTSPICE_EXE, "-b", asc_path]
        proc = subprocess.run(cmd, capture_output=True, text=True)

        meas = parse_meas_from_log(log_path)
        metric_key = item["gain_metric"]
        sim_val = meas.get(metric_key, None)
        theo_val = item["expected_value"]

        if sim_val is not None:
            err_pct = abs((sim_val - theo_val) / theo_val) * 100.0 if theo_val != 0 else abs(sim_val)
            status = "PASS" if err_pct < 0.1 else "WARN"
        else:
            err_pct = None
            status = "FAIL"

        result_entry = {
            "id": cid,
            "name": cname,
            "formula": item["formula"],
            "components": item["components"],
            "theoretical": theo_val,
            "simulated": sim_val,
            "error_pct": err_pct,
            "unit": item["unit"],
            "status": status,
            "all_measurements": meas
        }
        results.append(result_entry)

    print("\n" + "=" * 105)
    print(f"{'Circuit Name':<28} | {'Formula':<30} | {'Theory':<9} | {'Simulated':<10} | {'Error %':<8} | {'Status'}")
    print("-" * 105)

    for r in results:
        theo_str = f"{r['theoretical']:.4f}"
        sim_str = f"{r['simulated']:.4f}" if r["simulated"] is not None else "N/A"
        err_str = f"{r['error_pct']:.4f}%" if r["error_pct"] is not None else "N/A"
        print(f"{r['name']:<28} | {r['formula']:<30} | {theo_str:<9} | {sim_str:<10} | {err_str:<8} | [{r['status']}]")

    print("=" * 105)

    # Save results to JSON inside opamps/
    json_path = os.path.join(OPAMPS_DIR, "simulation_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Complete numeric results saved to: {json_path}")

    # Generate plots
    print("\nGenerating waveform plots...")
    plot_script = os.path.join(BASE_DIR, "plot_all_waveforms.py")
    subprocess.run([sys.executable, plot_script])
    print("\nAll simulations and visualizations completed successfully!")


if __name__ == "__main__":
    main()
