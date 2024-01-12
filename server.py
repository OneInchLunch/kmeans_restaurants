from kmeans import find_restaurants
from flask import Flask, request, jsonify, render_template
import threading

app = Flask(__name__)

# Just some random test data
# This is the data used on the first load
test_user = {
    'user_latitude': 22.154329,
    'user_longitude': -100.987229,
    'user_cuisine': 'Thai',
    'user_rating': 3
}

# Standard flask code, just runs opens an html file.
@app.route('/')
def frontend():
    return render_template('index.html')

# This isn't really an API but it gets the job done.
# This endpoint just provides the initial data.
# Why? Because.
# (It is useful for testing if everything is working properly.)
@app.route('/api', methods=['GET'])
def api():   
    try:
        json_objects = find_restaurants(test_user).to_dict(orient='records')
        return jsonify({'restaurants': json_objects})

    except Exception as e:
        return jsonify({'error': str(e)})

# This is where everything happens.
# The user submits new data that needs to be
# processed by k-means, after which this function
# passes that data to the algorithm, and returns
# the output provided by the algorithm as a 
# collection of json objects.
@app.route('/api/submit_form', methods=['POST'])
def submit_form():
    cuisine = request.form.get('cuisine')
    rating = request.form.get('rating')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')

    new_features = {
        'user_latitude': latitude,
        'user_longitude': longitude,
        'user_cuisine': cuisine,
        'user_rating': rating
    }

    restaurants = find_restaurants(new_features).to_dict(orient='records')

    response = {
        'status': 'success',
        'message': 'Form data received successfully',
        'restaurants': restaurants
    }

    return jsonify(response)
    
def run_flask_app(port):
    app.run(port=port)

# The app is run on two seperate threads,
# One for the frontend
# One for the "API"
def start_app():
    frontend_thread = threading.Thread(target=run_flask_app, args=(8000,))
    api_thread = threading.Thread(target=run_flask_app, args=(5000,))

    frontend_thread.start()
    api_thread.start()
