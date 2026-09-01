"""
Skill Taxonomy & Role Requirements Loader Module
------------------------------------------------
Provides helper functions to load, validate, and query skill taxonomy datasets
and role requirement profiles for assessment and gap analysis.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import streamlit as st

# Define default paths relative to this script directory
BASE_DIR = Path(__file__).parent.resolve()
TAXONOMY_FILE = BASE_DIR / "skill_taxonomy.json"
ROLE_REQ_FILE = BASE_DIR / "role_requirements.json"

# In-memory caches to avoid redundant file I/O
_skills_cache: Optional[List[Dict[str, Any]]] = None
_skills_dict_cache: Optional[Dict[str, Dict[str, Any]]] = None
_roles_cache: Optional[Dict[str, List[Dict[str, Any]]]] = None


def load_dataset(
    taxonomy_path: Path = TAXONOMY_FILE,
    role_req_path: Path = ROLE_REQ_FILE,
    force_reload: bool = False,
) -> None:
    """
    Loads and validates the skill taxonomy and role requirement datasets.
    Raises ValueError if validation fails (e.g. invalid skill references).
    """
    global _skills_cache, _skills_dict_cache, _roles_cache

    if not force_reload and _skills_cache is not None and _roles_cache is not None:
        return

    if not Path(taxonomy_path).exists():
        raise FileNotFoundError(f"Taxonomy dataset file not found at: {taxonomy_path}")
    if not Path(role_req_path).exists():
        raise FileNotFoundError(f"Role requirements dataset file not found at: {role_req_path}")

    with open(taxonomy_path, "r", encoding="utf-8") as f:
        skills_data = json.load(f)

    with open(role_req_path, "r", encoding="utf-8") as f:
        roles_data = json.load(f)

    # Validate skill structure & duplicate IDs
    skills_dict: Dict[str, Dict[str, Any]] = {}
    valid_categories = {"technical", "domain", "soft"}

    for idx, skill in enumerate(skills_data):
        sid = skill.get("id")
        if not sid:
            raise ValueError(f"Taxonomy error at index {idx}: Missing 'id' field.")
        if sid in skills_dict:
            raise ValueError(f"Taxonomy error: Duplicate skill ID found '{sid}'.")
        category = skill.get("category")
        if category not in valid_categories:
            raise ValueError(
                f"Taxonomy error for skill '{sid}': Invalid category '{category}'. "
                f"Must be one of {valid_categories}"
            )
        skills_dict[sid] = skill

    # Validate role requirements against skill taxonomy
    for role_name, req_list in roles_data.items():
        if not isinstance(req_list, list):
            raise ValueError(f"Role requirements error: Role '{role_name}' must map to a list.")
        for req in req_list:
            sid = req.get("skill_id")
            if sid not in skills_dict:
                raise ValueError(
                    f"Validation Error: Role '{role_name}' references non-existent skill_id '{sid}'."
                )
            level = req.get("required_level")
            if not isinstance(level, int) or level < 1 or level > 5:
                raise ValueError(
                    f"Validation Error: Role '{role_name}', skill '{sid}' has invalid required_level '{level}'. "
                    f"Must be an integer from 1 to 5."
                )

    _skills_cache = skills_data
    _skills_dict_cache = skills_dict
    _roles_cache = roles_data


@st.cache_data
def get_all_skills() -> List[Dict[str, Any]]:
    """Returns a list of all skills defined in the taxonomy."""
    load_dataset()
    return list(_skills_cache)  # type: ignore


@st.cache_data
def get_skills_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Returns skills filtered by category ('technical', 'domain', or 'soft').
    """
    load_dataset()
    cat_clean = category.lower().strip()
    return [s for s in _skills_cache if s["category"] == cat_clean]  # type: ignore


@st.cache_data
def get_role_requirements(role_name: str) -> List[Dict[str, Any]]:
    """
    Returns the required skill vector for a given role, enriched with skill metadata.
    """
    load_dataset()
    if role_name not in _roles_cache:  # type: ignore
        available = list(_roles_cache.keys())  # type: ignore
        raise KeyError(f"Role '{role_name}' not found. Available roles: {available}")

    requirements = []
    for req in _roles_cache[role_name]:  # type: ignore
        sid = req["skill_id"]
        meta = _skills_dict_cache[sid]  # type: ignore
        requirements.append({
            "skill_id": sid,
            "name": meta["name"],
            "category": meta["category"],
            "description": meta["description"],
            "required_level": req["required_level"],
        })
    return requirements


@st.cache_data
def get_available_roles() -> List[str]:
    """Returns a list of all configured target roles."""
    load_dataset()
    return list(_roles_cache.keys())  # type: ignore


if __name__ == "__main__":
    print("=== Testing Skill Taxonomy & Role Loader ===")
    try:
        load_dataset()
        print("[OK] Datasets loaded & validated successfully!\n")

        all_skills = get_all_skills()
        print(f"Total skills in taxonomy: {len(all_skills)}")

        tech_skills = get_skills_by_category("technical")
        domain_skills = get_skills_by_category("domain")
        soft_skills = get_skills_by_category("soft")
        print(f"  - Technical skills: {len(tech_skills)}")
        print(f"  - Domain skills:    {len(domain_skills)}")
        print(f"  - Soft skills:      {len(soft_skills)}")

        roles = get_available_roles()
        print(f"\nConfigured Target Roles: {roles}")

        print("\nSample Role Requirement Profile [Data Science]:")
        ds_reqs = get_role_requirements("Data Science")
        for req in ds_reqs[:5]:
            print(f"  * [{req['category'].upper()}] {req['name']} (ID: {req['skill_id']}) -> Required Level: {req['required_level']}/5")

    except Exception as e:
        print(f"[ERROR] Loader Error: {e}")

