import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="RootBeer2024",
    database="proj"  
)

cursor = conn.cursor()

def fetch_data(query): #function to pull data from MySQL DB for creation of pandas dataframe. 
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return data, columns


#PCA integrated data

pca_query = "SELECT * FROM pca"
pca_data, pca_columns = fetch_data(pca_query)

pca_df = pd.DataFrame(pca_data, columns=pca_columns)


#PVE integrated data

pve_query = "SELECT * FROM pve"
pve_data, pve_columns = fetch_data(pve_query)

pve_df = pd.DataFrame(pve_data, columns=pve_columns)


#SUPERPOP PCA
pop_query = "SELECT Population, Superpopulation FROM pop"
pop_data, pop_columns = fetch_data(pop_query)

pop_df = pd.DataFrame(pop_data, columns=pop_columns)


#conn.close()


st.title('Clustering Analysis') #page header

#2D plot for showing variance captured per component

st.subheader("Variance capture per component")

#st.write(pve_df) Conrad has indicated that the graph is sufficient. 

x_values = pve_df.columns.tolist() # Component numbers
y_values = pve_df.iloc[0].values   # Percentage variance captured


fig = px.bar(x=x_values, y=y_values)
fig.update_layout(xaxis_title='Component Number', yaxis_title='Percentage Variance Captured')
    
st.plotly_chart(fig)

#3D plot for PCA 

st.subheader('Principle Component Analysis')
with st.expander("Populations Analysis"):

    xvar = st.selectbox('Select x-axis:', pca_df.columns, key='x_selectbox')
    yvar = st.selectbox('Select y-axis:', pca_df.columns, key='y_selectbox')
    zvar = st.selectbox('Select z-axis:', pca_df.columns, key='z_selectbox')
        
    st.write(px.scatter_3d(pca_df, x=xvar, y=yvar, z=zvar, color='Population'))

with st.expander("Superpopulations Analysis"):

    merged_df = pca_df.merge(pop_df[['Population', 'Superpopulation']], on='Population', how='left')

    xsvar = st.selectbox('Select x-axis:', merged_df.columns[0:21], key='xs_selectbox')
    ysvar = st.selectbox('Select y-axis:', merged_df.columns, key='ys_selectbox')
    zsvar = st.selectbox('Select z-axis:', merged_df.columns, key='zs_selectbox')
        
    st.write(px.scatter_3d(merged_df, x=xsvar, y=ysvar, z=zsvar, color='Superpopulation'))
    