"""
Plotly Chart Generators for Skill Gap Engine & Portfolio
--------------------------------------------------------
Shared charting module for rendering Plotly Scatterpolar radar charts.
"""

import plotly.graph_objects as go
from typing import Dict, List, Any


def create_radar_chart(
    student_vector: Dict[str, int],
    role_requirements: List[Dict[str, Any]],
    target_role_name: str,
    student_name: str
) -> go.Figure:
    """
    Generates an overlapping Plotly Scatterpolar radar chart comparing
    the student's verified skill vector against target role requirements.
    """
    role_skill_ids = [r["skill_id"] for r in role_requirements]
    radar_categories = [r["name"] for r in role_requirements]

    student_scores = [student_vector.get(sid, 0) for sid in role_skill_ids]
    required_scores = [r["required_level"] for r in role_requirements]

    # Close polar loop by appending first element to the end
    categories_closed = radar_categories + [radar_categories[0]]
    student_scores_closed = student_scores + [student_scores[0]]
    required_scores_closed = required_scores + [required_scores[0]]

    fig = go.Figure()

    # Target Role Benchmark Trace
    fig.add_trace(go.Scatterpolar(
        r=required_scores_closed,
        theta=categories_closed,
        fill='toself',
        name=f'Required Benchmark ({target_role_name})',
        fillcolor='rgba(231, 111, 81, 0.25)',
        line=dict(color='#e76f51', width=2.5, dash='dash'),
        marker=dict(size=6, color='#e76f51'),
        hoverinfo='text',
        text=[f"Skill: {c}<br>Required Level: {val}/5" for c, val in zip(categories_closed, required_scores_closed)]
    ))

    # Student Verified Skill Trace
    fig.add_trace(go.Scatterpolar(
        r=student_scores_closed,
        theta=categories_closed,
        fill='toself',
        name=f'{student_name} (Verified Rating)',
        fillcolor='rgba(42, 157, 143, 0.45)',
        line=dict(color='#2a9d8f', width=3),
        marker=dict(size=8, color='#2a9d8f'),
        hoverinfo='text',
        text=[f"Skill: {c}<br>Student Rating: {val}/5" for c, val in zip(categories_closed, student_scores_closed)]
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5.2],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1 (Basic)', '2', '3 (Interm)', '4', '5 (Expert)'],
                gridcolor='#e2e8f0',
                angle=0
            ),
            angularaxis=dict(
                gridcolor='#cbd5e1',
                linecolor='#94a3b8'
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(l=50, r=50, t=30, b=70),
        height=500
    )
    return fig
