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


These are the vulnerabilities identified by Snyk:
{vuln_summary}

Please:
1. Modify the Dockerfile to address the critical and high vulnerabilities.
2. Suggest safer base images or commands if needed.
3. Provide only the updated Dockerfile.
"""

# Call Gemini
print("⏳ Sending request to Gemini for remediation...")
response = model.generate_content(prompt)
fixed_dockerfile = response.text.strip()

# Save result
Path("Dockerfile.fixed").write_text(fixed_dockerfile)
print("✅ Fixed Dockerfile saved as Dockerfile.fixed")

# Create a PR summary
summary_prompt = f"""
You just fixed a Dockerfile using the following Snyk vulnerabilities:
{vuln_summary[:800]}

Summarize the changes in a concise GitHub PR comment (bullets preferred).
"""

summary_response = model.generate_content(summary_prompt)
Path("pr_summary.md").write_text(summary_response.text.strip())

print("\n📋 PR Summary:\n")
print(summary_response.text.strip())



