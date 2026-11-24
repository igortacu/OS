#!/usr/bin/env python3
"""Build Lab 12 using the shared UTM report style."""
from pathlib import Path
import subprocess
import sys

subprocess.run([sys.executable, str(Path(__file__).with_name('build-utm-reports.py')),
                '--only', '12'], check=True)
