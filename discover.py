#!/usr/bin/env python3
import os
import subprocess
import json
from pathlib import Path

HOME = Path("/home/lala_02")

def run_cmd(cmd, cwd):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=15)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def inspect_git_repo(path):
    # Check remotes
    code, remotes, _ = run_cmd("git remote -v", path)
    remote_dict = {}
    for line in remotes.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            remote_dict[parts[0]] = parts[1]

    # Current branch
    code, branch, _ = run_cmd("git rev-parse --abbrev-ref HEAD", path)
    
    # Commit counts and authors
    code, authors_raw, _ = run_cmd("git log --format='%an <%ae>'", path)
    authors = {}
    total_commits = 0
    if code == 0 and authors_raw:
        for line in authors_raw.splitlines():
            line = line.strip()
            if line:
                total_commits += 1
                authors[line] = authors.get(line, 0) + 1

    # First and latest commit
    code, latest_commit, _ = run_cmd("git log -1 --format='%h|%an|%ae|%ad|%s' --date=iso", path)
    code, first_commit, _ = run_cmd("git log --reverse --format='%h|%an|%ae|%ad|%s' --date=iso | head -n 1", path)

    # Dirty status
    code, status, _ = run_cmd("git status --porcelain", path)
    is_dirty = bool(status)
    untracked_count = len([l for l in status.splitlines() if l.startswith("??")])
    modified_count = len([l for l in status.splitlines() if not l.startswith("??") and l.strip()])

    return {
        "is_git": True,
        "branch": branch,
        "remotes": remote_dict,
        "total_commits": total_commits,
        "authors": authors,
        "first_commit": first_commit,
        "latest_commit": latest_commit,
        "is_dirty": is_dirty,
        "modified_count": modified_count,
        "untracked_count": untracked_count,
    }

def detect_stack(path):
    files = set(os.listdir(path))
    stack = []
    if "Cargo.toml" in files:
        stack.append("Rust/Cargo")
    if "Anchor.toml" in files:
        stack.append("Solana/Anchor")
    if "foundry.toml" in files:
        stack.append("Solidity/Foundry")
    if "hardhat.config.js" in files or "hardhat.config.ts" in files:
        stack.append("Solidity/Hardhat")
    if "package.json" in files:
        stack.append("Node/JS/TS")
    if "requirements.txt" in files or "Pipfile" in files or "pyproject.toml" in files:
        stack.append("Python")
    if "go.mod" in files:
        stack.append("Go")
    if "Makefile" in files:
        stack.append("Makefile/C")
    if "docker-compose.yml" in files or "Dockerfile" in files:
        stack.append("Docker")
    if "supabase" in files and (path / "supabase").is_dir():
        stack.append("Supabase")

    # Check for subdirectories like backend, frontend, programs, contracts
    subdirs = [d for d in files if (path / d).is_dir()]
    return stack, subdirs

def main():
    results = {}
    entries = sorted(os.listdir(HOME))
    for entry in entries:
        full_path = HOME / entry
        if not full_path.is_dir():
            continue
        if entry.startswith(".") and entry not in [".agents"]:
            continue
        if entry in ["portfolio-research", "snap"]:
            continue

        git_dir = full_path / ".git"
        is_git = git_dir.is_dir()
        
        git_info = inspect_git_repo(full_path) if is_git else {"is_git": False}
        stack, subdirs = detect_stack(full_path)

        # Check for nested git repos
        nested_git = []
        for s in subdirs:
            if (full_path / s / ".git").is_dir():
                nested_git.append(s)

        results[entry] = {
            "path": str(full_path),
            "stack": stack,
            "subdirs": subdirs[:15],
            "nested_git": nested_git,
            "git": git_info
        }

    with open(HOME / "portfolio-research" / "inventory_raw.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Discovered {len(results)} directories. Written to inventory_raw.json")

if __name__ == "__main__":
    main()
