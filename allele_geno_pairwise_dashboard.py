import streamlit as st
import pandas as pd
from pandasgwas.get_studies import get_studies
import numpy as np
import plotly.express as px
import mysql.connector
import itertools # for Natalia's pairwise func

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

# Function to parse user input and return a list of IDs
def parse_input(input_text):
    return input_text.split(',')

# Function to parse genomic coordinates and return a list of IDs
def parse_coordinates(start, end):
    # Logic to generate IDs based on genomic coordinates
    # Example logic: generate a list of IDs between start and end coordinates
    ids = [f"rs{i}" for i in range(int(start), int(end) + 1)]
    return ids


#### PAIRWISE DATA FOR LATER ####

#pairwise table 

#selected_populations = populations selected in st.multiselect (list)
#selected_SNPs = list of snps? Might be like input_ids
#allele_freq_data = seems to be a pd df directly from the pairwise.tsv

pairwise_query = "SELECT * FROM pairwise"
pairwise_data, pairwise_columns = fetch_data(pairwise_query)

allele_freq_data = pd.DataFrame(pairwise_data, columns=pairwise_columns)

    





    #function for calculating fst, printing the matrix and showing the heatmap
def calculate_FST(allele_freq_data, selected_SNPs, selected_populations):
    # Filter allele frequency data for selected SNPs and populations
    selected_data = allele_freq_data[(allele_freq_data['ID'].isin(selected_SNPs)) & (allele_freq_data['Population'].isin(selected_populations))]

    populations = selected_data['Population'].unique()
    pairwise_FST = {}

    # Calculate pairwise FST
    for pop1, pop2 in itertools.combinations(populations, 2):
        FST_values = []
        for SNP, group in selected_data.groupby('ID'):
            p1 = group[group['Population'] == pop1]['Ref'].values[0]
            q1 = group[group['Population'] == pop1]['Alt'].values[0]
            p2 = group[group['Population'] == pop2]['Ref'].values[0]
            q2 = group[group['Population'] == pop2]['Alt'].values[0]
            n1 = group[group['Population'] == pop1]['TotalSamples'].values[0]
            n2 = group[group['Population'] == pop2]['TotalSamples'].values[0]
            n  = n1+n2

            pbar=(p1 + p2)/ n
            qbar=(q1 + q2)/ n
                
            hexp1= 1-((p1/n1)**2 + (q1/n1)**2)
            hexp2= 1-((p2/n2)**2 + (q2/n2)**2)
                
            hs = (hexp1 * n1 + hexp2 * n2)/n
            ht = 1 - (pbar**2 + qbar**2)

            FST_values.append((ht-hs)/ht)

        # Check if FST values are available
        if len(FST_values) > 0:
            pairwise_FST[(pop1, pop2)] = np.mean(FST_values)
        else:
            pairwise_FST[(pop1, pop2)] = np.nan  # Set FST value to NaN if no valid calculations 
                
    df = pd.DataFrame(list(pairwise_FST.items()), columns=['Pair', 'Value'])

    df[['Source', 'Target']] = pd.DataFrame(df['Pair'].tolist(), index=df.index)
       
    # Define the order of categories
    category_order = sorted(set(df['Source'].tolist() + df['Target'].tolist()), reverse=True)

    # Create an empty square matrix
    matrix_df = pd.DataFrame(0, index=category_order, columns=category_order)

    # Fill in the matrix with values from the original data
    for _, row in df.iterrows():
        matrix_df.at[row['Source'], row['Target']] = row['Value']
    # Keep only the lower triangular part of the matrix
    lower_triangular = np.tril(matrix_df)
    # Set the upper triangular part to the mirrored values from the lower triangular part
    matrix_df.replace(np.nan, 0, inplace=True)
    mirrored_values = lower_triangular.T
    np.fill_diagonal(mirrored_values, 0)
    matrix_df = matrix_df + mirrored_values
    st.write(matrix_df)
    # Plot the heatmap using Plotly Express
    fig = px.imshow(matrix_df, labels=dict(color='FST'),
                color_continuous_scale='blues')

    # Show the plot
    st.plotly_chart(fig)

        
