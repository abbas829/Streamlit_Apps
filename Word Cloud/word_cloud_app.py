import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
import base64
from io import BytesIO

# Functions for file reading
def read_txt(file):
    return file.getvalue().decode("utf-8")

def read_docx(file):
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in pdf.pages])

# Function to filter out stopwords
def filter_stopwords(text, additional_stopwords=[]):
    words = text.split()
    all_stopwords = STOPWORDS.union(set(additional_stopwords))
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    return " ".join(filtered_words)

# Function to create download link for plot
def get_image_download_link(buffered, format_):
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:image/{format_};base64,{image_base64}" download="wordcloud.{format_}">Download Word Cloud as {format_}</a>'

# Function to generate a download link for a DataFrame
def get_table_download_link(df, filename, file_label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'

# Streamlit UI
st.title("🌥️ Word Cloud Generator")
st.subheader("Upload a PDF, DOCX, or TXT file to generate a Word Cloud")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    file_details = {
        "File Name": uploaded_file.name, 
        "File Type": uploaded_file.type, 
        "File Size (KB)": round(uploaded_file.size / 1024, 2)
    }
    st.sidebar.write("**File Details:**", file_details)

    # File reading based on type
    if uploaded_file.type == "text/plain":
        text = read_txt(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a TXT, PDF, or DOCX file.")
        st.stop()

    # Word count table
    words = text.split()
    word_count = pd.DataFrame({'Word': words}).groupby('Word').size().reset_index(name='Count').sort_values('Count', ascending=False)

    # Sidebar: Stopwords and Word Cloud Customization
    use_standard_stopwords = st.sidebar.checkbox("Use standard stopwords?", True)
    top_words = word_count['Word'].head(50).tolist()
    additional_stopwords = st.sidebar.multiselect("Add stopwords:", sorted(top_words))

    all_stopwords = STOPWORDS.union(set(additional_stopwords)) if use_standard_stopwords else set(additional_stopwords)
    filtered_text = filter_stopwords(text, all_stopwords)

    if filtered_text:
        # Word Cloud dimensions
        width = st.sidebar.slider("Word Cloud Width (px)", 400, 2000, 1200, 50)
        height = st.sidebar.slider("Word Cloud Height (px)", 200, 2000, 800, 50)

        # Generate Word Cloud
        st.subheader("Generated Word Cloud")
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        wordcloud_img = WordCloud(width=width, height=height, background_color='white', max_words=200).generate(filtered_text)
        ax.imshow(wordcloud_img, interpolation='bilinear')
        ax.axis('off')

        # Display and save options
        st.pyplot(fig)
        format_ = st.selectbox("Save Word Cloud as:", ["png", "jpeg", "svg", "pdf"])
        resolution = st.slider("Image Resolution (DPI)", 100, 500, 300, 50)

        if st.button(f"Save Word Cloud as {format_.upper()}"):
            buffered = BytesIO()
            plt.savefig(buffered, format=format_, dpi=resolution)
            st.markdown(get_image_download_link(buffered, format_), unsafe_allow_html=True)

        # Display word count table
        st.subheader("Word Count Table")
        st.write(word_count)
        if st.button('Download Word Count Table as CSV'):
            st.markdown(get_table_download_link(word_count, "word_count.csv", "Download CSV"), unsafe_allow_html=True)

# Footer with author info
st.sidebar.markdown("### Created by: [Tassawar Abbas](https://github.com/Abbas829)")
st.sidebar.markdown("Contact: [Email](mailto:abbas829@gmail.com)")
st.sidebar.markdown("Facebook: [Tassawar Abbas](https://www.facebook.com/abbas829)")
st.sidebar.markdown("Linkedin: [Tassawar Abbas](https://www.linkedin.com/in/abbas829pro)")
