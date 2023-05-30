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


################################################ O V E R V I E W #######################################################

# 3 Tabellen: authored, authors, publications
#authored: ORCID, key, name, title
#authors: orcid, name
#publications: key, title, pupyear, mdate, publtype

#conn = psycopg.connect(host="localhost", dbname="dblp", user="postgres", password="")


############################################# S E T U P ################################################################

st.set_page_config(page_title = "Was für Themen haben in den letzten Jahren einen Zuwachs an Publikationen erhalten.", layout='wide', initial_sidebar_state='expanded')   #Muss erste Zeile von st. sein


st.title("Was für Themen haben in den letzten Jahren einen Zuwachs an Publikationen erhalten.")


with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


info1, info2, info3, info4 = st.columns(4, gap = "medium")  #Widgets, "einfache" Infos, z.b. Anzahl Authoren


plot1, plot2 = st.columns(2, gap = "large")     #2x2 Matrix an Plots

plot3, plot4 = st.columns(2, gap = "large")


#################################################### S Q L #############################################################
@st.cache_resource
def db_connection():
    return st.experimental_connection(name = "dblpppppp", type="sql", max_entries=None, ttl=None, autocommit=True)


conn = db_connection()

table_publications = conn.query("select * from publications")

all_titles = conn.query("select title from publications")

all_pubyear = conn.query("select pubyear from publications")

all_mdate = conn.query("select mdate from publications")

all_publtype = conn.query("select publtype from publications")

all_authors = conn.query("select name from authors")

df_publtype = conn.query("SELECT pubyear, publtype, COUNT(publtype) FROM publications WHERE pubyear != 'None' AND publtype != 'habil' GROUP BY pubyear, publtype")

df_publPerYear = conn.query("SELECT pubyear, COUNT(pubyear) FROM publications WHERE pubyear != 'None' GROUP BY pubyear")


############################################### F U N C T I O N S ######################################################


@st.cache_data
def readDataToList(query, number):
    non_keywords = ["none", "home", "page"]
    stop_words = set(stopwords.words('english'))
    all_titles_string = query.to_string(decimal=";", index=False)
    keywords = []
    word_list = all_titles_string.split()
    for word in word_list:
        if "." in word:
            word = word.replace(".", "")
        if word.lower() not in stop_words and word.lower() not in non_keywords:
            keywords.append(word.lower())
    keywords = list(filter(lambda x: x != "", keywords))            #"" ist ein eigener Char in Keywords, darum wird das auch ersetzt.
    #with open("keywords.txt", "w", encoding="utf-8") as file:
        #file.write(str(keywords))
    counter = collections.Counter(keywords)                         #Gibt ein Dict aus. Das Wort ist der Key, und die Häufigkeit das Value.
    most_common_keywords = counter.most_common(number)
    return most_common_keywords                                              #Sieht so aus [('none', 528876), ('home', 12867), ('page', 12866), ('data', 2192)]


hist_values = readDataToList(all_titles, 10)

keywords = []
keywords_valcount = []

for i in hist_values:
    keywords.append(i[0])
    keywords_valcount.append(i[1])


@st.cache_data
def keyword_per_year(keyword):
        bool_keyword = all_titles["title"].str.contains(keyword, case = False, flags = 0)    #Gibt True und False zurück. Wörter mit Bindestrich werden hier glaub auch dazugezählt! Darum sinds mehr.
        keyword_year = all_pubyear.merge(bool_keyword, left_index=True, right_index=True)
        keyword_True = keyword_year.loc[keyword_year.title, :]          #Filtere nach True.
        keyword_per_year = keyword_True.groupby("pubyear").sum()           #Gruppiere nach pubyear und gib die Anzahl zurück
        return keyword_per_year


def analyzePublType(df_publtype):
    keywords = []
    for i in range(0, len(df_publtype.index)):
        if df_publtype['publtype'][i] not in keywords:
            keywords.append(df_publtype['publtype'][i])
    years = []
    for j in range(0, len(df_publtype.index)):
        if df_publtype['pubyear'][j] not in years:
            years.append(df_publtype['pubyear'][j])
    years = sorted(years)
    firstYear = int(years[0])
    lastYear = int(years[len(years) - 1])
    publications = [[],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    []]
    n = 0
    for k in range(firstYear, lastYear):
        for l in keywords:
            for m in range(0, len(df_publtype.index)):
                if df_publtype['publtype'][m] == l:
                    if df_publtype['pubyear'][m] == k:
                        publications[n].append(df_publtype['count'][m])
                    else:
                        publications[n].append(0)
        n += 1
    print(publications)

    # create plot
    fig, ax = plt.subplots()
    im = ax.imshow(publications)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(years)), labels=years)
    ax.set_yticks(np.arange(len(keywords)), labels=keywords)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # ax.set_title("Publications from keywords (publication/year)")
    return plt.show()

##################################################### S I D E B A R ####################################################


tab1, tab2 = st.sidebar.tabs(["Eingabe", "Detail Bar"])


with tab1:
    st.header("Plot Nummer 1")

    userinput_keyword = st.text_input("Tippe ein Keyword ein", value= "data")


    plot_zwei = st.header("Plot Nummer 2")




    plot_drei = st.header("Plot Nummer 3")




    plot_vier = st.header("Plot Nummer 4")



    plot_fünf = st.header("Plot Nummer 5")


with tab2:
    plot_detail = st.header("Detailplot Nummer 1")

    fig, ax = plt.subplots(figsize=(6,8))
    ax.barh(keywords, keywords_valcount)
    st.pyplot(fig)

    plot_detail2 = st.header("Detailplot Nummer 2")

    x = []
    y = []

    # prepare data
    for i in range(0, len(df_publPerYear.index)):
        x.append(df_publPerYear['pubyear'][i])
        y.append(df_publPerYear['count'][i])

    # plot
    fig, ax = plt.subplots(figsize=(20,12))
    ax.plot(x, y)
    st.pyplot(fig)


################################################ P L O T S #############################################################

keyword_Lineplot = keyword_per_year(userinput_keyword)

with info1:

    st.metric(label = "Publikationen", value = len(all_titles))

with info2:

    st.metric(label="Authoren", value=len(all_authors))

with plot1:

    st.line_chart(keyword_Lineplot, use_container_width=True)

with plot2:

    line_plot_df = pd.DataFrame(keyword_Lineplot)
    st.write(line_plot_df)                          #Idee: Mein pubyear mit Lisas Liste "x" (auch pubyear) vergleichen und wenn == True dann gib Lisas y an dieser Stelle zurück. Dann teile title (also die Anzahl vorkommen) durch y.


with plot3:
    pass



with plot4:
    pass
