import streamlit as st
import streamlit.components.v1 as components

# =========================
# PAGE
# =========================

st.set_page_config(
    page_title="Wrestle AI Pro (No API)",
    page_icon="🥋",
    layout="centered"
)

st.title("🥋 Wrestle AI Pro (Offline Mode)")
st.caption("No API required — fully local version")

# =========================
# TABS
# =========================

tabs = st.tabs([
    "🤖 Coach",
    "🎤 Voice",
    "📋 Drills",
    "📊 Stats",
    "🍎 Nutrition"
])

coach_tab, voice_tab, drills_tab, stats_tab, nutrition_tab = tabs

# =========================
# 🤖 COACH (RULE BASED)
# =========================

with coach_tab:

    st.subheader("AI Wrestling Coach (Offline)")

    style = st.selectbox("Style", ["Folkstyle", "Freestyle", "Greco", "BJJ"])
    position = st.selectbox("Position", ["Neutral", "Top", "Bottom", "Scramble"])
    question = st.text_area("Ask something")

    if st.button("Ask Coach"):

        q = question.lower()

        advice = []

        if "shoot" in q or "takedown" in q:
            advice.append("Work level changes + penetration step + finish to corner")

        if "gas" in q or "tired" in q:
            advice.append("Improve conditioning: short explosive circuits (20–30 sec bursts)")

        if "defense" in q:
            advice.append("Sprawl early, head position, and underhook recovery")

        if "top" in position.lower():
            advice.append("Focus on wrist control + breakdown pressure")

        if "bottom" in position.lower():
            advice.append("Stand-ups, hip heist, and hand fighting")

        if not advice:
            advice.append("Focus on fundamentals: stance, motion, hand fighting, and pressure")

        st.write("### Coaching Advice")
        for a in advice:
            st.write("•", a)

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
# 📋 DRILLS (LOCAL GENERATOR)
# =========================

with drills_tab:

    st.subheader("Drill Generator")

    level = st.selectbox("Level", ["Beginner", "High School", "College"])
    focus = st.text_input("Focus", "Double leg")

    if st.button("Generate Drills"):

        drills = {
            "Beginner": [
                "Stance & motion (5 min)",
                "Level change reps (3x20)",
                "Basic shot entries",
                "Wall wrestling pressure drill"
            ],
            "High School": [
                "Penetration step series",
                "Shot → finish chain drilling",
                "Live situational starts",
                "Hand fighting rounds"
            ],
            "College": [
                "Chain wrestling sequences",
                "Scramble recovery drills",
                "Short offense bursts",
                "Mat return pressure drill"
            ]
        }

        st.write("### Plan")
        for d in drills[level]:
            st.write("•", d)

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

        if rate < 40:
            st.warning("Work on finishing angles and driving through")
        else:
            st.success("Good offensive efficiency")

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
            st.success("You are already on weight")
        else:
            st.metric("Total Cut", f"{diff:.1f} lbs")
            st.metric("Per Day", f"{diff/d:.2f} lbs/day")

            st.write("### Basic Plan")
            st.write("• Reduce sugar + processed foods")
            st.write("• Increase water early, taper before weigh-in")
            st.write("• Maintain protein for muscle retention")
            st.write("• Light cardio daily (20–30 min)")