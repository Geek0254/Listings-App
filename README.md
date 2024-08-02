# Listings-App
This is the flask app for enlisting the airbnb listings randomly and after applying filters

# Installing Dependencies
pip install flask pandas flask-cors

# Starting the Flask Backend App
python run.py

# Manually Testing using The HTML Templtate
Ensure you have Started the flask app
Open the html page with live server and give it time to load initial DOM using the /listings endpoint
Try using the filters and then press the button to fetch. This will use /filter endpoint

# TESTING THE ENDPOINTS [SAMPLE URLS] in POSTMAN
http://127.0.0.1:5000/listings?city=NYC
http://127.0.0.1:5000/listings?city=Amsterdam
http://127.0.0.1:5000/filter?city=Barcelona&max_price=200
http://127.0.0.1:5000/filter?city=Rome&min_price=50&max_price=150
http://127.0.0.1:5000/filter?city=Sydney&min_rating=4.0&min_reviews=100&max_price=300

NB: Ensure to include the 'datasets' folder containing the datasets into the root directory as I can't due to Github file size limitations.
