# Chunk 1: Import necessary libraries
import folium
import geopandas as gpd
from folium.features import GeoJson, GeoJsonTooltip
import pandas as pd

# Chunk 2: Load data
# Load the GeoJSON file for hospitals
hospitals = gpd.read_file('FILEPATH/LeafletMapPython/Data/Hospitals.geojson')

# Load the county shapefile using GeoPandas
counties = gpd.read_file('FILEPATH/LeafletMapPython/Data/CountyShapefiles/cb_2018_us_county_500k.shp')

# Chunk 3: Convert non-JSON serializable columns
# Convert all Timestamp columns to strings in hospitals GeoDataFrame
for column in hospitals.select_dtypes(include=['datetime', 'datetimetz']):
    hospitals[column] = hospitals[column].astype(str)

# Chunk 4: Filter hospital data for point layers (General Medical with 100+ beds)
# Retain only "GENERAL MEDICAL AND SURGICAL HOSPITALS" with 100 or more beds for point layers
filtered_hospitals_points = hospitals[
    (hospitals['NAICS_DESC'] == "GENERAL MEDICAL AND SURGICAL HOSPITALS") & 
    (hospitals['BEDS'] >= 100)
]

# Chunk 5: Prepare hospital data by types for tooltips (Point Layers)
# Extract information for tooltips for hospitals (points)
filtered_hospitals_points.loc[:, 'tooltip'] = filtered_hospitals_points.apply(lambda row: f"""
    <b>Name:</b> {row['NAME']}<br>
    <b>Address:</b> {row['ADDRESS']}<br>
    <b>City, State:</b> {row['CITY']}, {row['STATE']}<br>
    <b>Type:</b> {row['NAICS_DESC']}<br>
    <b>Beds:</b> {row.get('BEDS', 'N/A')}
    """, axis=1)

# Chunk 6: Create a Folium map with no visible layers initially
m = folium.Map(location=[39.8283, -98.5795], zoom_start=5, control_scale=True)  

# Chunk 7: Add hospital GeoJSON layers by type (initially hidden)
hospital_layer_group = folium.FeatureGroup(name="Hospitals (General Medical, 100+ Beds)", show=False).add_to(m)

# Add GeoJson layer for filtered hospitals (hidden initially)
GeoJson(
    filtered_hospitals_points,
    name="General Medical and Surgical Hospitals (100+ Beds)",
    tooltip=GeoJsonTooltip(fields=['tooltip'], labels=False)
).add_to(hospital_layer_group)

# Chunk 8: Filter hospital data for county-level mapping (Only Trauma Level I)
# Retain only hospitals with TRAUMA value of "LEVEL I" for county choropleth layers
filtered_hospitals_trauma = hospitals[hospitals['TRAUMA'] == "LEVEL I"]

# Get the count of Trauma Level I hospitals by county GEOID
trauma_counts = filtered_hospitals_trauma.groupby('COUNTYFIPS').size().reset_index(name='trauma_count')

# Merge trauma counts with counties data
counties_trauma = counties.merge(trauma_counts, left_on='GEOID', right_on='COUNTYFIPS', how='left')
counties_trauma['trauma_count'] = counties_trauma['trauma_count'].fillna(0)

#Chunk 9: Coloring County by Facilities
# Define colors for trauma center counts
def get_color(trauma_count):
    if trauma_count == 0:
        return '#ffffff00'  # Transparent
    elif trauma_count == 1:
        return '#ffffb2'
    elif trauma_count == 2:
        return '#fecc5c'
    elif trauma_count <= 4:
        return '#fd8d3c'
    elif trauma_count <= 6:
        return '#f03b20'
    elif trauma_count <= 12:
        return '#bd0026'
    else:
        return '#800026'

# Prepare list of hospital names in each county for popup using the existing NAME field
county_hospital_info = filtered_hospitals_trauma.groupby('COUNTYFIPS')['NAME'].apply(lambda x: "<br>".join(x)).reset_index()
county_hospital_info = county_hospital_info.rename(columns={'NAME': 'hospital_names'})

# Merge hospital names with counties data
counties_trauma = counties_trauma.merge(county_hospital_info, left_on='GEOID', right_on='COUNTYFIPS', how='left')
counties_trauma['hospital_names'] = counties_trauma['hospital_names'].fillna('No hospitals')

# Add a combined choropleth and GeoJson layer for Trauma Level I facilities (initially hidden)
folium.GeoJson(
    counties_trauma,
    style_function=lambda feature: {
        'fillColor': get_color(feature['properties']['trauma_count']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7 if feature['properties']['trauma_count'] > 0 else 0
    },
    name='Trauma Level I Facilities',
    tooltip=folium.GeoJsonTooltip(
        fields=['hospital_names'],
        aliases=['Name of Trauma Level I Hospitals:'],
        localize=True
    )
).add_to(m)

# Chunk 10: Add custom legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 300px; height: 250px; 
            background-color: white; z-index:1000; font-size:14px;
            border:2px solid grey; padding: 10px;">
    <b>Number of Trauma Level I Facilities by County</b><br>
    <i style="background: #ffffff00; border: 1px solid black; padding: 5px;">&nbsp;&nbsp;</i> No Facilities<br>
    <i style="background: #ffffb2; padding: 5px;">&nbsp;&nbsp;</i> 1 Facility<br>
    <i style="background: #fecc5c; padding: 5px;">&nbsp;&nbsp;</i> 2 Facilities<br>
    <i style="background: #fd8d3c; padding: 5px;">&nbsp;&nbsp;</i> 3 - 4 Facilities<br>
    <i style="background: #f03b20; padding: 5px;">&nbsp;&nbsp;</i> 5 - 6 Facilities<br>
    <i style="background: #bd0026; padding: 5px;">&nbsp;&nbsp;</i> 7 - 12 Facilities<br>
    <i style="background: #800026; padding: 5px;">&nbsp;&nbsp;</i> 13+ Facilities
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Chunk 11: Add layer control and save the map
# Adding Layer Control on the right
folium.LayerControl(position='topright', collapsed=True).add_to(m)

#Chunk 12: Save File
# Save map as HTML
m.save('FILEPATH/LeafletMapPython/hospital_density_map.html')
