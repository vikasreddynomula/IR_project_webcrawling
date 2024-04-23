VIKAS REDDY NOMULA

A20539316

ABSTRACT:

This project endeavors to create a web document retrieval system using Python, Scikit-Learn, Scrapy, and Flask. It encompasses a Scrapy-based Crawler for fetching web documents, a Scikit-Learn-based Indexer for building an inverted index, and a Flask-based Processor for managing free text queries. The goals encompass proficient web crawling, precise document indexing, and swift query processing. Future plans entail augmenting the system with extra functionalities like distributed crawling and semantic search capabilities.


OVERVIEW:

The proposed system consists of three main components: a web crawler, an indexer, and a query processor.
The web crawler is responsible for traversing the web, downloading web documents, and extracting relevant content. It provides functionalities to initialize crawling with seed URLs, limit the number of pages to crawl, and control the crawling depth(Crawl depth indicates the number of links a web crawler follows from the initial webpage, determining the extent of web content exploration. It helps manage the scope of crawling and target specific areas within websites or the entire web) . Optional features like concurrent crawling with autothrottle and distributed crawling using scrapyd enhance the efficiency and scalability of the crawler.

The indexer constructs an inverted index from the crawled documents, enabling efficient retrieval of relevant documents based on user queries. It utilizes Scikit-Learn's TF-IDF (Term Frequency-Inverse Document Frequency) scoring mechanism to represent documents and calculate their relevance. Additionally, it supports optional features such as vector embedding representation using word2vec and neural/semantic search using kNN similarity.
The query processor handles user queries, validates them, and returns the top-K ranked results based on relevance scores calculated by the indexer. It uses Flask to provide a RESTful API for querying the indexed documents in JSON format.



DESIGN:

The system's capabilities include initiating a crawl with seed URLs, constructing an inverted index with TF-IDF scores, and processing user queries to retrieve relevant documents. Interactions between components involve passing data between the crawler, indexer, and processor. Integration is achieved through standardized input/output formats.


ARCHITECTURE:

The project comprises four core components:

Crawler: Utilizing Scrapy, this component navigates the web, retrieves documents, and prepares them for indexing. Parameters like seed URLs (https://www.wikihow.com/Main-Page  in our case), maximum pages(300 in our case), and crawl depth(2 in our case) are configurable.

Indexer: Using Scikit-Learn, the indexer constructs an inverted index from the crawler-obtained documents, employing TF-IDF scores to represent word importance and enable efficient search.

Processor: Implemented with Flask, this module manages user queries, validates them, performs spell checking with NLTK, and can expand queries using WordNet.

GUI: Integrated NiceGUI provides a user-friendly interface for viewing retrieved web documents, facilitating content visualization during the crawling process.


OPERATION:

Instructions to run the Application:

1. pip install nice gui

2. pip install scrapy

3. In python shell run following commands
    >>import nltk
    >>nltk.download('stopwords')
    >>nltk.download('wordnet')
    >>nltk.download('punkt)

4. Now type python main.py which will execute the application

5. The app will be opened in the browser then click on "Load Data" and check for the loader in terminal after its loaded completely type something and click on "go".

6. Top 10 results will appear below




<img width="1440" alt="Screenshot 2024-04-22 at 8 44 25 PM" src="https://github.com/vikasreddynomula/IR_project_webcrawling/assets/72304061/f290a3d2-5d47-41b5-872b-d47bb66344fb">

   
![image](https://github.com/vikasreddynomula/IR_project_webcrawling/assets/72304061/f4e1fbc2-a561-4540-82ca-54d5c62b5459)

<img width="561" alt="image" src="https://github.com/vikasreddynomula/IR_project_webcrawling/assets/72304061/a157a4bc-bee3-4d0a-b292-86040ca93442">






CONCLUSION:

In summary, we've successfully built a web document retrieval system leveraging Python, Scikit-Learn, Scrapy, Flask, and NiceGUI. Our accomplishments include:

1. Streamlined Web Crawling: The system adeptly navigates web pages, extracting pertinent content within defined parameters.
2. Precision Indexing: Through TF-IDF scoring, we've crafted an inverted index that accurately reflects word significance in documents.
3. User-Centric Query Handling: The processor effectively manages user queries, furnishing top-ranked outcomes based on relevance metrics. Integration of NiceGUI enriches the user experience, offering an appealing interface for web document visualization during crawling.
4. Storage Efficiency: By storing processed pages in a pickle file (processed_data.pkl), we optimize resource utilization and diminish the necessity for page reloading.


DATA SOURCES:

1. https://www.wikihow.com/Main-Page



SOURCE CODE:

1. processor.py:

This code implements a Flask-based web service for handling text queries and returning relevant documents. It also includes a data collection component using Scrapy for web crawling. Here's a brief overview of its functionality in 10 lines:

1. `DataCollector` class initiates web crawling using Scrapy based on predefined settings and parameters.
2. `QueryHandler` class manages query processing, including data loading, preprocessing, vectorization, and ranking of search results.
3. `search_and_rank` method ranks documents based on query similarity using TF-IDF scores.
4. `validate_query` method checks for empty queries to ensure data integrity.
5. `handle_query` method processes incoming queries, validates them, and returns relevant search results.
6. Flask routes `/process_query` and `/init` handle query processing and data initialization, respectively.
7. The `/process_query` route processes POST requests containing query data.
8. The `/init` route initializes the data and returns a success message upon completion.
9. Global variables `query_handler` and `data_collector` manage instances of QueryHandler and DataCollector classes.
10. The script is executed as the main module, with multiprocessing support and Flask app debugging enabled.


2. main.py

This script utilizes NiceGUI to create a user interface for a web document retrieval system. It starts a Flask server and sends requests to initialize data and process queries. Search results are displayed in a list format, and user interactions trigger corresponding actions. The UI elements include a button to start data loading, an input field for entering search queries, and a button to execute the search. The search results are listed with blue-colored items, and the script runs within a NiceGUI environment.

3. Indexer2.py

This script defines classes for processing text data and vectorizing it for document retrieval tasks. It preprocesses JSON data by combining specific fields, tokenizing, lemmatizing, and removing stopwords. Then, it vectorizes the text using TF-IDF and Word2Vec models. Finally, it implements a query method to retrieve the most relevant documents based on cosine similarity scores. When executed, it loads data, fits the vectorizer, processes a query, and returns relevant documents.

4. Indexer.py

This script defines a `DocumentIndexer` class for searching similar documents using TF-IDF and Word2Vec models. It loads, preprocesses, and indexes documents from a specified directory. It provides methods for searching similar documents based on TF-IDF and Word2Vec models. Finally, it demonstrates the usage of the class by searching for similar documents based on a query.


5. wikihowspider.py

This script defines a Scrapy spider named `WikiHowSpider` for crawling WikiHow webpages. It starts from the main page and can crawl up to 300 pages with a maximum depth of 2. It parses each webpage, extracts article titles, introductions, and step-by-step instructions, and saves the data to JSON files. It follows internal links within each page, limiting the depth to avoid disambiguation and category pages. The parsed data is saved in JSON format with filenames indicating the page number.



BIBILIOGRAPHY:

CITATIONS

1.https://www.baeldung.com/crawler4j

2.https://chat.openai.com/share/245753cc-ec81-4981-ac1e-c4202e5fe259

3.https://www.scrapingbee.com/blog/crawling-python/













