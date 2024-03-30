import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout='wide')
st.title('Sweep AI')
st.subheader('Upload a CSV file to analyze its contents')

file = st.file_uploader('Upload CSV', type=['csv'])

if file is not None:
    df = pd.read_csv(file)
    st.write('**CSV file contents:**')
    st.write(df)

    st.markdown('---')
    st.subheader('Analytics')

    col1, col2 = st.columns(2)

    # Line plot
    with col1:
        st.write('**Interactive Line Plot**')
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=x, y=y, mode='lines'))
        fig_line.update_layout(
            xaxis_title='X-axis',
            yaxis_title='Y-axis',
            template='plotly_white',
            hovermode='x',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_line, use_container_width=True, align="center")

    # Bar graph
    with col2:
        st.write('**Bar Graph**')
        categories = ['A', 'B', 'C', 'D']
        values = [20, 30, 15, 35]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=categories, y=values))
        fig_bar.update_layout(
            xaxis_title='Categories',
            yaxis_title='Values',
            template='plotly_white',
            hovermode='x',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_bar, use_container_width=True, align="center")

    # Pie chart
    col3, col4 = st.columns(2)
    with col3:
        st.write('**Pie Chart**')
        fig_pie = go.Figure()
        fig_pie.add_trace(go.Pie(labels=categories, values=values))
        fig_pie.update_layout(
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_pie, use_container_width=True, align="center")

    # Scatter plot
    with col4:
        st.write('**Scatter Plot**')
        scatter_x = np.random.rand(50)
        scatter_y = np.random.rand(50)
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(x=scatter_x, y=scatter_y, mode='markers'))
        fig_scatter.update_layout(
            xaxis_title='X-axis',
            yaxis_title='Y-axis',
            template='plotly_white',
            hovermode='closest',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
             height=300,
         )
        st.plotly_chart(fig_scatter, use_container_width=True, align="center")

    st.markdown('---')
    st.subheader('Verdict')
    st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed fermentum massa et sapien vehicula, sed lacinia ligula cursus. Quisque ut risus at est placerat vulputate. Nulla facilisi. Nam fringilla mi ac quam sollicitudin, nec tempor metus bibendum. Maecenas a quam velit. Donec sodales pharetra diam, sit amet malesuada magna.')

    st.markdown('---')
    st.write('<div style="text-align: center;">Thank you for using <span style="font-size: 22px; font-weight: 800;">SweepAI</span>!</div>', unsafe_allow_html=True)
