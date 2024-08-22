# Import all Libraries
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd
import pydeck as pdk
import random
from shapely.geometry import Point

# Set the page layout to wide
st.set_page_config(layout="wide")

# Insert Centered Title Image
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')
with col2:
    st.image("ejpic.jpg", use_column_width=True, caption='“The fight for environmental justice is a fight for your life." - Image by Wake Forest University')
with col3:
    st.write(' ')

# Title + Descriptions; Used HTML/CSS for additional customization; I wanted specific colors, margin to reduce white space and saw most customization through this
st.markdown("<p style='text-align: center; font-size: 16px; margin-bottom: -10px; color: grey;'>PUBLISHED DEC. 10, 2023, AT 12:00 AM</p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 50px; margin-top: -20px; margin-bottom: -20px;'>North Carolina Equity Atlas: Race and Risk Mapping</h1>", unsafe_allow_html=True)

# Small Blurb Text
st.markdown("""
    <div style="text-align: justify; font-size: 18px; max-width: 800px; margin: auto;">
        Explore the intersection of race and environmental justice in North Carolina with this Streamlit Application.
    </div>
    """, unsafe_allow_html=True)

# LinkedIn + GitHub Link
st.markdown("""
    <p style='text-align: center; font-size: 16px; color: grey; margin-top: 5px; margin-bottom: 5px;'>
        By <a href="https://www.linkedin.com/in/riley-leprell/" style="color: grey; text-decoration: underline; text-decoration-color: black; text-decoration-thickness: 2px;">Riley LePrell</a>
    </p>
    <p style='text-align: center; font-size: 16px; margin-top: 5px; color: grey;'>
        Get Data on <a href="https://github.com/RileyLePrell/ejrace" style="color: grey; text-decoration: underline; text-decoration-color: black; text-decoration-thickness: 2px;">Github</a>
    </p>
    """, unsafe_allow_html=True)

# Bottom dotted separator
st.markdown("""<hr style="border-top: 1px dotted #8c8b8b; max-width: 800px; margin-left: auto; margin-right: auto; margin-top: -5px;">""", unsafe_allow_html=True)

# Additional Text with Embedded Link
st.markdown("""
    <div style="text-align: justify; font-size: 18px; max-width: 800px; margin: auto;">
        In the shadow of North Carolina's sprawling hog farms, communities grapple with the toxic legacy of environmental injustice, where the burden of agricultural pollution falls heaviest on those least able to bear it. This issue is particularly burdensome in Eastern North Carolina, where since the 1980s, industrial pork production has exploded in minority-dominated areas. The use of open-air feces lagoons and sprayers for animal waste has inflicted serious environmental harm, leading to contaminated wells, reduced property values, and various <a href="https://www.vox.com/future-perfect/23003487/north-carolina-hog-pork-bacon-farms-environmental-racism-black-residents-pollution-meat-industry">health issues</a>.
    </div>
    """, unsafe_allow_html=True)

# YouTube Video for Hog Farm Index
st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center; margin-top: 20px;'>
        <div style='border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); overflow: hidden; max-width: 480px;'>
            <iframe width="480" height="270" src="https://www.youtube.com/embed/ZgonVE-atgQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Caption for the Second Video
st.markdown("""
    <div style="text-align: center; font-size: 14px; margin-top: 10px; margin-bottom: 20px; color: grey;">
        Courtesy of The Smell of Money/Shawn Bannon
    </div>
    """, unsafe_allow_html=True)

# Additional Text
st.markdown("""
<div style="text-align: justify; font-size: 18px; max-width: 800px; margin: auto;">
    "Environmental Justice seeks equitable environmental protection for all communities, while environmental injustice occurs when minority and low-income areas disproportionately suffer from  <a href="https://www.atsdr.cdc.gov/placeandhealth/eji/index.html">environmental hazards</a>". A prime example of this can be seen in the text/video above about hog farms in North Carolina.
    <br><br>
    This Streamlit Application investigates the distribution of race across North Carolina's counties. As seen below, users can explore two maps: the left map illustrates the racial distribution in counties alongside levels of environmental injustice risk, while the right map focuses on the racial distribution in each county. Additionally, bar graphs below these maps further detail racial percentages, highlighting the link between environmental injustice and race. Please use the dropdown menus on the side to select different counties and EJ Concern Levels. Notice how in a majority of the counties as Environmental Injustice Concern Level rises so does the % minority. 
</div>
""", unsafe_allow_html=True)

