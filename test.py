import streamlit as st
import pandas as pd
import plotly.graph_objs as go

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
def create_demographic_bar_chart(data, title, y_label):
    fig = go.Figure()
    for category, percentage in data.items():
        fig.add_trace(go.Bar(
            x=[percentage],
            y=[y_label],
            name=category.capitalize(),
            orientation='h',
            marker=dict(color=colors[category])
        ))
    
    fig.update_traces(texttemplate='%{x:.1f}%', textposition='inside')
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis=dict(range=[0, 100], showticklabels=True),
        yaxis=dict(showticklabels=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Get unique county names for dropdown
county_names = df['COUNTY'].unique()

# Sidebar for county selection
selected_county = st.sidebar.selectbox('Select a COUNTY', county_names)

# Sidebar for EJI category selection
selected_eji_category = st.sidebar.selectbox('Select an EJI Category', list(eji_categories.keys()))

# Filter data for selected county
county_data = df[df['COUNTY'] == selected_county]

# Calculate overall demographics for the selected county
overall_demographics = calculate_demographics(county_data)

# Calculate demographics for the selected EJI category within the selected county
eji_demographics = calculate_eji_demographics(county_data, eji_categories[selected_eji_category])

# Create a two-column layout
col1, col2 = st.columns(2)

# Display the overall demographics in the first column
with col1:
    overall_fig = create_demographic_bar_chart(overall_demographics, f"Demographic Distribution for {selected_county}", "Overall")
    st.plotly_chart(overall_fig, use_container_width=True)

# Display the EJI-specific demographics in the second column
with col2:
    eji_fig = create_demographic_bar_chart(eji_demographics, f"{selected_county} - {selected_eji_category} EJI Demographics", "EJI Specific")
    st.plotly_chart(eji_fig, use_container_width=True)
