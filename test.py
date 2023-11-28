import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Directly load the data
df = pd.read_csv('ej_nc.csv')

# Define the RPL_EJI categories
eji_categories = {
    'Low': (0, 0.25),
    'Low/Moderate': (0.25, 0.5),
    'Moderate/High': (0.5, 0.75),
    'High': (0.75, 1)
}

# Function to calculate percentages for each demographic within each EJI category in a county
def calculate_eji_demographics(data, eji_range):
    filtered_data = data[(data['RPL_EJI'] >= eji_range[0]) & (data['RPL_EJI'] < eji_range[1])]
    sums = filtered_data[['white', 'black', 'asian', 'latino', 'other']].sum()
    total = sums.sum()
    percentages = {cat: sums[cat] / total * 100 for cat in ['white', 'black', 'asian', 'latino', 'other']}
    return percentages, total

# Sum the demographic data for each county
county_totals = df.groupby('COUNTY')[['white', 'black', 'asian', 'latino', 'other']].sum().reset_index()

# Calculate percentages for each demographic within each county
for category in ['white', 'black', 'asian', 'latino', 'other']:
    county_totals[f'percent_{category}'] = county_totals[category] / county_totals[['white', 'black', 'asian', 'latino', 'other']].sum(axis=1) * 100

# Get unique county names
county_names = county_totals['COUNTY'].unique()

# Sidebar for county selection
selected_county = st.sidebar.selectbox('Select a COUNTY', county_names)

# Filter data for selected county
county_data = df[df['COUNTY'] == selected_county]

# Sidebar for EJI category selection
selected_eji_category = st.sidebar.selectbox('Select an EJI Category', list(eji_categories.keys()))

# Calculate demographics for the selected EJI category within the selected county
eji_demographics, eji_total = calculate_eji_demographics(county_data, eji_categories[selected_eji_category])

# Custom colors for each demographic
colors = {
    'white': '#ffb262',
    'black': '#129e56',
    'latino': '#7570b3',
    'asian': '#e7298a',
    'other': '#43a8b5'
}

# Plotting function for the county demographics bar chart
def create_demographic_plotly_bar(data, county_name):
    fig = go.Figure()
    categories = ['white', 'black', 'asian', 'latino', 'other']
    color_values = [colors[cat] for cat in categories]

    # Add bars for each demographic
    for i, category in enumerate(categories):
        fig.add_trace(go.Bar(
            x=[data[f'percent_{category}'].iloc[0]],
            y=[county_name],
            name=category.capitalize(),
            orientation='h',
            marker=dict(
                color=color_values[i],
                line=dict(color='white', width=0)  # No border
            ),
            hoverinfo='text',
            text=f"{category.capitalize()}: {data[f'percent_{category}'].iloc[0]:.1f}%"
        ))

    # Update layout for a stacked bar chart
    fig.update_layout(
        barmode='stack',
        title={
            'text': f"<b>{county_name}</b>",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        title_font_size=22,
        height=300,  # Height of the bar
        margin=dict(l=20, r=20, t=100, b=100),  # Adjust margins to fit the legend below
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,  # Position the legend between the title and the bar
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        )
    )

    # Disable the plotly toolbar
    config = {"displayModeBar": False}

    return fig, config

# Plotting function for the EJI demographics bar chart
def create_eji_demographic_bar(demographics, total, county_name, eji_category):
    fig = go.Figure()
    categories = ['white', 'black', 'asian', 'latino', 'other']
    color_values = [colors[cat] for cat in categories]
    
    # Add bars for each demographic
    for i, category in enumerate(categories):
        # Calculate the value for each category
        value = demographics.get(category, 0) / 100 * total
        fig.add_trace(go.Bar(
            x=[value],
            y=[f"{eji_category} EJI"],
            name=category.capitalize(),
            orientation='h',
            marker=dict(
                color=color_values[i],
                line=dict(color='white', width=0)  # No border
            ),
            hoverinfo='text',
            text=f"{category.capitalize()}: {demographics.get(category, 0):.1f}%"
        ))

    # Update layout for a stacked bar chart
    fig.update_layout(
        barmode='stack',
        title={
            'text': f"<b>{county_name} - {eji_category} EJI Demographics</b>",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        title_font_size=22,
        height=300,  # Height of the bar
        margin=dict(l=20, r=20, t=100, b=100),  # Adjust margins to fit the legend below
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,  # Position the legend between the title and the bar
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        )
    )

    # Disable the plotly toolbar
    config = {"displayModeBar": False}

    return fig, config

# Display the title and the first bar chart for overall county demographics
st.title(f"Demographic Distribution for {selected_county}")
plotly_fig, config = create_demographic_plotly_bar(county_totals[county_totals['COUNTY'] == selected_county], selected_county)
st.plotly_chart(plotly_fig, use_container_width=True, config=config)

# Display the title and the second bar chart for demographics based on EJI category
st.title(f"{selected_county} - {selected_eji_category} EJI Demographics")
eji_plotly_fig, eji_config = create_eji_demographic_bar(eji_demographics, eji_total, selected_county, selected_eji_category)
st.plotly_chart(eji_plotly_fig, use_container_width=True, config=eji_config)
