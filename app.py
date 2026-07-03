import streamlit as st
import streamlit.components.v1 as components

# =========================
# PAGE CONFIG (FULL WIDTH FIX)
# =========================

st.set_page_config(
    page_title="Wrestle AI Pro",
    page_icon="🥋",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding: 1rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🥋 Wrestle AI Pro")
st.caption("Fully Working Offline Wrestling Trainer")

# =========================
# TABS
# =========================

tabs = st.tabs([
    "Coach",
    "Voice",
    "Drills",
    "Stats",
    "Nutrition"
])

coach_tab, voice_tab, drills_tab, stats_tab, nutrition_tab = tabs

# =========================
# COACH (NO API)
# =========================

with coach_tab:

    st.subheader("Wrestling Coach")

    style = st.selectbox("Style", ["Folkstyle", "Freestyle", "Greco", "BJJ"])
    position = st.selectbox("Position", ["Neutral", "Top", "Bottom", "Scramble"])
    question = st.text_area("Ask a question")

    if st.button("Get Advice"):

        q = question.lower()

        output = []

        if "takedown" in q or "shoot" in q:
            output.append("Improve level changes + penetration step + finish to corner")

        if "tired" in q or "gas" in q:
            output.append("Do sprint intervals (20s on / 40s off) for conditioning")

        if "defense" in q:
            output.append("Focus on sprawl timing + head position")

        if position == "Top":
            output.append("Use wrist control + pressure breakdowns")

        if position == "Bottom":
            output.append("Work stand-ups + hip heists")

        if not output:
            output.append("Focus on stance, motion, and hand fighting")

        st.write("### Advice")
        for o in output:
            st.write("•", o)

# =========================
# VOICE TRAINER (FIXED SIZE)
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

    components.html(html, height=500)

# =========================
# DRILLS
# =========================

with drills_tab:

    st.subheader("Drill Builder")

    level = st.selectbox("Level", ["Beginner", "High School", "College"])
    focus = st.text_input("Focus", "Double leg")

    if st.button("Generate"):

        base = {
            "Beginner": [
                "Stance + motion (5 min)",
                "Basic shots (3x10)",
                "Wall pressure drill"
            ],
            "High School": [
                "Shot → finish chain",
                "Hand fighting rounds",
                "Live situational starts"
            ],
            "College": [
                "Chain wrestling",
                "Scramble drills",
                "Short offense bursts"
            ]
        }

        st.write("### Plan")
        for d in base[level]:
            st.write("•", d)

# =========================
# STATS
# =========================

with stats_tab:

    st.subheader("Match Stats")

    shots = st.number_input("Shots", 0, 50, 5)
    finishes = st.number_input("Finishes", 0, 50, 2)

    if st.button("Calculate"):

        rate = (finishes / shots * 100) if shots > 0 else 0

        st.metric("Finish Rate", f"{rate:.1f}%")

        if rate < 40:
            st.warning("Work on finishing angles")
        else:
            st.success("Good offense")

# =========================
# NUTRITION
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
            st.metric("Total Cut", f"{diff:.1f} lbs")
            st.metric("Per Day", f"{diff/d:.2f} lbs/day")

            st.write("### Plan")
            st.write("• Reduce sugar + junk food")
            st.write("• Increase water early, taper late")
            st.write("• Light cardio daily")
            st.write("• Keep protein high")