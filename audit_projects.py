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
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=10)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def get_readme_summary(path):
    for fname in ["README.md", "readme.md", "README", "readme"]:
        p = path / fname
        if p.is_file():
            try:
                with open(p, "r", errors="ignore") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    title = lines[0] if lines else "Empty README"
                    desc = lines[1] if len(lines) > 1 else ""
                    return title[:120], desc[:200]
            except:
                pass
    return "No README", ""

def inspect_project(entry):
    path = HOME / entry
    if not path.is_dir() or entry in [".cache", ".cargo", ".codex", ".config", ".copilot", ".docker", ".dotnet", ".foundry", ".gemini", ".grok", ".landscape", ".local", ".npm", ".nvm", ".okx-agent-task", ".ollama", ".onchainos", ".railway", ".rustup", ".sp1", ".ssh", ".storybook", ".supabase", ".venv", ".vim", ".vscode-remote-containers", ".wakatime", ".yarn", ".bun", ".avm", ".antigravity-ide-server", "portfolio-research", "snap"]:
        return None

    is_git = (path / ".git").is_dir()
    title, desc = get_readme_summary(path)

    # Detect stack
    files = set(os.listdir(path))
    stack = []
    if "Cargo.toml" in files: stack.append("Rust/Cargo")
    if "Anchor.toml" in files: stack.append("Solana/Anchor")
    if "foundry.toml" in files: stack.append("Solidity/Foundry")
    if "package.json" in files: stack.append("Node/TS")
    if any(x in files for x in ["requirements.txt", "Pipfile", "pyproject.toml", "manage.py"]): stack.append("Python")
    if "go.mod" in files: stack.append("Go")
    if "Makefile" in files: stack.append("Makefile/C")
    if any(x.endswith(".c") or x.endswith(".h") for x in files): stack.append("C")
    if "supabase" in files and (path / "supabase").is_dir(): stack.append("Supabase")

    res = {
        "name": entry,
        "path": str(path),
        "is_git": is_git,
        "title": title,
        "description_snippet": desc,
        "stack": stack,
    }

    if is_git:
        _, remotes, _ = run_cmd("git remote -v", path)
        remote_url = remotes.split()[1] if remotes else "No remote"
        _, branch, _ = run_cmd("git rev-parse --abbrev-ref HEAD", path)
        _, authors_raw, _ = run_cmd("git log --format='%an <%ae>'", path)
        
        user_commits = 0
        total_commits = 0
        collaborators = set()
        if authors_raw:
            for a in authors_raw.splitlines():
                a = a.strip()
                if a:
                    total_commits += 1
                    if is_user(a):
                        user_commits += 1
                    else:
                        collaborators.add(a.split("<")[0].strip())

        _, first_commit, _ = run_cmd("git log --reverse --format='%h|%ad|%s' --date=short | head -n 1", path)
        _, latest_commit, _ = run_cmd("git log -1 --format='%h|%ad|%s' --date=short", path)
        _, status, _ = run_cmd("git status --porcelain", path)

        # check user branches
        _, user_branches, _ = run_cmd("git branch --list", path)

        res.update({
            "remote": remote_url,
            "branch": branch,
            "total_commits": total_commits,
            "user_commits": user_commits,
            "other_commits": total_commits - user_commits,
            "first_commit": first_commit,
            "latest_commit": latest_commit,
            "is_dirty": bool(status),
            "collaborators": sorted(list(collaborators))[:5],
            "branches": [b.strip().replace("* ", "") for b in user_branches.splitlines() if b.strip()]
        })
    else:
        # Non-git files count
        non_git_files = [f for f in path.rglob("*") if not any(x in str(f) for x in ["venv", "target", "node_modules", ".pytest_cache", ".git"])]
        res.update({
            "file_count": len(non_git_files),
            "sample_files": [str(f.relative_to(path)) for f in non_git_files[:8]]
        })

    return res

def main():
    entries = sorted(os.listdir(HOME))
    projects = []
    for e in entries:
        info = inspect_project(e)
        if info:
            projects.append(info)

    out_file = HOME / "portfolio-research" / "discovered_projects.json"
    with open(out_file, "w") as f:
        json.dump(projects, f, indent=2)

    print(f"Audited {len(projects)} projects. Saved to {out_file}")

if __name__ == "__main__":
    main()
