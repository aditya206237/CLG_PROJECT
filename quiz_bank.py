"""
Oppenheimer Skill Portal (Team Oppenheimer)
Quiz Bank Management & Question Rotation Engine
-----------------------------------------------
Loads micro-quiz questions from data/quiz_bank.json and manages persistent question rotation state
via data/quiz_usage.json.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
QUIZ_BANK_FILE = DATA_DIR / "quiz_bank.json"
QUIZ_USAGE_FILE = DATA_DIR / "quiz_usage.json"


def load_quiz_bank() -> Dict[str, List[Dict[str, Any]]]:
    """
    Loads and returns the quiz bank JSON dataset mapping skill_id to a list of question dicts.
    """
    if not QUIZ_BANK_FILE.exists():
        raise FileNotFoundError(f"Quiz bank dataset not found at: {QUIZ_BANK_FILE}")

    with open(QUIZ_BANK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_quiz_usage() -> Dict[str, List[int]]:
    """
    Loads the persistent tracking dict from data/quiz_usage.json mapping skill_id -> list of used indices.
    """
    if not QUIZ_USAGE_FILE.exists():
        return {}
    try:
        with open(QUIZ_USAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_quiz_usage(usage_data: Dict[str, List[int]]) -> None:
    """
    Saves the updated tracking dict to data/quiz_usage.json.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(QUIZ_USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(usage_data, f, indent=2)


def get_question_for_skill(skill_id: str) -> Dict[str, Any]:
    """
    Returns ONE question dict for skill_id that has NOT been used yet in the current cycle.
    
    Reads data/quiz_usage.json to find used question indices. If all questions for skill_id
    have been used across submissions, the cycle resets automatically and index 0 is returned.

    The returned dict contains:
    {
        "question": str,
        "options": List[str],
        "correct": str,
        "index": int,
        "skill_id": str
    }
    """
    bank = load_quiz_bank()
    questions = bank.get(skill_id, [])

    # Fallback if skill_id not present or empty in quiz_bank.json
    if not questions:
        # Check if any skills exist in bank
        first_available_skill = next(iter(bank.keys())) if bank else None
        if first_available_skill and bank[first_available_skill]:
            questions = bank[first_available_skill]
            skill_id = first_available_skill
        else:
            return {
                "question": "Which data structure operates on a First In, First Out (FIFO) principle?",
                "options": ["Stack (LIFO)", "Queue (FIFO)", "Binary Search Tree", "Hash Table"],
                "correct": "Queue (FIFO)",
                "index": 0,
                "skill_id": skill_id
            }

    usage = _load_quiz_usage()
    used_indices = usage.get(skill_id, [])

    # Find unused indices for this skill
    unused_indices = [i for i in range(len(questions)) if i not in used_indices]

    # If all questions have been used in the current cycle, reset the cycle for this skill
    if not unused_indices:
        used_indices = []
        usage[skill_id] = []
        _save_quiz_usage(usage)
        unused_indices = list(range(len(questions)))

    next_index = unused_indices[0]
    q_data = dict(questions[next_index])
    q_data["index"] = next_index
    q_data["skill_id"] = skill_id

    return q_data


def mark_question_used(skill_id: str, question_index: int) -> None:
    """
    Marks a question index as used for skill_id in data/quiz_usage.json.
    If all questions for the skill have now been used, resets the used list back to empty.
    """
    bank = load_quiz_bank()
    questions = bank.get(skill_id, [])
    total_questions = len(questions) if questions else 10

    usage = _load_quiz_usage()
    used_list = usage.get(skill_id, [])

    if question_index not in used_list:
        used_list.append(question_index)

    # Reset cycle if all questions have been served once
    if len(used_list) >= total_questions:
        used_list = []

    usage[skill_id] = used_list
    _save_quiz_usage(usage)


if __name__ == "__main__":
    print("=== Testing Quiz Bank Module ===")
    bank = load_quiz_bank()
    print(f"[OK] Quiz bank loaded with {len(bank)} skills.")
    
    q_tech = get_question_for_skill("py_prog")
    print(f"[OK] Tech Question fetched: {q_tech['question']} (Index: {q_tech['index']})")
    
    mark_question_used("py_prog", q_tech["index"])
    print("[OK] Question marked as used.")
    
    q_tech_2 = get_question_for_skill("py_prog")
    print(f"[OK] Next Tech Question fetched: {q_tech_2['question']} (Index: {q_tech_2['index']})")