### Page title ###
st.title('Allele & Genotype Frequencies')

# User input options
option = st.radio("Select input method:", ("List of IDs", "Genomic Coordinates", "List of Genes"))

if option == "List of IDs":
    # Input field for user to enter a list of IDs
    input_ids = st.text_input("Enter a comma-separated list of IDs (e.g., rs1538389,rs12184279,rs12562034):")
    
    cursor.execute("SELECT DISTINCT Population FROM freq")
    populations = [row[0] for row in cursor.fetchall()]

    selected_populations = st.multiselect("Select Population(s)", populations)

    input_ids = parse_input(input_ids) #turning string into a list of ID's

    filtered_columns = ["ID", "Population", "Genotype_0", "Genotype_1", "Genotype_2", "RefFrequency","AltFrequency"]
    filtered_df = pd.DataFrame(columns=filtered_columns)

    filtered_rows = []

    for id in input_ids:
        for population in selected_populations:
            query = f"SELECT * FROM freq WHERE ID = '{id}' AND Population = '{population}'"
            cursor.execute(query)
            filtered_rows.extend(cursor.fetchall())

            filtered_df = pd.DataFrame(filtered_rows, columns=filtered_columns)
        
        # Display the retrieved frequencies
    st.write("Allele/Genotype Frequencies based on input IDs:")

    st.write(filtered_df)

    cursor.close()

        #Clinical info section    https://caotianze.github.io/pandasgwas/get_studies/
    snp_option = st.radio("Select SNP ID:", input_ids)

    st.write(f"For {snp_option} the associated GWAS studies are:") #test id: rs1121980,  rs753760, rs1538389
    studies = get_studies(variant_id=snp_option)
    st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]]) #This method is static but having quite a lot of difficulties to target "columns" via title
                    #19: "publicationinfo.title", 17: "publicationinfo.publicationDate", 18: "publicationinfo.publication", 15: "diseaseTrait.trait",16: "publicationinfo.pubmedId"]])
                    #studies.studies[0:4] replace .iloc with this to see all available columns

    if len(selected_populations) > 1:
        st.write("As two or more populations have been selected, please see below for the pairwise analysis:")
        calculate_FST(allele_freq_data, input_ids, selected_populations)



elif option == "Genomic Coordinates":
    # Input fields for user to enter start and end genomic coordinates
    start_coord = st.text_input("Enter start genomic coordinate (e.g., 100127097):")
    end_coord = st.text_input("Enter end genomic coordinate (e.g., 100139121):")
    if start_coord and end_coord: #maybe delete parse_coords()
        query = f"SELECT ID FROM metadata WHERE Pos BETWEEN {start_coord} AND {end_coord}"
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch IDs of selected rows
        input_ids = [row[0] for row in cursor.fetchall()] #this variable differs from the "List of IDs" path as the IDs are not inputted 
                                                          #but filtered from the metadata table within the MySQL db

        # Display the IDs
        st.write("SNP IDs with positions between start and end coordinates:")
        #st.write(input_ids) #needs to be presented better on the Dash. 
        st.text(", ".join(input_ids))

#end of conversion from coordinates to snp IDS, following is coped from the "List of IDs" method

        cursor.execute("SELECT DISTINCT Population FROM freq")
        populations = [row[0] for row in cursor.fetchall()]

        selected_populations = st.multiselect("Select Population(s)", populations)

        filtered_columns = ["ID", "Population", "Genotype_0", "Genotype_1", "Genotype_2", "RefFrequency","AltFrequency"]
        filtered_df = pd.DataFrame(columns=filtered_columns)

        filtered_rows = []

        for id in input_ids:
            for population in selected_populations:
                query = f"SELECT * FROM freq WHERE ID = '{id}' AND Population = '{population}'"
                cursor.execute(query)
                filtered_rows.extend(cursor.fetchall())

                filtered_df = pd.DataFrame(filtered_rows, columns=filtered_columns)
            
            # Display the retrieved frequencies
        st.write("Allele/Genotype Frequencies based on input IDs:")

        st.write(filtered_df)

        cursor.close()
        conn.close()

        #Clinical info section    https://caotianze.github.io/pandasgwas/get_studies/
        snp_option = st.radio("Select SNP ID:", input_ids)
        #snp_option = st.text_input("Please enter the SNP ID which you would like to check:") #ideally would implement st.radio from ids 
                                                                                                 #but there seems to be a limitation with pandasgwas.get_studies()

        st.write(f"For {snp_option} the associated GWAS studies are:") #test id: rs1121980,  rs753760, rs1538389
        studies = get_studies(variant_id=snp_option)
        st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]])

        if len(selected_populations) > 1:
            st.write("As two or more populations have been selected, please see below for the pairwise analysis:")
            calculate_FST(allele_freq_data, input_ids, selected_populations)


