#These instructions are for windows. 
#The assumption is made that the user has python (Version: 3.12.1) and conda installed. 

#navigate to the pulled directory (directories that should be present include portal, mysite and streamlit). 

#create virtual environment using conda
"conda create --name myenv"

#activate environment
"conda activate myenv"

#install all necessary software
"pip install -r requirements.txt"

#verify streamlit installation
"streamlit hello"

#Configure your database settings to settings.py (This MVP was built using an MySQL Database).

#Apply python migrations
"python manage.py migrate"

#once confirmed navigate to the streamlit directory 
"cd streamlit"

#activate PCA dashboard: http://localhost:8501
"streamlit run clustering_analysis_dashboard.py"

#Using a new cmd window, navigate to the app directory, activate myenv and cd into streamlit

#activate Frequency dashboard: http://localhost:8502
"streamlit run allele_geno_pairwise_dashboard.py"

#Using a new cmd window, navigate to the app directory, activate myenv and cd into streamlit

#activate Admixture dashboard: http://localhost:8503
"streamlit run admix_analysis_dashboard.py"

#Using a new cmd window, navigate to the app directory and activate myenv
"python manage.py runserver"

#Follow http address to local development server, e.g. http://127.0.0.1:8000/
