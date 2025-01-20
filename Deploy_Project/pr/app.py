import streamlit as st
import joblib
import os
import glob
import zipfile
import tempfile
from datetime import datetime
import urllib3

# Page configuration
st.set_page_config(
    page_title="Email Spam Classifier",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
            background-color: #ff4b4b;
            color: white;
        }
        .stTextArea>div>div>textarea {
            background-color: #f0f2f6;
        }
        .css-1d391kg {
            padding: 2rem;
            border-radius: 0.5rem;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .status-box {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    model_path = 'spam_classifier.pkl'
    if not os.path.exists(model_path):
        url = 'https://github.com/Sumit-Telawane/Data-science/raw/main/Deploy_Project/pr/spam_classifier.pkl'
        http = urllib3.PoolManager()
        response = http.request('GET', url, preload_content=False)
        if response.status == 200:
            with open(model_path, 'wb') as out_file:
                while True:
                    data = response.read(1024)
                    if not data:
                        break
                    out_file.write(data)
            response.release_conn()
        else:
            response.release_conn()
            raise Exception(f"Failed to download the model. HTTP status code: {response.status}")
    return joblib.load(model_path)

# Header section
st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b; margin-bottom: 2rem;'>
        📧 Email Spam Classifier
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center; font-size: 1.2rem; margin-bottom: 3rem;'>
        Detect spam emails using machine learning technology
    </p>
""", unsafe_allow_html=True)

# Create two columns with better spacing
col1, spacer, col2 = st.columns([4, 0.5, 4])

# Column 1: Single Email Classification
with col1:
    st.markdown("""
        <h3 style='color: #ff4b4b; margin-bottom: 1rem;'>
            ✉️ Single Email Classification
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style='margin-bottom: 1rem;'>
            Enter the email content below to check if it's spam or not.
        </p>
    """, unsafe_allow_html=True)

    # Custom CSS
    st.markdown("""
        <style>
            .stTextArea>div>div>textarea {
                background-color: #f0f2f6;
                color: black !important;
                font-size: 20px !important;
                caret-color: black !important;  /* Makes the cursor/caret black */
            }
        </style>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "",
        placeholder="Paste your email content here...",
        height=200
    )
    
    if st.button("🔍 Analyze Email", key="single"):
        if user_input.strip():
            with st.spinner("Analyzing..."):
                prediction = clf.predict([user_input])[0]
                if prediction == 1:
                    st.error("🚨 This email is classified as **SPAM**")
                    st.markdown("""
                        <div style='font-size: 0.9rem; color: #666;'>
                            ⚠️ This email contains characteristics commonly associated with spam messages.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ This email is classified as **LEGITIMATE**")
                    st.markdown("""
                        <div style='font-size: 0.9rem; color: #666;'>
                            👍 This email appears to be a legitimate communication.
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter email content before analyzing.")

# Column 2: Batch Classification
with col2:
    st.markdown("""
        <h3 style='color: #ff4b4b; margin-bottom: 1rem;'>
            📁 Batch Classification
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style='margin-bottom: 1rem;'>
            Upload a ZIP file containing multiple email text files for batch analysis.
        </p>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["zip"])
    
    if uploaded_file is not None:
        with st.spinner("Processing files..."):
            with tempfile.TemporaryDirectory() as tmpdirname:
                zip_path = os.path.join(tmpdirname, "uploaded_folder.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                
                text_files = glob.glob(os.path.join(tmpdirname, "*.txt"))
                
                if text_files:
                    results = {
                        'spam': [],
                        'legitimate': []
                    }
                    
                    for file in text_files:
                        with open(file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            filename = os.path.basename(file)
                            if clf.predict([content])[0] == 1:
                                results['spam'].append(filename)
                            else:
                                results['legitimate'].append(filename)
                    
                    # Display results in an organized way
                    st.markdown("### 📊 Analysis Results")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Files", len(text_files))
                    with col2:
                        st.metric("Spam Detected", len(results['spam']))
                    
                    if results['spam']:
                        with st.expander("🚨 Spam Files"):
                            for file in results['spam']:
                                st.write(f"- {file}")
                    
                    if results['legitimate']:
                        with st.expander("✅ Legitimate Files"):
                            for file in results['legitimate']:
                                st.write(f"- {file}")
                else:
                    st.warning("📝 No text files found in the uploaded ZIP folder.")
    else:
        st.info("📤 Upload a ZIP file to start batch analysis")
