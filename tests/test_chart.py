import streamlit as st
import plotly.express as px
import pandas as pd

# 1. Beispieldaten für den zeitlichen Verlauf erstellen
data = {
    'Jahr': [2021, 2022, 2023, 2024],
    'Gewinn': [15000, 22000, 19000, 31000],
    'Meilenstein': ['Firmengründung', 'Erster Mitarbeiter', 'Lieferengpässe', 'Neuer Onlineshop']
}
df = pd.DataFrame(data)

st.title("Interaktives Liniendiagramm")

# 2. Liniendiagramm erstellen 
# 'markers=True' macht die einzelnen Datenpunkte auf der Linie sichtbar
fig = px.line(
    df, 
    x='Jahr', 
    y='Gewinn',
    title='Unternehmensgewinn (Bewege die Maus über die Punkte!)',
    markers=True,
    hover_data=['Meilenstein'] # Nimmt die Zusatzinfo in den Hover-Speicher auf
)

# 3. Das Aussehen des Pop-ups beim Drüberhalten anpassen
fig.update_traces(
    hovertemplate="<br>".join([
        "<b>Jahr:</b> %{x}",
        "<b>Gewinn:</b> %{y} €",
        "<b>Ereignis:</b> %{customdata[0]}"
    ])
)

# Optional: Macht das Hover-Fenster optisch moderner (blauer Hintergrund, weiße Schrift)
fig.update_layout(
    hoverlabel=dict(
        bgcolor="royalblue",
        font_size=16,
        font_family="Arial"
    )
)

# 4. Diagramm in Streamlit rendern
st.plotly_chart(fig)
