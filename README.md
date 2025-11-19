# 8BSleeplessCyberSec Agent

**Current State:** The purpose of this code is to help us understand how to build an AI Agent. The agent uses LangGraph to create a graph of the different stages in the Analysis pipeline. Currently we have the following nodes:
[start] -> [fetch_repo] -> [extract_php_files] -> [analyze_files] -> [save_output] -> [cleanup]

in the [analyze_files] node we use OpenAI's Completions API to make calls to a gpt-4o-mini LLM model. In the app itself, we pass the link to a publically accessible **github repo**. The app then parses all **php** files in the repo and fetches all possible security vulnerabilities associated with the endpoints or actions in th file. It the stores the vulnerabilities in an output file in app/output_action. to view the latest run's endpoints goto **http://127.0.0.1:8000/api/latest-routes**.

**Next State:**
1. Update the prompt and file to add more security vulnerability field (eg: OWASP top 10, etc).
2. Expand analysis to beyonf PHP files.
3. Add security measures on this app. Certificate, login creds.
4. Update agent to use MCP.

**Running the backend app locally:**
1. *run uvicorn app.main:app --reload to start the app from the root directory.
2. *Open http://127.0.0.1:8000/api/purpose to see purpose of this project
3. once the app is running locally, pass the repo link you want to analyse
**curl -X POST http://127.0.0.1:8000/api/run-graph \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "<<\github repo link>>"}'**
4. To see vulnerabilities idenified in JSON format, open **http://127.0.0.1:8000/api/latest-vulnerabilities**


**Running the frontend app locally:**
First time run:
1. cd into 8BSleeplessCyberSec/frontend
2. **run npm install** to install necessary packages
3. run npm run dev to start the server. It will run at http://localhost:5173
4. Input the Github link of the repo that you want to analyze
5. view results at http://localhost:5173/results
