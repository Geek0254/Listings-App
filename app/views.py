from flask import Blueprint, request, jsonify
import pandas as pd

main = Blueprint('main', __name__)

# Function to load the dataset based on city
def load_dataset(city):
    city_files = {
        'Amsterdam': 'datasets/Amsterdam_Airbnb_Listings.csv',
        'Barcelona': 'datasets/Barcelona_Airbnb_Listings.csv',
        'Berlin': 'datasets/Berlin_Airbnb_Listings.csv',
        'Brussels': 'datasets/Brussels_Airbnb_Listings.csv',
        'NYC': 'datasets/NYC_Airbnb_Listings.csv',
        'Rome': 'datasets/Rome_Airbnb_Listings.csv',
        'Sydney': 'datasets/Sydney_Airbnb_Listings.csv',
        'Tokyo': 'datasets/Tokyo_Airbnb_Listings.csv',
    }
    return pd.read_csv(city_files[city])

def clean_price(price):
    try:
        return float(price.replace('$', '').replace(',', ''))
    except:
        return None

@main.route('/listings', methods=['GET'])
def get_listings():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    df = load_dataset(city)
    df['price'] = df['price'].apply(clean_price)
    
    # Existing filtering logic for /listings
    filtered_df = df[(df['review_scores_rating'] > 4.0) & (df['name'].str.split().str.len() < 5) & df['price'].notnull()]
    if len(filtered_df) < 9:
        return jsonify({'error': 'Not enough listings available'}), 400

    sample_listings = filtered_df.sample(n=9)

    listings = []
    for _, row in sample_listings.iterrows():
        place = row['neighbourhood_cleansed']
        if pd.notna(row['neighbourhood_group_cleansed']):
            place += f", {row['neighbourhood_group_cleansed']}"
        
        listing = {
            'name': row['name'],
            'place': place,
            'rating': row['review_scores_rating'],
            'number_of_reviews': f"{row['number_of_reviews']} reviews",
            'price': f"${row['price']} per night",
            'picture_url': row['picture_url'],
            'listing_url': row['listing_url']
        }
        listings.append(listing)

    return jsonify(listings=listings)

@main.route('/filter', methods=['GET'])
def filter_listings():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    df = load_dataset(city)
    df['price'] = df['price'].apply(clean_price)
    
    min_rating = request.args.get('min_rating', type=float)
    min_reviews = request.args.get('min_reviews', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    # Basic validation
    if min_price and min_price < 0:
        return jsonify({'error': 'Minimum price cannot be negative'}), 400
    if max_price and max_price < 0:
        return jsonify({'error': 'Maximum price cannot be negative'}), 400
    if min_rating and (min_rating < 0 or min_rating > 5):
        return jsonify({'error': 'Rating must be between 0 and 5'}), 400
    if min_price and max_price and min_price > max_price:
        return jsonify({'error': 'Minimum price cannot be higher than maximum price'}), 400
    if min_reviews and min_reviews < 0:
        return jsonify({'error': 'Minimum reviews cannot be negative'}), 400

    filtered_df = df[df['price'].notnull()]

    if min_rating:
        filtered_df = filtered_df[filtered_df['review_scores_rating'] >= min_rating]
    if min_reviews:
        filtered_df = filtered_df[filtered_df['number_of_reviews'] >= min_reviews]
    if min_price:
        filtered_df = filtered_df[filtered_df['price'] >= min_price]
    if max_price:
        filtered_df = filtered_df[filtered_df['price'] <= max_price]

    filtered_df = filtered_df[(filtered_df['review_scores_rating'] > 4.0) & (filtered_df['name'].str.split().str.len() < 5)]
    if len(filtered_df) < 9:
        return jsonify({'error': 'Not enough listings available'}), 400

    sample_listings = filtered_df.sample(n=9)

    listings = []
    for _, row in sample_listings.iterrows():
        place = row['neighbourhood_cleansed']
        if pd.notna(row['neighbourhood_group_cleansed']):
            place += f", {row['neighbourhood_group_cleansed']}"
        
        listing = {
            'name': row['name'],
            'place': place,
            'rating': row['review_scores_rating'],
            'number_of_reviews': f"{row['number_of_reviews']} reviews",
            'price': f"${row['price']} per night",
            'picture_url': row['picture_url'],
            'listing_url': row['listing_url']
        }
        listings.append(listing)

    return jsonify(listings=listings)


