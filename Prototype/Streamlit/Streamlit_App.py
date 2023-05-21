import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from numba import jit
import psycopg as psycopg
from matplotlib import pyplot as plt


#conn = psycopg.connect(host="localhost", dbname="dblp", user="postgres", password="")


st.set_page_config(page_title = "Auswirkungen von Corona auf die Publikationen in der DBLP", layout='wide', initial_sidebar_state='expanded')


conn = st.experimental_connection(name = "dblp", type="sql", max_entries=None, ttl=None, autocommit=True)


st.title("Auswirkungen von Corona auf die Publikationen in der DBLP")


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


info1, info2, info3, info4 = st.columns(4, gap = "medium")  #Widgets, "einfache" Infos, z.b. Anzahl Authoren


plot1, plot2 = st.columns(2, gap = "large")

plot3, plot4 = st.columns(2, gap = "large")


df = conn.query("select * from publications")
st.dataframe(df)

with info1:
    all_publications = conn.query("select title from publications")
    st.metric(label = "Publikationen", value = len(all_publications))

with info2:
    all_authors = conn.query("select name from authors")
    st.metric(label="Authoren", value=len(all_authors))

with plot1:
    st.line_chart(df.pubyear)
    with st.expander("See explanation"):
        st.write("Das siehts du hier wegen xyz")

with plot2:
    st.bar_chart(df.pubyear)

with plot3:
    st.area_chart(df.pubyear)

with plot4:
    st.line_chart(df.pubyear)

tab1, tab2 = st.sidebar.tabs(["Eingabe", "Detail Bar"])

with tab1:
    st.header("Plot Nummer 1")

    def selectbox(df):
        sidebar_selectbox = st.selectbox("Wähle eine Option", ("Option 1", "Option 2", "Option 3"))
        return df.pubyear
    selectbox(df.pubyear)

    plot_zwei = st.header("Plot Nummer 2")

    def slider(df):
        sidebar_slider = st.slider('Zeit', 0, 24, 0)
        return df.pubyear

    slider(df.pubyear)


    plot_drei = st.header("Plot Nummer 3")

    def button(df):
        sidebar_button = st.button("Hit me")
        return df.pubyear
    button(df.pubyear)

    def checkbox(df):
        sidebar_checkbox = st.checkbox("Zeig etwas an")
        return df.pubyear

    checkbox(df.pubyear)


    plot_vier = st.header("Plot Nummer 4")

    def date_input(df):
        sidebar_date_input = st.date_input("test")
        return df.pubyear

    date_input(df.pubyear)


    plot_vier = st.header("Plot Nummer 5")


with tab2:
    plot_detail = st.header("Detailplot Nummer 1")


    plot_detail2 = st.header("Detailplot Nummer 2")




#Um das Dashobard zu starten, folgende Zeile in die Anaconda Powershell, am Ort des CodingProjekt, eingeben:
#streamlit run Streamlit_App.py



#Damit konnte ich Streamlit ausführen, bei mir war die Version veraltet:
#pip install --upgrade streamlit

