import json

with open("/home/lala_02/portfolio-research/inventory_raw.json") as f:
    data = json.load(f)

print(f"{'Project':<25} | {'Branch':<22} | {'Total':<6} | {'User':<6} | {'Other':<6} | {'Top Authors / Notes'}")
print("-" * 105)

user_keywords = ["olumide", "olalolo", "lala_02", "muhammed", "suleiman"]

for name, info in sorted(data.items()):
    if not info["git"].get("is_git"):
        continue
    g = info["git"]
    commits = g.get("total_commits", 0)
    authors = g.get("authors", {})
    user_commits = 0
    other_authors = {}
    for author, count in authors.items():
        if any(alias in author.lower() for alias in user_keywords):
            user_commits += count
        else:
            other_authors[author] = count
    
    branch = str(g.get("branch", ""))[:21]
    top_other_str = ""
    if other_authors:
        top = sorted(other_authors.items(), key=lambda x: x[1], reverse=True)[:2]
        top_other_str = ", ".join([f"{k.split('<')[0].strip()} ({v})" for k, v in top])
    elif user_commits > 0:
        top_other_str = "100% User"
    else:
        top_other_str = "No commits / Empty"

    print(f"{name:<25} | {branch:<22} | {commits:<6} | {user_commits:<6} | {commits - user_commits:<6} | {top_other_str}")
