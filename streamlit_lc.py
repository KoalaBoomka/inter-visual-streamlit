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
st.set_page_config(page_title="MPG Explorer", page_icon="🚗", layout="wide")


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
    ax.scatter(df['displ'], df['hwy'], alpha=0.7, color='#DA70D6')
    
    if show_means == 'Yes':
        ax.scatter(means['displ'], means['hwy'], alpha=0.7, color='#7FFF00', s=100)
    
    ax.set_title('Engine Size vs Highway Fuel Mileage')
    ax.set_xlabel('Displacement (Liters)')
    ax.set_ylabel('Highway MPG')
    return fig


def create_plotly_plot(df, means, show_means):
    """Create Plotly scatter plot."""
    fig = px.scatter(df, x='displ', y='hwy', opacity=0.7,
                     range_x=[1, 8], range_y=[10, 50],
                     width=750, height=800,
                     labels={"displ": "Displacement (Liters)", "hwy": "Highway MPG"},
                     title="Engine Size vs Highway Fuel Mileage",
                     color_discrete_sequence=['#DA70D6'])
    
    if show_means == "Yes":
        fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'], 
                                 mode="markers",
                                 marker=dict(color='#7FFF00', size=10)))
        fig.update_layout(showlegend=False)
    
    return fig


# Main app
st.title('🚗 MPG Data Explorer')

# Load data
mpg_df = load_data('data/mpg.csv')

# Show dataset option
with st.expander("View Dataset"):
    st.dataframe(mpg_df)

# Controls
col1, col2, col3 = st.columns([3, 1, 1])

years = ['All'] + sorted(mpg_df['year'].unique().tolist())
year = col1.selectbox('Choose a year', years)
show_means = col2.radio('Show means', ['No', 'Yes'], index=1)
plot_type = col3.radio("Plot type", ["Plotly", "Matplotlib"])

# Filter data
filtered_df = mpg_df if year == 'All' else mpg_df[mpg_df['year'] == year]
means = filtered_df.groupby('class').mean(numeric_only=True)

# Display plot
if plot_type == "Matplotlib":
    st.pyplot(create_matplotlib_plot(filtered_df, means, show_means), use_container_width=False)
else:
    st.plotly_chart(create_plotly_plot(filtered_df, means, show_means))

# Footer
st.caption("Data: [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/auto+mpg)")

# Map demo
st.subheader("Map Demo")
ds_geo = px.data.carshare()
ds_geo[['lat', 'lon']] = ds_geo[['centroid_lat', 'centroid_lon']]
ds_geo['color'] = '#DA70D6'
st.map(ds_geo, color='color')