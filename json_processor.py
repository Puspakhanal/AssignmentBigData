import requests
import redis
import json
import matplotlib.pyplot as plt

class JsonProcessor:
    """A class called JsonProcessor is made to process Json data fetched from an API.
    Attributes used below:
    api_url(str): it is the url of the API to fetch JSON data from.
    redis_host(str): It is the hostname of the Redis server.
    redis_port(str):It is the  port number of the redis server.
    redis_password(str):It is the  password of the redis server.
    """

    def __init__(self, api_url, redis_host, redis_port, redis_password):
        """Initializing the JsonProcessor class"""
        self.api_url = api_url
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

    def read_json_from_api(self):
        """ It helps to fetch json data from the given APi
                also returns dict """
        response = requests.get(self.api_url)
        return response.json()

    def insert_into_redis(self, data):
        self.redis_client.set('api_data', json.dumps(data))

    def process_Jsondata (self, data):
        results = data.get('Results', [])
        make_counts = {}
        for result in results:
            make_name = result.get('Make_Name', 'Unknown')
            make_counts[make_name] = make_counts.get(make_name, 0) + 1

        """Plotting a bar chart of counts"""
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.bar(make_counts.keys(), make_counts.values())
        plt.xlabel('Make Name')
        plt.ylabel('Count')
        plt.title('Number of Cars by Make')
        plt.xticks(rotation=45)

        """Aggregating total count of cars"""
        total_count = sum(make_counts.values())
        print("Total number of cars:", total_count)

        """Searching for models of a specific make"""
        search_make = 'Accord'
        search_results = [result for result in results if result.get('Model_Name') == search_make]
        print("Models of", search_make, ":", [result.get('Model_Name') for result in search_results])

        """Determining the top N makes"""
        top_n = 20
        top_makes = dict(sorted(make_counts.items(), key=lambda item: item[1], reverse=True)[:top_n])

        """Plotting the top N makes"""
        plt.subplot(1, 2, 2)
        plt.bar(top_makes.keys(), top_makes.values(), color='black')
        plt.xlabel('Make Name')
        plt.ylabel('Count')
        plt.title(f'Top {top_n} Makes by Count')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()


# Reference
# https://matplotlib.org/stable/api/figure_api.html
# https://matplotlib.org/stable/api/colorbar_api.html
# https://realpython.com/sort-python-dictionary/