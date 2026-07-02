# filename: wrestle_ai_mobile.py
import streamlit as st
import os
import time
from google import genai
from google.genai import types

# Page configuration optimized for mobile screens
st.set_page_config(
    page_title="WrestleAI Mobile", 
    page_icon="🤼‍♂️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to make look like an iOS Native App
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none;}
    .main .block-container {padding-top: 1.5rem; padding-bottom: 1rem;}
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background-color: #007AFF;
        color: white;
        height: 3em;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        width: 100%;
    }
    .stTabs [data-baseweb="tab"] {
        flex-grow: 1;
        text-align: center;
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤼‍♂️ WrestleAI Companion")

# Initialize official Gemini Client
@st.cache_resource
def get_gemini_client():
    return genai.Client()

try:
    client = get_gemini_client()
except Exception:
    st.error("Please set your GEMINI_API_KEY configuration.")

tab1, tab2, tab3 = st.tabs(["🥋 AI Coach", "🍎 Calories", "⚖️ Weight Plan"])

# TAB 1: STANCE & MOTION AI COACH
with tab1:
    st.header("Stance Analysis")
    st.write("Record a video or upload from your camera roll.")
    
    uploaded_video = st.file_uploader("Choose video...", type=["mp4", "mov", "m4v"])
    
    if uploaded_video is not None:
        st.video(uploaded_video)
        if st.button("🚀 Run AI Analysis", key="btn_stance"):
            with st.spinner("Processing video..."):
                temp_filename = f"temp_{uploaded_video.name}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_video.read())
                try:
                    video_file = client.files.upload(file=temp_filename)
                    while video_file.state.name == "PROCESSING":
                        time.sleep(3)
                        video_file = client.files.get(name=video_file.name)
                        
                    if video_file.state.name == "FAILED":
                        st.error("Processing failed.")
                    else:
                        prompt = "Act as an elite wrestling coach. Rate this stance/motion 1-10. Give 2 technique tips and 1 drill to fix flaws."
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[video_file, prompt]
                        )
                        st.success("Analysis Complete!")
                        st.markdown(response.text)
                    client.files.delete(name=video_file.name)
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)

# TAB 2: CALORIE TRACKER
with tab2:
    st.header("Nutrition Log")
    meal = st.text_area("What did you eat today?", placeholder="e.g., 3 eggs, chicken breast, oatmeal")
    workout = st.text_area("Wrestling workouts?", placeholder="e.g., 2 hour hard live drilling")
    
    if st.button("📊 Calculate Balance", key="btn_cal"):
        with st.spinner("Analyzing macros..."):
            prompt = f"Wrestler metrics tool. Food: {meal}. Output: {workout}. Provide calories consumed, calories burned, deficit/surplus, and quick high-protein athletic feedback."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown(response.text)

# TAB 3: WEIGHT LOSS PLANNER
with tab3:
    st.header("Weight Blueprint")
    current = st.number_input("Current Weight", value=155.0)
    target = st.number_input("Target Weight", value=145.0)
    days = st.number_input("Days Left", value=14, min_value=1)
    
    if st.button("⚖️ Generate Cut Strategy", key="btn_weight"):
        diff = current - target
        if diff <= 0:
            st.success("On weight!")
        else:
            weekly = (diff / days) * 7
            st.metric("Total to drop", f"{diff:.1f} lbs")
            st.metric("Rate per week", f"{weekly:.1f} lbs/wk")
            if weekly > 2.5:
                st.warning("⚠️ High weight cut speed. Hydrate intensely.")
                
            prompt = f"Provide a safe weight loss cut strategy for a wrestler dropping from {current} to {target} in {days} days. Include high protein macro targets and hydration advice."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown(response.text)
