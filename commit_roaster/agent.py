"""
Commit Roaster: Main Workflow Agent
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from .analyzer import fetch_commits, analyze_commit_message
from .grader import score_commit
from .feedback_generator import generate_feedback


def create_roast_report(repo_url: str, max_commits: int = 10) -> str:
    """Main workflow: fetch commits -> analyze -> grade -> generate feedback."""
    
    print(f"[*] Fetching commits from {repo_url}...")
    commits = fetch_commits(repo_url, max_commits)
    
    if isinstance(commits, dict) and "error" in commits:
        return f"Error: {commits['error']}"
    
    if not commits:
        return "No commits found. Make sure the repo is public or your token is valid."
    
    report_lines = [
        "=" * 70,
        "COMMIT ROASTER REPORT",
        "=" * 70,
        "",
    ]
    
    for idx, commit in enumerate(commits, 1):
        message = commit["message"]
        analysis = analyze_commit_message(message)
        scores = score_commit(analysis, message)
        feedback = generate_feedback(scores, message)
        
        report_lines.append(f"[Commit {idx}/{len(commits)}]")
        report_lines.append(feedback)
        report_lines.append("")
    
    summary = f"""
{"=" * 70}
SUMMARY
{"=" * 70}
Commits roasted: {len(commits)}
Overall vibes: Your code is interesting.
Recommendation: Keep shipping.
"""
    report_lines.append(summary)
    
    report = "\n".join(report_lines)
    safe_report = report.encode('ascii', errors='ignore').decode('ascii')
    return safe_report


if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo = sys.argv[1]
        max_c = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        result = create_roast_report(repo, max_c)
        print(result)
    else:
        print("Usage: python agent.py <repo_url> [max_commits]")
