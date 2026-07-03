 # ============================================
# Wrestle AI Pro
# Part 1/4
# ============================================

import os
import time
import tempfile

import streamlit as st
import streamlit.components.v1 as components

from google import genai

# ----------------------------
# Page Setup
# ----------------------------

st.set_page_config(
    page_title="Wrestle AI Pro",
    page_icon="🤼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

[data-testid="stHeader"]{
display:none;
}

.main .block-container{
padding-top:1rem;
padding-bottom:2rem;
max-width:900px;
}

.feature-card{
background:#151922;
padding:20px;
border-radius:16px;
border:1px solid #333;
margin-bottom:15px;
}

div.stButton > button{
width:100%;
border-radius:12px;
height:50px;
font-weight:bold;
background:#ff2f63;
color:white;
}

</style>
""", unsafe_allow_html=True)

st.title("🤼 Wrestle AI Pro")
st.caption("AI Wrestling Performance System")

# ----------------------------
# Gemini Client
# ----------------------------

@st.cache_resource
def get_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)

try:
    client = get_client()
except Exception:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# ----------------------------
# Navigation
# ----------------------------

tabs = st.tabs([
    "🤖 Coach",
    "🎥 Video",
    "🎤 Voice",
    "📋 Drills",
    "📊 Stats",
    "🍎 Nutrition"
])

coach_tab, video_tab, voice_tab, drills_tab, stats_tab, nutrition_tab = tabs

# =====================================
# COACH TAB
# =====================================

with coach_tab:

    st.markdown(
        '<div class="feature-card"><h3>AI Wrestling Coach</h3></div>',
        unsafe_allow_html=True
    )

    style = st.selectbox(
        "Style",
        [
            "Folkstyle",
            "Freestyle",
            "Greco Roman",
            "BJJ"
        ]
    )

    position = st.selectbox(
        "Position",
        [
            "Neutral",
            "Top",
            "Bottom",
            "Scramble"
        ]
    )

    question = st.text_area(
        "Ask your coach anything..."
    )

    if st.button("Ask Coach"):

        prompt = f"""
You are an elite wrestling coach.

Style:
{style}

Position:
{position}

Question:
{question}

Give technical coaching,
mistakes,
drills,
and match strategy.
"""

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.markdown(response.text)

# =====================================
# VIDEO TAB
# =====================================

with video_tab:

    st.markdown(
        '<div class="feature-card"><h3>Video Analysis</h3></div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Upload Match Video",
        type=["mp4", "mov", "m4v"]
    )

    if uploaded:

        st.video(uploaded)

        if st.button("Analyze Match"):

            with st.spinner("Uploading..."):

                with tempfile.NamedTemporaryFile(delete=False) as tmp:

                    tmp.write(uploaded.read())

                    temp_name = tmp.name

            try:

                video = client.files.upload(
                    file=temp_name
                )

                while True:

                    status = client.files.get(
                        name=video.name
                    )

                    if status.state.name != "PROCESSING":
                        break

                    time.sleep(2)

                prompt = """
Analyze this wrestling match.

Return:

Overall Score

Strengths

Weaknesses

Takedown opportunities

Defense issues

Conditioning

Three drills

Final coaching summary.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        video,
                        prompt
                    ]
                )

                st.success("Analysis Complete")

                st.markdown(response.text)

                client.files.delete(
                    name=video.name
                )

            finally:

                if os.path.exists(temp_name):
                    os.remove(temp_name)
# ============================================
# Part 2/4 - Voice Trainer + Drill Generator
# ============================================

# =========================
# VOICE TRAINER TAB
# =========================

with voice_tab:

    st.markdown(
        '<div class="feature-card"><h3>Voice Stance Trainer</h3></div>',
        unsafe_allow_html=True
    )

    round_time = st.number_input(
        "Round Time (seconds)",
        min_value=20,
        max_value=300,
        value=60,
        step=10
    )

    html = f"""
    <div style="background:#111;padding:20px;border-radius:12px;text-align:center;color:white;">
        <h1 id="cmd" style="color:#ff2f63;">READY</h1>
        <p id="time">{round_time}</p>

        <button onclick="startRound()" style="width:100%;padding:12px;border:none;border-radius:10px;background:green;color:white;font-weight:bold;">
            Start
        </button>

        <button onclick="stopRound()" style="width:100%;padding:12px;margin-top:10px;border:none;border-radius:10px;background:red;color:white;font-weight:bold;">
            Stop
        </button>
    </div>

    <script>
    let time = {round_time};
    let running = false;
    let interval;

    const moves = [
        "Sprawl",
        "Shoot",
        "Circle Left",
        "Circle Right",
        "Level Change",
        "Snap Down",
        "Hand Fight"
    ];

    function speak(text){
        let msg = new SpeechSynthesisUtterance(text);
        msg.rate = 1.2;
        speechSynthesis.speak(msg);
    }

    function startRound(){
        if(running) return;
        running = true;
        time = {round_time};

        interval = setInterval(() => {
            time--;
            document.getElementById("time").innerText = time;

            if(time <= 0){
                stopRound();
                speak("Round over");
            }
        }, 1000);

        loopMoves();
    }

    function loopMoves(){
        if(!running) return;

        let move = moves[Math.floor(Math.random() * moves.length)];
        document.getElementById("cmd").innerText = move;
        speak(move);

        setTimeout(loopMoves, Math.random() * 2000 + 1000);
    }

    function stopRound(){
        running = false;
        clearInterval(interval);
    }
    </script>
    """

    components.html(html, height=300)


