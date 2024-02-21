
import pandas as pd
import numpy as np
import itertools
import plotly.express as px
allele_freq_data = pd.read_csv('path/to/pairwise.tsv')



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
    print(matrix_df)
    # Plot the heatmap using Plotly Express
    fig = px.imshow(matrix_df, labels=dict(color='FST'),
                color_continuous_scale='blues')

    # Show the plot
    fig.show()




#example
selected_SNPs = ['rs1000313', 'rs1001704', 'rs1002005']
selected_populations = ['GBR', 'SIB', 'ACB', 'BIB']
pairwise_FST = calculate_FST(allele_freq_data, selected_SNPs, selected_populations)





