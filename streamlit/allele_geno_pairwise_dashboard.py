import streamlit as st
import pandas as pd
from pandasgwas.get_studies import get_studies
import numpy as np
import plotly.express as px
import mysql.connector
import itertools #for pairwise func

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

#Function to parse user input and return a list
def parse_input(input_text):
    return input_text.split(',')


#### PAIRWISE DATA FOR LATER ####

#selected_populations = populations selected in st.multiselect (list).
#selected_SNPs = list of snps, similar to input_ids once parsed. 
#allele_freq_data = pandas dataframe pulling directly from pairwise table in database. 

pairwise_query = "SELECT * FROM pairwise"
pairwise_data, pairwise_columns = fetch_data(pairwise_query)

allele_freq_data = pd.DataFrame(pairwise_data, columns=pairwise_columns) #As calculate_FST() utilisies pandas df

    #function for calculating fst, printing the matrix and showing the heatmap produced by group member
def calculate_FST(allele_freq_data, selected_SNPs, selected_populations): 
    #Filter allele frequency data for selected SNPs and populations
    selected_data = allele_freq_data[(allele_freq_data['ID'].isin(selected_SNPs)) & (allele_freq_data['Population'].isin(selected_populations))]

    populations = selected_data['Population'].unique()
    pairwise_FST = {}

    #Calculate pairwise FST
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
            pairwise_FST[(pop1, pop2)] = np.nan  #Sets FST value to NaN if no valid calculations 
                
    df = pd.DataFrame(list(pairwise_FST.items()), columns=['Pair', 'Value'])

    df[['Source', 'Target']] = pd.DataFrame(df['Pair'].tolist(), index=df.index)
       
    #Defining the order of categories
    category_order = sorted(set(df['Source'].tolist() + df['Target'].tolist()), reverse=True)

    #Creates an empty square matrix
    matrix_df = pd.DataFrame(0, index=category_order, columns=category_order)

    #Fill in the matrix with values from the original data
    for _, row in df.iterrows():
        matrix_df.at[row['Source'], row['Target']] = row['Value']
    #Keeping only the lower triangular part of the matrix
    lower_triangular = np.tril(matrix_df)
    #Sets the upper triangular part to the mirrored values from the lower triangular part
    matrix_df.replace(np.nan, 0, inplace=True)
    mirrored_values = lower_triangular.T
    np.fill_diagonal(mirrored_values, 0)
    matrix_df = matrix_df + mirrored_values
    st.write(matrix_df)
    
    fig = px.imshow(matrix_df, labels=dict(color='FST'),
                color_continuous_scale='blues')

    #Displays the ploty figure. 
    st.plotly_chart(fig)

        
### Page title ###
st.title('Allele & Genotype Frequencies')

#User input options as per brief. 
option = st.radio("Select input method:", ("List of IDs", "Genomic Coordinates", "List of Genes"))

