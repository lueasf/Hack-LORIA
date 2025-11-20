## map du mix energetique, cad le carbon intensity par pays (KgCO2/kWh)

import plotly.graph_objects as go
import pandas as pd
import base64
import math
from datetime import datetime

def create_numeric_activity():
    # Données d'exemple pour le graphique
    fig = go.Figure()

    # Données d'exemple : émissions CO2 par activité numérique (en g CO2)
    activities = ['Requête web', 'Email simple', 'Email avec PJ', 'Visio 1h']
    emissions = [0.2, 4, 50, 150]

    fig.add_trace(go.Bar(
        x=activities,
        y=emissions,
        marker=dict(
            color=emissions,
            colorscale='Greens',
            showscale=True,
            colorbar=dict(title="g CO2")
        ),
        text=[f"{e} g" for e in emissions],
        textposition='auto',
    ))

    fig.update_layout(
        xaxis=dict(
            title="Activité",
            title_font=dict(color='#000000'),
            tickfont=dict(color='#000000')
        ),
        yaxis=dict(
            title="Emissions CO2 (grammes)",
            title_font=dict(color='#000000'),
            tickfont=dict(color='#000000')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', family='Righteous'),
        height=400,
    )
    return fig

def create_carbon_intensity_map():
    """
    Crée une carte choroplèthe mondiale montrant l'intensité carbone par pays.
    Données basées sur les mix énergétiques (gCO2eq/kWh).
    """
    
    # Données d'intensité carbone par pays (gCO2eq/kWh)
    # Source: Electricity Maps / IEA
    carbon_intensity_data = {
        'country': [
            'France', 'Germany', 'United States', 'China', 'India', 'Japan',
            'United Kingdom', 'Canada', 'Australia', 'Brazil', 'Russia',
            'South Africa', 'Norway', 'Sweden', 'Spain', 'Italy', 'Poland',
            'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Denmark',
            'Finland', 'Portugal', 'Greece', 'Czech Republic', 'Hungary',
            'Romania', 'Bulgaria', 'Slovakia', 'Ireland', 'New Zealand',
            'Argentina', 'Mexico', 'Chile', 'Colombia', 'Indonesia',
            'Thailand', 'Vietnam', 'Malaysia', 'Philippines', 'Singapore',
            'South Korea', 'Taiwan', 'Turkey', 'Ukraine', 'Egypt',
            'Saudi Arabia', 'United Arab Emirates', 'Israel'
        ],
        'code': [
            'FRA', 'DEU', 'USA', 'CHN', 'IND', 'JPN',
            'GBR', 'CAN', 'AUS', 'BRA', 'RUS',
            'ZAF', 'NOR', 'SWE', 'ESP', 'ITA', 'POL',
            'NLD', 'BEL', 'CHE', 'AUT', 'DNK',
            'FIN', 'PRT', 'GRC', 'CZE', 'HUN',
            'ROU', 'BGR', 'SVK', 'IRL', 'NZL',
            'ARG', 'MEX', 'CHL', 'COL', 'IDN',
            'THA', 'VNM', 'MYS', 'PHL', 'SGP',
            'KOR', 'TWN', 'TUR', 'UKR', 'EGY',
            'SAU', 'ARE', 'ISR'
        ],
        'intensity': [
            60, 420, 420, 600, 700, 480,
            220, 130, 680, 100, 480,
            900, 20, 40, 180, 280, 780,
            390, 180, 30, 90, 120,
            85, 250, 380, 550, 280,
            320, 480, 120, 350, 110,
            380, 420, 380, 180, 720,
            480, 520, 620, 680, 420,
            480, 520, 420, 350, 480,
            620, 480, 520
        ]
    }
    
    df = pd.DataFrame(carbon_intensity_data)
    
    # Créer la carte choroplèthe
    fig = go.Figure(data=go.Choropleth(
        locations=df['code'],
        z=df['intensity'],
        text=df['country'],
        colorscale=[
            [0.0, 'rgb(85,107,47)'],    # DarkOliveGreen / olive foncé (valeurs basses = vert foncé)
            [0.2, 'rgb(107,142,35)'],   # OliveDrab / olive moyen
            [0.4, 'rgb(154,205,50)'],   # YellowGreen / vert lumineux
            [0.6, 'rgb(189,183,107)'],  # DarkKhaki / ton olive pâle
            [0.8, 'rgb(222,184,135)'],  # Burlywood / ton sable
            [1.0, 'rgb(240,240,230)']   # Très clair (beige) (valeurs hautes = beige)
        ],
        autocolorscale=False,
        reversescale=False,
        marker_line_color='white',
        marker_line_width=0.5,
        colorbar=dict(
            title=dict(
                text="Intensité carbone<br>(gCO2eq/kWh)",
                font=dict(size=14, color='#000000')
            ),
            tickfont=dict(color='#000000'),
            thickness=20,
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      'Intensité: %{z} gCO2eq/kWh<br>' +
                      '<extra></extra>'
    ))
    
    # Mise en page
    fig.update_layout(
        title=dict(
            text='Intensité Carbone du Mix Énergétique par Pays',
            font=dict(size=20, color='#000000'),
            x=0.5,
            xanchor='center'
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)',
            landcolor='rgba(200,200,200,0.3)',
            coastlinecolor='#000000'
        ),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(color='#000000')
    )
    
    return fig

def create_lightbulb_chart():
    # --- Données ---
    categories = [
        "1 Aller-Retour<br>Paris-NY (1 passager)",
        "Conso. d'un foyer<br>français (1 an)",
        "Voiture thermique<br>(1 an / 12 000 km)",
        "Entraînement du modèle<br>BLOOM (open source)",
        "Entraînement<br>de GPT-3"
    ]

    valeurs_mwh = [3.5, 4.7, 16, 433, 1287]

    # --- Image ---
    image_path = r"app/assets/lightbulb.png"
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    # --- Calcul des tailles avec échelle logarithmique pour mieux voir les petites valeurs ---
    # Utilisation de log pour que les petites valeurs soient plus visibles
    sizes_raw = [math.log(v + 1) for v in valeurs_mwh]  # +1 pour éviter log(0)
    
    # Normalisation : la plus grosse ampoule fait 1.2, la plus petite au moins 0.25
    max_val = max(sizes_raw)
    min_val = min(sizes_raw)
    min_display_size = 0.25
    max_display_size = 1.2
    
    sizes_normalized = [
        min_display_size + ((s - min_val) / (max_val - min_val)) * (max_display_size - min_display_size)
        for s in sizes_raw
    ]

    # --- Graphique ---
    fig = go.Figure()

    # Disposition en grille 3x2 pour mieux occuper l'espace
    # Ligne 1: indices 0, 1, 2
    # Ligne 2: indices 3, 4 (centrés)
    positions_x = [0, 1, 2, 0.5, 1.5]  # Positions horizontales
    positions_y = [0.7, 0.7, 0.7, -0.3, -0.3]  # Positions verticales ajustées pour mieux centrer

    # --- Ajout des ampoules ---
    for i, cat in enumerate(categories):
        size = sizes_normalized[i]
        val = valeurs_mwh[i]
        x_pos = positions_x[i]
        y_pos = positions_y[i]
        
        # Ajout de l'image
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_b64}",
                x=x_pos,
                y=y_pos,
                xref="x",
                yref="y",
                yanchor="bottom",
                sizex=size * 0.8,  # Ajustement pour éviter les chevauchements
                sizey=size * 0.8,
                xanchor="center",
                opacity=0.9,
                layer="above"
            )
        )
        
        # Ajout du texte au-dessus de l'ampoule
        fig.add_annotation(
            x=x_pos,
            y=y_pos + size * 0.8,
            text=f"<b>{val} MWh</b>",
            showarrow=False,
            yshift=15,
            font=dict(size=13, color="#000000", family="Helvetica, sans-serif"),
            bgcolor="rgba(255,255,255,0)",
            borderpad=4
        )
        
        # Ajout du label en dessous
        fig.add_annotation(
            x=x_pos,
            y=y_pos,
            text=cat,
            showarrow=False,
            yshift=-30,
            font=dict(size=11, color="#000000"),
            xanchor="center"
        )

    # --- Layout optimisé ---
    # Calculer les hauteurs réelles
    # Ligne du haut : position 0.7 + taille max des petites ampoules (indices 0,1,2)
    max_size_top = max(sizes_normalized[0], sizes_normalized[1], sizes_normalized[2])
    top_limit = 0.7 + max_size_top * 0.8 + 0.08  # position + taille + marge pour texte
    
    # Ligne du bas : position -0.3, le bas des labels
    bottom_limit = -0.3 - 0.15  # position + marge pour les labels en dessous
    
    fig.update_layout(
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            range=[bottom_limit, top_limit],  # Range ajusté au contenu réel
            visible=False,
            fixedrange=True,
            scaleanchor=None
        ),
        xaxis=dict(
            range=[-0.15, 2.25],  # Ajout d'un peu plus d'espace à droite
            visible=False,
            showgrid=False,
            zeroline=False,
            fixedrange=True,
            scaleanchor=None
        ),
        margin=dict(l=5, r=15, t=5, b=5),  # Marge droite légèrement augmentée
        font=dict(color='#000000', family="Helvetica, sans-serif"),
        showlegend=False
    )

    return fig


