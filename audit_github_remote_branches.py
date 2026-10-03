#!/usr/bin/env python3
import urllib.request
import json
from pathlib import Path

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

with open("/home/lala_02/portfolio-research/github_repos.json") as f:
    repos = json.load(f)

# Focus on repos owned by Olalolo22 + relevant partner orgs
relevant_repos = [r for r in repos if r["owner"] in ["Olalolo22", "School-of-Solana", "WebDevConstruct", "MarketPadi-Org", "FINSA-TECH-ORG"]]

print(f"Checking remote branches for {len(relevant_repos)} relevant repos...")

remote_branch_results = {}

for r in relevant_repos:
    full_name = r["full_name"]
    branches = gh_api(f"/repos/{full_name}/branches?per_page=100")
    if isinstance(branches, list):
        branch_list = []
        for b in branches:
            bname = b.get("name")
            sha = b.get("commit", {}).get("sha", "")[:8]
            branch_list.append({"name": bname, "sha": sha})
        remote_branch_results[full_name] = {
            "default_branch": r.get("default_branch"),
            "private": r.get("private"),
            "fork": r.get("fork"),
            "branch_count": len(branch_list),
            "branches": branch_list
        }
    else:
        remote_branch_results[full_name] = {"error": str(branches)}

out_file = Path("/home/lala_02/portfolio-research/github_remote_branches.json")
with open(out_file, "w") as f:
    json.dump(remote_branch_results, f, indent=2)

print(f"Audited branches for {len(remote_branch_results)} repos. Saved to {out_file}")
