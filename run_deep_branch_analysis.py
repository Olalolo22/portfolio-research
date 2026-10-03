#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path

HOME = Path("/home/lala_02")

MULTI_BRANCH_REPOS = [
    "routedock",
    "aegis-ledger",
    "harvest",
    "ProofPass",
    "Stellar-iPredict",
    "rescue2",
    "Sentinel",
    "Ragent",
    "MarketPadi",
    "Vicar",
    "program-Olalolo22",
    "program-Olalolo22-copy",
    "rugroll",
    "Mizan",
    "SJ_consulting",
    "Stellarlend-frontend",
    "alx-polly2"
]

def run_cmd(cmd, cwd):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=20)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def analyze_repo_deep(repo_name):
    p = HOME / repo_name
    print(f"Deep analyzing {repo_name}...")
    
    # Get default branch
    _, head_ref, _ = run_cmd("git symbolic-ref refs/remotes/origin/HEAD", p)
    default_branch = head_ref.replace("refs/remotes/origin/", "") if head_ref else ""
    if not default_branch:
        for candidate in ["main", "master", "feature/zero-trust-refactor", "implementation-drips"]:
            code, _, _ = run_cmd(f"git rev-parse --verify {candidate}", p)
            if code == 0:
                default_branch = candidate
                break
    if not default_branch:
        default_branch = "main"

    # Get all branches
    _, branches_out, _ = run_cmd("git branch -a --format='%(refname:short)'", p)
    branches = [b.strip() for b in branches_out.splitlines() if b.strip() and not b.endswith("/HEAD") and not b.startswith("upstream/")]

    # Deduplicate branches: prefer local over origin/ if same commit
    unique_branches = {}
    for b in branches:
        code, sha, _ = run_cmd(f"git rev-parse {b}", p)
        if code == 0:
            clean_name = b.replace("origin/", "")
            if clean_name not in unique_branches:
                unique_branches[clean_name] = {"ref": b, "sha": sha}
            else:
                # prefer local
                if not b.startswith("origin/"):
                    unique_branches[clean_name] = {"ref": b, "sha": sha}

    repo_data = {
        "repo": repo_name,
        "default_branch": default_branch,
        "branches": {}
    }

    for bname, binfo in unique_branches.items():
        ref = binfo["ref"]
        sha = binfo["sha"]
        code, commit_info, _ = run_cmd(f"git log -1 --format='%h|%ad|%an <%ae>|%s' --date=short {ref}", p)
        
        # Check divergence from default_branch
        ahead_list = []
        behind_list = []
        diff_stat = ""
        diff_files = []
        
        if bname != default_branch:
            code, ahead_out, _ = run_cmd(f"git log {default_branch}..{ref} --oneline", p)
            code, behind_out, _ = run_cmd(f"git log {ref}..{default_branch} --oneline", p)
            code, stat_out, _ = run_cmd(f"git diff --stat {default_branch}...{ref}", p)
            code, files_out, _ = run_cmd(f"git diff --name-only {default_branch}...{ref}", p)
            
            ahead_list = ahead_out.splitlines() if ahead_out else []
            behind_list = behind_out.splitlines() if behind_out else []
            diff_stat = stat_out.splitlines()[-1] if stat_out else "No diff"
            diff_files = files_out.splitlines() if files_out else []

        repo_data["branches"][bname] = {
            "ref": ref,
            "sha": sha[:8],
            "commit_summary": commit_info,
            "is_default": (bname == default_branch),
            "ahead_count": len(ahead_list),
            "behind_count": len(behind_list),
            "ahead_commits": ahead_list[:10],
            "behind_commits": behind_list[:5],
            "diff_stat": diff_stat,
            "files_changed_count": len(diff_files),
            "sample_files_changed": diff_files[:8]
        }

    return repo_data

def main():
    all_data = {}
    for r in MULTI_BRANCH_REPOS:
        all_data[r] = analyze_repo_deep(r)

    out_file = HOME / "portfolio-research" / "deep_branch_analysis.json"
    with open(out_file, "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"Deep branch analysis completed for {len(all_data)} repos. Saved to {out_file}")

if __name__ == "__main__":
    main()