def create_adoption_chart():
    dates = [
        datetime(2022, 11, 30), datetime(2023, 1, 31), 
        datetime(2025, 2, 28), datetime(2025, 10, 31), datetime(2026, 12, 31)
    ]
    users_in_millions = [0, 100, 400, 800, 1000]
    annotations_text = [
        "<b>Lancement</b><br>1M en 5j", "<b>Record</b><br>100M / mois",
        "400M / sem.", "800M / sem.", "<b>Projection</b><br>> 1 Md"
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=users_in_millions, mode='lines+markers', name="Utilisateurs",
        line=dict(color='#2E7D32', width=4, shape='spline'), # J'ai mis vert pour rester dans le thème
        marker=dict(color='#1B5E20', size=10, symbol='circle-open-dot'),
        hovertemplate="<b>%{x|%B %Y}</b><br>%{y} millions<extra></extra>"
    ))

    for i, txt in enumerate(annotations_text):
        fig.add_annotation(
            x=dates[i], y=users_in_millions[i], text=txt, showarrow=True, arrowhead=4,
            ax=0, ay=-40 - (i % 2 * 25),
            font=dict(size=12, color="#333"),
            bgcolor="rgba(255,255,255,0.8)", bordercolor="#2E7D32", borderwidth=1
        )

    fig.update_layout(
        title=dict(text="<b>L'adoption fulgurante des LLM</b>", font=dict(size=20)),
        yaxis_title="Millions d'utilisateurs",
        # Ajout de la configuration explicite des axes en noir
        xaxis=dict(
            tickfont=dict(color='#000000'),
            title_font=dict(color='#000000')
        ),
        yaxis=dict(
            tickfont=dict(color='#000000'),
            title_font=dict(color='#000000')
        ),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', # Fond transparent
        font=dict(family="Helvetica, sans-serif", color="black"),
        hovermode="x unified", height=450,
        margin=dict(l=20, r=60, t=50, b=20)
    )
    return fig


# Pour utiliser dans Streamlit:
# import streamlit as st
# from backend.map import create_carbon_intensity_map
# 
# fig = create_carbon_intensity_map()
# st.plotly_chart(fig, use_container_width=True)


