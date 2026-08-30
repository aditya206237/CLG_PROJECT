"""
Skill Gap-Analysis & Vector Match Engine
----------------------------------------
Compares a student's self-assessed/verified skill vector against target role requirements
using Cosine Similarity vector math and multi-dimensional gap calculation.

COSINE SIMILARITY MATH EXPLAINED (For SIH Hackathon Judges):
------------------------------------------------------------
Cosine Similarity measures the cosine of the angle (θ) between two multi-dimensional vectors:

    Cosine Similarity = (A • B) / (||A|| * ||B||)
                      = Σ(A_i * B_i) / ( sqrt(Σ A_i^2) * sqrt(Σ B_i^2) )

- Vector A: Student's verified skill ratings vector [e.g., Python: 5, SQL: 4, Machine Learning: 2]
- Vector B: Target role's required skill vector   [e.g., Python: 5, SQL: 4, Machine Learning: 5]

Why Cosine Similarity instead of Euclidean Distance?
---------------------------------------------------
Euclidean distance only measures straight-line distance, which harshly penalizes general rating levels.
Cosine Similarity evaluates the relative BALANCE and PROPORTIONAL ALIGNMENT of the student's skills
against the target role profile.
- A score of 1.0 (100%) indicates perfect proportional skill alignment.
- A score of 0.0 (0%) indicates no skill alignment whatsoever.
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Any, Union
from load_taxonomy import get_all_skills, get_role_requirements


def _normalize_role_reqs(
    role_requirements: Union[str, List[Dict[str, Any]], Dict[str, int]]
) -> Dict[str, Dict[str, Any]]:
    """
    Normalizes various role requirements input formats into a uniform dictionary mapping:
    { skill_id: {"name": str, "required_level": int} }
    """
    req_dict: Dict[str, Dict[str, Any]] = {}
    
    # Case 1: Role name passed as string (e.g. "Data Science")
    if isinstance(role_requirements, str):
        role_requirements = get_role_requirements(role_requirements)

    # Case 2: List of requirement dicts from get_role_requirements() or role_requirements.json
    if isinstance(role_requirements, list):
        for item in role_requirements:
            sid = item["skill_id"]
            req_dict[sid] = {
                "name": item.get("name", sid),
                "required_level": item["required_level"]
            }
    # Case 3: Raw dict {skill_id: level}
    elif isinstance(role_requirements, dict):
        all_skills_map = {s["id"]: s["name"] for s in get_all_skills()}
        for sid, level in role_requirements.items():
            req_dict[sid] = {
                "name": all_skills_map.get(sid, sid),
                "required_level": level
            }
            
    return req_dict


def build_vectors(
    student_skills: Dict[str, int],
    role_requirements: Union[str, List[Dict[str, Any]], Dict[str, int]],
    all_skill_ids: List[str] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Constructs two aligned NumPy arrays (student_vector, required_vector)
    guaranteeing identical skill ordering and length.
    
    Fills 0 for any unrated skill or skills not required by the target role.
    """
    if all_skill_ids is None:
        all_skill_ids = [s["id"] for s in get_all_skills()]

    role_dict = _normalize_role_reqs(role_requirements)

    student_vec = []
    required_vec = []

    for sid in all_skill_ids:
        # Extract student rating, defaulting to 0 if unrated
        student_val = student_skills.get(sid, 0)
        # Extract required rating, defaulting to 0 if not required by role
        required_val = role_dict.get(sid, {}).get("required_level", 0)

        student_vec.append(float(student_val))
        required_vec.append(float(required_val))

    return np.array(student_vec), np.array(required_vec)


def compute_match_score(
    student_vector: np.ndarray,
    required_vector: np.ndarray
) -> float:
    """
    Computes overall match score percentage (0-100%) using Cosine Similarity between vectors.
    """
    # Guard against zero vectors to prevent division-by-zero math errors
    if np.all(student_vector == 0) or np.all(required_vector == 0):
        return 0.0

    # Reshape vectors to 2D arrays expected by scikit-learn (1 sample, N features)
    student_2d = student_vector.reshape(1, -1)
    required_2d = required_vector.reshape(1, -1)

    sim_score = cosine_similarity(student_2d, required_2d)[0][0]
    
    # Scale from [0.0, 1.0] range to percentage [0.0, 100.0]
    percentage_score = round(float(sim_score) * 100.0, 1)
    return max(0.0, min(100.0, percentage_score))


