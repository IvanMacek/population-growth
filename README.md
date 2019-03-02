# Web
### Install pipenv
Install pipenv on OSX by running:

    brew install pipenv

### Install project packages
Run in terminal:

    pipenv install --dev
    
To access python terminal, run:

    pipenv shell
    
### Run locally
Create an .env file in your project root and paste the following content in it:

    FLASK_ENV=development
    ZIP_TO_CBSA_URL=https://s3.amazonaws.com/peerstreet-static/engineering/zip_to_msa/zip_to_cbsa.csv
    CBSA_TO_MSA_URL=https://s3.amazonaws.com/peerstreet-static/engineering/zip_to_msa/cbsa_to_msa.csv
 
Run in terminal:

    flask run
    
In web browser go to:

    http://localhost:5000/
    
    
# Testing
Run in terminal:

    pytest
 

# Deployment
- Deploy to Heroku by pushing to https://git.heroku.com/population-growth-ps.git  

### Production
- Heroku app: https://dashboard.heroku.com/apps/population-growth-ps
- App link: http://population-growth-ps.herokuapp.com/search-zip/90034