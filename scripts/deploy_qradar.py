import os
import yaml
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_URL = os.getenv("QRADAR_URL", "https://qradar.local/api")
QRADAR_TOKEN = os.getenv("QRADAR_TOKEN", "your_qradar_sec_token")

def deploy_qradar_rules():
    rules_dir = "rules/qradar"
    headers = {
        "SEC": QRADAR_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    for filename in os.listdir(rules_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(rules_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                rule_data = yaml.safe_load(f)
                
            rule_name = rule_data.get("title", filename)
            qradar_aql = rule_data.get("qradar_aql", "")
            
            payload = {
                "name": rule_name,
                "type": "AQL",
                "expression": qradar_aql,
                "description": rule_data.get("description", "")
            }
            
            endpoint = f"{QRADAR_URL}/siem/custom_rules"
            response = requests.post(endpoint, headers=headers, json=payload, verify=False)
            if response.status_code in [200, 201]:
                print(f"[QRadar] Successfully deployed rule: {rule_name}")
            else:
                print(f"[QRadar] Failed to deploy {rule_name}: {response.text}")

if __name__ == "__main__":
    deploy_qradar_rules()
