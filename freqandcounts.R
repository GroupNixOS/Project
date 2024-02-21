#R code deriving genotype and allele frequencies as well as allele counts
#Command line code used for obtaining the csv file: bcftools query -i 'F_MISSING<0.1' -f '%ID[\n%SAMPLE\t%GT]\n' chr1.vcf.gz -o output_final.csv
#loading necessary packages
library(dplyr)
library(tidyverse)
library(zoo)
library(readr)
#reading in the csv file derived from the vcf file
data<- read.csv('Documents/output_final.csv', header=F, sep = '\t', row.names = NULL)
#transforming the dataframe into a more useful format
id_rows <- grepl("^rs", data$V1)
data$ID <- ifelse(id_rows, data$V1, NA)
data$ID <- zoo::na.locf(data$ID, na.rm = FALSE)
data <- data[!id_rows, ]
#adding column names
colnames(data) <- c("Sample", "Genotype", "ID")
#changing the genotypes value format to a more suitable unified one
data <- data %>%
  mutate(Genotype = case_when(
    Genotype %in% c("0/0", "0|0") ~ "0",
    Genotype %in% c("1/0", "0/1", "1|0", "0|1") ~ "1",
    Genotype %in% c("1/1", "1|1") ~ "2",
    Genotype == "./." ~ NA_character_,
    TRUE ~ as.character(Genotype)  # Keep other values as they are
  ))
#removing the ends of the IDs
data$ID <- sub(";.*", "", data$ID)
#reading in the file with sample IDs and populations
samplepop<- read.table('Documents/sample_pop.tsv', header=T)
#changing the column name 'id' to 'Sample'
samplepop <- samplepop %>%
  rename(Sample = id)
#merging the samplepop and data dfs to add a 'population' column to the data
merged_data <- merge(data, samplepop, by = 'Sample', all.x = TRUE)
#removing rows with unknown genotype
merged <- merged_data[complete.cases(merged_data$Genotype), ]
#calculating the number of each genotype in each population for every SNP
genotype_freq <- merged %>%
  group_by(ID, population, Genotype) %>%
  summarise(Frequency = n())
#calculating the number of samples in each population for every SNP
total_samples <- merged %>%
  group_by(population, ID) %>%
  summarise(TotalSamples = n_distinct(Sample))
#joining these results
gencount <- left_join(genotype_freq, total_samples, by = c("ID", "population"))

#
#genotype frequency calculation
#

result <- gencount %>%
  mutate(Ratio = Frequency / TotalSamples)
#renaming the population column
result <- result %>%
  rename(Population = population)
#removing unnecessary columns
genfreq <- result %>%
  select(ID, Population, Genotype, Ratio)
#pivoting the genotype frequency table
gen_wide <- pivot_wider(
  data = genfreq,
  names_from = Genotype,
  values_from = Ratio,
  names_prefix = "Genotype_"
)
#removing NAs
gen_wide <- gen_wide %>%
  mutate_all(~ifelse(is.na(.), 0, .))

#
#allele frequency calculation
#

#calculating reference allele frequency using genotype frequencies
allele_freq <- result %>%
  group_by(ID, Population) %>%
  summarise(
    RefFrequency = sum(ifelse(any(Genotype == 0), Ratio[Genotype == 0], 0) + ifelse(any(Genotype == 1), Ratio[Genotype == 1] * 0.5, 0)) 
  )
#calculating alternative allele frequency using the reference allele frequency
allele_freq <- allele_freq %>%
  mutate(AltFrequency = 1 - RefFrequency)
#merging genotype and allele frequencies into 1 dataframe
freq<-merge(gen_wide, allele_freq, by=c('ID', 'Population'))
#exporting the dataframe in a tsv format
write_delim(freq, delim='\t', quote='none', 'freq.tsv')

#
#preparing allele count data for pairwise analysis
#

#pivoting the genotype count dataframe
freq_wide <- pivot_wider(
  data = gencount,
  names_from = Genotype,
  values_from = Frequency,
  names_prefix = "Genotype_"
)
#replacing NAs with 0
freq_wide <- freq_wide %>%
  mutate_all(~coalesce(., 0))
#calculating reference allele count from the genotype count
freq_wide$Ref <- 2 * freq_wide$Genotype_0 + freq_wide$Genotype_1
#calculating alternative allele count from the genotype count
freq_wide$Alt <- freq_wide$Genotype_1 + 2 * freq_wide$Genotype_2
#removing columns with genotype count
freq_sub<- subset(freq_wide, select= -c(Genotype_0, Genotype_1, Genotype_2))
#multiplying all values in the 'TotalSamples' column by 2 to calculate the total allele count
freq_sub <- freq_sub %>%
  mutate(TotalSamples = TotalSamples * 2)
#exporting the dataframe as a tsv file
write_delim(freq_sub, delim='\t', quote='none', 'pairwise.tsv')

