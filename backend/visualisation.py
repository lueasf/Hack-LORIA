import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import json


def load_session_data():
    """Charge les données de session depuis session_data.json"""
    session_file = Path("data/session_data.json")
    
    if not session_file.exists():
        return []
    
    with open(session_file, 'r') as f:
        return json.load(f)


def create_model_comparison_chart():
    """
    Crée un graphique comparatif des modèles LLM basé sur les données de session.
    Compare l'émission carbone (gCO2) et le temps de réponse par modèle.
    """
    
    # Charger les données
    session_data = load_session_data()
    
    if not session_data:
        # Retourner un graphique vide avec message
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée disponible.<br>Commencez par appeler un modèle !",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#000000", family='Righteous')
        )
        fig.update_layout(
            title=dict(
                text="Comparaison des Modèles LLM",
                font=dict(size=18, color='#000000', family='Righteous'),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='rgba(255,255,255,0.25)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    # Convertir en DataFrame
    df = pd.DataFrame(session_data)
    
    # Grouper par modèle et calculer les moyennes
    model_stats = df.groupby('model').agg({
        'carbon': 'mean',
        'tdev_seconds': 'mean'
    }).reset_index()
    
    # Compter le nombre d'appels par modèle
    model_counts = df['model'].value_counts().reset_index()
    model_counts.columns = ['model', 'count']
    
    # Fusionner
    model_stats = model_stats.merge(model_counts, on='model')
    
    # Palette de couleurs vert/olive
    colors = [
        'rgb(85,107,47)',   # DarkOliveGreen
        'rgb(107,142,35)',  # OliveDrab
        'rgb(154,205,50)',  # YellowGreen
        'rgb(189,183,107)', # DarkKhaki
        'rgb(222,184,135)'  # Burlywood
    ]
    
    # Assigner une couleur à chaque modèle
    model_colors = [colors[i % len(colors)] for i in range(len(model_stats))]
    
    # Créer le graphique à double axe
    fig = go.Figure()
    
    # Barres pour les émissions carbone
    fig.add_trace(go.Bar(
        x=model_stats['model'],
        y=model_stats['carbon'],
        name='Émissions CO₂ (gCO₂e)',
        marker=dict(
            color=model_colors,
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        ),
        text=[f"{c:.3f} g<br>({n} appels)" for c, n in zip(model_stats['carbon'], model_stats['count'])],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>' +
                      'Émissions: %{y:.4f} gCO₂e<br>' +
                      '<extra></extra>',
        yaxis='y1'
    ))
    
    # Ligne pour le temps de réponse
    fig.add_trace(go.Scatter(
        x=model_stats['model'],
        y=model_stats['tdev_seconds'],
        name='Temps de réponse (s)',
        mode='lines+markers',
        marker=dict(
            size=18,
            color='rgb(0,0,0)',
            line=dict(width=4, color='rgb(255,255,255)')
        ),
        line=dict(width=7, color='rgb(0,0,0)', dash='solid'),
        hovertemplate='<b>%{x}</b><br>' +
                      'Temps: %{y:.3f} s<br>' +
                      '<extra></extra>',
        yaxis='y2'
    ))
    
    # Mise en page avec double axe Y
    fig.update_layout(
        title=dict(
            text='Comparaison des Modèles LLM — Émissions vs Temps de Réponse',
            font=dict(size=20, color='#000000', family='Righteous'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Modèle LLM',
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=11, color='#000000'),
            tickangle=-45,
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Émissions CO₂ (gCO₂e)',
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=11, color='#000000'),
            side='left',
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True,
            zeroline=False
        ),
        yaxis2=dict(
            title='Temps de réponse (secondes)',
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=11, color='#000000'),
            overlaying='y',
            side='right',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False,
            showticklabels=True
        ),
        legend=dict(
            x=0.5,
            y=-0.3,
            xanchor='center',
            yanchor='top',
            orientation='h',
            font=dict(size=12, color='#000000'),
            bgcolor='rgba(255,255,255,0.5)',
            bordercolor='rgba(255,255,255,0.4)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=80, r=120, t=80, b=120),
        hovermode='x unified',
        font=dict(family='Righteous')
    )
    
    return fig


def create_session_timeline():
    """
    Crée un graphique temporel montrant l'évolution des émissions au fil de la session.
    """
    session_data = load_session_data()
    
    if not session_data:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée disponible",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#000000", family='Righteous')
        )
        fig.update_layout(
            title=dict(
                text="Chronologie de la Session",
                font=dict(size=18, color='#000000', family='Righteous'),
                x=0.5,
                xanchor='center'
            ),
            paper_bgcolor='rgba(255,255,255,0.25)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        return fig
    
    df = pd.DataFrame(session_data)
    df['call_number'] = range(1, len(df) + 1)
    
    fig = go.Figure()
    
    # Ligne pour les émissions
    fig.add_trace(go.Scatter(
        x=df['call_number'],
        y=df['carbon'],
        mode='lines+markers',
        name='Émissions',
        marker=dict(
            size=8,
            color=df['carbon'],
            colorscale='Greens',
            showscale=True,
            colorbar=dict(title="gCO₂e")
        ),
        line=dict(width=2),
        text=df['model'],
        hovertemplate='<b>Appel %{x}</b><br>' +
                      'Modèle: %{text}<br>' +
                      'Émissions: %{y:.4f} gCO₂e<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Évolution des Émissions au Fil de la Session',
            font=dict(size=18, color='#000000', family='Righteous'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Numéro d\'appel',
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Émissions CO₂ (gCO₂e)',
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True,
            zeroline=False
        ),
        paper_bgcolor='rgba(255,255,255,0.25)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        font=dict(color='#000000', family='Righteous')
    )
    
    return fig
