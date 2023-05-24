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


st.set_page_config(page_title = "Auswirkungen von Corona auf die Publikationen in der DBLP", layout='wide', initial_sidebar_state='expanded')   #Muss erste Zeile von st. sein

@st.cache_resource(show_spinner="Lade die Daten aus der Datenbank...")          #https://docs.streamlit.io/library/advanced-features/caching
def db_connection():
    return st.experimental_connection(name = "dblpppppp", type="sql", max_entries=None, ttl=None, autocommit=True)


conn = db_connection()

@st.cache_data              #Cache diese Querry. Geht nur als Funktion.
def table_publications():
    return conn.query("select * from publications")

@st.cache_data
def all_titles():
    return conn.query("select title from publications")

def all_pubyear():
    return conn.query("select pubyear from publications")

@st.cache_data
def all_mdate():
    return conn.query("select mdate from publications")

@st.cache_data
def all_publtype():
    return conn.query("select publtype from publications")


@st.cache_data
def all_authors():
    return conn.query("select name from authors")


#table_publications = table_publications()               #Bin mir unsicher ob das so gut ist, werde mich informieren.

all_titles = all_titles()

all_pubyear = all_pubyear()

all_mdate = all_mdate()

all_publtype = all_publtype()

all_authors = all_authors()

table_publications = table_publications()


st.title("Auswirkungen von Corona auf die Publikationen in der DBLP")


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


info1, info2, info3, info4 = st.columns(4, gap = "medium")  #Widgets, "einfache" Infos, z.b. Anzahl Authoren


plot1, plot2 = st.columns(2, gap = "large")     #2x2 Matrix an Plots

plot3, plot4 = st.columns(2, gap = "large")


def readDataToList(all_publications):
    most_common_num = 10
    keywords = []
    word_list = all_publications.split()
    for word in word_list:
        if "." in word:
            word = word.replace(".", "")
        if "-" in word:
            word = word.replace("-", "")
        if word.lower() not in stop_words:
            keywords.append(word.lower())
    new_list = list(filter(lambda x: x != "", keywords))            #"" ist ein eigener Char in Keywords, darum wird das auch ersetzt.
    # with open("keywords.txt", "w", encoding="utf-8") as file:
    # file.write(str(new_list))
    counter = collections.Counter(new_list)                         #Gibt ein Dict aus. Das Wort ist der Key, und die Häufigkeit das Value.
    most_common = counter.most_common(most_common_num)
    return most_common                                              #Sieht so aus [('none', 528876), ('home', 12867), ('page', 12866), ('data', 2192)]




with info1:
    st.metric(label = "Publikationen", value = len(all_titles))

with info2:
    st.metric(label="Authoren", value=len(all_authors))

with plot1:
    st.bar_chart()
    with st.expander("See explanation"):
        st.write("Das siehts du hier wegen xyz")
        pass

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


    plot_fünf = st.header("Plot Nummer 5")


with tab2:
    plot_detail = st.header("Detailplot Nummer 1")


    #publications_per_year = table_publications.pubyear.where(table_publications.pubyear > "1993")
    st.bar_chart(all_pubyear)


    plot_detail2 = st.header("Detailplot Nummer 2")

    just_publications = table_publications.drop(["mdate", "publtype", "key", "pubyear"], axis = 1)
    #print(just_publications.describe())
    all_publications = just_publications.to_string(decimal = ";", index = False)           #Series_to_string geht leider nicht, darum so

    hist_values = readDataToList(all_publications)


    #values = all_publtype.value_counts()
    #labels = ["data", "disambiguation", "edited", "encyclopedia", "group", "habil", "informal", "informal withdrawn", "noshow", "software", "survey", "withdrawn", "none"]

    st.bar_chart(data = all_publtype)

    def histogram(histvalues):
        histdf = pd.DataFrame(data = histvalues, columns=["word", "counting"])          #Wandle Liste in df zurück
        st.bar_chart(data = histdf.counting)
        st.write(histdf)

    histogram(hist_values)

#Um das Dashobard zu starten, folgende Zeile in die Anaconda Powershell, am Ort des CodingProjekt, eingeben:
#streamlit run Streamlit_App.py



#Damit konnte ich Streamlit ausführen, bei mir war die Version veraltet:
#pip install --upgrade streamlit

