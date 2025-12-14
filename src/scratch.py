import altair as alt
import geopandas as gpd
import json
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

# Prep Chart 


## Hexes Layer
hexes = (
    alt.Chart(gdf)
    # .mark_geoshape(stroke="white", strokeWidth=2, fill="#69b3a2")
    .mark_geoshape(stroke="white", strokeWidth=3) 
    .encode(
        color=alt.Color("count:Q", scale=alt.Scale(scheme="greens")),
        tooltip=["state:N", "count:Q"]
    )
)

gap_labels = (
    alt.Chart(gdf)
    .mark_text(fontSize=12, fontWeight="bold")
    .encode(
        longitude="centroid_lon:Q",
        latitude="centroid_lat:Q",
        text=alt.Text("gender_gap:Q", format=".1%")
    )
)

## Labels Layer
labels = (
    alt.Chart(gdf)
    .mark_text(fontSize=14, fontWeight="bold", color="black")
    .encode(
        longitude="centroid_lon:Q",
        latitude="centroid_lat:Q",
        text="state:N"
    )
)

## Text and stuff...
chart_title = alt.TitleParams(
    "US Hexmap Blablablalba, bon c'est le titre",
    subtitle="And here commes the reading example...",
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
    text=alt.value("Source: ANES 2024 XYZ"),
    x=alt.value(800 - 10),
    y=alt.value(500 - 10),
)

# Combine 
hexmap = (hexes + gap_labels + source_text).project(
    type="mercator"  
).properties(
    width=800,
    height=500,
    title=chart_title
).configure_view(stroke=None) # remove greyed square from source_text... 
                              # there's probably an easier work around

hexmap

hexmap.save('a-chart.pdf')
