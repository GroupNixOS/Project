import streamlit as st
import pandas as pd #delete?
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np


#Establish a connection to MySQL db
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="RootBeer2024",
    database="proj"  
)

cursor = conn.cursor()

st.title('Admixture Analysis') #page header

#Choice 1, superpops
with st.expander("Superpopulations Analysis"):

    #Select Superpopulations using MySQL query
    cursor.execute("SELECT DISTINCT Superpopulation FROM admixture_superpop")
    populations = [row[0] for row in cursor.fetchall()]
    selected_superpops = st.multiselect("Select Superpopulations", populations)

    if selected_superpops:
        #Constructs the MySQL query based on the selected superpopulations
        query = f"""
            SELECT EUR, SAS, AFR1, AFR2, EAS, id, Superpopulation
            FROM admixture_superpop
            WHERE Superpopulation IN ({','.join(['%s']*len(selected_superpops))})  
        """
        cursor.execute(query, selected_superpops)
        data = cursor.fetchall()

        #Creating lists for storage from MySQL query. 
        ids = []
        superpopulations = []
        eas = []
        afr2 = []
        afr1 = []
        sas = []
        eur = []

        for row in data: #one loop which grows each list per iteration. 
            ids.append(row[5])
            superpopulations.append(row[6])
            eas.append(row[4])
            afr2.append(row[3])
            afr1.append(row[2])
            sas.append(row[1])
            eur.append(row[0])

        #Matplotlib graph. 
        fig, ax = plt.subplots()


        #Colour-blind friendly palette for graph. Waiting for Matteo's confirmation.
        colour = ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'] #colorbrewer2.org
        #colour = ['#006BA4', '#FF800E', '#ABABAB', '#595959', '#5F9ED1'] #matplotlib tableau-colorblind10 

        #creating numpy arrays for the bottom parameter in ax.bar() to all stacking. 
        eas_array = np.array(eas)
        afr1_array = np.array(afr1)
        afr2_array = np.array(afr2)
        sas_array = np.array(sas)
        eur_array = np.array(eur)

        #Plot stacked bars
        ax.bar(ids, eas_array, label='EAS', width=1.0, color=colour[0])
        ax.bar(ids, afr2_array, bottom=eas_array, label='AFR2', width=1.0, color=colour[1])
        ax.bar(ids, afr1_array, bottom=eas_array+afr2_array, label='AFR1', width=1.0, color=colour[2])
        ax.bar(ids, sas_array, bottom=eas_array+afr2_array+afr1_array, label='SAS', width=1.0, color=colour[3])
        ax.bar(ids, eur_array, bottom=eas_array+afr2_array+afr1_array+sas_array, label='EUR', width=1.0, color=colour[4])
        

        #Set labels and title
        ax.set_xlabel('superpopulations')
        ax.set_ylabel('Admixture coefficients')
        ax.set_title('Ancestry matrix of superpopulations')

        #Removes samples labelled along x-axis, if not done large blob of IDs are shown due to the number of samples.
        ax.set_xticks([])

        #legend placement
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

        #Display plot in Streamlit
        st.pyplot(fig)
            
#Choice 2, pops
with st.expander("Populations Analysis"):
    cursor.execute("SELECT DISTINCT Population FROM admixture_superpop")
    populations = [row[0] for row in cursor.fetchall()]
    selected_pops = st.multiselect("Select Populations", populations)

    if selected_pops:
        #Constructs the MySQL query based on the selected superpopulations
        query = f"""
            SELECT EUR, SAS, AFR1, AFR2, EAS, id, Population
            FROM admixture_superpop
            WHERE Population IN ({','.join(['%s']*len(selected_pops))})
        """
        cursor.execute(query, selected_pops)
        data = cursor.fetchall()


        #Initial code which proved to be inefficient (loading times)
        # Extract data for each population
        # ids = [row[5] for row in data]
        # populations = [row[6] for row in data]
        # eas = [row[4] for row in data]
        # afr2 = [row[3] for row in data]
        # afr1 = [row[2] for row in data]
        # sas = [row[1] for row in data]
        # eur = [row[0] for row in data]

        #alternate code, one big loop
        ids = []
        populations = []
        eas = []
        afr2 = []
        afr1 = []
        sas = []
        eur = []

        for row in data:
            ids.append(row[5])
            populations.append(row[6])
            eas.append(row[4])
            afr2.append(row[3])
            afr1.append(row[2])
            sas.append(row[1])
            eur.append(row[0])

        #Matplotlib plot
        fig, ax = plt.subplots()

        #Colour-blind friendly palette for graph. Matteo has confirmed both.
        colour = ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'] #colorbrewer2.org
        #colour = ['#006BA4', '#FF800E', '#ABABAB', '#595959', '#5F9ED1'] #matplotlib tableau-colorblind10 

        #creating numpy arrays for the bottom parameter in ax.bar() to all stacking. 
        eas_array = np.array(eas)
        afr1_array = np.array(afr1)
        afr2_array = np.array(afr2)
        sas_array = np.array(sas)
        eur_array = np.array(eur)

        
        #Plot stacked bars
        ax.bar(ids, eas_array, label='EAS', width=1.0, color=colour[0])
        ax.bar(ids, afr2_array, bottom=eas_array, label='AFR2', width=1.0, color=colour[1])
        ax.bar(ids, afr1_array, bottom=eas_array+afr2_array, label='AFR1', width=1.0, color=colour[2])
        ax.bar(ids, sas_array, bottom=eas_array+afr2_array+afr1_array, label='SAS', width=1.0, color=colour[3])
        ax.bar(ids, eur_array, bottom=eas_array+afr2_array+afr1_array+sas_array, label='EUR', width=1.0, color=colour[4])

        #Title and axis labels. 
        ax.set_xlabel('Populations')
        ax.set_ylabel('Admixture coefficients')
        ax.set_title('Ancestry matrix of populations')

        #Removes samples labelled along x-axis. 
        ax.set_xticks([])

        #Legend
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

        #Streamlit display plot
        st.pyplot(fig)

    #Closing the cursor and database connection
    cursor.close()
    conn.close()