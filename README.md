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


ABSTRACT:

This project endeavors to create a web document retrieval system using Python, Scikit-Learn, Scrapy, and Flask. It encompasses a Scrapy-based Crawler for fetching web documents, a Scikit-Learn-based Indexer for building an inverted index, and a Flask-based Processor for managing free text queries. The goals encompass proficient web crawling, precise document indexing, and swift query processing. Future plans entail augmenting the system with extra functionalities like distributed crawling and semantic search capabilities.


Overview:

The proposed system consists of three main components: a web crawler, an indexer, and a query processor.
The web crawler is responsible for traversing the web, downloading web documents, and extracting relevant content. It provides functionalities to initialize crawling with seed URLs, limit the number of pages to crawl, and control the crawling depth(Crawl depth indicates the number of links a web crawler follows from the initial webpage, determining the extent of web content exploration. It helps manage the scope of crawling and target specific areas within websites or the entire web) . Optional features like concurrent crawling with autothrottle and distributed crawling using scrapyd enhance the efficiency and scalability of the crawler.

The indexer constructs an inverted index from the crawled documents, enabling efficient retrieval of relevant documents based on user queries. It utilizes Scikit-Learn's TF-IDF (Term Frequency-Inverse Document Frequency) scoring mechanism to represent documents and calculate their relevance. Additionally, it supports optional features such as vector embedding representation using word2vec and neural/semantic search using kNN similarity.
The query processor handles user queries, validates them, and returns the top-K ranked results based on relevance scores calculated by the indexer. It uses Flask to provide a RESTful API for querying the indexed documents in JSON format.



Design:

The system's capabilities include initiating a crawl with seed URLs, constructing an inverted index with TF-IDF scores, and processing user queries to retrieve relevant documents. Interactions between components involve passing data between the crawler, indexer, and processor. Integration is achieved through standardized input/output formats.


Architecture:

The project comprises four core components:

Crawler: Utilizing Scrapy, this component navigates the web, retrieves documents, and prepares them for indexing. Parameters like seed URLs (https://www.wikihow.com/Main-Page  in our case), maximum pages(300 in our case), and crawl depth(2 in our case) are configurable.

Indexer: Using Scikit-Learn, the indexer constructs an inverted index from the crawler-obtained documents, employing TF-IDF scores to represent word importance and enable efficient search.

Processor: Implemented with Flask, this module manages user queries, validates them, performs spell checking with NLTK, and can expand queries using WordNet.

GUI: Integrated NiceGUI provides a user-friendly interface for viewing retrieved web documents, facilitating content visualization during the crawling process.


Operation:

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


Conclusion:

In summary, we've successfully built a web document retrieval system leveraging Python, Scikit-Learn, Scrapy, Flask, and NiceGUI. Our accomplishments include:

1. Streamlined Web Crawling: The system adeptly navigates web pages, extracting pertinent content within defined parameters.
2. Precision Indexing: Through TF-IDF scoring, we've crafted an inverted index that accurately reflects word significance in documents.
3. User-Centric Query Handling: The processor effectively manages user queries, furnishing top-ranked outcomes based on relevance metrics. Integration of NiceGUI enriches the user experience, offering an appealing interface for web document visualization during crawling.
4. Storage Efficiency: By storing processed pages in a pickle file (processed_data.pkl), we optimize resource utilization and diminish the necessity for page reloading.


Data







