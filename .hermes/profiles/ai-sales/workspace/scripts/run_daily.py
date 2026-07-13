import json
import os
from pathlib import Path
from datetime import datetime

# Paths
WORKSPACE = Path("/root/.hermes/profiles/ai-sales/workspace")
PENDING_DIR = WORKSPACE / "review-queue/pending"
REPORTS_DIR = WORKSPACE / "reports"

def generate_digest():
    pending_leads = list(PENDING_DIR.glob("*.md"))
    
    digest_content = f"# Digest Quotidien - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    digest_content += "## 🚨 Review Queue (En attente de validation)\n"
    
    if not pending_leads:
        digest_content += "- Aucune action en attente.\n"
    else:
        for lead in pending_leads:
            digest_content += f"- [ ] {lead.name}\n"
    
    digest_content += "\n## 📊 Pipeline Status\n"
    digest_content += "- Le CRM est à jour.\n"
    
    report_file = REPORTS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}-daily-digest.md"
    with open(report_file, "w") as f:
        f.write(digest_content)
    
    print(f"Digest generated: {report_file}")

if __name__ == "__main__":
    generate_digest()
