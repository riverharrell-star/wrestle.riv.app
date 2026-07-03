import streamlit as st
import streamlit.components.v1 as components

# =========================
# PAGE SETUP (FULL SCREEN FIX)
# =========================

st.set_page_config(
    page_title="Wrestle AI Pro",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# FULL WIDTH + MOBILE FIX
st.markdown("""
<style>

html, body {
    width: 100% !important;
}

.block-container {
    padding: 0.5rem 1rem 2rem 1rem !important;
    max-width: 100% !important;
}

main {
    width: 100% !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🥋 Wrestle AI Pro")
st.caption("Offline Wrestling Training System (No API Required)")

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
# COACH
# =========================

with coach_tab:

    st.subheader("Wrestling Coach")

    style = st.selectbox("Style", ["Folkstyle", "Freestyle", "Greco", "BJJ"])
    position = st.selectbox("Position", ["Neutral", "Top", "Bottom", "Scramble"])
    question = st.text_area("Ask a question")

    if st.button("Get Advice"):

        q = question.lower()

        tips = []

        if "shoot" in q or "takedown" in q:
            tips.append("Work on level changes + penetration step + finishing to the corner")

        if "tired" in q or "gas" in q:
            tips.append("Do sprint intervals (20s work / 40s rest)")

        if "defense" in q:
            tips.append("Sprawl early + strong head position")

        if position == "Top":
            tips.append("Use wrist control + pressure breakdowns")

        if position == "Bottom":
            tips.append("Focus on stand-ups + hip heists")

        if not tips:
            tips.append("Work stance, motion, hand fighting, and pressure")

        st.write("### Advice")
        for t in tips:
            st.write("•", t)

# =========================
# VOICE TRAINER
# =========================

with voice_tab:

    st.subheader("Voice Stance Trainer")

    seconds = st.number_input("Round Time (sec)", 30, 300, 60)

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

    function speak(t){
        let msg = new SpeechSynthesisUtterance(t);
        msg.rate = 1.2;
        speechSynthesis.speak(msg);
    }

    function start(){
        if(running) return;
        running = true;
        time = {seconds};

        interval = setInterval(() => {
            time--;
            document.getElementById("time").innerText = time;
            if(time <= 0) stop();
        }, 1000);

        loop();
    }

    function loop(){
        if(!running) return;
        let m = moves[Math.floor(Math.random()*moves.length)];
        document.getElementById("cmd").innerText = m;
        speak(m);
        setTimeout(loop, 2000);
    }

    function stop(){
        running = false;
        clearInterval(interval);
        speechSynthesis.cancel();
    }
    </script>
    """

    components.html(html, height=520)

# =========================
# DRILLS
# =========================

with drills_tab:

    st.subheader("Drill Generator")

    level = st.selectbox("Level", ["Beginner", "High School", "College"])
    focus = st.text_input("Focus", "Double leg takedown")

    if st.button("Generate Drills"):

        base = {
            "Beginner": [
                "Stance & motion",
                "Basic shots (3x10)",
                "Wall pressure drill"
            ],
            "High School": [
                "Shot → finish chains",
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

    shots = st.number_input("Shots", 0, 100, 5)
    finishes = st.number_input("Finishes", 0, 100, 2)

    if st.button("Calculate"):

        rate = (finishes / shots * 100) if shots > 0 else 0

        st.metric("Finish Rate", f"{rate:.1f}%")

        if rate < 40:
            st.warning("Improve finishing angles + drive-through pressure")
        else:
            st.success("Good offensive efficiency")

# =========================
# NUTRITION
# =========================

with nutrition_tab:

    st.subheader("Weight Cut Planner")

    current = st.number_input("Current Weight", 100.0)
    target = st.number_input("Target Weight", 100.0)
    days = st.number_input("Days", 1)

    if st.button("Plan"):

        diff = current - target

        if diff <= 0:
            st.success("You are already on weight")
        else:
            st.metric("Total Cut", f"{diff:.1f} lbs")
            st.metric("Per Day", f"{diff/days:.2f} lbs/day")

            st.write("### Plan")
            st.write("• Clean diet (low sugar)")
            st.write("• Water early, taper late")
            st.write("• Daily light cardio")
            st.write("• High protein intake")