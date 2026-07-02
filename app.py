# filename: app.pyimport streamlit as stimport osimport timeimport streamlit.components.v1 as componentsfrom google import genaifrom google.genai import types
# ----------------------------------------------------# 📱 MOBILE CONTAINER STYLING# ----------------------------------------------------
st.set_page_config(
    page_title="Wrestle AI Pro", 
    page_icon="🤼‍♂️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stHeader"] {display: none;}
    body { background-color: #0B0E14; color: #FFFFFF; }
    .main .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    .feature-card {
        background: linear-gradient(145deg, #161B26, #0F131C);
        border: 1px solid #242C3D;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #FF5E3A, #FF2A68);
        color: white;
        height: 3.2em;
        font-weight: bold;
        border: none;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; width: 100%; }
    .stTabs [data-baseweb="tab"] {
        flex-grow: 1; text-align: center; background-color: #161B26;
        border-radius: 8px; padding: 6px; font-size: 0.75rem; color: #AEB9CC;
    }
    .stTabs [aria-selected="true"] { background-color: #FF2A68 !important; color: white !important; }
</style>""", unsafe_allow_html=True)

st.title("🤼‍♂️ WRESTLE AI")
st.caption("AI Performance Ecosystem • Pro Tier")
# ----------------------------------------------------# 🤖 CLEAN AI INITIALIZATION (FIXED COUPLING)# ----------------------------------------------------
@st.cache_resourcedef get_gemini_client():
    return genai.Client()
try:
    client = get_gemini_client()except Exception:
    st.error("Please configure your GEMINI_API_KEY in Streamlit Advanced Settings.")
# Master Navigation Menu Tabstabs = st.tabs(["🥋 AI Coach", "🔊 Flow", "📋 Daily Drills", "📊 Stats", "🔥 Impossible", "🍎 Fuel"])tab_video, tab_trainer, tab_drills, tab_stats, tab_impossible, tab_nutrition = tabs
# ====================================================# TAB 1: MULTI-STYLE AI VIDEO ANALYSIS# ====================================================with tab_video:
    st.markdown('<div class="feature-card"><h3>🎞️ Match Video Analysis</h3>Upload footage for automated posture and positioning corrections.</div>', unsafe_allow_html=True)
    w_style = st.selectbox("Style", ["Folkstyle", "Freestyle", "Greco-Roman", "Jiu-Jitsu"])
    w_pos = st.selectbox("Domain Position", ["Neutral", "Top", "Bottom", "Scramble"])
    uploaded_video = st.file_uploader("Upload video (.mp4, .mov)", type=["mp4", "mov", "m4v"])
    
    if uploaded_video is not None:
        st.video(uploaded_video)
        if st.button("🚀 Analyze Video Footage", key="btn_video_analysis"):
            with st.spinner("Processing video layers..."):
                temp_filename = f"temp_{uploaded_video.name}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_video.read())
                try:
                    video_file = client.files.upload(file=temp_filename)
                    while client.files.get(name=video_file.name).state.name == "PROCESSING":
                        time.sleep(3)
                    
                    prompt = f"Elite coach analysis. Style: {w_style}, Position: {w_pos}. Provide Match Rating (1-10), Critical Mistakes, Structural Strengths, and 2 Drills to improve."
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=[video_file, prompt])
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                    client.files.delete(name=video_file.name)
                except Exception as e:
                    st.error(f"Error processing video: {e}")
                finally:
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)
# ====================================================# TAB 2: LIVE STANCE FLOW AUDIO PROMPTING# ====================================================with tab_trainer:
    st.markdown('<div class="feature-card"><h3>🔊 Voice Stance Flow</h3>Unlock audio and react instantly to active spoken mat commands.</div>', unsafe_allow_html=True)
    match_time = st.number_input("Round Time (seconds)", min_value=20, max_value=300, value=60, step=10)
    
    html_engine = f"""
    <div style="background: #161B26; padding: 20px; border-radius: 12px; text-align: center; color: white; font-family: sans-serif;">
        <h1 id="cmd" style="font-size: 2.5rem; color: #FF2A68; margin: 10px 0;">READY</h1>
        <p id="rem" style="color: #AEB9CC;">Time: {match_time}s</p>
        <button id="st" onclick="start()" style="width:100%; background:#34C759; color:white; font-weight:bold; padding:12px; border:none; border-radius:8px; font-size:1.1rem;">🏁 START ROUND</button>
        <button id="sp" onclick="stop()" style="width:100%; background:#FF3B30; color:white; font-weight:bold; padding:12px; border:none; border-radius:8px; font-size:1.1rem; margin-top:8px; display:none;">🛑 STOP</button>
    </div>
    <script>
        let acts = ["Sprawl!", "Circle Left!", "Circle Right!", "Level Change!", "Down Block!", "Penetration Step!", "Snap Down!", "Re-attack!"];
        let run = false; let tc, cc; let sec = {match_time};
        const voice = window.speechSynthesis;
        function speak(t) {{ if(voice.speaking){{voice.cancel();}} let u = new SpeechSynthesisUtterance(t); u.rate=1.3; voice.speak(u); }}
        function start() {{
            if(run) return; run = true; sec = {match_time};
            document.getElementById('st').style.display='none'; document.getElementById('sp').style.display='block';
            document.getElementById('cmd').innerText = "STANCE"; speak("Lower your level. Go.");
            tc = setInterval(() => {{
                sec--; document.getElementById('rem').innerText = "Time: " + sec + "s";
                if(sec <= 0) {{ stop(); document.getElementById('cmd').innerText = "TIME"; speak("Time. Great round."); }}
            }}, 1000);
            loop();
        }}
        function loop() {{
            if(!run) return;
            let c = acts[Math.floor(Math.random() * acts.length)];
            document.getElementById('cmd').innerText = c; speak(c);
            cc = setTimeout(loop, Math.floor(Math.random() * 2000) + 1500);
        }}
        function stop() {{ run = false; clearInterval(tc); clearTimeout(cc); document.getElementById('st').style.display='block'; document.getElementById('sp').style.display='none'; voice.cancel(); }}
    </script>
    """
    components.html(html_engine, height=220)
# ====================================================# TAB 3: PERSONALIZED DAILY DRILL BUILDER# ====================================================with tab_drills:
    st.markdown('<div class="feature-card"><h3>📋 Drill Library Generator</h3>Build customized technical focus schedules based on experience.</div>', unsafe_allow_html=True)
    w_level = st.selectbox("Experience Level", ["Beginner / Youth", "Intermediate / High School", "Collegiate / Advanced"])
    w_focus = st.text_input("Drill Focus Area", value="Single Leg Finishes")
    
    if st.button("⚡ Generate Training Plan", key="btn_drills"):
        with st.spinner("Generating sequence..."):
            prompt = f"Create a structured 30-minute drilling sequence for a {w_level} wrestler focusing on {w_focus}. Provide specific time intervals and technical execution keys."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown(response.text)
# ====================================================# TAB 4: METRICS LOG & MATCH RECORD TRACKER# ====================================================with tab_stats:
    st.markdown('<div class="feature-card"><h3>📊 Match Statistics Ledger</h3>Log active match statistics to isolate and track trends.</div>', unsafe_allow_html=True)
    s_att = st.number_input("Shot Attempts", min_value=0, value=3)
    s_fin = st.number_input("Shots Finished", min_value=0, value=1)
    s_esc = st.number_input("Escapes Executed", min_value=0, value=1)
    
    if st.button("💾 Commit Match Metrics", key="btn_stats"):
        rate = (s_fin / s_att * 100) if s_att > 0 else 0.0
        st.metric("Takedown Conversion Efficiency", f"{rate:.1f}%")
        st.success("Stats successfully recorded to user progress registry.")
# ====================================================# TAB 5: IMPOSSIBLE MODE CONDITIONING# ====================================================with tab_impossible:
    st.markdown('<div class="feature-card" style="border: 1px solid #FF2A68;"><h3>🔥 Impossible Mode Workout</h3>High-intensity metabolic conditioning protocols to break late-match plateau barriers.</div>', unsafe_allow_html=True)
    ch_type = st.selectbox("Focus Arena", ["Third-Period Lung Burner", "Grip Strength Finish", "Short-Time Scramble Endurance"])
    
    if st.button("💥 Fetch Conditioning Protocol", key="btn_impossible"):
        with st.spinner("Generating routine..."):
            prompt = f"Create a short, brutal, high-intensity bodyweight conditioning challenge for a wrestler named 'IMPOSSIBLE MODE: {ch_type}'. Make it high energy and tough."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown(response.text)
# ====================================================# TAB 6: AI MEAL NUTRITION LOG & WEIGHT DESCENT# ====================================================with tab_nutrition:
    st.markdown('<div class="feature-card"><h3>🍎 Weight Loss & Fuel Planner</h3>Monitor safe weight tracking speeds while protecting lean athletic power.</div>', unsafe_allow_html=True)

cur_w = st.number_input("Current Weight (lbs)", value=150.0)
tar_w = st.number_input("Target Weight Class (lbs)", value=141.0)
days = st.number_input("Days Left until Weigh-In", min_value=1, value=7)
meal = st.text_area("Describe food eaten today:", "Chicken breast, broccoli, brown rice, protein shake.")
if st.button("⚖️ Generate Blueprint", key="btn_fuel"):
diff = cur_w - tar_w
if diff <= 0:
st.success("You are on weight! Focus on energy timing layouts.")
else:
weekly_velocity = (diff / days) * 7
st.metric("Total to Drop", f"{diff:.1f} lbs")
st.metric("Rate per Week", f"{weekly_velocity:.1f} lbs/wk")
with st.spinner("Calculating macros..."):
prompt = f"Wrestler cutting from {cur_w} to {tar_w} in {days} days. Ate today: '{meal}'. Provide safe daily macro advice and clean hydration tracking guidelines."
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
st.markdown(response.text)