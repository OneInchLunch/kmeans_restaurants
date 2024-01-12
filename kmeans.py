import pandas as pd
from sklearn.cluster import KMeans
from geopy.distance import geodesic
from sklearn.preprocessing import OneHotEncoder
import warnings
import matplotlib.pyplot as plt

def find_restaurants(u_input):
    # These lines just supress annoying warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
    warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

    # The data in this project is expected to be in a 
    # .csv file.
    # Initially a sqlite database was considered however
    # There was no point as this code will never be used
    # With such a large dataset to have any benefit from 
    # that.
    df = pd.read_csv('restaurant_dataset/geoplaces.csv')

    user_location = (u_input['user_latitude'], u_input['user_longitude'])
    user_cuisine = u_input['user_cuisine']
    user_rating = u_input['user_rating'] 

    # Reading .csv data into a pandas DataFrame
    features = df[['latitude', 'longitude', 'Rcuisine', 'rating']]

    # Since the cuisines are strings they need yo be encoded
    # You can read more about how that works here:
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    encoder = OneHotEncoder(sparse=False, drop='first')
    encoded_cuisine = pd.DataFrame(encoder.fit_transform(features[['Rcuisine']]), columns=encoder.get_feature_names_out(['Rcuisine']))
    features = pd.concat([features, encoded_cuisine], axis=1).drop(['Rcuisine'], axis=1)

    # This code was used at one point for weighing input parameters
    # This proved to be overy complicated for the use case of this project
    # And the dataset isn't all that skewed to call for this.
    # scaler = StandardScaler()
    # features_scaled = scaler.fit_transform(features)

    ### USED FOR ESTIMATING THE NUMBER OF DESIRED CLUSTERS ###
    # Just uncomment this code below and comment all of the code from line 50

    # inertias = []
    # for k in range(1, 100):
    #     kmeans = KMeans(n_clusters=k, random_state=42)
    #     kmeans.fit(features)
    #     inertias.append(kmeans.inertia_)
    # plt.plot(range(1, 100), inertias, marker='o')
    # plt.xlabel('Number of Clusters (k)')
    # plt.ylabel('Inertia')
    # plt.title('Elbow Method')
    # plt.savefig('elbow_plot.png')
    # plt.close()
    ##########################################################

    # Choose the number of clusters (k) based on the elbow plot
    k = 7 # Adjust based on your preferences

    # Initialize KMeans model and fit the data
    # If you don't know what this means you can
    # Read about it here:
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
    # And here:
    # https://en.wikipedia.org/wiki/K-means_clustering
    # And watch all of this:
    # https://www.youtube.com/watch?v=mHl5P-qlnCQ&list=PLBv09BD7ez_6cgkSUAqBXENXEhCkb_2wl
    kmeans = KMeans(n_clusters=k, random_state=42)

    df['Cluster'] = kmeans.fit_predict(features)

    # Function to calculate the distance between a restaurant
    # and the user
    def calculate_distance(row):
        restaurant_location = (row['latitude'], row['longitude'])
        return geodesic(user_location, restaurant_location).km

    # Apply the distance calculation to create a new 'Distance' column
    df['Distance'] = df.apply(calculate_distance, axis=1)

    # Find the cluster of the user's current location
    user_cuisine_encoded = encoder.transform([[user_cuisine]])[0]
    user_features = [[u_input['user_latitude'], u_input['user_longitude'], user_rating] + user_cuisine_encoded.tolist()]
    user_cluster = kmeans.predict(user_features)[0]

    # Find the nearest restaurant in the user's cluster
    user_cluster_df = df[df['Cluster'] == user_cluster]
    
    # Used in testing.
    # nearest_in_cluster = user_cluster_df.loc[user_cluster_df['Distance'].idxmin()]
    # rows = user_cluster_df[user_cluster_df['Rcuisine'] == user_cuisine]

    # The K-means clustering does a pretty good job
    # however there are only so many restaurants in mexico
    # and that being the case the AI needs some help picking out
    # the best restaurants.
    # All this code does is makes sure the output matches
    # what the user wants.
    def best_matches(cluster_df):
        rows = cluster_df[cluster_df['Rcuisine'] == user_cuisine]
        return rows


    data = best_matches(user_cluster_df)
    return data