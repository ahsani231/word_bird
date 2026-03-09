import streamlit as st
import random
import time
import chime


words = {
"Country Name": ["pakistan", "china", "indonesia", "japan", "south korea"],
"Movie Name": ["harry potter", "titanic", "dispicable me", "gladiator", "interstellar"],
"PC Part": ["processor", "motherboard", "graphics card", "powersupply", "ram"],
"Animal": ["elephant", "giraffe", "kangaroo", "dolphin", "tiger"],
"Fruit": ["pineapple", "strawberry", "watermelon", "mango", "banana"]
}

letters="qwertyuiopasdfghjklzxcvbnm"

st.markdown("""
<style>
    div[aria-label="dialog"] > button[aria-label="Close"]{display:none;}
    [data-testid="stColumn"] {max-width:50}
    div[data-testid="stLayoutWrapper"] > div[data-testid="stHorizontalBlock"] {display:flex;justify-content:center;}
    .stColumn.st-emotion-cache-13tbzbm.e12zf7d52{max-width:50px;background-color:#91ffa4;height:50px;width:auto;border-radius:10px;box-shadow:inset 0 2px 4px rgba(0,0,0,0.5);}
    .st-key-display div[data-testid="stHeadingWithActionElements"] {border-radius:10px;box-shadow:inset 0 1px 3px rgba(0,0,0,0.2);background-color:#E4CFFF;text-align:center;margin-top:50px;}
    h1, p,h2,div{text-align: center;padding:0px;}
    p{font-size:20px;}
    div[data-testid="stButton"] {width:50px;height:50px;border-radius:10px;background-color:#E4CFFF;border:1px solid black}
    .st-key-pop1 div[data-testid="stButton"],.st-key-pop2 div[data-testid="stButton"]{height:auto;width:100px;}
    .st-key-cato div[data-testid="stMarkdownContainer"] {width:50%;height:55px; background-color:#004e7a; font-size:30px;margin:auto;position:absolute;bottom:-68px;left:25%;border-radius:30px 30px 0px 0px;border:1px solid black;}
    .st-key-cato p{margin:0;color:white;}
    .st-key-body {background-image: linear-gradient(to top,#a2e1fc, #e3f7ff);padding-left:20px;padding-right:30px;border-radius:60px;}
    .st-key-body {}
    header {visibility: hidden;}
</style>

""", unsafe_allow_html=True)

st.set_page_config(layout="wide",page_title="Word Bird",page_icon="images/owl.png",)

with st.container(key='body'):
    col1,col2=st.columns([1,2])

    if "chance" not in st.session_state:
            st.session_state["chance"]=4
    
    
    with col1:
        if st.session_state["chance"]==4:
            st.image('images/1.png',width=600)
        if st.session_state["chance"]==3:
            st.image('images/2.png',width=600)
        if st.session_state["chance"]==2:
            st.image('images/3.png',width=600)
        if st.session_state["chance"]==1:
            st.image('images/4.png',width=600)
        if st.session_state["chance"]==0:
            st.image('images/5.png',width=600)
    
    
    with col2:
        if "category" not in st.session_state:
            
            category=random.choice(list(words.keys()))
            word = words[category][random.randint(0,len(words[category])-1)]
            st.session_state["category"]=category
            st.session_state['word']=word

        category = st.session_state["category"]
        word = st.session_state["word"]

        if "display" not in st.session_state:
            display=("_"*len(word))
            for i , let in enumerate(word):
                if let == " ":
                    display=display[:i]+"-"+display[i+1:]
            st.session_state["display"]=display
        display=st.session_state["display"]

        if "streak" not in st.session_state:
            st.session_state["streak"]=0
        streak=st.session_state["streak"]

        for d in letters:
            if d not in st.session_state:
                st.session_state[d]=False


        chance = st.session_state["chance"]
        st.title("Chances")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            if chance<=3:
                st.subheader("❌")
        with col2:
            if chance<=2:
                st.subheader("❌")
        with col3:
            if chance<=1:
                st.subheader("❌")
        with col4:
            if chance<=0:
                st.subheader("❌")

        with st.container(key="cato"):
            st.write(category)
        with st.container(key="display"):
            st.header(" ".join(display))

        if chance == 0:
            time.sleep(1)
            @st.dialog("Out of chances",dismissible=False)
            def lose():
                st.header("🚫Faild to Guess")
                st.error(f"word was {word}")
                st.write(f"You ended with streak of {streak}")
                if st.button("Try Again",key="pop1"): 
                    st.session_state["streak"]=0
                    del st.session_state["display"]
                    del st.session_state["chance"]
                    del st.session_state["category"]
                    for d in letters:
                            del st.session_state[d]
                    st.rerun()
            lose()


        if "_" not in display:
            time.sleep(1)
            @st.dialog("Win")
            def win():
                st.header("you gussed it!!👏")
                st.success(f"word was {word}")
                if st.button("Next",key="pop2"): 
                    st.session_state["streak"]+=1
                    del st.session_state["display"]
                    del st.session_state["chance"]
                    del st.session_state["category"]
                    for d in letters:
                            del st.session_state[d]
                    st.rerun()
            win()

        st.write(" ")
        st.write(" ")

        cols=st.columns(10)
        for i,l in enumerate(letters):
            if i<10:
                col=cols[i%10]
            elif i<19:
                col=cols[(i+1)%10]
            else:
                col=cols[(i+3)%10]
            with col:
                bt=st.button(l.capitalize(),disabled=st.session_state[l])
                if bt:
                    st.session_state[l]=True
                    for num,letter in enumerate(word):
                        if letter==l:
                            display=display[:num]+l+display[num+1:]
                    if l not in word:
                        chime.theme('mario')
                        chime.warning()
                        chance-=1
                    else:
                        chime.theme('mario')
                        chime.success()
                    st.session_state["chance"]=chance
                    st.session_state["display"]=display
                    st.rerun()

        st.title(f"Your Winning Streak {streak}")
    
        





