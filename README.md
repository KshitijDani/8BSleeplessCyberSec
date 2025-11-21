---

# 8BSleeplessCyberSec Agent
This is a static security analysis agent that helps developers and repo owners discover security vulnerabilities in their code. In the future, it is meant to be run directly where code is hosted. A plug-in is envisioned for developers to run this tool against files they are updating.

The Agent provides updates on possible security vulnerabilities, type of attack that could exploit the vulnerability, the severity and a remediation.

## Current Status

The purpose of this project is to help us understand how to build an Agent and find common use-cases.
The agent uses LangGraph to create a graph of the different stages in the Analysis pipeline.

### Current Pipeline

```
[start] -> [fetch_repo] -> [extract_php_files] -> [analyze_files] -> [save_output] -> [cleanup]
```
We start by fetching all code files in a repo, analyze each file for vulnerabilities, come up with severities and remediations and output this as a CSV file to the user.

### Analysis Details

* In the **[analyze_files]** node we use OpenAI's Completions API to make calls to a **gpt-4o-mini** LLM model.
* Users can input a link to a publically accessible **github repo**.
* The app parses all **php** files in the repo and fetches all possible security vulnerabilities associated with the endpoints or actions in each file.
* It then stores the vulnerabilities in an output file in **app/output_action**.
* To view the latest run's endpoints go to **[http://127.0.0.1:8000/api/latest-routes](http://127.0.0.1:8000/api/latest-routes)**.

---

## Next Steps

1. Update the prompt and file to add more security vulnerability fields (eg: OWASP top 10, etc).
2. Allow users to sort by severity.
3. Expand analysis from just PHP files to any type of programming language.
4. Add security measures on this app. Certificate, login creds.
5. Update agent to use MCP.

---

## Running the Backend App Locally

1.  cd into **8BSleeplessCyberSec/app**
    Run:

   ```
   uvicorn app.main:app --reload
   ```
2. Open **[http://127.0.0.1:8000/api/purpose](http://127.0.0.1:8000/api/purpose)** to see purpose of this project.
3. Once the app is running locally, input a publically accessible github repo link you want to analyse:

   ```
   curl -X POST http://127.0.0.1:8000/api/run-graph \
     -H "Content-Type: application/json" \
     -d '{"repo_url": "<<\github repo link>>"}'
   ```
4. To see vulnerabilities idenified in JSON format, open:
   **[http://127.0.0.1:8000/api/latest-vulnerabilities](http://127.0.0.1:8000/api/latest-vulnerabilities)**

---

## Running the Frontend App Locally

### First Time Installation

1. `cd` into **8BSleeplessCyberSec/frontend**
2. Run
   
   ```
   npm install
   ```
   to install necessary packages

### Running the app
1. Run
   
   ```
   npm run dev
   ```
  to start the server ([http://localhost:5173](http://localhost:5173)).
  
2. Input the Github link of the repo that you want to analyze.
   
3. View results at **[http://localhost:5173/results](http://localhost:5173/results)**.

---

<img width="1440" height="900" alt="Screenshot 2025-11-18 at 20 25 29" src="https://github.com/user-attachments/assets/0a6b443a-edfb-42b3-9c1a-9e7fc1e4ffc5" />

---
