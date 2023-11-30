import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Set the page layout to wide
st.set_page_config(layout="wide")

# Load the data
df = pd.read_csv('ej_nc.csv')

# Define the RPL_EJI categories and their corresponding numerical ranges
eji_categories = {
    'Low': (0, 0.25),
    'Low/Moderate': (0.25, 0.5),
    'Moderate/High': (0.5, 0.75),
    'High': (0.75, 1)
}

# Function to calculate percentages for each demographic within a county
def calculate_demographics(data):
    sums = data[['white', 'black', 'asian', 'latino', 'other']].sum()
    total = sums.sum()
    return (sums / total * 100).to_dict()

# Function to calculate percentages for each demographic within each EJI category in a county
def calculate_eji_demographics(data, eji_range):
    filtered_data = data[(data['RPL_EJI'] >= eji_range[0]) & (data['RPL_EJI'] < eji_range[1])]
    return calculate_demographics(filtered_data)

# Custom colors for each demographic
colors = {
    'white': '#ffb262',
    'black': '#129e56',
    'latino': '#7570b3',
    'asian': '#e7298a',
    'other': '#43a8b5'
}

# Plotting function for demographic data
def create_demographic_bar_chart(data, title, legend_labels, display_legend=False):
    fig = go.Figure()
    annotations = []
    for i, (category, percentage) in enumerate(data.items()):
        fig.add_trace(go.Bar(
            x=[percentage],
            y=['Demographics'],
            name=legend_labels[category],
            orientation='h',
            marker=dict(color=colors[category]),
            text='',
            hoverinfo='none'
        ))
        # Add annotations below the bar
        annotations.append(dict(
            x=sum(list(data.values())[:i+1]) - (percentage/2),  # Position at the center of each segment
            y=-.5,  # Slightly below the bar
            text=f"{percentage:.1f}%",
            showarrow=False,
            font=dict(color="Black")
        ))
    
    fig.update_layout(
        barmode='stack',
        title=title,
        title_x=0.5,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 100]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        annotations=annotations,
        showlegend=display_legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=300  # Fixed height for a 1:5 aspect ratio
    )
    return fig

# Get unique county names for dropdown
county_info = df[['COUNTY', 'StateAbbr']].drop_duplicates()

# Sidebar for county selection
selected_county_info = st.sidebar.selectbox('Select a COUNTY', county_info.itertuples(index=False), format_func=lambda x: x.COUNTY)
selected_county, selected_state_abbr = selected_county_info.COUNTY, selected_county_info.StateAbbr

# Sidebar for EJI category selection
selected_eji_category = st.sidebar.selectbox('Select an EJI Category', list(eji_categories.keys()))

# Filter data for selected county
county_data = df[df['COUNTY'] == selected_county]

# Calculate overall demographics for the selected county
overall_demographics = calculate_demographics(county_data)

# Calculate demographics for the selected EJI category within the selected county
eji_demographics = calculate_eji_demographics(county_data, eji_categories[selected_eji_category])

# Set legend labels for the bar charts
legend_labels = {'white': 'White', 'black': 'Black', 'latino': 'Latino', 'asian': 'Asian', 'other': 'Other'}

# Display the main title centered at the top using HTML and CSS
st.markdown(f"<h1 style='text-align: center;'>{selected_county}, {selected_state_abbr}</h1>", unsafe_allow_html=True)

# Display the legend directly below the main title using similar HTML and CSS styling
legend_html = "<div style='text-align: center; margin-bottom: 20px;'>"
for category in colors:
    legend_html += f"<span style='display: inline-block; margin-right: 10px;'>"
    legend_html += f"<span style='background: {colors[category]}; width: 15px; height: 15px; display: inline-block;'></span>"
    legend_html += f" {legend_labels[category]}</span>"
legend_html += "</div>"
st.markdown(legend_html, unsafe_allow_html=True)

# Create a two-column layout for side-by-side bar charts
col1, col2 = st.columns(2)

with col1:
    # Use Markdown with unsafe_allow_html to allow HTML content
    st.markdown("<h3 style='text-align: center;'>Alamance Low EJ Risk</h3>", unsafe_allow_html=True)
    eji_fig = create_demographic_bar_chart(eji_demographics, '', legend_labels, display_legend=False)
    st.plotly_chart(eji_fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    # Use Markdown with unsafe_allow_html to allow HTML content
    st.markdown("<h3 style='text-align: center;'>Alamance Surrounding Area</h3>", unsafe_allow_html=True)
    overall_fig = create_demographic_bar_chart(overall_demographics, '', legend_labels)
    st.plotly_chart(overall_fig, use_container_width=True, config={'displayModeBar': False})