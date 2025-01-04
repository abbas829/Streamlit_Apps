import streamlit as st
import pandas as pd
import os
from autogluon.tabular import TabularPredictor
from autogluon.timeseries import TimeSeriesPredictor
from autogluon.multimodal import MultiModalPredictor
import json

# App Configuration
st.set_page_config(
    page_title="Kaggle AutoGluon Submission Generator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "## Kaggle AutoGluon Submission App\nAutomatically generate submission files for Kaggle competitions!"
    }
)

# Sidebar Options
st.sidebar.header("Model Configuration")
task_type = st.sidebar.selectbox(
    "Select Task Type",
    ["Tabular", "Multimodal", "Time Series"]
)
time_limit = st.sidebar.slider("Set Time Limit (seconds)", 60, 3600, 60)
target_column = st.sidebar.text_input("Target Column Name", value="target etc.")

# File Uploads
st.sidebar.header("Upload Files")
train_file = st.sidebar.file_uploader("Upload Training File (CSV)", type="csv")
test_file = st.sidebar.file_uploader("Upload Test File (CSV)", type="csv")
sample_file = st.sidebar.file_uploader("Upload Sample Submission File (CSV)", type="csv")

# Header
st.title("Kaggle AutoGluon Submission Generator")
st.markdown("""
This app allows you to:
- Train models using [AutoGluon](https://autogluon.mxnet.io/).
- Automatically generate submission files for Kaggle competitions.
- View a summary of model performance and preprocessing steps.
""")

# Helper: Display a sample DataFrame
def display_dataframe(file, name):
    if file:
        df = pd.read_csv(file)
        st.subheader(f"{name} Data Preview")
        st.dataframe(df.head())
        return df
    else:
        st.warning(f"Please upload the {name} file.")
        return None

# Display Uploaded Data
train_data = display_dataframe(train_file, "Training")
test_data = display_dataframe(test_file, "Test")
sample_data = display_dataframe(sample_file, "Sample Submission")

# Train and Generate Predictions
if st.button("Start Training"):
    if not train_data or not test_data:
        st.error("Please upload the required files!")
    else:
        st.info(f"Task Type Selected: {task_type}")
        
        try:
            if task_type == "Tabular":
                # Tabular Predictor
                st.info("Training Tabular Model...")
                predictor = TabularPredictor(label=target_column, path="ag_models_tabular").fit(
                    train_data=train_data,
                    time_limit=time_limit
                )
            elif task_type == "Time Series":
                # Time Series Predictor
                st.info("Training Time Series Model...")
                predictor = TimeSeriesPredictor(label=target_column, path="ag_models_timeseries").fit(
                    train_data=train_data,
                    time_limit=time_limit
                )
            elif task_type == "Multimodal":
                # Multimodal Predictor
                st.info("Training Multimodal Model...")
                predictor = MultiModalPredictor(label=target_column, path="ag_models_multimodal").fit(
                    train_data=train_data,
                    time_limit=time_limit
                )
            else:
                st.error("Invalid task type selected!")

            # Generate Predictions
            st.success("Training completed successfully!")
            st.info("Generating predictions...")
            predictions = predictor.predict(test_data)
            
            # Align with Sample Submission Format
            predictions.reset_index(drop=True, inplace=True)
            if sample_data is not None:
                submission = sample_data.copy()
                submission.iloc[:, -1] = predictions.values
            else:
                submission = predictions

            # Save Predictions
            submission_file_name = "submission.csv"
            submission.to_csv(submission_file_name, index=False)
            st.success(f"Submission file '{submission_file_name}' generated successfully!")
            st.download_button(
                label="Download Submission File",
                data=open(submission_file_name, "rb"),
                file_name=submission_file_name,
                mime="text/csv"
            )

            # Summary of Training
            st.header("Training Summary")
            leaderboard = predictor.leaderboard(silent=True)
            st.dataframe(leaderboard)
            st.json(predictor.info())

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
# Footer
st.markdown("---")
st.markdown("""
**Created by Tassawar Abbas**  
- Email: [abbas829@gmail.com](mailto:abbas829@gmail.com)  
- LinkedIn: [linkedin.com/abbas829pro](https://linkedin.com/abbas829pro)  
- GitHub: [github.com/abbas829](https://github.com/abbas829)  
""")