# Caching data
@st.cache_data
def load_csv_SPEEDY(file_path):
    return pd.read_csv(file_path)

# Loading EJ_CSV Data w/ cache
df = load_csv_SPEEDY('ej_nc.csv')

# Defining EJI Risk Categories & Ranges
eji_categories = {
    'Minor': (0, 0.25),
    'Moderate': (0.25, 0.5),
    'Major': (0.5, 0.75),
    'Severe': (0.75, 1)
}

# Assigning Custom Colors for Each Race
colors = {
    'white': '#ffb262',
    'black': '#129e56',
    'latino': '#7570b3',
    'asian': '#e7298a',
    'other': '#43a8b5'
}

# Creating Labels for Legend below Title
legend_labels = {'white': 'White', 'black': 'Black', 'latino': 'Latino', 'asian': 'Asian', 'other': 'Other'}

# Function that displays % by Race from any Data Source
def calculate_demographics(data):
    sums = data[['white', 'black', 'asian', 'latino', 'other']].sum()  # Sum for Each Race
    total = sums.sum()  # Total Sum
    return (sums / total * 100).to_dict()

# Function that Calculates the % for each Race within a specific EJI Category in a County
def calculate_eji_demographics(data, eji_range):
    filtered_data = data[(data['RPL_EJI'] >= eji_range[0]) & (data['RPL_EJI'] < eji_range[1])]
    return calculate_demographics(filtered_data)

# Function to Create a Stacked Bar Chart of Racial %'s
def create_demographic_bar_chart(data, title, legend_labels, display_legend=False):
    fig = go.Figure()

    # Some County + EJI Combos = No Census Tracts For that Combo
    # This Runs an If Statement so when there are population values it makes a bar and when not, displays some text explaining that.
    if data and not all(value == 0 for value in data.values()):
        annotations = []
        cumulative_percent = 0

        # Bar Chart + Hover Functionality
        for i, (category, percentage) in enumerate(data.items()):
            fig.add_trace(go.Bar(
                x=[percentage],
                y=['Demographics'],
                name=legend_labels[category],
                orientation='h',
                marker=dict(color=colors[category]),
                hoverinfo='text',
                hovertext=f"{category.capitalize()}: {percentage:.1f}%"
            ))

            # Wanted %'s to show below bar chart, but felt cluttered when low values near each other
            # Set the %'s to only show above 7 felt like >7% looked more aesthetically pleasing.
            if percentage > 7:
                position = cumulative_percent + (percentage / 2)
                cumulative_percent += percentage
                annotations.append(dict(
                    x=position,
                    y=-0.1,
                    text=f"{legend_labels[category]}: {percentage:.1f}%",
                    showarrow=False,
                    font=dict(size=12),
                    xref="x",
                    yref="paper"
                ))
       
        # Making Bars Stacked; I saw a stacked bar chart on another website and looked cooler imo
        fig.update_layout(
            barmode='stack',
            title=title,
            title_x=.5,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=annotations,
            showlegend=False,
            height=300  
        )

    # Text explaining that there are none of the selected EJI in the county.
    else:
        fig.add_annotation(text="There is no population for the selected County/EJI Concern Combination",
                           xref="paper", yref="paper",
                           x=position, y=-.1, showarrow=False,
                           font=dict(size=16))
    return fig

# Grab Unique County/State Abbr Combo from the ej_nc df
county_info = df[['COUNTY', 'StateAbbr']].drop_duplicates()

# Title + Warning
st.sidebar.markdown("## 🌍 Select a County/EJ Concern Level")
st.sidebar.markdown("**Please be patient: maps take a few seconds to load.** ⏳")

# Select County Title + There was a lot of White Space so made the reduced it be 50px + Selectbox + Explanation
st.sidebar.markdown("### ")
st.sidebar.markdown('<style>div.row-widget.stSelectbox{margin-top:-50px;}</style>', unsafe_allow_html=True)

# Convert the DataFrame to a list of dictionaries
county_list = county_info[['COUNTY', 'StateAbbr']].to_dict('records')

# Use the list of dictionaries in the selectbox
selected_county_info = st.sidebar.selectbox(
    'Select a County', 
    county_list, 
    format_func=lambda x: x['COUNTY']
)

# Assign selected COUNTY and StateAbbr to variables
selected_county = selected_county_info['COUNTY']
selected_state_abbr = selected_county_info['StateAbbr']

st.sidebar.markdown("Choose any county in North Carolina. Expansion to other states planned for the future.")

