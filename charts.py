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
    Dark futuristic themed with high-contrast labels.
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

    # Target Role Benchmark Trace (Neon Red/Coral)
    fig.add_trace(go.Scatterpolar(
        r=required_scores_closed,
        theta=categories_closed,
        fill='toself',
        name=f'Required Benchmark ({target_role_name})',
        fillcolor='rgba(244, 63, 94, 0.25)',
        line=dict(color='#f43f5e', width=2.5, dash='dash'),
        marker=dict(size=6, color='#f43f5e'),
        hoverinfo='text',
        text=[f"Skill: {c}<br>Required Level: {val}/5" for c, val in zip(categories_closed, required_scores_closed)]
    ))

    # Student Verified Skill Trace (Neon Cyan)
    fig.add_trace(go.Scatterpolar(
        r=student_scores_closed,
        theta=categories_closed,
        fill='toself',
        name=f'{student_name} (Verified Rating)',
        fillcolor='rgba(56, 189, 248, 0.4)',
        line=dict(color='#38bdf8', width=3),
        marker=dict(size=8, color='#38bdf8'),
        hoverinfo='text',
        text=[f"Skill: {c}<br>Student Rating: {val}/5" for c, val in zip(categories_closed, student_scores_closed)]
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family='Inter, sans-serif'),
        polar=dict(
            bgcolor='rgba(15, 23, 42, 0.65)',
            radialaxis=dict(
                visible=True,
                range=[0, 5.2],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1 (Basic)', '2', '3 (Interm)', '4', '5 (Expert)'],
                gridcolor='rgba(148, 163, 184, 0.25)',
                tickfont=dict(color='#cbd5e1', size=10),
                angle=0
            ),
            angularaxis=dict(
                gridcolor='rgba(148, 163, 184, 0.25)',
                linecolor='#38bdf8',
                tickfont=dict(color='#f8fafc', size=11)
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#f8fafc')
        ),
        margin=dict(l=60, r=60, t=30, b=70),
        height=520
    )
    return fig

