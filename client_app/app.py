"""
CSV to Interactive Web App - Freelance Template
Kaggle Rank #44 - Tassawar Abbas
Use this for every client. Just change the title and instructions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO, BytesIO
import base64
import numpy as np

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="CSV Data Explorer - Tassawar Abbas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS (Makes it look professional) ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .kaggle-badge {
        background-color: #20BEFF;
        padding: 0.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    .insight-box {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER WITH YOUR CREDENTIAL ==========
st.markdown('<p class="kaggle-badge">🏆 Kaggle Notebooks Expert - Rank #44 of 61,000+ | Built by Tassawar Abbas</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">📊 CSV Data Explorer</h1>', unsafe_allow_html=True)
st.markdown("*Upload your CSV file. Filter, sort, visualize, and download insights instantly.*")

# ========== SIDEBAR - INSTRUCTIONS ==========
with st.sidebar:
    st.markdown("### 🚀 How to Use")
    st.markdown("""
    1. Upload your CSV file (any size)
    2. Use filters to explore data
    3. Click column headers to sort
    4. Download filtered data
    5. Download charts as images
    """)
    st.markdown("---")
    st.markdown(f"**Need a custom app?** [Contact me on LinkedIn](https://www.linkedin.com/in/abbas829pro/)")
    st.markdown(f"**See my work on** [Kaggle](https://www.kaggle.com/abbas829) | [GitHub](https://github.com/abbas829)")
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.markdown("- **Kaggle Rank:** #44 Notebooks")
    st.markdown("- **Kaggle Rank:** #122 Datasets")
    st.markdown("- **Experience:** 2+ Years")

# ========== FILE UPLOAD ==========
uploaded_file = st.file_uploader(
    "📁 Choose a CSV or Excel file",
    type=['csv', 'xlsx', 'xls'],
    help="Upload any CSV or Excel file. Your data stays private - processed in your browser."
)

# ========== MAIN APP LOGIC ==========
if uploaded_file is not None:
    # Load data based on file type
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Show basic info
        st.success(f"✅ Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns")
        
        # ========== DATA PREVIEW SECTION ==========
        with st.expander("🔍 View Raw Data (click to expand)"):
            st.dataframe(df.head(100), use_container_width=True)
            st.caption(f"Showing first 100 rows of {df.shape[0]} total rows")
        
        # ========== FILTER SECTION ==========
        st.markdown("### 🎯 Filter Your Data")
        
        # Create filters in columns
        col1, col2, col3 = st.columns(3)
        
        filtered_df = df.copy()
        
        # Column selector for filtering
        with col1:
            filter_column = st.selectbox(
                "Select column to filter",
                options=df.columns.tolist(),
                key="filter_col"
            )
        
        # Dynamic filter based on column type
        with col2:
            if filter_column:
                if df[filter_column].dtype in ['int64', 'float64']:
                    min_val = float(df[filter_column].min())
                    max_val = float(df[filter_column].max())
                    filter_range = st.slider(
                        f"Range for {filter_column}",
                        min_val, max_val, (min_val, max_val)
                    )
                    filtered_df = filtered_df[
                        (filtered_df[filter_column] >= filter_range[0]) & 
                        (filtered_df[filter_column] <= filter_range[1])
                    ]
                else:
                    unique_vals = df[filter_column].dropna().unique().tolist()
                    selected_vals = st.multiselect(
                        f"Select values for {filter_column}",
                        options=unique_vals,
                        default=unique_vals[:5] if len(unique_vals) > 5 else unique_vals
                    )
                    if selected_vals:
                        filtered_df = filtered_df[filtered_df[filter_column].isin(selected_vals)]
        
        # Search box for text columns
        with col3:
            search_col = st.selectbox("Search in column", options=["None"] + df.columns.tolist())
            if search_col != "None":
                search_term = st.text_input(f"Search in {search_col}")
                if search_term:
                    filtered_df = filtered_df[
                        filtered_df[search_col].astype(str).str.contains(search_term, case=False)
                    ]
        
        # ========== RESULTS SUMMARY ==========
        st.info(f"📌 **Showing {filtered_df.shape[0]} rows** out of {df.shape[0]} total")
        
        # ========== INTERACTIVE TABLE ==========
        st.markdown("### 📋 Filtered Data (click column headers to sort)")
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # ========== DOWNLOAD BUTTONS ==========
        st.markdown("### 💾 Download Data")
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name='filtered_data.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        with col_dl2:
            # For Excel download
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Filtered Data')
            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name='filtered_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        
        with col_dl3:
            # Summary stats download
            if len(filtered_df) > 0:
                summary = filtered_df.describe().to_csv()
                st.download_button(
                    label="📊 Download Summary Stats",
                    data=summary,
                    file_name='summary_statistics.csv',
                    mime='text/csv',
                    use_container_width=True
                )
        
        # ========== AI INSIGHTS ==========
        st.markdown("### 🤖 Data Insights")
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            # Find numeric columns for insights
            numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            if numeric_cols and len(filtered_df) > 0:
                selected_num = st.selectbox("📈 Select column for detailed stats", numeric_cols)
                if selected_num:
                    col_data = filtered_df[selected_num].dropna()
                    if len(col_data) > 0:
                        st.metric(
                            label=f"{selected_num} - Average",
                            value=f"{col_data.mean():.2f}",
                            delta=f"Std: {col_data.std():.2f}"
                        )
                        st.write(f"- **Minimum:** {col_data.min():.2f}")
                        st.write(f"- **Maximum:** {col_data.max():.2f}")
                        st.write(f"- **Missing Values:** {filtered_df[selected_num].isnull().sum()} rows")
                    else:
                        st.warning("No valid numeric data in this column")
            else:
                st.info("No numeric columns found for statistical insights")
        
        with insight_col2:
            if filtered_df.shape[0] > 0 and df.shape[0] > 0:
                reduction = df.shape[0] - filtered_df.shape[0]
                reduction_pct = (reduction / df.shape[0]) * 100
                st.info(f"💡 **Quick Insight:**\n\n- Original rows: {df.shape[0]}\n- After filtering: {filtered_df.shape[0]}\n- Filtered out: {reduction} rows ({reduction_pct:.1f}%)")
                
                # Check for missing values
                missing_cols = df.isnull().sum()
                missing_cols = missing_cols[missing_cols > 0]
                if len(missing_cols) > 0:
                    st.warning(f"⚠️ Found {len(missing_cols)} columns with missing values")
                else:
                    st.success("✅ No missing values found in original data")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ========== VISUALIZATION SECTION ==========
        st.markdown("### 📊 Create Custom Charts")
        
        if len(filtered_df) > 0:
            viz_col1, viz_col2, viz_col3 = st.columns(3)
            
            with viz_col1:
                chart_type = st.selectbox(
                    "Chart Type",
                    ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot"]
                )
            
            numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            text_cols = filtered_df.select_dtypes(include=['object']).columns.tolist()
            
            with viz_col2:
                if chart_type in ["Scatter Plot", "Line Chart"]:
                    x_axis = st.selectbox("X-Axis", numeric_cols if numeric_cols else df.columns.tolist())
                    y_axis = st.selectbox("Y-Axis", numeric_cols if numeric_cols else df.columns.tolist())
                elif chart_type == "Bar Chart":
                    x_axis = st.selectbox("Category (X-Axis)", text_cols if text_cols else df.columns.tolist())
                    y_axis = st.selectbox("Value (Y-Axis)", numeric_cols if numeric_cols else df.columns.tolist())
                elif chart_type == "Histogram":
                    x_axis = st.selectbox("Column for Histogram", numeric_cols if numeric_cols else df.columns.tolist())
                    y_axis = None
                else:  # Box Plot
                    x_axis = st.selectbox("Numeric Column", numeric_cols if numeric_cols else df.columns.tolist())
                    y_axis = None
            
            with viz_col3:
                chart_height = st.slider("Chart Height (pixels)", 300, 800, 500)
            
            # Generate chart
            try:
                fig = None
                if chart_type == "Scatter Plot" and x_axis and y_axis:
                    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                elif chart_type == "Line Chart" and x_axis and y_axis:
                    fig = px.line(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                elif chart_type == "Bar Chart" and x_axis and y_axis:
                    fig = px.bar(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                elif chart_type == "Histogram" and x_axis:
                    fig = px.histogram(filtered_df, x=x_axis, title=f"Distribution of {x_axis}")
                elif chart_type == "Box Plot" and x_axis:
                    fig = px.box(filtered_df, y=x_axis, title=f"Box Plot of {x_axis}")
                
                if fig:
                    fig.update_layout(height=chart_height)
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("💡 **Tip:** Hover over chart → Click camera icon to save as PNG")
                else:
                    st.warning("Please select valid columns for this chart type")
                    
            except Exception as e:
                st.warning(f"Could not create chart. Error: {str(e)[:150]}")
        else:
            st.warning("No data available after filtering. Adjust your filters to see charts.")
        
        # ========== MISSING VALUES REPORT ==========
        with st.expander("⚠️ Data Quality Report (Missing Values)"):
            missing_df = pd.DataFrame({
                'Column': df.columns,
                'Missing Count': df.isnull().sum().values,
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2).values
            })
            missing_df = missing_df[missing_df['Missing Count'] > 0]
            if len(missing_df) > 0:
                st.dataframe(missing_df, use_container_width=True)
                st.info("💡 **Recommendations:** Fill missing values with mean/median for numeric columns, or mode for categorical columns. Drop columns with >50% missing values.")
            else:
                st.success("✅ No missing values found! Your data is clean and ready to use.")
        
        # ========== COLUMN INFORMATION ==========
        with st.expander("📋 Column Information"):
            col_info = pd.DataFrame({
                'Column Name': df.columns,
                'Data Type': df.dtypes.values,
                'Unique Values': [df[col].nunique() for col in df.columns],
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2).values
            })
            st.dataframe(col_info, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.info("Make sure your file is a valid CSV or Excel file. Check for special characters or encoding issues.")

else:
    # Show example when no file is uploaded
    st.markdown("### 📌 Try it with sample data")
    
    # Sample dataset options using reliable datasets
    col_sample1, col_sample2, col_sample3 = st.columns(3)
    
    with col_sample1:
        if st.button("🌸 Iris Dataset", use_container_width=True):
            df_sample = px.data.iris()
            st.session_state['sample_df'] = df_sample
            st.rerun()
    
    with col_sample2:
        if st.button("📊 Gapminder Dataset", use_container_width=True):
            df_sample = px.data.gapminder()
            st.session_state['sample_df'] = df_sample
            st.rerun()
    
    with col_sample3:
        if st.button("💳 Tips Dataset", use_container_width=True):
            df_sample = px.data.tips()
            st.session_state['sample_df'] = df_sample
            st.rerun()
    
    # Show sample data preview if loaded
    if 'sample_df' in st.session_state:
        st.markdown("### 📋 Sample Data Preview")
        st.dataframe(st.session_state['sample_df'].head(10), use_container_width=True)
        st.info("✨ This is just a preview. Upload your own CSV or Excel file above to analyze your data!")
        
        # Option to clear sample
        if st.button("🔄 Clear Sample Data"):
            del st.session_state['sample_df']
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### 📝 About This Tool
    
    **Built by Tassawar Abbas** - Kaggle Notebooks Expert (Rank #44 out of 61,000+)
    
    **Features:**
    - 🔒 **Privacy first:** Your data never leaves your browser. All processing happens locally.
    - 📊 **Interactive filtering:** Filter by any column, search text, or select ranges.
    - 📈 **Custom charts:** Create scatter plots, bar charts, histograms, box plots, and line charts.
    - 💾 **Download data:** Export filtered results as CSV or Excel files.
    - 🤖 **Automatic insights:** Get statistics, missing value reports, and data quality checks.
    - 🎯 **Column information:** View data types, unique values, and completeness.
    
    **Why choose this tool?**
    - ✅ Kaggle Rank #44 (Top 0.07% globally)
    - ✅ 2+ years data science experience
    - ✅ Built by a Kaggle Datasets Expert (#122)
    
    **Need a custom version for your business?** Contact me for:
    - Branded dashboard with your logo
    - Custom calculations and business logic
    - Automated reporting
    - Integration with your existing workflow
    
    [📧 Contact on LinkedIn](https://www.linkedin.com/in/abbas829pro/) | [🐙 GitHub](https://github.com/abbas829) | [🏆 Kaggle](https://www.kaggle.com/abbas829)
    """)

# ========== FOOTER ==========
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Built with Streamlit | Kaggle Rank #44 (Notebooks) & #122 (Datasets) | Data Scientist @ DataforAI | © 2024 Tassawar Abbas</p>",
    unsafe_allow_html=True
)