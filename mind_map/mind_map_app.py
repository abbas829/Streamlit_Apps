import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import io

# Function to create the mind map graph
def create_mind_map(central_topic, subtopics):
    G = nx.Graph()
    
    # Add the central topic as the root node
    G.add_node(central_topic, type="central")
    
    # Add subtopics and detailed information as nodes and edges
    for subtopic, details in subtopics.items():
        G.add_node(subtopic, type="subtopic")
        G.add_edge(central_topic, subtopic)
        
        for detail in details:
            G.add_node(detail, type="detail")
            G.add_edge(subtopic, detail)
    
    return G

# Function to visualize the mind map
def visualize_mind_map(G, central_topic, layout_style, central_color, subtopic_color, detail_color, central_style, subtopic_style, node_size, edge_width, font_size):
    # Select layout style
    if layout_style == "Spring":
        pos = nx.spring_layout(G)
    elif layout_style == "Circular":
        pos = nx.circular_layout(G)
    elif layout_style == "Shell":
        pos = nx.shell_layout(G)
    elif layout_style == "Planar":
        pos = nx.planar_layout(G)
    else:
        pos = nx.spring_layout(G)  # Default layout
    
    plt.figure(figsize=(12, 8))
    
    # Draw the nodes with different colors based on their type
    central_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == "central"]
    subtopic_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == "subtopic"]
    detail_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == "detail"]
    
    nx.draw_networkx_nodes(G, pos, nodelist=central_nodes, node_color=central_color, node_size=node_size, node_shape=central_style)
    nx.draw_networkx_nodes(G, pos, nodelist=subtopic_nodes, node_color=subtopic_color, node_size=node_size * 0.8, node_shape=subtopic_style)
    nx.draw_networkx_nodes(G, pos, nodelist=detail_nodes, node_color=detail_color, node_size=node_size * 0.6)
    
    # Draw the edges
    nx.draw_networkx_edges(G, pos, edge_color="black", width=edge_width)
    
    # Draw the labels
    nx.draw_networkx_labels(G, pos, font_size=font_size, font_family='sans-serif')
    
    plt.title(f"Mind Map: {central_topic}", size=20)
    plt.axis('off')
    
    # Save the figure in a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Streamlit interface
st.title("State-of-the-Art Mind Map Generator")
st.write("Create a visually appealing mind map with various customization options.")

# Input for central topic
central_topic = st.text_input("Enter the Central Topic", "Central Idea")

# Input for subtopics
num_subtopics = st.slider("Number of Subtopics", 1, 10, 3)

subtopics = {}
for i in range(num_subtopics):
    subtopic = st.text_input(f"Enter Subtopic {i+1}")
    num_details = st.slider(f"Number of Details for {subtopic}", 1, 5, 2, key=f'detail_slider_{i}')
    details = []
    for j in range(num_details):
        detail = st.text_input(f"Enter Detail {j+1} for {subtopic}", key=f'detail_input_{i}_{j}')
        details.append(detail)
    subtopics[subtopic] = details

# Visualization options in sidebar
st.sidebar.header("Visualization Options")

layout_style = st.sidebar.selectbox("Select Layout Style", ["Spring", "Circular", "Shell", "Planar"])
central_color = st.sidebar.color_picker("Pick a Color for the Central Topic", "#ff5733")
subtopic_color = st.sidebar.color_picker("Pick a Color for Subtopics", "#33c3ff")
detail_color = st.sidebar.color_picker("Pick a Color for Details", "#66ff66")

# Additional visualization parameters with sliders and style selectors
central_style = st.sidebar.selectbox("Central Topic Style", ["o", "s", "D", "^"])  # 'o' for circle, 's' for square, 'D' for diamond, '^' for triangle
subtopic_style = st.sidebar.selectbox("Subtopic Style", ["o", "s", "D", "^"])

node_size = st.sidebar.slider("Node Size", 100, 5000, 3000)
edge_width = st.sidebar.slider("Edge Width", 1, 10, 2)
font_size = st.sidebar.slider("Label Font Size", 8, 24, 12)

# Button to generate mind map
if st.button("Generate Mind Map"):
    G = create_mind_map(central_topic, subtopics)
    buf = visualize_mind_map(G, central_topic, layout_style, central_color, subtopic_color, detail_color, central_style, subtopic_style, node_size, edge_width, font_size)
    
    st.image(buf, caption=f"Preview: {central_topic}", use_column_width=True)
    
    with st.expander("Download Options"):
        # File download options
        st.download_button(
            label="Download Mind Map as PNG",
            data=buf,
            file_name=f"{central_topic}_mind_map.png",
            mime="image/png"
        )
        
        # Rewind buffer for other formats
        buf.seek(0)
        img = plt.imread(buf, format='png')
        
        # Option to download as JPG
        buf_jpg = io.BytesIO()
        plt.imsave(buf_jpg, img, format='jpg')
        buf_jpg.seek(0)
        st.download_button(
            label="Download Mind Map as JPG",
            data=buf_jpg,
            file_name=f"{central_topic}_mind_map.jpg",
            mime="image/jpeg"
        )
        
        # Option to download as PDF
        buf_pdf = io.BytesIO()
        plt.savefig(buf_pdf, format='pdf')
        buf_pdf.seek(0)
        st.download_button(
            label="Download Mind Map as PDF",
            data=buf_pdf,
            file_name=f"{central_topic}_mind_map.pdf",
            mime="application/pdf"
        )

# Footer with author info
st.sidebar.markdown("### Created by: [Tassawar Abbas](https://github.com/Abbas829)")
st.sidebar.markdown("Contact: [Email](mailto:abbas829@gmail.com)")
st.sidebar.markdown("Facebook: [Tassawar Abbas](https://www.facebook.com/abbas829)")
st.sidebar.markdown("Linkedin: [Tassawar Abbas](https://www.linkedin.com/in/abbas829pro)")
