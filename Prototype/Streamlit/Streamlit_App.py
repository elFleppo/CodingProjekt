import streamlit as st
import pandas as pd
import numpy as np
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
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) #css


info1, info2, info3, info4 = st.columns(4, gap = "large")  #Widgets, "einfache" Infos, z.b. Anzahl Authoren


plot1, plot2 = st.columns(2, gap = "large")     #2x2 Matrix an Plots

plot3, plot4 = st.columns(2, gap = "large")


#################################################### S Q L #############################################################
@st.cache_resource                  #cached die db und lässt veränderungen zu.
def db_connection():
    return st.experimental_connection(name = "dblp", type="sql", max_entries=None, ttl=None, autocommit=True)   #Connection zu der Datenbank erstellen


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
#progress_bar = st.progress(0) #Wir haben versucht einen Ladebalken zu implementieren, jedoch haben wir sehr kurze Ladezeiten.

@st.cache_data
def readDataToList(query, number):
    with st.spinner("Wird geladen"):
        non_keywords = ["none", "home", "page"]         #Keywords die bei uns zu oft vorkamen und deshalb geblacklisted wurden
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
        #with open("keywords.txt", "w", encoding="utf-8") as file:      #Keywords kontrollieren
            #file.write(str(keywords))
        counter = collections.Counter(keywords)                         #Gibt ein Dict aus. Das Wort ist der Key, und die Häufigkeit das Value.
        most_common_keywords = counter.most_common(number)
        return most_common_keywords                                              #Sieht so aus [('none', 528876), ('home', 12867), ('page', 12866), ('data', 2192)]


hist_values = readDataToList(all_titles, 10)            #Top ten Keywords

keywords = []
keywords_valcount = []

for i in hist_values:
    with st.spinner("Wird geladen"):
        keywords.append(i[0])
        keywords_valcount.append(i[1])


@st.cache_data
def keyword_per_year(keyword):
    with st.spinner("Wird geladen"):
        bool_keyword = all_titles["title"].str.contains(keyword, case = False)    #Gibt True und False zurück. Wörter mit Bindestrich werden hier glaub auch dazugezählt! Darum sinds mehr.
        keyword_year = all_pubyear.merge(bool_keyword, left_index= True, right_index= True)
        keyword_True = keyword_year.loc[keyword_year.title, :]          #Filtere nach True.
        keyword_per_year = keyword_True.groupby("pubyear").sum()        #Gruppiere nach pubyear und gib die Anzahl zurück
        if keyword_per_year.empty == True:
            return st.error("Das eingegebene Keyword existiert nicht - Geben Sie ein anderes ein.")
        else:
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
    st.header("Keywords suchen")

    userinput_keyword = st.text_input("Tippe ein Keyword ein", value= "data")


    plot_zwei = st.header("Hier könnten weitere Plots folgen...")



with tab2:
    plot_detail = st.header("Top Ten Keywords")

    fig, ax = plt.subplots(figsize=(6,8))  #Sieht so besser aus
    ax.barh(keywords, keywords_valcount)
    st.pyplot(fig, use_container_width=True)

    plot_detail2 = st.header("Anzahl Publikationen gesamt")

    x = []
    y = []

    # prepare data
    for i in range(0, len(df_publPerYear.index)):
        with st.spinner("Plot wird geladen"):
            x.append(df_publPerYear['pubyear'][i])
            y.append(df_publPerYear['count'][i])



    # plot
    x = pd.to_datetime(x, format='%Y')
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig, use_container_width=True)



################################################ P L O T S #############################################################

keyword_Lineplot = keyword_per_year(userinput_keyword)

with info1:

    st.metric(label = "Publikationen", value = len(all_titles)) #Wie viel Publikationen wir haben

with info2:

    st.metric(label="Authoren", value= len(all_authors))

with plot1:

    one_x_axis = pd.to_datetime(keyword_Lineplot.index, format='%Y') #umformatieren damit die X-Achse besser aussieht
    fig, ax = plt.subplots()
    ax.plot(one_x_axis, keyword_Lineplot.title)
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Anzahl")
    ax.set_title("Anzahl an Keywords pro Jahr")


    st.pyplot(fig, use_container_width=True) #Nutze den ganzen Container den wir angegeben haben.

with plot2:
    line_plot_df = pd.DataFrame(keyword_Lineplot)           #Nutze die Daten die wir schon erarbeitet haben
    df_publPerYear_keyword = df_publPerYear.merge(right = line_plot_df, how = 'left', left_on = 'pubyear', right_on= 'pubyear')    #SQL left join
    df_publPerYear_keyword = df_publPerYear_keyword.rename(columns={"pubyear": "Year", "count": "Publications", "title": "Keywords"})
    df_publPerYear_keyword = df_publPerYear_keyword.fillna(value = 0, axis = 1)

    percent_list = []
    for i, j in zip(df_publPerYear_keyword.Keywords, df_publPerYear_keyword.Publications):      #Gehe beide Tabellenspalten durch
        try:
            percent = 100*i/j
        except ZeroDivisionError:
            percent_list.append(0)   #Nicht durch 0 teilen.
        else:
            percent_list.append(percent)

    df_publPerYear_keyword['Percent'] = percent_list


    df_publPerYear_keyword.Year = pd.to_datetime(df_publPerYear_keyword.Year, format='%Y')

    fig, ax = plt.subplots()
    ax.plot(df_publPerYear_keyword.Year, df_publPerYear_keyword.Percent)
    ax.set_xlabel("Jahr")
    ax.set_ylabel("Prozent")
    ax.set_title("Prozentanteil Keywords an Gesamtpublikationen")
    st.pyplot(fig, use_container_width=True)


with plot3:
    pass



with plot4:
    pass
