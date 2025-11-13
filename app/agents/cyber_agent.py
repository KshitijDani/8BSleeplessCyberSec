from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
You extract PHP application actions that behave like implicit API routes.
Many PHP projects do not use explicit URL routers; instead, actions are triggered
through `$_POST['action']` checks, switch statements, or conditional comparisons.

Your task:

1. Analyze the provided PHP file contents.
2. Identify every unique action name used inside:
   - $_POST['action']
   - switch ($action) { ... }
   - if ($action === '...') or similar
3. For each action, produce a synthetic route in the format:
   "<filename>: <action_name1>, <action_name2>,..."
4. Return ONLY a JSON array.
5. Do NOT include explanations, comments, or extra text.
6. If no actions exist, return [].

Example:

If the file is 'users.php' and contains actions 'add_user', 'edit_user', and 'delete_user', output:

[
  "users.php: add_user, edit_user, delete_user",
]
"""


class CyberAgent:
    def __init__(self):
        self.client = client

    def run(self, query: str) -> str:
        print("inside run of CyberAgent\n")
        print("Here is the query to call gpt", query)
        response = self.client.chat.completions.create(
            model="gpt-5",#"gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "You are a cybersecurity analysis agent. "
                    "You analyze code, detect vulnerabilities, and provide precise recommendations."
                    "Specifically for now you will be given the path of a code repo on my local system. Access the repo and find all the API routes and return them to me as a list"
                )},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    
    def extract_routes(self, file_name, file_content: str) -> str:
        print("Extracting routes for: ", file_name)
        response = self.client.chat.completions.create(
            model="gpt-5",#"gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": file_content}
            ]
        )
        
        #print(f"Extracted routes from file {file_name}: {response.choices[0].message.content}")
        return response.choices[0].message.content