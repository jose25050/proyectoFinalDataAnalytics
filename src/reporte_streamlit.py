import streamlit as st
import pandas as pd
import numpy as np

st.title('Reporte de análisis exploratorio de datos')

data = pd.read_csv("data/ifood_df.csv")


st.write(data)