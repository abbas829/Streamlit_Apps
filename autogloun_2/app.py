import streamlit as st
import pandas as pd
from autogluon.tabular import TabularPredictor

# App Configuration
st.set_page_config(
    page_title="Kaggle AutoGluon Trainer & Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "## Kaggle AutoGluon Trainer\nTrain and analyze models using AutoGluon with ease."
    }
)

# Sidebar Options
st.sidebar.header("App Options")
task_type = st.sidebar.selectbox("Select Task Type", ["Tabular"])
time_limit = st.sidebar.selectbox("Set Time Limit", ["Auto", "Custom"])
custom_time_limit = st.sidebar.slider("Custom Time Limit (seconds)", 60, 3600, 600)
time_limit = None if time_limit == "Auto" else custom_time_limit
target_column = st.sidebar.text_input("Target Column Name", value="target")

# File Uploads
st.sidebar.header("Upload Files")
train_file = st.sidebar.file_uploader("Upload Training File (CSV)", type="csv")
test_file = st.sidebar.file_uploader("Upload Test File (CSV)", type="csv")
sample_file = st.sidebar.file_uploader("Upload Sample Submission File (CSV)", type="csv")

# Header
st.title("Kaggle AutoGluon Trainer & Analyzer")
st.markdown("""
This app allows you to:
- Train models using [AutoGluon](https://autogluon.mxnet.io/).
- Automatically generate submission files for Kaggle competitions.
- Analyze model performance and preprocessing steps.
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
    if train_data is None or test_data is None:
        st.error("Please upload the required files!")
    else:
        try:
            st.info("Starting AutoGluon Training...")
            
            # Tabular Predictor
            predictor = TabularPredictor(label=target_column, path="ag_models").fit(
                train_data=train_data, 
                time_limit=time_limit
            )
            
            st.success("Training completed successfully!")
            
            # Generate Predictions
            st.info("Generating predictions...")
            predictions = predictor.predict(test_data)
            
            # Align with Sample Submission Format
            predictions.reset_index(drop=True, inplace=True)
            if sample_data is not None:
                submission = sample_data.copy()
                submission.iloc[:, -1] = predictions.values
            else:
                submission = pd.DataFrame(predictions, columns=[target_column])
            
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
            
            # Training Summary
            st.header("Training Summary")
            leaderboard = predictor.leaderboard(silent=True)
            st.dataframe(leaderboard)
            st.json(predictor.info())
            
            # Best Practices and Critical Analysis
            st.header("Critical Analysis of AutoGluon Training Process")
            st.markdown("""
            ### AutoGluon's Approach to Training
            AutoGluon employs a robust and automated pipeline that includes:
            - **Preprocessing**: Handles missing values, categorical encoding, and feature scaling automatically.
            - **Model Selection**: Trains multiple models and ensembles them for enhanced robustness.
            - **Hyperparameter Optimization**: Dynamically tunes hyperparameters based on dataset characteristics.

            ### Strengths
            - **Automation**: Reduces the need for manual intervention.
            - **Ensemble Strength**: Consistently outperforms individual models.
            - **Efficiency**: Optimizes for time and resource constraints.

            ### Weaknesses
            - **Resource Intensive**: High computational requirements for complex ensembles.
            - **Limited Interpretability**: Difficult to explain individual predictions.
            - **Overfitting Risk**: Small datasets or high dimensionality can lead to overfitting.

            ### Recommendations
            1. **Imputation**: Ensure domain-specific alignment in missing value handling.
            2. **Feature Engineering**: Complement AutoGluon's pipeline with domain-specific transformations.
            3. **Hyperparameter Tuning**:
               - Experiment with `num_bagging_folds` and `stack_ensemble_levels`.
               - Optimize `time_limit` for resource balance.
            4. **Validation**: Use external validation sets to monitor overfitting.
            5. **Dataset Scaling**: Standardize numerical features if they vary significantly.

            ### Observed Performance Metrics
            - Leaderboard rankings provide a detailed comparison of models.
            - Feature importance insights help in understanding prediction drivers.
            """)
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
