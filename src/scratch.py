import altair as alt
import pandas as pd
import geopandas as gpd
import json

alt.renderers.enable("browser")

# Load Datasets (No ANES ATM)
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

# Hexes Layer
hexes = (
    alt.Chart(alt.Data(values=geojson, format=alt.DataFormat(property="features")))
    .mark_geoshape(stroke="white", strokeWidth=1)
    .encode(
        tooltip=["properties.state:N"],
    )
)

# Labels Layer
labels = (
    alt.Chart(gdf)
    .mark_text(fontSize=10, fontWeight="bold")
    .encode(
        longitude="centroid_lon:Q",
        latitude="centroid_lat:Q",
        text="state:N"
    )
)

# Combine 
hexmap = (hexes + labels).project(
    type="mercator"  
).properties(
    width=800,
    height=500,
    title="US States Hexgrid Map",
)

hexmap

