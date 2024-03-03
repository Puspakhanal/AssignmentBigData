from json_processor import JsonProcessor

if __name__ == "__main__":
    api_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/honda?format=json'
    redis_host = 'redis-18648.c56.east-us.azure.cloud.redislabs.com'
    redis_port = 18648
    redis_password = 'qk67b07VM9zjFO13kDLyIRbmmFHK5kIS'

    processor = JsonProcessor(api_url, redis_host, redis_port, redis_password)

    # Fetch JSON data from API
    json_data = processor.read_json_from_api()

    # Insert JSON data into Redis
    processor.insert_into_redis(json_data)

    # Process data
    processor.process_Jsondata(json_data)
