#!/usr/bin/env python3
import subprocess, sys
cmd=[sys.executable, "/root/.hermes/profiles/ai-sales/workspace/scripts/run_daily.py"]
cp=subprocess.run(cmd, text=True, capture_output=True)
# Deliver a concise message; full JSON is saved under workspace/reports/.
if cp.returncode == 0:
    print("✅ ai-sales daily orchestration OK — digest généré, Slack notifié, aucun envoi cold automatique. Voir workspace/reports/.")
else:
    print("⚠️ ai-sales daily orchestration KO")
    print(cp.stdout[-2000:])
    print(cp.stderr[-2000:])
sys.exit(cp.returncode)
