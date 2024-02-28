#mysite/portal/
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('ClusteringAnalysis/', views.clustering_analysis, name='clustering_analysis'),
    #path('PairwisePopulationMatrix/', views.pairwise_population_matrix, name='pairwise_population_matrix'),
    path('AdmixtureAnalysis/', views.admixture_analysis, name='admixture_analysis'),
    path('AlleleGenotypeFrequencies/', views.allele_genotype_frequencies, name='allele_genotype_frequencies'),
]