if option == "List of IDs":
    #Input field for user to enter a list of IDs, plus examples. 
    input_ids = st.text_input("Enter a comma-separated list of IDs (e.g., rs1538389,rs12184279,rs12562034):")

    input_ids = parse_input(input_ids) #turning string into a list of ID's

    if len(input_ids) > 3: #Softcap to allow user to proceed with higher numbers of SNPs. 
        st.warning ("Providing more than three SNP IDs may result in longer wait times.")
    
    cursor.execute("SELECT DISTINCT Population FROM freq")
    populations = [row[0] for row in cursor.fetchall()]

    selected_populations = st.multiselect("Select Population(s) (e.g., FIN, BEB & GBR)",populations) #These 3 usually produce a nice graph

    filtered_columns = ["ID", "Population", "Genotype_0", "Genotype_1", "Genotype_2", "RefFrequency","AltFrequency"]
    filtered_df = pd.DataFrame(columns=filtered_columns)

    filtered_rows = []

    for id in input_ids:
        for population in selected_populations:
            query = f"SELECT * FROM freq WHERE ID = '{id}' AND Population = '{population}'" #can replace * with specifics. 
            cursor.execute(query)
            filtered_rows.extend(cursor.fetchall())

            filtered_df = pd.DataFrame(filtered_rows, columns=filtered_columns)
        
    #Display the retrieved frequencies as a table 
    st.write("Allele/Genotype Frequencies based on input IDs:")

    st.write(filtered_df) #st.write allows the user to download the table. 

    cursor.close()

    #Clinical info section    https://caotianze.github.io/pandasgwas/get_studies/
    snp_option = st.radio("Select SNP ID:", input_ids) #allows user to select specific ID from the list they submitted. 

    st.write(f"For {snp_option} the associated GWAS studies are:") #test id: rs1121980,  rs753760, rs1538389
    studies = get_studies(variant_id=snp_option)
    #st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]]) 
        #This method is static but having quite a lot of difficulties to target "columns" via title
        #19: "publicationinfo.title", 17: "publicationinfo.publicationDate", 18: "publicationinfo.publication", 15: "diseaseTrait.trait",16: "publicationinfo.pubmedId"]])
        #studies.studies[0:4] replace .iloc with this to see all available columns

    try: #Setting up error handling, as if loops are tricky to use with PandasGWAS especially if the first SNP ID does not produce any papers (gives a nasty error message)
        table_data = {  #Setting up a table, to make results look clear. 
            'Title': studies.studies.iloc[:, 19],
            'Publication Date': studies.studies.iloc[:, 17],
            'Disease Trait': studies.studies.iloc[:, 15],
            'Publication': studies.studies.iloc[:, 18],
            'PubMed ID': studies.studies.iloc[:, 16]
        }
        table_df = pd.DataFrame(table_data)

        #Displaying results of table/
        st.write(table_df)

        #Link creation and display. 
        for pubmed_id in table_df['PubMed ID']: #for loop to produce one link per paper. 
            pubmed_link = f'[PubMed Link: {pubmed_id}](https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/)'
            st.write(pubmed_link, unsafe_allow_html=True)
                           
    except:
        st.error("No associated GWAS studies were found") #Can change to st.write to remove red box. 
    

    if len(selected_populations) > 1:
        st.write("As two or more populations have been selected, please see below for the pairwise analysis:")
        calculate_FST(allele_freq_data, input_ids, selected_populations)



elif option == "Genomic Coordinates":
    #Input fields for user to enter start and end genomic coordinates with examples. 
    start_coord = st.text_input("Enter start genomic coordinate (e.g., 111784500):") #Other example, 100127097
    end_coord = st.text_input("Enter end genomic coordinate (e.g., 111787000):") #Other example, 100139121
    #The example coords will produce two SNP IDs, one with a GWAS study one without.

    #MySQL Query dependant on users input. 
    if start_coord and end_coord:
        query = f"SELECT ID FROM metadata WHERE Pos BETWEEN {start_coord} AND {end_coord}"
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch IDs of selected rows
        input_ids = [row[0] for row in cursor.fetchall()] #this variable differs from the "List of IDs" path as the IDs are not inputted 
                                                          #but filtered from the metadata table within the MySQL db

        #Displaying captured IDs
        st.write("SNP IDs with positions between start and end coordinates:")
        #st.write(input_ids) #needs to be presented better on the Dash. 
        st.text(", ".join(input_ids))

        #end of conversion from coordinates to snp IDS, following is copied from the "List of IDs" method

        cursor.execute("SELECT DISTINCT Population FROM freq")
        populations = [row[0] for row in cursor.fetchall()]

        selected_populations = st.multiselect("Select Population(s) (e.g., FIN, BEB & GBR)",populations) #These 3 usually produce a nice graph

        filtered_columns = ["ID", "Population", "Genotype_0", "Genotype_1", "Genotype_2", "RefFrequency","AltFrequency"]
        filtered_df = pd.DataFrame(columns=filtered_columns)

        filtered_rows = []

        for id in input_ids:
            for population in selected_populations:
                query = f"SELECT * FROM freq WHERE ID = '{id}' AND Population = '{population}'" 
                cursor.execute(query)
                filtered_rows.extend(cursor.fetchall())

                filtered_df = pd.DataFrame(filtered_rows, columns=filtered_columns)
            
        #Display the retrieved frequencies
        st.write("Allele/Genotype Frequencies based on input IDs:")

        st.write(filtered_df)

        cursor.close()
        conn.close()

        #Clinical info section    https://caotianze.github.io/pandasgwas/get_studies/
        snp_option = st.radio("Select SNP ID:", input_ids)

        st.write(f"For {snp_option} the associated GWAS studies are:") #test id: rs1121980,  rs753760, rs1538389
        studies = get_studies(variant_id=snp_option)
        #st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]])

        try: #Setting up error handling, as if loops are tricky to use with PandasGWAS.
            #Setting up a table, to make results look clear. 
            table_data = { 
                'Title': studies.studies.iloc[:, 19],
                'Publication Date': studies.studies.iloc[:, 17],
                'Disease Trait': studies.studies.iloc[:, 15],
                'Publication': studies.studies.iloc[:, 18],
                'PubMed ID': studies.studies.iloc[:, 16]
            }
            table_df = pd.DataFrame(table_data)

            #Displaying results of table/
            st.write(table_df)

            #Link creation and display. 
            for pubmed_id in table_df['PubMed ID']:
                pubmed_link = f'[PubMed Link: {pubmed_id}](https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/)'
                st.write(pubmed_link, unsafe_allow_html=True)
                           
        except:
            st.error("No associated GWAS studies were found") #Can change to st.write to remove red box. 

        if len(selected_populations) > 1:
            st.write("As two or more populations have been selected, please see below for the pairwise analysis:")
            calculate_FST(allele_freq_data, input_ids, selected_populations)


