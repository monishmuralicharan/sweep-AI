import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import pointbiserialr
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

openai.api_key = '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';

# Function to process the uploaded file and interact with OpenAI's API
def analyze_uploaded_file(text):
    # Assuming the file is a text file. Adjust accordingly for other types.
    try:

        scrap_column_name = 'IsScrap'
        correlations = []
        all_columns = df.columns.to_list()
        for column in all_columns:
            if column == scrap_column_name:
                all_columns.remove(column)
                break
        for i in range(len(all_columns)):
            if all_columns[i] == scrap_column_name:
                continue
            scatter_x = df[all_columns[i]].values.astype(float)
            scatter_y = df[scrap_column_name].values.astype(float)
            corr, p = pointbiserialr(scatter_x, scatter_y)
            correlations.append(round(corr * 100, 2))

        combined = list(zip(all_columns, correlations))
        sorted_combined = sorted(combined, key=lambda x: x[1])
        all_columns, correlations = zip(*sorted_combined)
        input_columns = ""
        for i in range(len(all_columns)):
            input_columns += str(all_columns[i]) + ":" + str(correlations[i]) + ","


        # Crafting a prompt for the OpenAI model to analyze the causes of scrap from the content
        prompt_text = f"Take the following list of names of columns and their corresponding coefficients (take absolute values) and find the top 3." + input_columns + " Give actionable steps on how to minimize scrap because of these columns in a manufacturing facility in this format: Column 1: 'name of column'\n 1. 'actionable step 1'\n 2. 'actionable step 2'\n 3. 'actionable step 3'\n complete these for the next 3 columns"
        system_prompt = f"You give suggestions for how to reduce scrap in a manufacturing facility given the factors."

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)  # For debugging purposes


def csv_to_text(df):
    text_columns = []

    for column in df.columns:
        # Ensure each cell value is converted to string to prevent type errors
        column_values_as_str = map(str, df[column].values)
        column_text = " | ".join(column_values_as_str)
        # Explicitly convert column name to string to ensure compatibility
        column_name_as_str = str(column)
        text_columns.append(column_name_as_str + ":\n" + column_text + "\n")

    full_text = "\n".join(text_columns)
    return full_text


st.set_page_config(layout='wide')
st.title('Sweep AI')
st.subheader('Upload a CSV file to analyze its contents')

file = st.file_uploader('Upload CSV', type=['csv'])

