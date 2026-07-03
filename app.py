import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Wrestle AI Pro", page_icon="🥋", layout="wide")

st.markdown("""
<style>
.block-container{max-width:100%!important;padding:1rem;}
</style>
""", unsafe_allow_html=True)

st.title("🥋 Wrestle AI Pro")
tabs = st.tabs(["Coach","Voice","Drills","Stats","Weight"])

with tabs[0]:
    st.header("Coach")
    q=st.text_area("Question")
    if st.button("Get Advice"):
        st.write("Focus on stance, motion, hand fighting, level changes, and finishing through the hips.")

with tabs[1]:
    st.header("Voice Trainer")
    html="""
    <h2 id='cmd'>READY</h2>
    <button onclick='go()'>Start</button>
    <script>
    const moves=['Sprawl','Shoot','Circle','Snap Down','Level Change'];
    function go(){
      setInterval(()=>{
        let m=moves[Math.floor(Math.random()*moves.length)];
        document.getElementById('cmd').innerText=m;
        speechSynthesis.cancel();
        speechSynthesis.speak(new SpeechSynthesisUtterance(m));
      },2000);
    }
    </script>
    """
    components.html(html,height=400)

with tabs[2]:
    st.header("Drills")
    focus=st.text_input("Focus","Single Leg")
    if st.button("Generate Drills"):
        st.write("- Stance & motion 5 min")
        st.write("- %s reps 10 min"%focus)
        st.write("- Live goes 10 min")
        st.write("- Conditioning 5 min")

with tabs[3]:
    st.header("Stats")
    shots=st.number_input("Shots",0,100,5)
    fins=st.number_input("Finishes",0,100,2)
    if st.button("Calculate"):
        rate=(fins/shots*100) if shots else 0
        st.metric("Finish %",f"{rate:.1f}%")

with tabs[4]:
    st.header("Weight Manager")
    cur=st.number_input("Current Weight",100.0,350.0,160.0)
    goal=st.number_input("Goal Weight",100.0,350.0,150.0)
    days=st.number_input("Days Until Weigh-In",1,90,14)
    water=st.slider("Water (oz)",0,200,80)
    sleep=st.slider("Sleep (hours)",0.0,12.0,8.0)
    if st.button("Build Plan"):
        diff=max(cur-goal,0)
        st.metric("Weight to Lose",f"{diff:.1f} lb")
        st.metric("Average / Day",f"{diff/days:.2f} lb")
        if diff/days>1:
            st.warning("Very aggressive target. Consider a safer pace with your coach.")
        elif diff>0:
            st.success("Steady goal.")
        else:
            st.success("On weight.")
        st.write("### Daily Checklist")
        st.checkbox("Drink enough water", value=water>=100, disabled=True)
        st.checkbox("Sleep 8+ hours", value=sleep>=8, disabled=True)
        st.write("- Lean protein")
        st.write("- Vegetables")
        st.write("- Avoid sugary drinks")
