# hired
Hired web app for internal hiring at IITH. Created as part of core selection project at lambda IITH.

This app has been created in django with html and css in the frontend. Frontend also uses django template language and some javascript. The backend uses a postgresql database. 

The website has been deployed on heroku and can be accessed on https://hiredfromiith.herokuapp.com/

Currently, the website allows IITH students and recruiters to register on the website using OTP verification. The user can then login to the website and after logging in, can search for jobs or job applicants depending on their roles. 

The website is intended for use by startups within IITH or otherwise and also professors who might require students to help in their labs. The use of this website can be more general than the services provided by OCS. The students may work as freelancers on this website and do not have limitations (like at OCS). 

The website uses a search engine built using generalized inverted index which is an advanced information retrieval technique. The search also uses a lemmatizer based on natural language processing. These features have been utilized from postgresql. 

Strict security checks have been implemented at each webpage to ensure no data breach. 
