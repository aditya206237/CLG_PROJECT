"""
Plotly Chart Generators for Skill Gap Engine & Portfolio
--------------------------------------------------------
Shared charting module for rendering Plotly Scatterpolar radar charts.
Editorial Data Analytics styling (Dark panel, Mint student trace, Cream benchmark trace).
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
    Editorial Dark Panel aesthetic with Mint student trace & Cream benchmark.
    
    Font color readability rules:
    - Angular axis labels (skill names around the radar) sit outside on the cream background: #1C1A16 (dark near-black)
    - Legend labels sit outside on the cream background: #1C1A16 (dark near-black)
    - Radial axis tick labels (1-5 levels) sit INSIDE the dark #14120F panel: #EFEBDF (light cream)
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

    # Target Role Benchmark Trace (Warm Cream / Off-white)
    fig.add_trace(go.Scatterpolar(
        r=required_scores_closed,
        theta=categories_closed,
        fill='toself',
        name=f'Required Benchmark ({target_role_name})',
        fillcolor='rgba(239, 235, 223, 0.12)',
        line=dict(color='#EFEBDF', width=2, dash='dash'),
        marker=dict(size=6, color='#EFEBDF'),
        hoverinfo='text',
        text=[f"Skill: {c}<br>Required Level: {val}/5" for c, val in zip(categories_closed, required_scores_closed)]
    ))

    # Student Verified Skill Trace (Warm Mint)
    fig.add_trace(go.Scatterpolar(
        r=student_scores_closed,
        theta=categories_closed,
        fill='toself',
        name=f'{student_name} (Verified Rating)',
        fillcolor='rgba(143, 224, 176, 0.3)',
        line=dict(color='#8FE0B0', width=3),
        marker=dict(size=8, color='#8FE0B0'),
        hoverinfo='text',
        text=[f"Skill: {c}<br>Student Rating: {val}/5" for c, val in zip(categories_closed, student_scores_closed)]
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1C1A16', family='JetBrains Mono, monospace'),
        polar=dict(
            bgcolor='#14120F',
            radialaxis=dict(
                visible=True,
                range=[0, 5.2],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1 (Basic)', '2', '3 (Interm)', '4', '5 (Expert)'],
                gridcolor='rgba(239, 235, 223, 0.2)',
                tickfont=dict(color='#EFEBDF', size=10, family='JetBrains Mono, monospace'),
                angle=0
            ),
            angularaxis=dict(
                gridcolor='rgba(239, 235, 223, 0.2)',
                linecolor='#14493D',
                tickfont=dict(color='#1C1A16', size=12, family='JetBrains Mono, monospace')
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#1C1A16', family='JetBrains Mono, monospace')
        ),
        margin=dict(l=80, r=80, t=30, b=80),
        height=540
    )
    return fig
