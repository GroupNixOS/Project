import streamlit as st
import pandas as pd
from pandasgwas.get_studies import get_studies
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

def fetch_data(query): #function to pull data from MySQL DB
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return data, columns

# Function to retrieve allele/genotype frequencies based on input IDs or genomic coordinates
def retrieve_frequencies(input_data):
    # Query to retrieve frequencies based on input IDs or genomic coordinates
    query = f"SELECT * FROM freq WHERE ID IN ({','.join(map(str, input_data))})"
    # Execute the query and fetch the data
    data, columns = fetch_data(query)
    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=columns)
    return df

# Function to parse user input and return a list of IDs
def parse_input(input_text):
    return input_text.split(',')

# Function to parse genomic coordinates and return a list of IDs
def parse_coordinates(start, end):
    # Logic to generate IDs based on genomic coordinates
    # Example logic: generate a list of IDs between start and end coordinates
    ids = [f"rs{i}" for i in range(int(start), int(end) + 1)]
    return ids


freq_query = "SELECT * FROM freq"
freq_data, freq_columns = fetch_data(freq_query)

freq_df = pd.DataFrame(freq_data, columns=freq_columns)




# Page title
st.title('Allele & Genotype Frequencies')

# User input options
option = st.radio("Select input method:", ("List of IDs", "Genomic Coordinates"))

if option == "List of IDs":
    # Input field for user to enter a list of IDs
    input_ids = st.text_input("Enter a comma-separated list of IDs (e.g., rs12184279,rs12564807,rs12562034):")
    
    populations = freq_df['Population'].unique()

    selected_populations = st.multiselect("Select Population(s)", populations)

    filtered_df = freq_df[freq_df['Population'].isin(selected_populations)] #reduces the dataframe through filtering by user-selected populations. 

    if input_ids:
       
        ids = parse_input(input_ids) 

        ids_filtered_df = pd.DataFrame(columns=freq_df.columns)
        # Filter DataFrame based on selected IDs and concatenate with ids_filtered_df
        for id in ids:
            ids_filtered_df = pd.concat([ids_filtered_df, filtered_df[filtered_df['ID'] == id]])
        
        # Display the retrieved frequencies
        st.write("Allele/Genotype Frequencies based on input IDs:")

        st.write(ids_filtered_df)

        #Clinical info section    https://caotianze.github.io/pandasgwas/get_studies/
        snp_option = st.radio("Select SNP ID:", ids)
        #snp_option = st.text_input("Please enter the SNP ID which you would like to check:") #ideally would implement st.radio from ids 
                                                                                             #but there seems to be a limitation with pandasgwas.get_studies()

        st.write(f"For {snp_option} the associated GWAS studies are:") #test id: rs1121980,  rs753760, rs1538389
        studies = get_studies(variant_id=snp_option)
        st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]]) #This method is static but having quite a lot of difficulties to target "columns" via title
                #19: "publicationinfo.title", 17: "publicationinfo.publicationDate", 18: "publicationinfo.publication", 15: "diseaseTrait.trait",16: "publicationinfo.pubmedId"]])
                #studies.studies[0:4] replace .iloc with this to see all available columns


       

        



        


            
            
           
           
                
            
            

            

        

        
     















    elif option == "Genomic Coordinates":
        # Input fields for user to enter start and end genomic coordinates
        start_coord = st.text_input("Enter start genomic coordinate:")
        end_coord = st.text_input("Enter end genomic coordinate:")
        if start_coord and end_coord:
            # Parse the genomic coordinates and generate a list of IDs
            ids = parse_coordinates(start_coord, end_coord)
            # Retrieve frequencies based on genomic coordinates
            frequencies_df = retrieve_frequencies(ids)
            # Display the retrieved frequencies
            st.write("Allele/Genotype Frequencies based on genomic coordinates:")
            st.write(frequencies_df)
