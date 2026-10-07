import streamlit as st
from database import init_db, register, authenticate
from university_data import DEPARTMENTS

st.set_page_config(page_title="Aditya360", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
init_db()

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
*{font-family:Poppins,sans-serif}.stApp{background:radial-gradient(circle at 85% 15%,#0c7a3b55,transparent 28%),linear-gradient(135deg,#031a20,#061b18 48%,#06301e);color:white}
.block-container{max-width:1250px;padding-top:1.15rem}
.logoBox{
    width:fit-content;max-width:380px;background:#ffffff;border-radius:20px;
    padding:9px 15px;margin:0 0 16px 0;border:1px solid #6ff7b1;
    box-shadow:0 10px 30px #0005,0 0 20px #35e58a22;
}
.logoBox img{display:block;width:100%;height:auto;max-height:112px;object-fit:contain}
.hero{padding:2px 0 10px}.tag{font-size:17px;color:#b8d6cc;margin-bottom:12px}
.quote{font-size:25px;font-weight:600;line-height:1.45;margin:10px 0 18px;color:#eafff3;max-width:1080px}
.quote b{color:#57f287}
@media(max-width:700px){
 .block-container{padding-top:.7rem}
 .logoBox{max-width:290px;border-radius:16px;padding:7px 12px;margin-bottom:12px}
 .logoBox img{max-height:90px}
 .tag{font-size:14px}.quote{font-size:19px}
}
.card{background:linear-gradient(145deg,#0a3536cc,#08251fcc);border:1px solid #2b9477;border-radius:22px;padding:22px;min-height:165px;box-shadow:0 12px 30px #0004}
.card h3{margin:0 0 8px;color:white}.card p{color:#b8d6cc}.green{color:#57f287}.footer{text-align:center;margin-top:28px;color:#a8c8bc}.venkys{font-size:25px;font-weight:800}.venkys span{color:#57f287}
div.stButton>button{border-radius:16px;border:1px solid #3abf8c;background:#0b332d;color:white;font-weight:600}
div[data-testid="stForm"]{background:#071d1ddd;border:1px solid #28745e;border-radius:22px;padding:20px}
</style>""", unsafe_allow_html=True)

def header():
    st.markdown("""
    <div class="logoBox">
      <img src="data:image/png;base64,{}" alt="Aditya360 AI Campus Assistant">
    </div>
    """.format(__import__("base64").b64encode(open("assets/aditya360_logo.png","rb").read()).decode()), unsafe_allow_html=True)
    st.markdown("""<div class="hero">
    <div class="tag">Your Intelligent Guide to Learning, Placements, Departments and Beyond</div>
    <div class="quote">“Data becomes valuable when it drives decisions. <b>AI becomes powerful when it turns those decisions into intelligent action.</b>”</div>
    </div>""",unsafe_allow_html=True)

if "user" not in st.session_state: st.session_state.user=None
if "page" not in st.session_state: st.session_state.page="home"

header()

if not st.session_state.user:
    c1,c2=st.columns([1.45,1])
    with c1:
        st.markdown("### Explore Aditya360")
        a,b=st.columns(2)
        with a:
            st.markdown('<div class="card"><h3>🏛️ University Information</h3><p>Academics, departments, facilities and campus guidance.</p></div>',unsafe_allow_html=True)
            st.markdown('<div class="card"><h3>💼 Placements & Careers</h3><p>Skills, training, career roadmaps and employability guidance.</p></div>',unsafe_allow_html=True)
        with b:
            st.markdown('<div class="card"><h3>🎓 Courses & Departments</h3><p>Explore programs, technical learning paths and career directions.</p></div>',unsafe_allow_html=True)
            st.markdown('<div class="card"><h3>📖 Smart Study Plan</h3><p>Personalized learning plans powered by Agentic AI.</p></div>',unsafe_allow_html=True)
    with c2:
        login, signup=st.tabs(["Student Login","Register"])
        with login:
            with st.form("login"):
                sid=st.text_input("Student ID")
                pw=st.text_input("Password",type="password")
                if st.form_submit_button("Access Aditya360",use_container_width=True):
                    u=authenticate(sid,pw)
                    if u:
                        st.session_state.user=u; st.rerun()
                    else: st.error("Invalid Student ID or password.")
        with signup:
            with st.form("register"):
                sid=st.text_input("Student ID",key="rsid")
                name=st.text_input("Full Name")
                email=st.text_input("Email")
                dept=st.selectbox("Department",list(DEPARTMENTS))
                year=st.selectbox("Year",["1st Year","2nd Year","3rd Year","4th Year","PG"])
                p1=st.text_input("Create Password",type="password")
                p2=st.text_input("Confirm Password",type="password")
                submit=st.form_submit_button("Create Student Account",use_container_width=True)
                if submit:
                    if p1!=p2: st.error("Passwords do not match.")
                    else:
                        ok,msg=register(sid,name,email,dept,year,p1)
                        (st.success if ok else st.error)(msg)
else:
    from agent import ask
    u=st.session_state.user
    top1,top2=st.columns([6,1])
    top1.markdown(f"### Welcome, {u['name']}  ·  `{u['student_id']}`  ·  {u['department']}")
    if top2.button("Logout",use_container_width=True):
        st.session_state.user=None; st.session_state.messages=[]; st.rerun()

    cards=st.columns(4)
    labels=[("🏛️","University Information","Admissions, academics & facilities"),
            ("🎓","Courses & Departments","Programs, skills & careers"),
            ("💼","Placements & Career","Training & roadmaps"),
            ("📖","Study Plan","Personalized learning")]
    for col,(icon,title,sub) in zip(cards,labels):
        with col: st.markdown(f'<div class="card"><h3>{icon} {title}</h3><p>{sub}</p></div>',unsafe_allow_html=True)

    st.markdown("### 🤖 Ask Aditya360")
    if "messages" not in st.session_state: st.session_state.messages=[]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    q=st.chat_input("Ask Aditya360...")
    if q:
        st.session_state.messages.append({"role":"user","content":q})
        with st.chat_message("user"): st.markdown(q)
        with st.chat_message("assistant"):
            with st.spinner("Aditya360 is thinking and selecting the right tool..."):
                try: ans=ask(q)
                except Exception as e: ans=f"I couldn't complete that request. {e}"
            st.markdown(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})

st.markdown('<div class="footer">Designed by <div class="venkys">Venkys<span>AI</span></div><small>DATA &nbsp; | &nbsp; IDEAS &nbsp; | &nbsp; INTELLIGENCE &nbsp; | &nbsp; IMPACT</small></div>',unsafe_allow_html=True)
