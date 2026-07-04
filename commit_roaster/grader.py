"""Roasting Grader Agent: Scores commits on 5 hilarious dimensions."""

ROASTING_RUBRIC = {
    "entropy": {
        "name": "Chaos Energy",
        "description": "How vague/chaotic is this message?",
        "low": "Crystal clear what was changed",
        "high": "Future you will be very confused"
    },
    "professionalism": {
        "name": "Professional Decorum",
        "description": "Does this belong in a resume?",
        "low": "Shakespearean precision",
        "high": "Your team lead just sighed"
    },
    "helpfulness": {
        "name": "Future Self Approval",
        "description": "Will 6-month-ago you thank current you?",
        "low": "Extremely thoughtful documentation",
        "high": "You forgot why you did this"
    },
    "creativity": {
        "name": "Artistic License",
        "description": "Is there personality in this message?",
        "low": "Bland corporate speak",
        "high": "Shakespeare meets Stack Overflow"
    },
    "honesty": {
        "name": "Truth Factor",
        "description": "Does this message reflect reality?",
        "low": "Diplomatically accurate",
        "high": "Brutally truthful (we respect it)"
    }
}


def score_commit(analysis: dict, message: str) -> dict:
    """
    Score a commit on the 5 roasting dimensions.
    
    Args:
        analysis: Output from analyzer.analyze_commit_message()
        message: The actual commit message
    
    Returns:
        Scores for each dimension (1-10)
    """
    scores = {}
    
    # Entropy: vague words → high score (chaotic)
    vague_words = ["fix", "update", "change", "lol", "oops", "bug", "stuff"]
    entropy = 1 + (sum(1 for word in vague_words if word in message.lower())) * 2
    entropy = min(entropy, 10)
    scores["entropy"] = entropy
    
    # Professionalism: all caps, emoji, "lol" → low score
    prof_penalty = 0
    if analysis.get("is_all_caps", False):
        prof_penalty += 3
    if analysis.get("has_emoji", False):
        prof_penalty += 2
    if "lol" in message.lower() or "haha" in message.lower():
        prof_penalty += 4
    prof_score = 10 - prof_penalty
    scores["professionalism"] = max(prof_score, 1)
    
    # Helpfulness: length + structure → higher score if well-formed
    helpful = 5
    if analysis.get("first_line_length", 0) > 50:
        helpful += 1
    if analysis.get("has_body", False):
        helpful += 2
    if analysis.get("has_subject_body_separation", False):
        helpful += 1
    if analysis.get("is_vague", False):
        helpful -= 2
    scores["helpfulness"] = max(helpful, 1)
    
    # Creativity: emoji, personality, unusual word choice → higher
    creativity = 4
    if analysis.get("has_emoji", False):
        creativity += 2
    if analysis.get("word_count", 0) > 10:
        creativity += 1
    if any(word in message for word in ["refactor", "optimize", "enhance"]):
        creativity -= 1  # Too corporate
    if any(word in message.lower() for word in ["fix", "update"]):
        creativity -= 1  # Too generic
    scores["creativity"] = max(creativity, 1)
    
    # Honesty: "fix lol" is honest; "refactor" when you just added "print" is not
    honesty = 5
    if message.lower().count("lol") > 0 or "oops" in message.lower():
        honesty += 2  # Admits chaos
    if analysis.get("is_vague", False):
        honesty += 1  # Actually honest about vagueness
    if "refactor" in message and analysis.get("word_count", 0) < 3:
        honesty -= 2  # Suspicious
    scores["honesty"] = max(honesty, 1)
    
    return scores
