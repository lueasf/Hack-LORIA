## map du mix energetique, cad le carbon intensity par pays (KgCO2/kWh)

import plotly.graph_objects as go
import pandas as pd
import base64
import math

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
        title="Empreinte carbone d'activités numériques courantes",
        xaxis_title="Activité",
        yaxis_title="Emissions CO2 (grammes)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', family='Righteous'),
        height=500,
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
                font=dict(size=14)
            ),
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
            bgcolor='rgba(0,0,0,0)'
        ),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0)
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

    # --- Image (Votre code) ---
    # Assurez-vous que le chemin est correct ou utilisez une URL pour le web
    image_path = r"app/assets/lightbulb.png"
    # Pour l'exemple, si l'image n'est pas chargée, le code plantera, 
    # donc assurez-vous que img_b64 est bien rempli comme dans votre code.
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    # --- 1. Calcul de la taille des ampoules ---
    # Pour une représentation visuelle honnête, on lie souvent l'aire à la valeur.
    # Donc la hauteur/largeur (size) doit être proportionnelle à la racine carrée de la valeur.
    # Si vous préférez votre échelle LOG pour mieux voir les petites, décommentez la ligne 'Log'

    # Option A : Proportionnel à la racine carrée (plus réaliste physiquement)
    sizes_raw = [math.sqrt(v) for v in valeurs_mwh]

    # Option B : Votre échelle Log (si vous voulez que les petites soient plus grosses)
    # sizes_raw = [math.log(v) for v in valeurs_mwh]

    # --- 2. Normalisation ---
    # On veut que la plus grosse ampoule ait une taille max définie (ex: 0.8 unité de grille)
    # pour ne pas qu'elle dépasse sur les voisins.
    max_val = max(sizes_raw)
    max_display_size = 0.8  # La plus grosse ampoule prendra 80% de la largeur d'une colonne
    sizes_normalized = [(s / max_val) * max_display_size for s in sizes_raw]

    # --- Graphique ---
    fig = go.Figure()

    # On ajoute une trace invisible juste pour définir les catégories en X
    fig.add_trace(go.Scatter(
        x=categories,
        y=[0] * len(categories),
        mode="markers",
        marker=dict(opacity=0)
    ))

    # --- Ajout des ampoules ---
    for i, cat in enumerate(categories):
        size = sizes_normalized[i]
        val = valeurs_mwh[i]
        
        # Ajout de l'image
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_b64}",
                x=cat,
                y=0,               # On pose tout le monde au sol (0)
                xref="x",
                yref="y",
                yanchor="bottom",  # L'image grandit vers le haut à partir de 0
                sizex=size,        # Largeur
                sizey=size,        # Hauteur (garder le ratio carré)
                xanchor="center",  # Centré horizontalement sur la catégorie
                opacity=0.9,
                layer="above"
            )
        )
        
        # Ajout du texte au-dessus de l'ampoule
        # On place le texte à une hauteur = taille de l'image + une petite marge
        fig.add_annotation(
            x=cat,
            y=size, # Le haut de l'ampoule
            text=f"<b>{val} MWh</b>",
            showarrow=False,
            yshift=20, # Décale le texte un peu vers le haut (en pixels)
            font=dict(size=14, color="black")
        )

    # --- Layout Épuré ---
    fig.update_layout(
        title=dict(
            text="Impact énergétique de l'entraînement d'un LLM",
            x=0.5, # Titre centré
            font=dict(size=20, color='#000000')
        ),
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # On fixe l'axe Y manuellement pour laisser de la place à la plus grosse ampoule + texte
        yaxis=dict(
            range=[0, max_display_size * 1.2], 
            visible=False, # On cache l'axe Y (graduations, lignes)
            fixedrange=True # Empêche le zoom sur Y
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            fixedrange=True,
            # On définit manuellement les limites de l'axe X.
            # Il y a 5 catégories (indices 0 à 4).
            # On commence à -0.6 (pour la marge gauche)
            # On finit à 4.6 (pour laisser de la place à droite de la dernière ampoule)
            range=[-0.6, len(categories) - 1 + 0.6] 
        ),
        # Vous pouvez aussi augmenter la marge droite globale si ça ne suffit pas
        margin=dict(l=20, r=50, t=80, b=20) 
    )

    return fig

# Pour utiliser dans Streamlit:
# import streamlit as st
# from backend.map import create_carbon_intensity_map
# 
# fig = create_carbon_intensity_map()
# st.plotly_chart(fig, use_container_width=True)