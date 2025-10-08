"""
MPG Data Explorer - Interactive fuel efficiency visualization
Data source: UCI Machine Learning Repository
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Configuration
st.set_page_config(page_title="MPG Explorer", page_icon="🚗")


@st.cache_data
def load_data(path):
    """Load and cache MPG dataset."""
    df = pd.read_csv(path)
    df.index = df.index + 1
    return df


def create_matplotlib_plot(df, means, show_means):
    """Create Matplotlib scatter plot."""

    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    if st.session_state.theme == 'dark':
        plt.style.use('dark_background')
    else:
        plt.style.use('default')

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.scatter(df['displ'], df['hwy'], alpha=0.8, color='#DA70D6')
    
    if show_means == 'Yes':
        ax.scatter(means['displ'], means['hwy'], alpha=0.8, color='#7FFF00', s=100)

        for class_name, row in means.iterrows():
            ax.annotate(class_name, 
                       (row['displ'], row['hwy']),
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=10,
                       color='#7FFF00')
    
    ax.set_title('Engine Size vs Highway Fuel Mileage')
    ax.set_xlabel('Displacement (Liters)')
    ax.set_ylabel('Highway MPG')
    return fig


def create_plotly_plot(df, means, show_means):
    """Create Plotly scatter plot."""
    fig = px.scatter(df, x='displ', y='hwy', opacity=0.8,
                     range_x=[df['displ'].min() - 0.5, df['displ'].max() + 0.5],
                     range_y=[df['hwy'].min() - 2, df['hwy'].max() + 2],
                     width=750, height=800,
                     labels={"displ": "Displacement (Liters)", "hwy": "Highway MPG"},
                     title="Engine Size vs Highway Fuel Mileage",
                     color_discrete_sequence=['#DA70D6'])
    
    if show_means == "Yes":
        fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'], opacity=0.8,
                                mode="markers+text",
                                marker=dict(color='#7FFF00', size=10),
                                text=means.index,  # Class names
                                textposition="middle right",
                                textfont=dict(color='#7FFF00', size=10),
                                name="Class Means"))
        fig.update_layout(showlegend=False)
    
    return fig


# Main app
st.title('🚗 MPG Data Explorer')

st.markdown("""
**Description:**
\nThis interactive application explores the **Auto MPG dataset** from the UCI Machine Learning Repository. 
The dataset contains fuel consumption data for 398 vehicles manufactured between 1970-1982, 
including engine specifications and performance metrics.

**Key Features:**
- Compare engine displacement vs. highway fuel efficiency
- Filter data by manufacturing year
- Visualize class averages across vehicle types
- Interactive charts with Plotly and Matplotlib
""")

# Load data
mpg_df = load_data('data/mpg.csv')

# Show dataset option
with st.expander("View Dataset"):
    st.dataframe(mpg_df)

# Chart demo
st.subheader("📊 Chart Examples")

col1, col2 = st.columns([3, 1])
years = ['All'] + sorted(mpg_df['year'].unique().tolist())
year = col1.selectbox('Choose a year', years)
show_means = col2.radio('Show means', ['No', 'Yes'], index=1)

# Filter data
filtered_df = mpg_df if year == 'All' else mpg_df[mpg_df['year'] == year]
means = filtered_df.groupby('class').mean(numeric_only=True)

# Controls
tab1, tab2 = st.tabs(['Plotly', 'Matplotlib'])

with tab1: 
    st.plotly_chart(create_plotly_plot(filtered_df, means, show_means))

with tab2:
    st.pyplot(create_matplotlib_plot(filtered_df, means, show_means), use_container_width=False)


# Footer
st.caption("Data: [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/auto+mpg)")


# Map demo
st.subheader("📍 Map Demo")

ds_geo = px.data.carshare()
ds_geo = ds_geo.rename(columns={
    'centroid_lat': 'lat',
    'centroid_lon': 'lon'
    }
)

map_style_options = {
    "Dark" : "carto-darkmatter", 
    "Light" : "open-street-map", 
    "Minimalistic" : "carto-positron"
}

selected_style = st.selectbox("Select Map Style", list(map_style_options.keys()), index=0)

fig_map = px.scatter_mapbox(
    ds_geo,
    lat='lat',
    lon='lon',
    color_discrete_sequence=['#DA70D6'],  
    zoom=12,  
    height=500,
    hover_data={
        
    }
)

fig_map.update_layout(
    mapbox_style=map_style_options[selected_style],  
    margin={"r":0,"t":0,"l":0,"b":0}
    )

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>"
    "Created by Daria at the <a href='https://nexademy.org/data-science' target='_blank' style='color: #DA70D6;'>Constructor Data Science Bootcamp</a> | "
    "Built with Streamlit 💜"
    "</p>", 
    unsafe_allow_html=True
)