# =========================
# DRILL GENERATOR TAB
# =========================

with drills_tab:

    st.markdown(
        '<div class="feature-card"><h3>AI Drill Generator</h3></div>',
        unsafe_allow_html=True
    )

    level = st.selectbox(
        "Skill Level",
        ["Beginner", "High School", "College", "Advanced"]
    )

    focus = st.text_input(
        "Focus Area",
        value="Double leg takedown"
    )

    if st.button("Generate Drills"):

        prompt = f"""
Create a wrestling training plan.

Level: {level}
Focus: {focus}

Include:
- Warmup
- Technique drills
- Live situational drills
- Conditioning
- Coaching points

Make it structured for 30 minutes.
"""

        with st.spinner("Generating drills..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.markdown(response.text)
# ============================================
# Part 3/4 - Stats + Conditioning
# ============================================

# =========================
# STATS TAB
# =========================

with stats_tab:

    st.markdown(
        '<div class="feature-card"><h3>Match Stats Tracker</h3></div>',
        unsafe_allow_html=True
    )

    shots = st.number_input("Shot Attempts", min_value=0, value=5)
    finishes = st.number_input("Shots Finished", min_value=0, value=2)
    escapes = st.number_input("Escapes", min_value=0, value=1)
    reversals = st.number_input("Reversals", min_value=0, value=0)

    if st.button("Calculate Performance"):

        takedown_rate = (finishes / shots * 100) if shots > 0 else 0

        st.metric("Takedown Efficiency", f"{takedown_rate:.1f}%")
        st.metric("Total Scoring Actions", finishes + escapes + reversals)

        if takedown_rate < 40:
            st.warning("Focus: penetration step + finishing angles")
        elif takedown_rate < 70:
            st.info("Good base — refine finishes under pressure")
        else:
            st.success("Elite efficiency — maintain pressure style")


# =========================
# CONDITIONING TAB
# =========================

with st.expander("🔥 Impossible Mode Conditioning"):

    st.markdown(
        '<div class="feature-card"><h3>Impossible Mode</h3></div>',
        unsafe_allow_html=True
    )

    mode = st.selectbox(
        "Conditioning Type",
        [
            "Late Match Burnout",
            "Explosive Shots",
            "Grip Strength Fatigue",
            "No Rest Scrambles"
        ]
    )

    if st.button("Generate Workout"):

        prompt = f"""
Create a brutal wrestling conditioning workout.

Type: {mode}

Include:
- warmup
- main circuit
- rest intervals
- mental toughness cues
- duration 20-30 minutes

Make it intense but safe for athletes.
"""

        with st.spinner("Building workout..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.markdown(response.text)
# ============================================
# Part 4/4 - Nutrition + Final System
# ============================================

# =========================
# NUTRITION TAB
# =========================

with nutrition_tab:

    st.markdown(
        '<div class="feature-card"><h3>Weight Cut & Nutrition Planner</h3></div>',
        unsafe_allow_html=True
    )

    current_weight = st.number_input("Current Weight (lbs)", value=150.0)
    target_weight = st.number_input("Target Weight (lbs)", value=145.0)
    days_left = st.number_input("Days Until Weigh-In", min_value=1, value=7)

    food_log = st.text_area(
        "Today's Food Intake",
        value="Chicken, rice, vegetables, protein shake"
    )

    if st.button("Generate Nutrition Plan"):

        weight_diff = current_weight - target_weight

        if weight_diff <= 0:
            st.success("You are already on weight. Focus on recovery + performance.")
        else:
            st.metric("Total Weight to Cut", f"{weight_diff:.1f} lbs")
            st.metric("Daily Cut Target", f"{weight_diff/days_left:.2f} lbs/day")

            prompt = f"""
You are a sports nutrition coach for wrestlers.

Current weight: {current_weight}
Target weight: {target_weight}
Days left: {days_left}
Food log: {food_log}

Give:
- safe calorie guidance
- hydration strategy
- performance-safe weight cut plan
- what to avoid
- match day fueling tips

Keep it safe and athlete-focused.
"""

            with st.spinner("Calculating plan..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.markdown(response.text)


# =========================
# FINAL CLEANUP / FOOTER
# =========================

st.markdown("---")
st.caption("Wrestle AI Pro • Streamlit Prototype • Mobile Optimized Build")