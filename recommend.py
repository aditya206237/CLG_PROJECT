"""
Learning Recommendations Layer for AIIA Skill Portal
------------------------------------------------------
Maps student skill deficits to curated academic courses, industry partner certifications,
workshops, and mentorship programs.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import streamlit as st

# Resolve default path relative to recommend.py script location
BASE_DIR = Path(__file__).parent.resolve()
RECOMMENDATIONS_FILE = BASE_DIR / "recommendations.json"

_recommendations_cache: Optional[Dict[str, List[Dict[str, Any]]]] = None


@st.cache_data
def load_recommendations(
    file_path: Path = RECOMMENDATIONS_FILE,
    force_reload: bool = False
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Loads and caches the curated recommendations JSON dataset.
    """
    global _recommendations_cache

    if not force_reload and _recommendations_cache is not None:
        return _recommendations_cache

    if not Path(file_path).exists():
        raise FileNotFoundError(f"Recommendations dataset file not found at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _recommendations_cache = data
    return data


def get_recommendations_for_gaps(
    top_gaps: List[Dict[str, Any]],
    n_per_skill: int = 2
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Given a list of skill gaps (e.g. from get_top_gaps() or compute_skill_gaps()),
    returns a dictionary mapping { skill_id: [resource1, resource2, ...] }
    ordered by gap priority.
    """
    rec_data = load_recommendations()
    results: Dict[str, List[Dict[str, Any]]] = {}

    for gap in top_gaps:
        # Only process actionable gaps (gap > 0)
        if gap.get("gap", 0) <= 0:
            continue

        sid = gap["skill_id"]
        resources = rec_data.get(sid, [])

        # Fallback if specific skill is not in recommendations.json
        if not resources:
            resources = [
                {
                    "title": f"Fundamentals & Applications of {gap.get('skill_name', sid)}",
                    "provider": "AIIA Industry Collaboration Partner",
                    "type": "workshop",
                    "duration": "4 weeks",
                    "url": "#"
                }
            ]

        results[sid] = resources[:n_per_skill]

    return results


if __name__ == "__main__":
    print("=== Testing Recommendations Layer ===")
    try:
        recs = load_recommendations()
        print(f"[OK] Recommendations dataset loaded successfully! Skills covered: {len(recs)}")

        # Simulated top gaps from gap_analysis.py
        sample_gaps = [
            {"skill_id": "stat_analysis", "skill_name": "Statistical Analysis & Inference", "gap": 4},
            {"skill_id": "machine_learning", "skill_name": "Machine Learning & Modeling", "gap": 3},
            {"skill_id": "linux_bash", "skill_name": "Linux Shell & Scripting", "gap": 3}
        ]

        gap_recs = get_recommendations_for_gaps(sample_gaps, n_per_skill=2)
        print(f"\n[OK] Generated recommendations for {len(gap_recs)} skill gaps:")

        for sid, res_list in gap_recs.items():
            print(f"\n  Skill ID: [{sid}]")
            for r in res_list:
                print(f"    * {r['title']} | Provider: {r['provider']} | Type: {r['type'].upper()} ({r['duration']})")


    except Exception as e:
        print(f"[ERROR] Recommendation Test Error: {e}")
