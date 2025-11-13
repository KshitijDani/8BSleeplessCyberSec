# 8BSleeplessCyberSec Agent

Current State: The purpose of this code is to help me understand how to build an AI Agent. The agent uses OpenAI's Completions API to make calls to a gpt-4o-mini LLM model. In the app itself, we either pass the path of a local repo or the link to a publically accessible github repo. The app then parses all php files in the repo and fetches all endpoints. It the stores the endpoints in an output file. to view the latest run's endpoints goto http://127.0.0.1:8000/api/latest-routes.

Next State: understand what exactly is required to call the endpoints we've extracted and call them while the targeted app is running. Then try to find and test any vulnerabilities in the app.


*run uvicorn app.main:app --reload to start the app from the root directory.

*Open http://127.0.0.1:8000/purpose to see purpose of this project

v0.0.1: the app currently opens a path you pass from your local machine. it then opens and recursively finds all php files. it then composes a lists of "Actions" which are the url routes possible for the scanned app to load.

once the app is running locally, pass the directory you want to analyse as a query. here is an example:
curl -X POST "http://127.0.0.1:8000/api/scan-repo" \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "<<file_path>>"}'

