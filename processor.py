from multiprocessing import freeze_support
import os
from flask import Flask, request, jsonify
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler.crawler.spiders.wikehow_spider import WikiHowSpider
from crawler.crawler import settings
from search_indexer.indexer2 import TextData, TextVectorizer


class DataCollector:

    def __init__(self):
        try:
            files = os.listdir(os.getcwd() + r'/crawler/data')
            print (len(files))
            if len(files) < 200:
                # The path seen from root, ie. from main.py
                settings_file_path = 'crawler.crawler'

                # Set the environment variable for the Scrapy settings module
                os.environ.setdefault(
                    'SCRAPY_SETTINGS_MODULE', settings_file_path)

                # Load the project settings
                project_settings = get_project_settings()
                # Update the settings with the specified log level
                project_settings.update({"LOG_LEVEL": "INFO"})

                # Create a CrawlerProcess object to run the specified spider
                process = CrawlerProcess(project_settings)

                # Specify the spider name to run
                process.crawl(WikiHowSpider)

                # Start the crawling process
                process.start()

        except:
            print("Unknown Error")


class QueryHandler:

    def __init__(self):
        self.collector = data_collector

        # Load the data from the specified path
        self.data = TextData(os.getcwd() + r'/crawler/data')
        # Load the data from the preprocessed text
        self.data.load_data()
        message = 'loaded'
        print(message)

        # Initialize the vectorizer using the preprocessed data
        self.vectorizer = TextVectorizer(self.data.preprocessed_data)
        # Fit the vectorizer to the data
        self.vectorizer.fit()
        message = 'Training vectorizer trained successfully'
        print(message)

    def search_and_rank(self, query: str, k: int) -> list:
        # Return top 10 documents
        return self.vectorizer.query(self.data.preprocess_text(query), k)

    def validate_query(self, query: str) -> bool:
        return bool(query.strip())  # Check for empty query

    def handle_query(self, query_data: dict) -> tuple:
        try:
            # Get the query and Top K from the input data
            query = query_data.get('query')
            k = query_data.get('range')
            # Check if the query is missing
            if query is None:
                return jsonify({'error': 'missing parameters'}), 400
            if k is None:
                k = 10

            # Validate the query using the processor's method
            if not self.validate_query(query):
                return jsonify({'error': 'Empty query'}), 400

            # Convert the query to lowercase and strip any leading or trailing whitespace
            query = query.lower().strip()

            # Search for the top k documents based on the query
            top_k_results = self.search_and_rank(query, k)

            # Create a JSON response containing the top k results
            response = {
                "message": "Successfully retrieved",
                'results': top_k_results
            }

            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


app = Flask(__name__)
query_handler = None


@app.route('/process_query', methods=['POST'])
def process_query():
    # Processes the query and returns the search results.
    global query_handler

    if query_handler is None:
        # Return an internal server error response
        return jsonify({'error': 'Internal Server Error: Click on Start Button'}), 500

    return query_handler.handle_query(request.get_json())


@app.route('/init', methods=['GET'])
def init():
    # This route is used to initialize the data and return a success message.
    try:
        # Create a global instance of the QueryHandler class
        global query_handler

        # Create an instance of the QueryHandler class with the initialized QueryProcessor object
        query_handler = QueryHandler()

        # Define a JSON response containing a success message
        response = {
            "message": "Data intialized successfully"
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    freeze_support()
    data_collector = DataCollector()
    app.run(debug=True)
