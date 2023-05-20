import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from numba import jit
import psycopg as psycopg

conn = psycopg.connect(host="localhost", dbname="dblp", user="postgres", password="")

cursor = conn.cursor()

st.set_page_config(page_title = "Auswirkungen von Corona auf die Publikationen in der DBLP", layout='wide', initial_sidebar_state='expanded')

st.title('Auswirkungen von Corona auf die Publikationen in der DBLP')

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


info1, info2, info3, info4 = st.columns(4, gap = "medium")


plot1, plot2 = st.columns(2, gap = "large")

plot3, plot4 = st.columns(2, gap = "large")

df = pd.DataFrame(np.random.randint(0,20,size=(10000, 15)), columns=list('ABCDEFGHIJKLMNO'))

eins = df.A

zwei = df.B


with info1:
    cursor.execute("SELECT title FROM publications")
    all_titles = cursor.fetchall()
    st.metric(label = "Publikationen", value = len(all_titles))

with info2:
    cursor.execute("SELECT name FROM authors")
    all_authors = cursor.fetchall()
    st.metric(label="Authoren", value=len(all_authors))

with plot1:
    st.line_chart(eins)
    with st.expander("See explanation"):
        st.write("Das siehts du hier wegen xyz")

with plot2:
    st.bar_chart(eins)

with plot3:
    st.area_chart(eins)

with plot4:
    st.line_chart(zwei)

plot_eins = st.sidebar.header("Plot Nummer 1")

def selectbox(df):
    sidebar_selectbox = st.sidebar.selectbox("Wähle eine Option", ("Option 1", "Option 2", "Option 3"))
    return df
selectbox(df)

plot_zwei = st.sidebar.header("Plot Nummer 2")

def slider(df):
    sidebar_slider = st.sidebar.slider('Zeit', 0, 24, 0)
    return df

slider(df)


plot_drei = st.sidebar.header("Plot Nummer 3")

def button(df):
    sidebar_button = st.sidebar.button("Des isch a Knopf")
    return df
button(df)

def checkbox(df):
    sidebar_checkbox = st.sidebar.checkbox("Zeig etwas an")
    return df.A

checkbox(df)


plot_vier = st.sidebar.header("Plot Nummer 4")

def date_input(df):
    sidebar_date_input = st.sidebar.date_input("test")
    return df

date_input(df)


plot_vier = st.sidebar.header("Plot Nummer 5")







#Um das Dashobard zu starten, folgende Zeile in die Anaconda Powershell, am Ort des CodingProjekt, eingeben:
#streamlit run Streamlit_App.py



#Damit konnte ich Streamlit ausführen, bei mir war die Version veraltet:
#pip install --upgrade streamlit