# Select EJI Concern Level Title + Reduction in the White Space + Selectbox + Explanation
st.sidebar.markdown("### **Select an Environmental Injustice Concern Level**")
st.sidebar.markdown('<style>div.row-widget.stSelectbox{margin-top:-50px;}</style>', unsafe_allow_html=True)
selected_eji_category = st.sidebar.selectbox(' ', list(eji_categories.keys()))
st.sidebar.markdown("Based on the CDC EJI Index, which combines 36 health, social, and environmental indicators to assign an environmental justice score for each census tract from 0-1. The index helps identify and prioritize vulnerable areas. Concern levels are divided into quartiles: Minor (0-0.25), Moderate (0.25-0.5), Major (0.5-0.75), and Severe (0.75-1).")

# County Level is Filtered and its Racial Percentages are Determined
county_data = df[df['COUNTY'] == selected_county]  # Only Grab ej_nc county data when county name = selected county name
overall_demographics = calculate_demographics(county_data)  # Use calculate_demographics Function to determine county racial %'s
eji_demographics = calculate_eji_demographics(county_data, eji_categories[selected_eji_category])  # Same as above but + EJI Racial %'s

# Set Caches for Shapefile
@st.cache_data
def load_shapefile_nc_dots():
    return gpd.read_file('Shapefiles/nc_dots.shp')

@st.cache_data
def load_shapefile_tracts():
    return gpd.read_file('Shapefiles/tl_2018_37_tract.shp')

@st.cache_data
def load_shapefile_county_boundaries():
    return gpd.read_file('Shapefiles/County_Boundaries.shp')

@st.cache_data
def load_shapefile_state_boundaries():
    return gpd.read_file('Shapefiles/State_Boundaries.shp')

# Load shapefiles
nc_dots_gdf = load_shapefile_nc_dots()
tracts_gdf = load_shapefile_tracts()
county_boundaries_gdf = load_shapefile_county_boundaries()
state_boundaries_gdf = load_shapefile_state_boundaries()

# The INTPTLON Has a Leading 0 That Needed to be Removed
tracts_gdf['INTPTLON'] = tracts_gdf['INTPTLON'].apply(lambda x: x.lstrip('0'))

# Merge the Dot Density + Tracts Data; nc_dots_gdf eji_rank_3 links with tracts_gdf GEOID
merged_gdf = nc_dots_gdf.merge(tracts_gdf[['GEOID', 'INTPTLAT', 'INTPTLON']], left_on='eji_rank_3', right_on='GEOID')

# Lon/Lat Changing from Text to Float and removing leading + from lon
merged_gdf['INTPTLAT'] = merged_gdf['INTPTLAT'].astype(float)
merged_gdf['INTPTLON'] = merged_gdf['INTPTLON'].apply(lambda x: float(x.replace('+', '')))

# Grab boundaries from county + state shapefiles; NC's StateFP is always 37 & have county_boundary to be whatever selected county is  
selected_county_boundary = county_boundaries_gdf[(county_boundaries_gdf['NAME'] == selected_county) & (county_boundaries_gdf['STATEFP'] == '37')]
nc_state_boundary = state_boundaries_gdf[state_boundaries_gdf['STATEFP'] == "37"]

# Set Colors for Dot Density Mapping They Match the Colors Above
racial_colors = {
    'white': [255, 178, 98],
    'black': [18, 158, 86],
    'latino': [117, 112, 179],
    'asian': [231, 41, 138],
    'other': [67, 168, 181]
}

# Grabbing Population Totals for Races
racial_totals_mapping = {
    'white': 'census_r_3',
    'black': 'census_r_4',
    'latino': 'census_r_6',
    'asian': 'census_r_5',
    'other': 'census_r_7'
}

# Function to generate random points within a polygon
def create_random_points_within_polygon(polygon, num_points):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if polygon.contains(random_point):
            points.append(random_point)
    return points

# Function to create a PyDeck map layer for dot density
def create_dot_density_layer(gdf, racial_total_columns, people_per_dot=25):  # 25 seems like a good balance for rural/urban
    layers = []
    for race, color in racial_colors.items():
        # Calculate the number of dots to represent the population
        gdf[race + '_dots'] = (gdf[racial_total_columns[race]] / people_per_dot).round().astype(int)
       
        for _, row in gdf.iterrows():
            # Get the geometry of the tract
            tract_id = row['eji_rank_3']
            tract_geometry = tracts_gdf[tracts_gdf['GEOID'] == tract_id].geometry.iloc[0]
           
            # Generate random points within the tract geometry
            num_dots = row[race + '_dots']
            random_points = create_random_points_within_polygon(tract_geometry, num_dots)
           
            # Prepare the data for the layer
            layer_data = [{'position': [point.x, point.y], 'race': race} for point in random_points]

            # Create the layer
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=layer_data,
                get_position='position',
                get_color=color,
                get_radius=125,  # adjust size of dots
            )
            layers.append(layer)
    return layers

