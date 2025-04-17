import google.generativeai as genai
import json
from pathlib import Path
import os

# Load Dockerfile and Snyk scan result
dockerfile_path = "Dockerfile"
scan_path = "scan.json"

# Read contents
dockerfile = Path(dockerfile_path).read_text()
scan_report = json.loads(Path(scan_path).read_text())

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Extract vulnerabilities
def format_snyk_vulns(scan_json):
    if "vulnerabilities" in scan_json:
        vulns = scan_json["vulnerabilities"]
    elif "docker" in scan_json and "vulnerabilities" in scan_json["docker"]:
        vulns = scan_json["docker"]["vulnerabilities"]
    else:
        vulns = []

    summaries = []
    for vuln in vulns:
        summaries.append(f"- **{vuln.get('title')}** (Severity: {vuln.get('severity')}): {vuln.get('description', '')[:200]}...")

    return "\n".join(summaries)

vuln_summary = format_snyk_vulns(scan_report)

# Construct prompt for Gemini
prompt = f"""
You are a DevSecOps AI assistant.

The following is the Dockerfile used in a project:
