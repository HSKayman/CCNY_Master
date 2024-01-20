import numpy as np
import pandas as pd

def get_distance(latitude1,longitude1,latitude2,longitude2):
    import math
    ## radius of the Earth in km
    R = 6373.0
    ## convert from degrees to radians
    lat1 = math.radians(latitude1)
    lon1 = math.radians(longitude1)
    lat2 = math.radians(latitude2)
    lon2 = math.radians(longitude2)
    
    ## get the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    ## calculate the distance between the two coordinates 
    ## using Haversine formula
    prod = math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    a = math.sin(dlat / 2)**2 + prod    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    ## convert distance to miles
    distance *= 0.621371
    return distance
## END OF get_distance()
    
def generate_distance_matrix(df):   
    ## set n to the number of cities in df
    n = df.shape[0]
    ## initialize the distance matrix as all zeros
    distance_matrix = np.zeros((n,n),dtype=int)
    
    ## calculate distance between each possible pairing of cities
    ## and store the results into distance_matrix
    for i in range(n):
        for j in range(n):
            lat1 = df['latitude'][i]
            lon1 = df['longitude'][i]
            lat2 = df['latitude'][j]
            lon2 = df['longitude'][j]
            distance_matrix[i][j] = get_distance(lat1,lon1,lat2,lon2)   
    return distance_matrix

## if you run this file as a main to test this is what you do:    
if __name__ == "__main__":
    cities_file = 'Carribean_countries.csv'
    df = pd.read_csv('Carribean_countries.csv')
    distance_matrix = generate_distance_matrix(df)
    print(distance_matrix)
    