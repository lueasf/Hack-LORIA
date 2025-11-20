## map du mix energetique, cad le carbon intensity par pays (KgCO2/kWh)

import plotly.graph_objects as go
import pandas as pd

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
            [0, 'rgb(0, 150, 0)'],      # Vert foncé (très faible)
            [0.2, 'rgb(100, 200, 100)'], # Vert clair
            [0.4, 'rgb(255, 255, 100)'], # Jaune
            [0.6, 'rgb(255, 180, 0)'],   # Orange
            [0.8, 'rgb(255, 100, 0)'],   # Orange foncé
            [1, 'rgb(200, 0, 0)']        # Rouge foncé (très élevé)
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

# Pour utiliser dans Streamlit:
# import streamlit as st
# from backend.map import create_carbon_intensity_map
# 
# fig = create_carbon_intensity_map()
# st.plotly_chart(fig, use_container_width=True)