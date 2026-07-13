import json
import os
from datetime import datetime, timedelta

# Configuration des chemins
CRM_INTERACTIONS = "/root/.hermes/profiles/ai-sales/workspace/crm/interactions.json"
PENDING_QUEUE = "/root/.hermes/profiles/ai-sales/workspace/review-queue/pending"
TEMPLATES = "/root/.hermes/profiles/ai-sales/workspace/content-assets/templates/followup_templates.md"

def load_json(path):
    if not os.path.exists(path): return []
    with open(path, 'r') as f: return json.load(f)

def is_replied(prospect_id, interactions):
    # Check if there's any response from the prospect
    for i in interactions:
        if i['prospect_id'] == prospect_id and i['direction'] == 'inbound':
            return True
    return False

def generate_followup():
    interactions = load_json(CRM_INTERACTIONS)
    
    # 1. Identifier les prospects à relancer
    # Simplification : chercher les messages J+0 non répondus depuis > 3 jours
    for i in interactions:
        if i['step'] == 'initial_outreach' and i['direction'] == 'outbound':
            prospect_id = i['prospect_id']
            sent_date = datetime.fromisoformat(i['date'])
            
            if not is_replied(prospect_id, interactions):
                days_passed = (datetime.now() - sent_date).days
                
                if days_passed >= 3 and days_passed < 7:
                    # Générer template J+3
                    create_draft(prospect_id, "followup_j3")
                elif days_passed >= 7:
                    # Générer template J+7
                    create_draft(prospect_id, "followup_j7")

def create_draft(prospect_id, stage):
    draft_path = f"{PENDING_QUEUE}/followup_{prospect_id}_{stage}.md"
    if not os.path.exists(draft_path):
        with open(draft_path, 'w') as f:
            f.write(f"Draft for {prospect_id} - Stage: {stage}\n\n[TEMPLATE PLACEHOLDER]")
        print(f"Draft created for {prospect_id} at {stage}")

if __name__ == "__main__":
    generate_followup()
