import streamlit as st
import pandas as pd
import numpy as np #delete?
import mysql.connector
import matplotlib.pyplot as plt #delete?
import seaborn as sns #delete?

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="RootBeer2024",
    database="proj"  
)

cursor = conn.cursor()

st.title('Admixture Analysis') #page header

with st.expander("Superpopulations Analysis"):

    # Select Superpopulations using MySQL query
    cursor.execute("SELECT DISTINCT Superpopulation FROM admixture_superpop")
    populations = [row[0] for row in cursor.fetchall()]
    selected_superpops = st.multiselect("Select Superpopulations", populations)

    if selected_superpops:

        CREATE INDEX IF NOT EXISTS idx_superpopulation ON admixture_superpop (Superpopulation);
        
        # Construct the SQL query based on the selected superpopulations
        query = f"""
            SELECT EUR, SAS, AFR1, AFR2, EAS, id, Superpopulation
            FROM admixture_superpop
            WHERE Superpopulation IN (%s)
        """
        cursor.execute(query, selected_superpops)
        data = cursor.fetchall()

        ids = [row[5] for row in data]
        superpopulations = [row[6] for row in data] #this is filtered based on the above st.multiselect for superpops. 
        eas = [row[4] for row in data]
        afr2 = [row[3] for row in data]
        afr1 = [row[2] for row in data]
        sas = [row[1] for row in data]
        eur = [row[0] for row in data]

        # Show plot
        fig, ax = plt.subplots()


        #Colour blind friendly palette for graph. Waiting for Matteo's confirmation.
        colour = ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'] #colorbrewer2.org
        #colour = ['#006BA4', '#FF800E', '#ABABAB', '#595959', '#5F9ED1'] #matplotlib tableau-colorblind10 

        # Plot stacked bars for each population 
        ax.bar(ids, eas, label='EAS', width=1.0, color = colour[0])
        ax.bar(ids, afr2, bottom=eas, label='AFR2', width=1.0, color = colour[1])
        ax.bar(ids, afr1, bottom=[e + a2 for e, a2 in zip(eas, afr2)], label='AFR1', width=1.0, color = colour[2])
        ax.bar(ids, sas, bottom=[e + a2 + a1 for e, a2, a1 in zip(eas, afr2, afr1)], label='SAS', width=1.0, color = colour[3])
        ax.bar(ids, eur, bottom=[e + a2 + a1 + s for e, a2, a1, s in zip(eas, afr2, afr1, sas)], label='EUR', width=1.0, color = colour[4])
        

        # Set labels and title
        ax.set_xlabel('superpopulations')
        ax.set_ylabel('Admixture coefficients')
        ax.set_title('Ancestry matrix of superpopulations')

        #Removes samples labelled along x-axis. 
        ax.set_xticks([])

        # Show legend
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

        # Show the plot in Streamlit
        st.pyplot(fig)
            

    # Close the cursor and database connection

with st.expander("Populations Analysis"):
    cursor.execute("SELECT DISTINCT Population FROM admixture_superpop")
    populations = [row[0] for row in cursor.fetchall()]
    selected_pops = st.multiselect("Select Populations", populations)

    if selected_pops:
        # Construct the SQL query based on the selected superpopulations
        query = f"""
            SELECT EUR, SAS, AFR1, AFR2, EAS, id, Population
            FROM admixture_superpop
            WHERE Population IN ({','.join(['%s']*len(selected_pops))})
        """
        cursor.execute(query, selected_pops)
        data = cursor.fetchall()

        # Extract data for each population
        ids = [row[5] for row in data]
        populations = [row[6] for row in data]
        eas = [row[4] for row in data]
        afr2 = [row[3] for row in data]
        afr1 = [row[2] for row in data]
        sas = [row[1] for row in data]
        eur = [row[0] for row in data]

        # Show plot
        fig, ax = plt.subplots()

        #Colour blind friendly palette for graph. Waiting for Matteo's confirmation.
        colour = ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'] #colorbrewer2.org
        #colour = ['#006BA4', '#FF800E', '#ABABAB', '#595959', '#5F9ED1'] #matplotlib tableau-colorblind10 

        # Plot stacked bars for each population
        ax.bar(ids, eas, label='EAS', width=1.0, color = colour[0])
        ax.bar(ids, afr2, bottom=eas, label='AFR2', width=1.0, color = colour[1])
        ax.bar(ids, afr1, bottom=[e + a2 for e, a2 in zip(eas, afr2)], label='AFR1', width=1.0, color = colour[2])
        ax.bar(ids, sas, bottom=[e + a2 + a1 for e, a2, a1 in zip(eas, afr2, afr1)], label='SAS', width=1.0, color = colour[3])
        ax.bar(ids, eur, bottom=[e + a2 + a1 + s for e, a2, a1, s in zip(eas, afr2, afr1, sas)], label='EUR', width=1.0, color = colour[4])
       

        # Set labels and title
        ax.set_xlabel('Populations')
        ax.set_ylabel('Admixture coefficients')
        ax.set_title('Ancestry matrix of populations')

        #Removes samples labelled along x-axis. 
        ax.set_xticks([])

        # Show legend
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

        # Show the plot in Streamlit
        st.pyplot(fig)

    # Close the cursor and database connection
    cursor.close()
    conn.close()

