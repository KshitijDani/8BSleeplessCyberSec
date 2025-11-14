# 8BSleeplessCyberSec Agent

Current State: The purpose of this code is to help me understand how to build an AI Agent. The agent uses LangGraph to create a graph of the different stages in the Analysis pipeline. Currently we have the following nodes:
[start]
   ↓
[fetch_repo]
   ↓
[extract_php_files]
   ↓
[analyze_files]
   ↓
[save_output]
   ↓
[cleanup]

in the [analyze_files] node we use OpenAI's Completions API to make calls to a gpt-4o-mini LLM model. In the app itself, we either pass the path of a local repo or the link to a publically accessible github repo. The app then parses all php files in the repo and fetches all endpoints. It the stores the endpoints in an output file. to view the latest run's endpoints goto **http://127.0.0.1:8000/api/latest-routes**.

Next State: 
Next, understand what exactly is required to call the endpoints we've extracted and call them while the targeted app is running. Then try to find and test any vulnerabilities in the app. Use CVSS scores to report to end users the scale of the vulnerability


*run uvicorn app.main:app --reload to start the app from the root directory.

*Open http://127.0.0.1:8000/purpose to see purpose of this project

once the app is running locally, pass the directory you want to analyse a repo run
**curl -X POST http://127.0.0.1:8000/api/run-graph \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "<<\github repo link>>"}'**

