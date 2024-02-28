# NixOS team project
NixOS is a molecular biology web-based software designed to handle population genetics data. This is donee by retrieving information from a database (mySQL) and running structure analysis on populations and superpopulation via clustering analysis (PCA), admixture analysis (ADMIXTURE) and pairwise genetic differentiation (Fst). 

# Contents
- [Requirements](#requirements)
- [Execution](#execution)

# Requirements
1. plotly.express 5.18.0 #Version: 5.18.0
2. Streamlit 1.31.0 #Version 1.31.0
3. Django 3.0.1 #Version 5.0.1
4. matplotlib 3.8.3 #Version: 3.8.3

These instructions are for windows. The assumption is made that the user has python (Version: 3.12.1) and conda installed.

# Execution
1. Navigate to the pulled directory (directories that should be present include portal, mysite and streamlit).
2. Create virtual environment using conda "conda create --name myenv"
3. Activate environment "conda activate myenv"
4. Install all necessary software "pip install -r requirements.txt"
5. Verify streamlit installation "streamlit hello"
6. Configure your database settings to settings.py (This MVP was built using an MySQL Database).
7. Apply python migrations "python manage.py migrate"
8. Once confirmed navigate to the streamlit directory "cd streamlit"
9. Activate PCA dashboard: http://localhost:8501 "streamlit run clustering_analysis_dashboard.py"
10. Using a new cmd window, navigate to the app directory, activate myenv and cd into streamlit
11. Activate Frequency dashboard: http://localhost:8502 "streamlit run allele_geno_pairwise_dashboard.py"
12. Using a new cmd window, navigate to the app directory, activate myenv and cd into streamlit
13. Activate Admixture dashboard: http://localhost:8503 "streamlit run admix_analysis_dashboard.py"
14. Using a new cmd window, navigate to the app directory and activate myenv "python manage.py runserver"
15. Follow http address to local development server, e.g. http://127.0.0.1:8000/

## 👥 Authors
- [@natzemla](https://github.com/natzemla)
- [@CianPK](https://github.com/CianPK)
- [@EllieGad](https://github.com/EllieGad)
- [@CeriHarman](https://github.com/CeriHarman)
