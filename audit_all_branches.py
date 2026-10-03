#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path

HOME = Path("/home/lala_02")

USER_IDENTIFIERS = [
    "olumide2956@gmail.com",
    "olumide2925@cloudshell",
    "116976810+olalolo22@users.noreply.github.com",
    "olalolo22@github.com",
    "lala@webdevconstruct.com",
    "harvest@stocklana.fi",
    "ubuntu@ip-172-31-14-153",
    "olumidelala",
    "olalolo22",
    "lala (wdc)"
]

def is_user(author_str):
    low = author_str.lower()
    return any(u in low for u in USER_IDENTIFIERS)

def run_cmd(cmd, cwd):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=20)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def audit_repo_branches(repo_dir):
    # Get remotes
    _, remotes_out, _ = run_cmd("git remote -v", repo_dir)
    remotes = {}
    for line in remotes_out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            remotes[parts[0]] = parts[1]

    # Find main / master / default branch
    _, head_ref, _ = run_cmd("git symbolic-ref refs/remotes/origin/HEAD", repo_dir)
    default_branch = head_ref.replace("refs/remotes/origin/", "") if head_ref else ""
    if not default_branch:
        for candidate in ["main", "master", "origin/main", "origin/master"]:
            code, _, _ = run_cmd(f"git rev-parse --verify {candidate}", repo_dir)
            if code == 0:
                default_branch = candidate.replace("origin/", "")
                break
    if not default_branch:
        default_branch = "main"

    # Get all branches
    _, branches_out, _ = run_cmd("git branch -a --format='%(refname:short)'", repo_dir)
    all_refs = [b.strip() for b in branches_out.splitlines() if b.strip() and not b.endswith("/HEAD")]

    branch_results = {}

    for ref in all_refs:
        # Check if ref is from an upstream remote that is NOT origin or local
        # E.g. skip remotes/upstream/* if it's someone else's branch
        if ref.startswith("upstream/"):
            continue

        # Check user commits on this ref
        cmd = f"git log {ref} --format='%h|%an <%ae>|%ad|%s' --date=short"
        code, log_out, _ = run_cmd(cmd, repo_dir)
        if code != 0 or not log_out:
            continue

        user_commits = []
        for line in log_out.splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                sha, author, date, msg = parts
                if is_user(author):
                    user_commits.append({
                        "sha": sha,
                        "author": author,
                        "date": date,
                        "message": msg
                    })

        if not user_commits:
            continue

        # If user has commits on this branch, calculate divergence from default_branch
        divergence = {}
        base_ref = default_branch
        # If ref is default_branch itself, comparison to base is not meaningful
        clean_ref_name = ref.replace("origin/", "")
        if clean_ref_name != default_branch:
            # Commits on ref not on default_branch
            code, ahead_log, _ = run_cmd(f"git log {default_branch}..{ref} --oneline", repo_dir)
            # Commits on default_branch not on ref
            code, behind_log, _ = run_cmd(f"git log {ref}..{default_branch} --oneline", repo_dir)
            # Diff stat
            code, diff_stat, _ = run_cmd(f"git diff --stat {default_branch}...{ref}", repo_dir)
            
            ahead_list = ahead_log.splitlines() if ahead_log else []
            behind_list = behind_log.splitlines() if behind_log else []
            
            # Check how many of the ahead commits are by user
            user_ahead = [c for c in user_commits if any(c["sha"] in a for a in ahead_list)]

            divergence = {
                "base_branch": default_branch,
                "ahead_count": len(ahead_list),
                "behind_count": len(behind_list),
                "user_ahead_commits": user_ahead,
                "diff_summary": diff_stat.splitlines()[-1] if diff_stat else "No diff"
            }

        # Deduplicate branch names (e.g. origin/foo vs foo)
        branch_key = ref
        branch_results[branch_key] = {
            "total_user_commits_in_history": len(user_commits),
            "latest_user_commit": user_commits[0] if user_commits else None,
            "divergence": divergence
        }

    return {
        "remotes": remotes,
        "default_branch": default_branch,
        "branches_with_user_work": branch_results
    }

def main():
    results = {}
    entries = sorted(os.listdir(HOME))
    for e in entries:
        p = HOME / e
        if not p.is_dir() or not (p / ".git").is_dir():
            continue
        if e in ["Betty", "wetty", "rust-crash-course", "welcome-to-docker", "example-zkloan"]:
            continue
        
        info = audit_repo_branches(p)
        if info["branches_with_user_work"]:
            results[e] = info

    out_json = HOME / "portfolio-research" / "branch_divergence.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Audited branches for {len(results)} repositories with user commits. Saved to {out_json}")

if __name__ == "__main__":
    main()
