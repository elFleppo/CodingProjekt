import streamlit as st
import pandas as pd
import numpy as np
from numba import jit


st.title('Auswirkungen von Corona auf die Publikationen im Bereich IT')

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}<style>")

df = pd.DataFrame(np.random.randint(0,20,size=(10000, 15)), columns=list('ABCDEFGHIJKLMNO'))

st.dataframe(df, use_container_width=True)


#@st.cache_data #When you mark a function with Streamlit’s cache annotation, it tells Streamlit that whenever the function is called that it should check two things: The input parameters you used for the function call. The code inside the function.




class plots:
    def __init__(self, df):
        hist_values = np.histogram(df.A)
        st.bar_chart(hist_values)
        st.subheader('Test Data')


def slider(df):
    hour_to_filter = st.slider('hour', 0, 23, 17)
    return df


slider(df)

plots(df)
#Um das Dashobard zu starten, folgende Zeile in die Anaconda Powershell, am Ort des CodingProjekt, eingeben:
#streamlit run App.py



#Damit konnte ich Streamlit ausführen, bei mir war die Version veraltet:
#pip install --upgrade streamlit

