import os
import re
import nltk
import json
import pickle
from tqdm import tqdm
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextData:
    def __init__(self, directory):
        self.directory = directory
        self.preprocessed_data = {}

    def load_data(self):
        # Get the list of files in the specified directory
        files = os.listdir(self.directory)

        # Check if the processed data file exists
        if os.path.exists("search_indexer/proceesed_data.pkl"):
            # Load the preprocessed data from the file
            self.preprocessed_data = pickle.load(
                open('search_indexer/proceesed_data.pkl', 'rb'))
        else:
            # Initialize a progress bar to show the progress of loading data
            progress_bar = tqdm(total=len(files))

            # Iterate through each file in the directory
            for filename in files:
                # Check if the file ends with ".json"
                if filename.endswith(".json"):
                    # Get the full path of the file
                    filepath = os.path.join(self.directory, filename)

                    # Open the file and load its content as JSON
                    with open(filepath, 'r', encoding='utf8') as file:
                        data = json.load(file)

                        # Preprocess the text and store it in the preprocessed data dictionary
                        self.preprocessed_data[filepath] = self.preprocess_text(
                            data)
                        progress_bar.update(1)

            # Save the preprocessed data to a file
            pickle.dump(self.preprocessed_data, open(
                'search_indexer/proceesed_data.pkl', 'wb'))
            progress_bar.close()

    def preprocess_text(self, data):
        text = ''

        # Initialize a WordNetLemmatizer object
        lemmatizer = WordNetLemmatizer()

        # Define a helper function to combine the title, subtitle, and sub-points of a JSON object
        def step_combo(x):
            return x["title"] + x["subtitle"] + str.join("", x["sub-points"])

        # Define a helper function to combine the name and sub-points of a JSON object
        def point(x):
            return x["name"] + str.join("", list(map(step_combo, x["steps"])))

        # Check if the JSON data contains an 'article' and 'intro' field
        if 'article' in data and 'intro' in data:
            # Combine the article and intro fields into a single text string
            text = data['article'] + data['intro'] + \
                str.join("", list(map(point, data['points'])))
        else:
            text = data

        # Converts to lowercase and Removes punctuation from the text using a regular expression
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)

        # Tokenize the text into individual words using the nltk.word_tokenize function
        words = nltk.word_tokenize(text)

        # Lemmatize the words using the WordNetLemmatizer object
        words = [lemmatizer.lemmatize(
            word) for word in words if word not in stopwords.words('english')]
        text = ' '.join(words)

        return text


class TextVectorizer:
    def __init__(self, texts: dict):
        self.texts: dict = texts
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.word2vec_model = None

    def fit(self):
        # Train the TfidfVectorizer object using the text content of the JSON files in the preprocessed_data dictionary
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            list(self.texts.values()))
        
        # Train the Word2Vec model using the text content of the JSON files in the preprocessed_data dictionary
        self.word2vec_model = Word2Vec(list(self.texts.values()))

    def query(self, query, k=10):
        # Check if the Vectorizer object has been fitted with the TfidfVectorizer and Word2Vec models
        if self.tfidf_matrix is None or self.word2vec_model is None:
            raise ValueError("Vectorizer not fitted")

        # Convert the query text to a vector using the TfidfVectorizer object
        query_vec = self.tfidf_vectorizer.transform(query.split())

        # Calculate the cosine similarity between the query vector and the text content of the JSON files in the preprocessed_data dictionary
        cosine_sim = cosine_similarity(query_vec, self.tfidf_matrix)

        # Find the index of the most similar text content using the sorted array of cosine similarity scores
        index = cosine_sim.argsort()[0][-1:-k:-1]

        # Get the filepaths of the most similar text content
        filepaths = [list(self.texts.keys())[i] for i in index]
        result = []

        # Iterate through the filepaths and load the JSON data
        for i in filepaths:
            
            with open(i, 'r', encoding='utf-8') as file:
                jsonData = json.load(file)
                item = {
                    "link": jsonData['link'],
                    "article": jsonData['article'],
                }
                result.append(item)

        return result


if __name__ == "__main__":
    data = TextData(os.getcwd() + r'\crawler\data')
    data.load_data()
    vectorizer = TextVectorizer(data.preprocessed_data)
    vectorizer.fit()

    query = "find deleted messages"
    vectorizer.query(data.preprocess_text(query))
