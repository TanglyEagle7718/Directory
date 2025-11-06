import requests
import datetime
from collections import OrderedDict

USERNAME = "tanglyeagle7718"
OUTPUT_FILE = "index.html"


# Add your custom static links here
CUSTOM_LINKS = [
    ("Text Comparing Tool", "https://tanglyeagle7718.github.io/TextCompTool/"),
    ("Image to Text Tool", "https://tanglyeagle7718.github.io/TextCompTool/"),
]

def fetch_repos(username):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"sort": "pushed", "direction": "desc", "per_page": 100, "page": page}
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise RuntimeError(f"GitHub API error: {r.status_code} {r.text}")
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def generate_html(custom_links, repos, username):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    static_html = "\n".join(
        f'<li><a href="{url}" target="_blank">{name}</a></li>' for name, url in custom_links
    )
    repo_html = "\n".join(
        f'<li><a href="https://github.com/{username}/{repo["name"]}" target="_blank">{repo["name"]}</a></li>'
        for repo in repos
    )
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Directory</title>
<style>
  body {{ font-family: sans-serif; background: #f9fafb; margin: 0; padding: 40px; }}
  h1 {{ text-align: center; margin-bottom: 20px; font-size: 2rem; }}
  h2 {{ margin-top: 40px; text-align: center; color: #374151; }}
  p {{ text-align: center; color: #6b7280; }}
  ul {{ list-style: none; padding: 0; max-width: 600px; margin: 20px auto; }}
  li {{ margin: 10px 0; }}
  a {{ display: block; text-decoration: none; background: #2563eb; color: white;
      padding: 12px 16px; border-radius: 6px; transition: background 0.2s; }}
  a:hover {{ background: #1e40af; }}
</style>
</head>
<body>
  <h1>Directory</h1>
  <p>Last updated: {now}</p>

  <h2>Featured Projects</h2>
  <ul>{static_html}</ul>

  <h2>All GitHub Repositories</h2>
  <ul>{repo_html}</ul>
</body>
</html>"""

def main():
    repos = fetch_repos(USERNAME)
    html = generate_html(CUSTOM_LINKS, repos, USERNAME)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated {OUTPUT_FILE} with {len(repos)} repositories and {len(CUSTOM_LINKS)} featured links.")

if __name__ == "__main__":
    main()
