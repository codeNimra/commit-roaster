"""Feedback Generator: Crafts funny, kind roasting commentary."""

ROAST_TEMPLATES = {
    "high_entropy": [
        "A commit message that embodies the spirit of 'it compiled, so ship it.'",
        "Your commit message is giving 'works on my machine' energy.",
        "Future debugging sessions have entered the chat... and they're confused.",
        "This is less a commit message and more a cryptic haiku.",
    ],
    "low_professionalism": [
        "Your team lead just developed a twitch at the sight of this.",
        "This commit message is somehow both honest and unprofessional.",
        "The corporate world isn't ready for this kind of authenticity.",
        "Your resume won't thank you, but your sense of humor will.",
    ],
    "high_creativity": [
        "We didn't know commit messages could be poetry.",
        "This is either a commit message or a PhD thesis abstract.",
        "If job interviews judged creativity this way, you'd be golden.",
        "Shakespeare writes commit messages now, apparently.",
    ],
    "low_helpfulness": [
        "Your future self will have many questions.",
        "In 6 months, you'll wish you'd been more specific.",
        "This is technically a commit message, legally speaking.",
        "Context is overrated anyway, right?",
    ],
    "high_honesty": [
        "At least you're honest about it.",
        "We appreciate the transparency.",
        "Brutal honesty > diplomatic vagueness.",
        "You get points for not pretending to know what you're doing.",
    ],
}


def generate_feedback(scores: dict, message: str) -> str:
    """
    Generate funny, constructive feedback based on scores.
    
    Args:
        scores: Output from grader.score_commit()
        message: The commit message
    
    Returns:
        Formatted feedback string
    """
    # Determine overall rating
    avg_score = sum(scores.values()) / len(scores)
    
    if avg_score >= 8:
        rating = "✨ Pristine (How?)"
    elif avg_score >= 6:
        rating = "👍 Respectable"
    elif avg_score >= 4:
        rating = "🔥 Spicy (But honest)"
    else:
        rating = "💀 Legendary (in a funny way)"
    
    # Pick commentary based on highest/lowest scores
    commentary = ""
    
    if scores.get("entropy", 0) >= 8:
        commentary += ROAST_TEMPLATES["high_entropy"][0] + "\n"
    
    if scores.get("professionalism", 10) <= 3:
        commentary += ROAST_TEMPLATES["low_professionalism"][0] + "\n"
    
    if scores.get("creativity", 0) >= 7:
        commentary += ROAST_TEMPLATES["high_creativity"][0] + "\n"
    
    if scores.get("helpfulness", 10) <= 3:
        commentary += ROAST_TEMPLATES["low_helpfulness"][0] + "\n"
    
    if scores.get("honesty", 0) >= 8:
        commentary += ROAST_TEMPLATES["high_honesty"][0] + "\n"
    
    # If no criteria matches, add a generic friendly roast
    if not commentary.strip():
        commentary = "A very standard, unremarkable commit. Neither a masterpiece nor a trainwreck. Keep on keeping on!"
    
    # Format output
    feedback = f"""
╔════════════════════════════════════════════════════════════════╗
║  COMMIT MESSAGE ROAST REPORT                                   ║
╠════════════════════════════════════════════════════════════════╣
║  Message: "{message[:60]}"
║
║  Scores:
║  ├─ Chaos Energy (Entropy):     {scores.get('entropy', 0)}/10
║  ├─ Professional Decorum:       {scores.get('professionalism', 0)}/10
║  ├─ Future Self Approval:       {scores.get('helpfulness', 0)}/10
║  ├─ Artistic License:           {scores.get('creativity', 0)}/10
║  └─ Truth Factor (Honesty):     {scores.get('honesty', 0)}/10
║
║  Overall Rating: {rating}
║
║  Feedback:
║  {commentary.strip()}
╚════════════════════════════════════════════════════════════════╝
"""
    
    return feedback
