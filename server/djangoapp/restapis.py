# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# Function to make a GET request to the backend API
def get_request(endpoint, **kwargs):
    """
    Makes a GET request to the specified endpoint with optional URL parameters.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    
    request_url = backend_url + endpoint + "?" + params
    print(f"GET from {request_url}")
    
    try:
        # Call GET method of requests library with the URL and parameters
        response = requests.get(request_url)
        
        # If response is successful, return the JSON data
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"Network exception occurred: {e}")
        return None

# Function to analyze the sentiment of a review using the sentiment analyzer service
def analyze_review_sentiments(text):
    """
    Sends the review text to the sentiment analyzer API and retrieves the sentiment result.
    """
    request_url = sentiment_analyzer_url + "analyze/" + text
    print(f"GET from {request_url}")
    
    try:
        # Call the sentiment analyzer API
        response = requests.get(request_url)
        
        # If response is successful, return the sentiment data
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"Network exception occurred: {e}")
        return None

# Function to post a review to the backend API
def post_review(data_dict):
    """
    Posts the review data to the backend API.
    """
    request_url = backend_url + "insert_review"
    try:
        # Send a POST request with review data
        response = requests.post(request_url, json=data_dict)
        
        # If response is successful, return the JSON data
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"Network exception occurred: {e}")
        return None