def compute_skill_gaps(
    student_skills: Dict[str, int],
    role_requirements: Union[str, List[Dict[str, Any]], Dict[str, int]]
) -> List[Dict[str, Any]]:
    """
    Identifies and calculates skill gaps for all skills required by the target role.
    
    Gap formula: gap = max(0, required_level - student_level)
    Returns list of dicts sorted by gap magnitude descending.
    """
    role_dict = _normalize_role_reqs(role_requirements)
    all_skills_map = {s["id"]: s["name"] for s in get_all_skills()}

    gaps = []
    for sid, req_info in role_dict.items():
        req_level = req_info["required_level"]
        student_level = student_skills.get(sid, 0)
        
        # Calculate skill deficit (floor at 0 if student meets or exceeds target)
        gap = max(0, req_level - student_level)

        gaps.append({
            "skill_id": sid,
            "skill_name": req_info.get("name") or all_skills_map.get(sid, sid),
            "student_level": student_level,
            "required_level": req_level,
            "gap": gap
        })

    # Sort descending: largest skill gap first
    gaps.sort(key=lambda x: x["gap"], reverse=True)
    return gaps


def get_top_gaps(
    student_skills: Dict[str, int],
    role_requirements: Union[str, List[Dict[str, Any]], Dict[str, int]],
    n: int = 5
) -> List[Dict[str, Any]]:
    """
    Returns the top N largest skill deficits where gap > 0.
    """
    all_gaps = compute_skill_gaps(student_skills, role_requirements)
    # Filter to only actionable gaps (gap > 0)
    positive_gaps = [g for g in all_gaps if g["gap"] > 0]
    return positive_gaps[:n]


# -----------------------------------------------------------------------------
# Test Suite / Execution Block
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Testing Skill Gap-Analysis Engine ===")

    # Sample student ratings (Simulated assessment submission for Data Science candidate)
    sample_student_skills = {
        "py_prog": 4,          # Required: 5 -> Gap: 1
        "sql_db": 3,           # Required: 4 -> Gap: 1
        "git_vcs": 2,          # Required: 3 -> Gap: 1
        "linux_bash": 0,       # Unrated, Required: 3 -> Gap: 3
        "machine_learning": 2, # Required: 5 -> Gap: 3
        "data_viz": 4,         # Required: 4 -> Gap: 0
        "stat_analysis": 1,    # Required: 5 -> Gap: 4
        "data_wrangling": 3,   # Required: 5 -> Gap: 2
        "comm_verbal": 4,      # Required: 4 -> Gap: 0
        "team_collab": 3,      # Required: 3 -> Gap: 0
        "prob_solving": 4,     # Required: 5 -> Gap: 1
        "adapt_agility": 4     # Required: 4 -> Gap: 0
    }

    target_role = "Data Science"

    # 1. Build Aligned Vectors
    s_vec, r_vec = build_vectors(sample_student_skills, target_role)
    print(f"[OK] Aligned vectors generated! Vector Length: {len(s_vec)}")

    # 2. Compute Match Score
    match_score = compute_match_score(s_vec, r_vec)
    print(f"\n[MATCH SCORE] Overall Role Match Score [{target_role}]: {match_score}%")

    # 3. Compute All Skill Gaps
    all_gaps = compute_skill_gaps(sample_student_skills, target_role)
    print(f"\n[DETAILED GAPS] Detailed Skill Gaps ({len(all_gaps)} Required Skills Analyzed):")
    print(f"{'SKILL ID':<18} {'SKILL NAME':<35} {'STUDENT':<8} {'REQUIRED':<9} {'GAP':<5}")
    print("-" * 78)
    for g in all_gaps:
        print(f"{g['skill_id']:<18} {g['skill_name']:<35} {g['student_level']:<8} {g['required_level']:<9} {g['gap']:<5}")

    # 4. Extract Top 5 Gaps
    top_5 = get_top_gaps(sample_student_skills, target_role, n=5)
    print(f"\n[TOP GAPS] Top 5 Target Improvement Priority Gaps:")
    for idx, item in enumerate(top_5, 1):
        print(f"  {idx}. {item['skill_name']} ({item['skill_id']}): Student={item['student_level']}/5 vs Required={item['required_level']}/5 [Deficit: -{item['gap']}]")

