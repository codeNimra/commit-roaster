"""Commit Analyzer Agent: Fetches and parses GitHub commits."""

import os
import requests


def fetch_commits(repo_url: str, max_commits: int = 10) -> list[dict]:
    """
    Fetch recent commits from a GitHub repository.
    
    Args:
        repo_url: e.g., "https://github.com/torvalds/linux"
        max_commits: How many recent commits to analyze
    
    Returns:
        List of commit objects with message, author, date, stats
    """
    # Parse repo from URL
    if "github.com/" not in repo_url:
        return {"error": "Invalid GitHub URL"}
    
    parts = repo_url.replace("https://github.com/", "").rstrip("/").split("/")
    if len(parts) < 2:
        return {"error": "Invalid GitHub URL structure"}
    owner, repo = parts[0], parts[1]
    
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    
    # Fetch commits
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={max_commits}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    
    if response.status_code != 200:
        return {"error": f"GitHub API error: {response.status_code}"}
    
    commits = response.json()
    if not isinstance(commits, list):
        return {"error": "Unexpected GitHub API response structure"}
    
    # Extract relevant data
    parsed_commits = []
    for commit in commits:
        parsed_commits.append({
            "sha": commit.get("sha", "")[:8],
            "message": commit.get("commit", {}).get("message", ""),
            "author": commit.get("commit", {}).get("author", {}).get("name", "Unknown"),
            "date": commit.get("commit", {}).get("author", {}).get("date", ""),
            "url": commit.get("html_url", ""),
            "stats": {
                "additions": commit.get("stats", {}).get("additions", 0),
                "deletions": commit.get("stats", {}).get("deletions", 0),
            }
        })
    
    return parsed_commits


def analyze_commit_message(message: str) -> dict:
    """
    Analyze a commit message for structure and clarity.
    
    Returns metrics for the Grader agent.
    """
    lines = message.strip().split("\n")
    first_line = lines[0] if lines else ""
    
    analysis = {
        "first_line_length": len(first_line),
        "has_subject_body_separation": len(lines) > 1 and lines[1] == "",
        "has_body": len(lines) > 2,
        "is_all_caps": first_line.isupper(),
        "is_all_lowercase": first_line.islower(),
        "has_emoji": any(ord(c) > 127 for c in first_line),
        "is_vague": any(vague in first_line.lower() for vague in ["fix", "update", "change", "lol", "oops"]),
        "word_count": len(first_line.split()),
    }
    
    return analysis
