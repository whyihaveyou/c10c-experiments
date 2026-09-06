"""Run the two deterministic certificate checks used in the C_10c baseline."""
import subprocess
import sys

for script in ("verify_known_certificate.py", "verify_hamming_8.py"):
    print(f"== {script} ==", flush=True)
    subprocess.run([sys.executable, script], check=True)
