import os
import yaml
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPLUNK_URL = os.getenv("SPLUNK_URL", "https://splunk.local:8089")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN", "your_splunk_bearer_token")

def deploy_splunk_rules():
    rules_dir = "rules/splunk"
    headers = {"Authorization": f"Bearer {SPLUNK_TOKEN}"}
    
    for filename in os.listdir(rules_dir):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(rules_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                rule_data = yaml.safe_load(f)
                
            rule_name = rule_data.get("title", filename)
            splunk_spl = rule_data.get("splunk_spl", "")
            
            payload = {
                "name": rule_name,
                "search": splunk_spl,
                "description": rule_data.get("description", "")
            }
            
            endpoint = f"{SPLUNK_URL}/services/saved/searches"
            response = requests.post(endpoint, headers=headers, data=payload, verify=False)
            if response.status_code in [200, 201]:
                print(f"[Splunk] Successfully deployed rule: {rule_name}")
            else:
                print(f"[Splunk] Failed to deploy {rule_name}: {response.text}")

if __name__ == "__main__":
    deploy_splunk_rules()