elif option == "List of Genes":
    input_genes = st.text_input("Enter a comma-separated list of Genes (e.g., KAZN,WASH7P,MACO1):")

    genes= parse_input(input_genes) #list of each gene as a string

    gene_ids = {}  # Dictionary to store the first 10 IDs for each gene, will be needed for later half. 

    if genes:
        #gene_list = [] #delete? 
        for gene in genes:
            query = f"SELECT ID FROM metadata WHERE GENE = '{gene}'"

            # Create a cursor and execute the query
            cursor = conn.cursor()
            cursor.execute(query)

            # Fetch IDs of selected rows
            input_ids = [row[0] for row in cursor.fetchall()]

            gene_ids[gene] = input_ids[0:10] #stores the first 10 SNP IDs of each gene into a dictionary. 


            with st.expander(f"SNP IDs found within Gene {gene}"):
                st.write(input_ids)
                st.download_button(
                label="Download SNP IDs",
                data="\n".join(gene),
                file_name= "snps.txt",
                mime="text/plain",
                key=f"download_button_{gene}")  # Unique key for each download button - if multiple genes are present in the list "genes" this step is needed.
        

        #Population selector
        cursor.execute("SELECT DISTINCT Population FROM freq")
        populations = [row[0] for row in cursor.fetchall()]

        selected_populations = st.multiselect("Select Population(s)", populations)

        if selected_populations:
        
        #Present allele & genotype frequencies table

            filtered_columns = ["ID", "Population", "Genotype_0", "Genotype_1", "Genotype_2", "RefFrequency","AltFrequency"]
            filtered_df = pd.DataFrame(columns=filtered_columns)

            for gene in genes:
                gene_snps = gene_ids.get(gene, [])
                with st.expander(f"{gene} info"): #edit this so that the description sounds better. 
                    if gene_snps:
                        for snp_id in gene_snps:
                            population_condition = ",".join([f"'{pop}'" for pop in selected_populations])
                            query = f"SELECT * FROM freq WHERE ID = '{snp_id}' AND Population IN ({population_condition})"
                            cursor.execute(query)
                            snp_rows = cursor.fetchall()
                            filtered_df = pd.DataFrame(snp_rows, columns=filtered_columns)
                            st.write(filtered_df)

                            #Clinical info section    https://caotianze.github.io/pandasgwas/get_studies/
                        snp_option = st.radio("For additional information regarding clinical relevance, please select a SNP ID:", gene_snps, key=f"radio_{gene}")
                        st.write(f"For {snp_option} the associated GWAS studies are:") 
                        studies = get_studies(variant_id=snp_option)
                        st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]])
                    if len(selected_populations) > 1:
                        st.write("As two or more populations have been selected, please see below for the pairwise analysis:")
                        calculate_FST(allele_freq_data, gene_snps, selected_populations)
                

            # Close cursor and database connection
            cursor.close()
            conn.close()

            #if len(selected_populations) > 1:
                #fst_option = st.radio("As two or more populations have been selected, if interested please select a SNP ID for pairwise analysis:", gene_snps)
                #calculate_FST(allele_freq_data, fst_option, selected_populations)
        else:
            st.warning("Please select at least one population.")
            

        



           
        