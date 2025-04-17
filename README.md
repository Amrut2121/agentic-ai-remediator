# agentic-ai-remediator

🛠️ Required Setup
In Azure DevOps ➝ your pipeline ➝ Variables tab:

Add GEMINI_API_KEY (secure string).

Make sure you have these files in the repo:

agentic_remediator.py

Dockerfile

requirements.txt with:

txt
Copy
Edit
google-generativeai
langchain

🔐 Make Sure:
You’ve set GEMINI_API_KEY in your environment or pipeline secrets.

The Snyk scan is successful and generates a JSON output.

The Dockerfile actually has a vulnerable base image or commands — otherwise Gemini might return it unchanged.

