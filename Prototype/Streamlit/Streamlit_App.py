import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
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


st.set_page_config(page_title = "Auswirkungen von Corona auf die Publikationen in der DBLP", layout='wide', initial_sidebar_state='expanded')   #Muss erste Zeile von st. sein

def db_connection():
    return st.experimental_connection(name = "dblpppppp", type="sql", max_entries=None, ttl=None, autocommit=True)


conn = db_connection()

table_publications = conn.query("select * from publications")

all_titles = conn.query("select title from publications")

all_pubyear = conn.query("select pubyear from publications")

all_mdate = conn.query("select mdate from publications")

all_publtype = conn.query("select publtype from publications")

all_authors = conn.query("select name from authors")



st.title("Auswirkungen von Corona auf die Publikationen in der DBLP")


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


info1, info2, info3, info4 = st.columns(4, gap = "medium")  #Widgets, "einfache" Infos, z.b. Anzahl Authoren


plot1, plot2 = st.columns(2, gap = "large")     #2x2 Matrix an Plots

plot3, plot4 = st.columns(2, gap = "large")



@st.cache_data
def readDataToList(query, number):
    all_titles_string = query.to_string(decimal=";", index=False)
    keywords = []
    word_list = all_titles_string.split()
    for word in word_list:
        if "." in word:
            word = word.replace(".", "")
        if word.lower() not in stop_words:
            keywords.append(word.lower())
    keywords = list(filter(lambda x: x != "", keywords))            #"" ist ein eigener Char in Keywords, darum wird das auch ersetzt.
    #with open("keywords.txt", "w", encoding="utf-8") as file:
        #file.write(str(keywords))
    counter = collections.Counter(keywords)                         #Gibt ein Dict aus. Das Wort ist der Key, und die Häufigkeit das Value.
    most_common_keywords = counter.most_common(number)
    #st.write(most_common_keywords)
    return most_common_keywords                                              #Sieht so aus [('none', 528876), ('home', 12867), ('page', 12866), ('data', 2192)]

hist_values = readDataToList(all_titles, 10)

def keyword_Lineplot(query):
    bool_keyword = all_titles["title"].str.contains("data", case = False, flags = 0)    #Gibt True und False zurück. Wörter mit Bindestrich werden hier glaub auch dazugezählt! Darum sinds mehr.
    keyword_year = all_pubyear.merge(bool_keyword, left_index=True, right_index=True)
    keyword_True = keyword_year.loc[keyword_year.title, :]        #Filtere nach True.
    keyword_per_year = keyword_True.groupby("pubyear").sum()      
    st.line_chart(keyword_per_year)

keyword_Lineplot(all_titles)

with info1:
    st.metric(label = "Publikationen", value = len(all_titles))

with info2:
    st.metric(label="Authoren", value=len(all_authors))

with plot1:

    keywords = []
    keywords_valcount = []

    for i in hist_values:
        keywords.append(i[0])
        keywords_valcount.append(i[1])

    fig, ax = plt.subplots()
    ax.plot(keywords, keywords_valcount)

    st.pyplot(fig)


with plot2:
    #ZWEITER PLOT HIER
    pass

with plot3:
    #DRITTER PLOT HIER
    pass

with plot4:
    #VIERTER PLOTT HIER
    pass


##################################################### S I D E B A R ####################################################


tab1, tab2 = st.sidebar.tabs(["Eingabe", "Detail Bar"])


with tab1:
    st.header("Plot Nummer 1")

    def selectbox():
        sidebar_selectbox = st.selectbox("Wähle ein Keyword", (keywords[0], keywords[1], keywords[2], keywords[3], keywords[4]))
        return sidebar_selectbox
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


    plot_fünf = st.header("Plot Nummer 5")


with tab2:
    plot_detail = st.header("Detailplot Nummer 1")


    #publications_per_year = table_publications.pubyear.where(table_publications.pubyear > "1993")
    st.bar_chart(all_pubyear)


    plot_detail2 = st.header("Detailplot Nummer 2")


    def histogram(hist_values):
        histdf = pd.DataFrame(data=hist_values, columns=["word", "counting"])  # Wandle Liste in df zurück
        st.bar_chart(data=histdf.counting)
        st.write(histdf)

        #histogram(hist_values)



    #values = all_publtype.value_counts()
    #labels = ["data", "disambiguation", "edited", "encyclopedia", "group", "habil", "informal", "informal withdrawn", "noshow", "software", "survey", "withdrawn", "none"]

    st.bar_chart(data = all_publtype)



#Um das Dashobard zu starten, folgende Zeile in die Anaconda Powershell, am Ort des CodingProjekt, eingeben:
#streamlit run Streamlit_App.py



#Damit konnte ich Streamlit ausführen, bei mir war die Version veraltet:
#pip install --upgrade streamlit

