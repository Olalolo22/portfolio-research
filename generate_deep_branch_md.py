#!/usr/bin/env python3
import json
from pathlib import Path

HOME = Path("/home/lala_02")

with open(HOME / "portfolio-research" / "deep_branch_analysis.json") as f:
    deep_data = json.load(f)

with open(HOME / "portfolio-research" / "branch_divergence.json") as f:
    div_data = json.load(f)

# Repositories
multi_branch = [r for r, d in deep_data.items() if len(d["branches"]) > 1]
single_branch = [r for r, d in div_data.items() if r not in multi_branch]

md_lines = []
md_lines.append("# Master Portfolio Branch Audit & Cross-Branch Divergence Register")
md_lines.append("**Dossier Date:** October 3, 2026  ")
md_lines.append("**Investigator:** Antigravity Engineering Portfolio Intelligence Analyst  ")
md_lines.append(f"**Total Repositories Audited:** 36 Repositories with Verified User Work  ")
md_lines.append(f"- **Multi-Branch Repositories:** {len(multi_branch)} Repositories (with unmerged feature branches, fork PRs, or divergent architectures)  ")
md_lines.append(f"- **Single-Branch Repositories:** {len(single_branch)} Repositories (all work consolidated on default or active issue branch)  ")
md_lines.append("\n---\n")

md_lines.append("## 1. Multi-Branch Repositories: Full Audit Matrix\n")

for repo in sorted(multi_branch):
    rdata = deep_data[repo]
    def_b = rdata["default_branch"]
    branches = rdata["branches"]
    
    md_lines.append(f"### `{repo}`")
    md_lines.append(f"- **Default Trunk:** `{def_b}`")
    md_lines.append(f"- **Total Distinct Branches Audited:** {len(branches)}")
    md_lines.append("")
    md_lines.append("| Branch Name | Commit SHA | Date | Divergence vs Default | Files Changed | Ahead Commits / Key Engineering Scope |")
    md_lines.append("| :--- | :---: | :---: | :---: | :---: | :--- |")

    for bname, binfo in sorted(branches.items()):
        sha = binfo["sha"]
        summary = binfo.get("commit_summary", "").split("|")
        date = summary[1] if len(summary) > 1 else "N/A"
        msg = summary[3] if len(summary) > 3 else "N/A"
        ahead = binfo["ahead_count"]
        behind = binfo["behind_count"]
        files_cnt = binfo["files_changed_count"]
        div_str = f"+{ahead} / -{behind}" if not binfo["is_default"] else "**Default Base**"
        
        ahead_commits_text = ""
        if binfo.get("ahead_commits"):
            ahead_commits_text = "<br>".join([f"• `{c[:8]}` {c[9:60]}" for c in binfo["ahead_commits"][:3]])
        else:
            ahead_commits_text = f"`{msg[:55]}`"

        md_lines.append(f"| `{bname}` | `{sha}` | {date} | {div_str} | {files_cnt} files | {ahead_commits_text} |")

    md_lines.append("\n---\n")

md_lines.append("## 2. Single-Branch Repositories (Consolidated Work)\n")
md_lines.append("| Repository | Active Branch | Latest Verified Commit | Date | Verified Scope of Work |")
md_lines.append("| :--- | :---: | :---: | :---: | :--- |")

for repo in sorted(single_branch):
    info = div_data[repo]
    def_b = info.get("default_branch", "main")
    branches = info.get("branches_with_user_work", {})
    latest_c = list(branches.values())[0].get("latest_user_commit", {}) if branches else {}
    sha = latest_c.get("sha", "N/A")[:8]
    date = latest_c.get("date", "N/A")
    msg = latest_c.get("message", "N/A")[:70]
    md_lines.append(f"| **`{repo}`** | `{def_b}` | `{sha}` | {date} | {msg} |")

out_file = HOME / "portfolio-research" / "DEEP_BRANCH_ANALYSIS.md"
with open(out_file, "w") as f:
    f.write("\n".join(md_lines))

print(f"Generated {out_file} ({len(md_lines)} lines)")
