import streamlit as st
import os
import time
import tempfile
from google import genai
import streamlit.components.v1 as components

# =========================
# PAGE SETUP
# =========================

st.set_page_config(
    page_title="Wrestle AI Pro",
    page_icon="🥋",
    layout="centered"
)

st.title("🥋 Wrestle AI Pro")
st.caption("AI Wrestling Training System")

# =========================
# GEMINI CLIENT
# =========================

@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

try:
    client = get_client()
except Exception:
    st.error("Missing GEMINI_API_KEY in Streamlit secrets.")
    st.stop()

# =========================
# TABS
# =========================

tabs = st.tabs([
    "🤖 Coach",
    "🎥 Video",
    "🎤 Voice",
    "📋 Drills",
    "📊 Stats",
    "🍎 Nutrition"
])

coach_tab, video_tab, voice_tab, drills_tab, stats_tab, nutrition_tab = tabs

# =========================
# 🤖 COACH
# =========================

with coach_tab:

    st.subheader("AI Wrestling Coach")

    style = st.selectbox(
        "Style",
        ["Folkstyle", "Freestyle", "Greco", "BJJ"]
    )

    position = st.selectbox(
        "Position",
        ["Neutral", "Top", "Bottom", "Scramble"]
    )

    question = st.text_area("Ask a question")

    if st.button("Ask Coach") and question:

        prompt = f"""
You are an elite wrestling coach.

Style: {style}
Position: {position}

Question: {question}

Give:
- technical advice
- mistakes
- drills
- strategy
"""

        with st.spinner("Thinking..."):

            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.write(res.text)

# =========================
# 🎥 VIDEO ANALYSIS
# =========================

with video_tab:

    st.subheader("Match Video Analysis")

    video = st.file_uploader("Upload video", type=["mp4", "mov", "m4v"])

    if video:

        st.video(video)

        if st.button("Analyze Video"):

            with st.spinner("Processing..."):

                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(video.read())
                    path = tmp.name

                uploaded = client.files.upload(file=path)

                while True:
                    status = client.files.get(name=uploaded.name)
                    if status.state.name != "PROCESSING":
                        break
                    time.sleep(2)

                prompt = """
Analyze this wrestling match:

- strengths
- weaknesses
- takedowns
- defense issues
- conditioning
- 3 drills
"""

                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[uploaded, prompt]
                )

                st.success("Done")
                st.write(res.text)

                client.files.delete(name=uploaded.name)

# =========================
# 🎤 VOICE TRAINER
# =========================

with voice_tab:

    st.subheader("Voice Stance Trainer")

    seconds = st.number_input("Round Time", 30, 300, 60)

    html = f"""
    <div style="text-align:center;padding:20px;background:#111;color:white;border-radius:12px;">
        <h2 id="cmd">READY</h2>
        <p id="time">{seconds}</p>

        <button onclick="start()">Start</button>
        <button onclick="stop()">Stop</button>
    </div>

    <script>
    let time = {seconds};
    let running = false;
    let interval;

    const moves = ["Sprawl", "Shoot", "Circle", "Level Change", "Snap Down"];

    function speak(t){{
        let msg = new SpeechSynthesisUtterance(t);
        msg.rate = 1.2;
        speechSynthesis.speak(msg);
    }}

    function start(){{
        if(running) return;
        running = true;
        time = {seconds};

        interval = setInterval(() => {{
            time--;
            document.getElementById("time").innerText = time;
            if(time <= 0) stop();
        }}, 1000);

        loop();
    }}

    function loop(){{
        if(!running) return;
        let m = moves[Math.floor(Math.random()*moves.length)];
        document.getElementById("cmd").innerText = m;
        speak(m);
        setTimeout(loop, 2000);
    }}

    function stop(){{
        running = false;
        clearInterval(interval);
        speechSynthesis.cancel();
    }}
    </script>
    """

    components.html(html, height=300)

# =========================
# 📋 DRILLS
# =========================

with drills_tab:

    st.subheader("AI Drill Generator")

    level = st.selectbox(
        "Level",
        ["Beginner", "High School", "College"]
    )

    focus = st.text_input("Focus", "Double leg takedown")

    if st.button("Generate Drills"):

        prompt = f"""
Create wrestling drills:

Level: {level}
Focus: {focus}

Include warmup, technique, live drilling, conditioning.
"""

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.write(res.text)

# =========================
# 📊 STATS
# =========================

with stats_tab:

    st.subheader("Match Stats")

    shots = st.number_input("Shots", 0, 50, 5)
    finishes = st.number_input("Finishes", 0, 50, 2)

    if st.button("Calculate"):

        rate = (finishes / shots * 100) if shots > 0 else 0

        st.metric("Finish Rate", f"{rate:.1f}%")

# =========================
# 🍎 NUTRITION
# =========================

with nutrition_tab:

    st.subheader("Weight Cut Planner")

    w = st.number_input("Current Weight", 100.0)
    t = st.number_input("Target Weight", 100.0)
    d = st.number_input("Days", 1)

    if st.button("Plan"):

        diff = w - t

        if diff <= 0:
            st.success("You are on weight")
        else:
            st.metric("To Cut", f"{diff:.1f} lbs")
            st.metric("Per Day", f"{diff/d:.2f}")

        prompt = f"""
Wrestler cut plan:
From {w} to {t} in {d} days.
Give safe nutrition plan.
"""

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.write(res.text)