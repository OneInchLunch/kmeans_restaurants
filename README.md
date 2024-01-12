# A university project for locating nearby restaurants based on a random dataset.

The project is done in python for the most part with some js on the frontend.

## Documentation
The code is documented here and through comments.

## Getting started:
### Initializing the project:
Before you can run the project you need to initialize a python virtual environment:

After cloning this directory run the following commands:
```
cd ${your_working_directory}/kmeans_restaurants
python -m venv .
```

### Installing dependencies:
To install the required dependencies, all of which are located in the included 
`requirements.txt` file simply run:
```
bin/pip install -r requirements.txt
```

### Running:
Once that's done you should be good to go, simply run:
```
bin/python main.py
```

If everything starts correctly you should be able to see the main page on: 
#### [http://localhost:8000](http://localhost:8000)

## How it works:
The code uses the k-means AI algorithm to cluster together groups of restaurants
based on their similarities.
The scikit-learn implementation of the k-means algorithm was used for this project.
User input data is processed sent from the frontend to the server and is then 
processed by the k-means algorithm that then returns the user's cluster of restaurants,
which is then displayed on the frontend.

The data provided to the algorithm was taken from: [kaggle.com](https://www.kaggle.com/datasets/uciml/restaurant-data-with-consumer-ratings)
although most of the data was discarded and the data that wasn't has been modified.
Favicon was taken from [icon-icons.com](https://icon-icons.com/icon/catering-food-dinner/19332)
