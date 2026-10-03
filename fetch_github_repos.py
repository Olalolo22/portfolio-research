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
        print(f"Error fetching {endpoint}: {e}")
        return None

def fetch_all_repos():
    repos = []
    page = 1
    while True:
        data = gh_api(f"/user/repos?per_page=100&page={page}&affiliation=owner,collaborator,organization_member&sort=pushed")
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos

def main():
    repos = fetch_all_repos()
    print(f"Fetched {len(repos)} repositories from GitHub API.")

    simplified = []
    for r in repos:
        simplified.append({
            "name": r.get("name"),
            "full_name": r.get("full_name"),
            "owner": r.get("owner", {}).get("login"),
            "private": r.get("private"),
            "fork": r.get("fork"),
            "description": r.get("description"),
            "html_url": r.get("html_url"),
            "ssh_url": r.get("ssh_url"),
            "default_branch": r.get("default_branch"),
            "created_at": r.get("created_at"),
            "updated_at": r.get("updated_at"),
            "pushed_at": r.get("pushed_at"),
            "language": r.get("language"),
            "topics": r.get("topics", [])
        })

    out_file = Path("/home/lala_02/portfolio-research/github_repos.json")
    with open(out_file, "w") as f:
        json.dump(simplified, f, indent=2)

    print(f"Saved to {out_file}")

if __name__ == "__main__":
    main()
