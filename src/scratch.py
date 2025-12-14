import altair as alt
import pandas as pd
import geopandas as gpd
import json

# Dynamic view in browser... Oui j'utilise encore et encore vim...
alt.renderers.enable("browser")

# Load Datasets (No ANES ATM)
# TODO include some useful ANES 2024 variable 

# Load the 2024 ANES example dataset
data_url = 'https://raw.githubusercontent.com/datamisc/ts-2024/main/data.csv'
df = pd.read_csv(data_url, compression='gzip')

df['V243001'].value_counts()

# Update title, reading example accordingly
url = (
    "https://raw.githubusercontent.com/holtzy/"
    "R-graph-gallery/refs/heads/master/DATA/us_states_hexgrid.geojson.json"
)

gdf = gpd.read_file(url)
gdf = gdf.rename(columns={"iso3166_2": "state"})

# Compute centroids for labels
gdf['centroid_lon'] = gdf.geometry.centroid.x
gdf['centroid_lat'] = gdf.geometry.centroid.y

# Cleanup
gdf = gdf.set_crs("EPSG:4326", allow_override=True)
gdf = gdf.drop(columns=['created_at', 'updated_at'])
geojson = json.loads(gdf.to_json())

# Prep Chart 

## Hexes Layer
hexes = (
    alt.Chart(
        alt.Data(
            values=geojson, 
            format=alt.DataFormat(property="features")
        )
    )
    .mark_geoshape(stroke="white", strokeWidth=2, fill="#69b3a2")
    .encode(
        tooltip=["properties.state:N"],
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
hexmap = (hexes + labels + source_text).project(
    type="mercator"  
).properties(
    width=800,
    height=500,
    title=chart_title
).configure_view(stroke=None) # remove greyed square from source_text... 
                              # there's probably an easier work around

hexmap

hexmap.save('a-chart.pdf')
