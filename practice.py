import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


st.title('web app practice')

dataset = pd.read_csv('C:/Users/cerih/practice/practice_data.csv')

st.subheader('Raw data')

st.write(dataset)

st.subheader('Explore the original data')

xvar = st.selectbox('Select x-axis:', dataset.columns[:-1])
yvar = st.selectbox('Select y-axis:', dataset.columns[:-1])

st.write(px.scatter(dataset, x=xvar, y=yvar, color='population_info'))

dataset_scaled = StandardScaler().fit_transform(dataset.drop('population_info', axis=1))
dataset_pca = PCA()
dataset_transformed = dataset_pca.fit_transform(dataset_scaled)

col_names = [f'component {i+1}' for i in range(dataset_transformed.shape[1])]

dataset_transformed_df = pd.DataFrame(dataset_transformed, columns=col_names)
dataset_transformed_df = pd.concat([dataset_transformed_df, dataset['population_info']], axis=1)

st.subheader('Transformed data')

st.write(dataset_transformed_df)

st.subheader('Explore principal components')

xvar = st.selectbox('Select x-axis:', dataset_transformed_df.columns[:-1])
yvar = st.selectbox('Select y-axis:', dataset_transformed_df.columns[:-1])

st.write(px.scatter(dataset_transformed_df, x=xvar, y=yvar, color='population_info'))

st.subheader('Explore loadings')

loadings = dataset_pca.components_.T * np.sqrt(dataset_pca.explained_variance_)

loadings_df = pd.DataFrame(loadings, columns=col_names)
loadings_df = pd.concat([loadings_df, 
                         pd.Series(dataset.columns[0:4], name='var')], 
                         axis=1)

component = st.selectbox('Select component:', loadings_df.columns[0:4])

bar_chart = px.bar(loadings_df[['var', component]].sort_values(component), 
                   y='var', 
                   x=component, 
                   orientation='h',
                   range_x=[-1,1])


st.write(bar_chart)

st.write(loadings_df)
