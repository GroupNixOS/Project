#code for creating a metadata file to populate the metadata table in SQL - uses output of the genenames code
#reading in a file with snp positions and IDs
#command line script used for obtaining the csv file: bcftools query -f ‘%POS\t%ID\n’ chr1.vcf.gz -o meta.tsv
meta<-read.table('Documents/metadata.csv', header=F)
#renaming the columns
colnames(meta) <- c("position", "ID")
#truncating SNP IDs
meta$ID <- sub(";.*", "", meta$ID)
#reading in a file with gene names and SNP positions
genename<- read.csv('gene_names.csv')
#removing the chromosome column
genename<- genename[, -1]
#merging the dfs
metadata<-merge(meta, genename, 'position')
#exporting the metadata file
write_delim(metadata, delim='\t', quote='none', 'meta.tsv')
