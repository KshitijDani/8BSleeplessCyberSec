# 8BSleeplessCyberSec

*run uvicorn app.main:app --reload to start the app from the root directory.

*Open http://127.0.0.1:8000/purpose to see purpose of this project

v0.0.1: the app currently opens a path you pass from your local machine. it then opens and recursively finds all php files. it then composes a lists of "Actions" which are the url routes possible for the scanned app to load.

once the app is running locally, pass the directory you want to analyse as a query. here is an example:
curl -X POST "http://127.0.0.1:8000/api/scan-repo" \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "<<file_path>>"}'

