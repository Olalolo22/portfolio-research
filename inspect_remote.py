#!/usr/bin/env python3
import urllib.request
import json
import base64

TOKEN = "REDACTED_GITHUB_TOKEN"
BASE_URL = "https://api.github.com"

def gh_api(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("User-Agent", "Portfolio-Audit")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

repos_to_check = [
    "Olalolo22/Persist",
    "Olalolo22/Shadowbox",
    "Olalolo22/hackathon-scanner",
    "Olalolo22/TG-ct-auto-checker",
    "Olalolo22/Nosana",
    "Olalolo22/SaroScope_dlmm",
    "Olalolo22/my-agent",
    "Olalolo22/AI_Grad",
    "School-of-Solana/task1-Olalolo22",
    "School-of-Solana/task2-Olalolo22",
    "Olalolo22/alx-system_engineering-devops"
]

results = {}

for repo in repos_to_check:
    print(f"Inspecting {repo}...")
    # Get commits count and latest commit
    commits = gh_api(f"/repos/{repo}/commits?per_page=5")
    # Get README
    readme_data = gh_api(f"/repos/{repo}/readme")
    readme_text = ""
    if "content" in readme_data:
        try:
            readme_text = base64.b64decode(readme_data["content"]).decode(errors="ignore")
        except:
            pass
    # Get repo root contents
    contents = gh_api(f"/repos/{repo}/contents")
    file_list = []
    if isinstance(contents, list):
        file_list = [c["name"] for c in contents]

    results[repo] = {
        "files": file_list,
        "readme_snippet": readme_text[:400] if readme_text else "No README",
        "recent_commits": [
            {
                "sha": c.get("sha", "")[:8],
                "date": c.get("commit", {}).get("author", {}).get("date"),
                "message": c.get("commit", {}).get("message", "").splitlines()[0] if c.get("commit") else ""
            }
            for c in (commits if isinstance(commits, list) else [])[:3]
        ]
    }

with open("/home/lala_02/portfolio-research/remote_repos_audit.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved to /home/lala_02/portfolio-research/remote_repos_audit.json")