# Function to create an outline of selected county
def create_county_outline_layer(gdf):
    return pdk.Layer(
        "GeoJsonLayer",
        data=gdf,
        get_fill_color=[0, 0, 0, 20],  
        get_line_color=[0, 0, 0, 150],  
        pickable=True,
        stroked=True,
        filled=True,
        extruded=True,
        line_width_min_pixels=1,
    )

# Function for displaying racial 4 county 
@st.cache_data
def create_overall_county_layer(selected_county):
    overall_county_gdf = merged_gdf[merged_gdf['eji_rank_5'] == selected_county]
    return create_dot_density_layer(overall_county_gdf, racial_totals_mapping)

# Get centroid coordinates of the selected county
selected_county_data = county_boundaries_gdf[(county_boundaries_gdf['NAME'] == selected_county) & (county_boundaries_gdf['STATEFP'] == '37')]
centroid_lat, centroid_lon = 0, 0
if not selected_county_data.empty:
    centroid_lat = selected_county_data.iloc[0]['INTPTLAT']
    centroid_lon = selected_county_data.iloc[0]['INTPTLON']

# Center View Around Selected County
initial_view_state = pdk.ViewState(
    latitude=float(centroid_lat),
    longitude=float(centroid_lon),
    zoom=9  # Nine seemed like a good balance for zoom level
)

# Display the main title and legend
st.markdown(f"<h1 style='text-align: center;'>{selected_county}, {selected_state_abbr}</h1>", unsafe_allow_html=True)
legend_html = "<div style='text-align: center; margin-bottom: 20px;'>"
for category in colors:
    legend_html += f"<span style='display: inline-block; margin-right: 10px;'>"
    legend_html += f"<span style='background: {colors[category]}; width: 15px; height: 15px; display: inline-block;'></span>"
    legend_html += f" {legend_labels[category]}</span>"
legend_html += "</div>"
st.markdown(legend_html, unsafe_allow_html=True)

# Map in Columns; lets them be side by side
col1, col2 = st.columns(2)

with col1:
    # Dot density map for the selected EJI category within the selected county
    st.markdown(f"<h3 style='text-align: center;'>{selected_county} {selected_eji_category} EJ Risk</h3>", unsafe_allow_html=True)
    selected_eji_gdf = merged_gdf[(merged_gdf['eji_ran_13'] >= eji_categories[selected_eji_category][0]) &
                                  (merged_gdf['eji_ran_13'] < eji_categories[selected_eji_category][1])]  # Filter for EJI_Categories 
    selected_eji_gdf = selected_eji_gdf[selected_eji_gdf.within(selected_county_boundary.geometry.unary_union)]
    eji_layers = create_dot_density_layer(selected_eji_gdf, racial_totals_mapping)
    county_outline_layer = create_county_outline_layer(selected_county_boundary)
    map1 = pdk.Deck(
        layers=eji_layers + [county_outline_layer],
         initial_view_state=initial_view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    )
    st.pydeck_chart(map1, use_container_width=True)

# Main code
with col2:
    # Dot density map for the overall county (not considering EJI category)
    st.markdown(f"<h3 style='text-align: center;'>{selected_county} EJ Risk</h3>", unsafe_allow_html=True)
    overall_layers = create_overall_county_layer(selected_county)
    map2 = pdk.Deck(
        layers=overall_layers + [county_outline_layer],
        initial_view_state=initial_view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    )
    st.pydeck_chart(map2, use_container_width=True)

# Bar Charts in Columns
col1, col2 = st.columns(2)

with col1:
    eji_fig = create_demographic_bar_chart(eji_demographics, '', legend_labels, display_legend=False)
    st.plotly_chart(eji_fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    overall_fig = create_demographic_bar_chart(overall_demographics, '', legend_labels)
    st.plotly_chart(overall_fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
    <div style="text-align: justify; font-size: 18px; max-width: 800px; margin: auto;">
        Please Note Some County + EJ Concern Combos Result with 0 Selected Census Tracts
    </div>
    """, unsafe_allow_html=True)
