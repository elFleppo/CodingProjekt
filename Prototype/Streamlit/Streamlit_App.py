import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from numba import jit
import psycopg as psycopg
import collections
from nltk.corpus import stopwords
from matplotlib import pyplot as plt

stop_words = set(stopwords.words('english'))

#ÜBERSICHT:
# 3 Tabellen: authored, authors, publications
#authored: ORCID, key, name, title
#authors: orcid, name
#publications: key, title, pupyear, mdate, publtype

#conn = psycopg.connect(host="localhost", dbname="dblp", user="postgres", password="")


st.set_page_config(page_title = "Auswirkungen von Corona auf die Publikationen in der DBLP", layout='wide', initial_sidebar_state='expanded')


conn = st.experimental_connection(name = "dblp", type="sql", max_entries=None, ttl=None, autocommit=True)


st.title("Auswirkungen von Corona auf die Publikationen in der DBLP")


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


info1, info2, info3, info4 = st.columns(4, gap = "medium")  #Widgets, "einfache" Infos, z.b. Anzahl Authoren


plot1, plot2 = st.columns(2, gap = "large")     #2x2 Matrix an Plots

plot3, plot4 = st.columns(2, gap = "large")


df = conn.query("select * from publications")

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

    def selectbox():
        sidebar_selectbox = st.selectbox("Wähle eine Option", ("Option 1", "Option 2", "Option 3"))
        return "test"
    selectbox()

    plot_zwei = st.header("Plot Nummer 2")

    def slider():
        sidebar_slider = st.slider('Zeit', 0, 24, 0)
        return "test"

    slider()


    plot_drei = st.header("Plot Nummer 3")

    def button():
        sidebar_button = st.button("Hit me")
        return "test"
    button()

    def checkbox():
        sidebar_checkbox = st.checkbox("Zeig etwas an")
        return "test"

    checkbox()


    plot_vier = st.header("Plot Nummer 4")

    def date_input():
        sidebar_date_input = st.date_input("test")
        return "test"

    date_input()


    plot_vier = st.header("Plot Nummer 5")


with tab2:
    plot_detail = st.header("Detailplot Nummer 1")
    counter = df.pubyear.value_counts()
    st.line_chart(counter)

    plot_detail2 = st.header("Detailplot Nummer 2")
    all_publications= df.title.to_string()

    def readDataToList(all_publications):
        most_common_num = 10
        keywords = []
        word_list = all_publications.split()
        for word in word_list:
            if "('" in word:
                word = word.replace("('", "")
            if ".',)" in word:
                word = word.replace(".',)", "")
            if "," in word:
                word = word.replace(",", "")
            if ":" in word:
                word = word.replace(":", "")
            if "..." in word:
                word = word.replace("...", "")
            if word.lower() not in stop_words:
                keywords.append(word.lower())
        counter = collections.Counter(keywords)
        most_common = counter.most_common(most_common_num)
        return most_common


    #st.write(readDataToList(all_publications))

    histvalues = readDataToList(all_publications)

    def histogram(histvalues):
        histdf = pd.DataFrame(data = histvalues, columns=["word", "counting"])
        st.bar_chart(data = histdf.counting)
        #st.write(histdf)

    histogram(histvalues)

#Um das Dashobard zu starten, folgende Zeile in die Anaconda Powershell, am Ort des CodingProjekt, eingeben:
#streamlit run Streamlit_App.py



#Damit konnte ich Streamlit ausführen, bei mir war die Version veraltet:
#pip install --upgrade streamlit

