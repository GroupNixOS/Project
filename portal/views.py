#mysite/portal/
from django.shortcuts import HttpResponse, render
import streamlit as st


def index(request):
    return render(request, "index.html")

def clustering_analysis(request):
    return render(request, 'clustering_analysis.html')

def admixture_analysis(request):
    return render(request, 'admixture_analysis.html')

def allele_genotype_frequencies(request):
    return render(request, 'allele_genotype_frequencies.html')

#def pairwise_population_matrix(request):    #muting this bit of the code as the matrix should be in above page. 
    #return render(request, 'pairwise_population_matrix.html')