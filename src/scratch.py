import altair as alt
import geopandas as gpd
from src.polk_gap import main as gap


df_gap = gap()

# Dynamic view in browser... Oui j'utilise encore et encore vim...
alt.renderers.enable("browser")

# Load Datasets (No ANES ATM)
# TODO include some useful ANES 2024 variable 

# Update title, reading example accordingly
data_hex_url = (
    "https://raw.githubusercontent.com/holtzy/"
    "R-graph-gallery/refs/heads/master/DATA/us_states_hexgrid.geojson.json"
)

gdf = gpd.read_file(data_hex_url)
gdf = gdf.rename(columns={"iso3166_2": "state"})

# Compute centroids for labels
gdf['centroid_lon'] = gdf.geometry.centroid.x
gdf['centroid_lat'] = gdf.geometry.centroid.y

# Merge Gap Variable
gdf = gdf.merge(df_gap, on='state', how='left')

gdf['gender_gap'] = gdf['gender_gap'] *-1


gdf['label'] = gdf['state'] + "\n" + (gdf['gender_gap'] * 100).round(1).astype(str) + "%"

# Chart Prep

tmp_val = max([abs(gdf['gender_gap'].min()), abs(gdf['gender_gap'].max())])
domain_range = [-tmp_val, tmp_val]

## Hexes Layer
hexes = (
    alt.Chart(gdf)
    .mark_geoshape(stroke="white", strokeWidth=3) 
    .encode(
        color=alt.Color(
            "gender_gap:Q",
            scale=alt.Scale(scheme="redgrey", domainMid=0, domain=domain_range),
            legend=alt.Legend(title=["Inégalité de", "Genre"])
        ),
        tooltip=["state:N", alt.Tooltip("gender_gap:Q", format=".1%"), "count:Q"]
    )
)

## Labels Layer
hex_labels = (
    alt.Chart(gdf)
    .mark_text(
        fontSize=14, 
        fontWeight="bold", 
        color="black", 
        align="center", 
        baseline="middle"
    )
    .encode(
        longitude="centroid_lon:Q",
        latitude="centroid_lat:Q",
        text="state:N"
    )
)

subtitle = [
    "Au Massachusetts, en 2024, l'écart de connaissance politique entre les hommes et les femmes",
    "est de -18,7 points de pourcentage. Les valeurs négatives indiquent un biais en faveur des hommes."
]

## Text and stuff...
chart_title = alt.TitleParams(
    "Inégalités de connaissance politique aux États-Unis selon le genre",
    subtitle=subtitle,
    fontSize=20,
    subtitleFontSize=14,
    anchor="start",
    fontWeight="bold"
)

source_text = alt.Chart().mark_text(
    align='right',
    baseline='bottom',
    fontSize=12,
    color='gray'
).encode(
    text=alt.value("Source: 2024 American National Election Study"),
    x=alt.value(800 - 10),
    y=alt.value(525 - 10),
)

hexmap = (hexes + hex_labels + source_text).project(
    type="mercator"
).properties(
    width=800,
    height=500,
    title=chart_title
).configure_view(stroke=None)

hexmap

hexmap.save('a-chart.pdf')
