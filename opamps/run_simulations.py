"""
Op-Amp Simulation Runner (Local)
-------------------------------
Direct runner for all circuits inside opamps/
"""

import os
import sys

# Ensure root directory is on python path so ltspice_mcp_client can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from run_all_simulations import main

if __name__ == "__main__":
    main()