elif option == "List of Genes":
    input_genes = st.text_input("Enter a comma-separated list of Genes (e.g., KAZN,WASH7P,MACO1) :")

    genes= parse_input(input_genes) #list of each gene as a string

    if len(genes) > 3:
        st.warning ("Providing more than three genes may result in longer wait times.")

    gene_ids = {} #Dictionary to store the first 10 IDs for each gene, will be needed for later half. 

    if genes: 
        for gene in genes:
            #MySQL query per gene
            query = f"SELECT ID FROM metadata WHERE GENE = '{gene}'" #pulls a lot of data. 

            cursor = conn.cursor()
            cursor.execute(query)

            #Pulling IDs of selected rows
            input_ids = [row[0] for row in cursor.fetchall()]

            gene_ids[gene] = input_ids[0:10] #stores the first 10 SNP IDs of each gene into gene_ids dictionary


            with st.expander(f"SNP IDs found within Gene {gene}"): #utilising st.expander() to reduce clutter on dashboard.
                st.write(input_ids)
                st.download_button(
                label="Download SNP IDs",
                data="\n".join(gene),
                file_name= "snps.txt",
                mime="text/plain",
                key=f"download_button_{gene}")  #Unique key for each download button - if multiple genes are present in the list "genes" this step is needed.
        

        #Population selector
        cursor.execute("SELECT DISTINCT Population FROM freq")
        populations = [row[0] for row in cursor.fetchall()]

        selected_populations = st.multiselect("Select Population(s) (e.g., FIN, BEB & GBR)",populations) #These 3 usually produce a nice graph

        #KAZN -> rs10157197, great example for demonstrating. 

        if selected_populations:
        
        #Present allele & genotype frequencies table

            filtered_columns = ["ID", "Population", "Genotype_0", "Genotype_1", "Genotype_2", "RefFrequency","AltFrequency"]
            filtered_df = pd.DataFrame(columns=filtered_columns)

            for gene in genes:
                gene_snps = gene_ids.get(gene, [])
                with st.expander(f"{gene}: First 10 SNPs found"): # 
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
                        #st.write(studies.studies.iloc[:, [19, 17, 15, 18, 16]])
                        

                        try: #Setting up error handling, as if loops are tricky to use with PandasGWAS.
                                #Setting up a table, to make results look clear. 
                                table_data = { 
                                    'Title': studies.studies.iloc[:, 19],
                                    'Publication Date': studies.studies.iloc[:, 17],
                                    'Disease Trait': studies.studies.iloc[:, 15],
                                    'Publication': studies.studies.iloc[:, 18],
                                    'PubMed ID': studies.studies.iloc[:, 16]
                                }
                                table_df = pd.DataFrame(table_data)

                                #Displaying results of table
                                st.write(table_df)

                                #Link creation and display. 
                                for pubmed_id in table_df['PubMed ID']:
                                    pubmed_link = f'[PubMed Link: {pubmed_id}](https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/)'
                                    st.write(pubmed_link, unsafe_allow_html=True)
                           
                        except:
                            st.error("No associated GWAS studies were found") #Can change to st.write to remove red box. 


                    if len(selected_populations) > 1:
                        st.write("As two or more populations have been selected, please see below for the pairwise analysis:")
                        calculate_FST(allele_freq_data, gene_snps, selected_populations)
                

            # Close cursor and database connection
            cursor.close()
            conn.close()

        else:
            st.warning("Please select at least one population.") #This prevents a complicated error message when no population is selected plus helps UX. 