if file is not None:

    df = pd.read_csv(file)
    df.columns = df.iloc[0]
    df = df[1:]

    st.write('**CSV file contents:**')
    st.write(df)

    st.markdown('---')

    parsed_text = csv_to_text(df)
    final_text = analyze_uploaded_file(parsed_text)

    st.subheader('Analytics')

    scrap_column_name = 'IsScrap'
    correlations = []
    all_columns = df.columns.to_list()
    for column in all_columns:
        if column == scrap_column_name:
            all_columns.remove(column)
            break
    for i in range(len(all_columns)):
        if all_columns[i] == scrap_column_name:
            continue
        scatter_x = df[all_columns[i]].values.astype(float)
        scatter_y = df[scrap_column_name].values.astype(float)
        corr, p = pointbiserialr(scatter_x, scatter_y)
        correlations.append(round(corr*100, 2))

    combined = list(zip(all_columns, correlations))
    sorted_combined = sorted(combined, key=lambda x: x[1])
    all_columns, correlations = zip(*sorted_combined)

    best_columns = all_columns
    best_correlations = correlations
    best_correlations = [abs(value) for value in best_correlations]

    best_combined = list(zip(best_columns, best_correlations))
    best_sorted_combined = sorted(best_combined, key=lambda x: x[1], reverse=True)
    best_columns, best_correlations = zip(*best_sorted_combined)

    best_columns = best_columns[:3]
    best_correlations = best_correlations[:3]

    st.write('**Columns vs Correlations**')
    categories = ['A', 'B', 'C', 'D']
    values = [20, 30, 15, 35]
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=all_columns, y=correlations))
    fig_bar.update_layout(
        xaxis_title='Dataset Columns',
        yaxis_title='Point Biserial Correlation (%)',
        template='plotly_white',
        hovermode='x',
        margin=dict(l=40, r=40, t=40, b=40),
        width=400,
        height=300,
    )
    st.plotly_chart(fig_bar, use_container_width=True, align="center")

    st.markdown('---')

    scatter_x = df[best_columns[0]].values.astype(float)
    scatter_y = df[scrap_column_name].values.astype(float)
    col1, col2 = st.columns(2)
    with col1:
        st.write(f'**{best_columns[0]}**')
        corr, p = pointbiserialr(scatter_x, scatter_y)
        st.write(f'**Correlation: {round(corr * 100, 2)}%**')
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(x=scatter_x, y=scatter_y, mode='markers'))
        fig_scatter.update_layout(
            xaxis_title=best_columns[0],
            yaxis_title=scrap_column_name,
            template='plotly_white',
            hovermode='closest',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_scatter, use_container_width=True, align="center")

    scatter_x = df[best_columns[1]].values.astype(float)
    with col2:
        st.write(f'**{best_columns[1]}**')
        corr, p = pointbiserialr(scatter_x, scatter_y)
        st.write(f'**Correlation: {round(corr * 100, 2)}%**')
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(x=scatter_x, y=scatter_y, mode='markers'))
        fig_scatter.update_layout(
            xaxis_title=best_columns[1],
            yaxis_title=scrap_column_name,
            template='plotly_white',
            hovermode='closest',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_scatter, use_container_width=True, align="center")

    scatter_x = df[best_columns[2]].values.astype(float)
    scatter_y = df[scrap_column_name].values.astype(float)
    col3, col4 = st.columns(2)
    with col3:
        st.write(f'**{best_columns[2]}**')
        corr, p = pointbiserialr(scatter_x, scatter_y)
        st.write(f'**Correlation: {round(corr * 100, 2)}%**')
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(x=scatter_x, y=scatter_y, mode='markers'))
        fig_scatter.update_layout(
            xaxis_title=best_columns[2],
            yaxis_title=scrap_column_name,
            template='plotly_white',
            hovermode='closest',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_scatter, use_container_width=True, align="center")

    scatter_x = df[best_columns[1]].values.astype(float)
    scatter_y_bool = [bool(int(val)) for val in scatter_y]
    scrap_count = 0
    non_scrap_count = 0
    for bool_val in scatter_y_bool:
        if bool_val:
            scrap_count += 1
        else:
            non_scrap_count += 1
    scatter_x_bool = [non_scrap_count, scrap_count]
    scatter_y_bool = [False, True]
    with col4:
        st.write(f'**Overall data division:**')
        fig_pie = go.Figure()
        # fig_pie.add_trace(go.Pie(labels=scatter_y, values=scatter_x))
        fig_pie.add_trace(go.Pie(labels=['Non-Scrap', 'Scrap'], values=scatter_x_bool, customdata=scatter_y_bool))
        fig_pie.update_layout(
            template='plotly_white',
            margin=dict(l=40, r=40, t=40, b=40),
            width=400,
            height=300,
        )
        st.plotly_chart(fig_pie, use_container_width=True, align="center")

    st.markdown('---')

    # # Line plot
    # with col1:
    #     st.write('**Interactive Line Plot**')
    #     x = np.linspace(0, 10, 100)
    #     y = np.sin(x)
    #     fig_line = go.Figure()
    #     fig_line.add_trace(go.Scatter(x=x, y=y, mode='lines'))
    #     fig_line.update_layout(
    #         xaxis_title='X-axis',
    #         yaxis_title='Y-axis',
    #         template='plotly_white',
    #         hovermode='x',
    #         margin=dict(l=40, r=40, t=40, b=40),
    #         width=400,
    #         height=300,
    #     )
    #     st.plotly_chart(fig_line, use_container_width=True, align="center")
    #
    # # Bar graph
    # with col2:
    #     st.write('**Bar Graph**')
    #     categories = ['A', 'B', 'C', 'D']
    #     values = [20, 30, 15, 35]
    #     fig_bar = go.Figure()
    #     fig_bar.add_trace(go.Bar(x=categories, y=values))
    #     fig_bar.update_layout(
    #         xaxis_title='Categories',
    #         yaxis_title='Values',
    #         template='plotly_white',
    #         hovermode='x',
    #         margin=dict(l=40, r=40, t=40, b=40),
    #         width=400,
    #         height=300,
    #     )
    #
    #     st.plotly_chart(fig_bar, use_container_width=True, align="center")
    #
    # # Pie chart
    # col3, col4 = st.columns(2)
    # with col3:
    #     st.write('**Pie Chart**')
    #     fig_pie = go.Figure()
    #     fig_pie.add_trace(go.Pie(labels=categories, values=values))
    #     fig_pie.update_layout(
    #         template='plotly_white',
    #         margin=dict(l=40, r=40, t=40, b=40),
    #         width=400,
    #         height=300,
    #     )
    #     st.plotly_chart(fig_pie, use_container_width=True, align="center")
    #
    # # Scatter plot
    # with col4:
    #     st.write('**Scatter Plot**')
    #     scatter_x = np.random.rand(50)
    #     scatter_y = np.random.rand(50)
    #     fig_scatter = go.Figure()
    #     fig_scatter.add_trace(go.Scatter(x=scatter_x, y=scatter_y, mode='markers'))
    #     fig_scatter.update_layout(
    #         xaxis_title='X-axis',
    #         yaxis_title='Y-axis',
    #         template='plotly_white',
    #         hovermode='closest',
    #         margin=dict(l=40, r=40, t=40, b=40),
    #         width=400,
    #         height=300,
    #     )
    #     st.plotly_chart(fig_scatter, use_container_width=True, align="center")
    # st.markdown('---')

    st.subheader('Verdict (Suggestions to reduce scrap)')
    st.write(final_text)
    st.markdown('---')
    st.subheader('Premium Tier (Hardware Configuration Recommendations)')

    system_prompt = "Please take the following columns and their values. Ignore the scrap column. " + parsed_text + "Find the ideal value which is determined by rows that have a 0 in the scrap column and output the results in the following format example: OvenCNT: 79.230944, add a newline for each column and repeat for all columns"
    prompt_text = "You are a hardware configuration recommender."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ]
    )
    output = response.choices[0].message.content
    st.write(output)

    st.markdown('---')
    st.write('<div style="text-align: center;">Thank you for using <span style="font-size: 22px; font-weight: 800;">SweepAI</span>!</div>', unsafe_allow_html=True)
