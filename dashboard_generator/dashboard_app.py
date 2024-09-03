import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
        return df
    else:
        st.info("Please upload a CSV or Excel file.")
        return None

def visualize_data(df, visualizations):
    for viz in visualizations:
        visualization_type = viz["type"]
        x_axis = viz["x"]
        y_axis = viz["y"]
        color = viz["color"]
        title = viz["title"]

        if x_axis not in df.columns or y_axis not in df.columns:
            st.error(f"Selected columns '{x_axis}' or '{y_axis}' do not exist in the uploaded data.")
            continue

        st.subheader(title)

        plt.figure(figsize=(10, 6))

        if visualization_type == "Line Chart":
            sns.lineplot(data=df, x=x_axis, y=y_axis, color=color)
        elif visualization_type == "Bar Chart":
            sns.barplot(data=df, x=x_axis, y=y_axis, color=color)
        elif visualization_type == "Scatter Plot":
            sns.scatterplot(data=df, x=x_axis, y=y_axis, color=color)
        elif visualization_type == "Histogram":
            sns.histplot(df[x_axis], kde=False, color=color)

        st.pyplot(plt)
        st.write("\n")

    # Apply filters if specified
    if visualizations[0]["filter"]:
        filter_condition = visualizations[0]["filter"]
        try:
            filtered_df = df.query(filter_condition)
            st.write("Filtered Data:")
            st.dataframe(filtered_df)
        except Exception as e:
            st.error(f"Error applying filter condition: {e}")

def main():
    st.title("Dashboard Generator")

    # Sidebar for options
    st.sidebar.header("Options")
    num_charts = st.sidebar.number_input("Number of Charts", min_value=1, max_value=5, value=1, step=1)

    visualizations = []
    for i in range(num_charts):
        st.sidebar.subheader(f"Chart {i + 1} Options")
        visualization_type = st.sidebar.selectbox(f"Visualization Type {i + 1}", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"])
        uploaded_file = st.file_uploader(f"Upload a CSV or Excel file for Chart {i + 1}", key=i)
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            if df is not None:
                x_axis = st.sidebar.selectbox(f"X-Axis {i + 1}", df.columns)
                y_axis = st.sidebar.selectbox(f"Y-Axis {i + 1}", df.columns)
                color = st.sidebar.color_picker(f"Pick a Color for Chart {i + 1}", "#4CAF50")
                filter_condition = st.sidebar.text_input(f"Filter Condition for Chart {i + 1} (e.g., 'column_name > 10')")
                title = st.sidebar.text_input(f"Chart {i + 1} Title", f"Chart {i + 1}")

                visualizations.append({
                    "type": visualization_type,
                    "x": x_axis,
                    "y": y_axis,
                    "color": color,
                    "filter": filter_condition,
                    "title": title,
                })

    if len(visualizations) > 0:
        visualize_data(df, visualizations)
    else:
        st.info("Please upload a data file and configure your charts.")

if __name__ == "__main__":
    main()
