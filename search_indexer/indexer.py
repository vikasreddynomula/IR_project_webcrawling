import json
import os
import pickle
import re
import nltk

from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class DocumentIndexer:
    def __init__(self, data_dir, k=10):
        self.data_dir = data_dir
        self.k = k  # Top K similar documents
        self.tfidf_vectorizer = None
        self.word2vec_model = None
        self.documents = self.load_documents()
        self.build_tfidf_index()
        self.build_word2vec_model()

    def load_documents(self):
        """
        Loads the preprocessed documents from the pickle file.
        If the file does not exist, it will load the documents from the data directory,
        preprocess them, and save them to the pickle file.
        """
        documents = []
        if os.path.exists("search_indexer/proceesed_data1.pkl"):
            # Loads the preprocessed documents from the pickle file.
            documents = pickle.load(
                open('search_indexer/proceesed_data1.pkl', 'rb'))
        else:
            # Lists all the files in the data directory.
            files = os.listdir(self.data_dir)
            # Creates a progress bar with total number of files
            progress_bar = tqdm(total=len(files))
            for filename in files:
                
                # Constructs the full path to the current file.
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r', encoding="utf-8") as f:
                    
                    # Defines a function that combines the 'title' and 'subtitle' fields,
                    # along with the 'sub-points' list, into a single string.
                    def step_combo(x):
                        return x["title"] + x["subtitle"] + str.join("", x["sub-points"])
                    
                    # Defines a function that constructs a string from the 'name' field,
                    # and the 'steps' list, where each step is combined using the 'step_combo' function.
                    def point(x):
                        return x["name"] + str.join("", list(map(step_combo, x["steps"])))
                    
                    # Loads the JSON data from the current file.
                    data = json.load(f)
                    
                    # Combines the 'article','intro' fields  and list of 'points' field into single string
                    text = data['article'] + data['intro'] + str.join("", list(map(point, data['points'])))
                    
                    documents.append(text)
                    progress_bar.update(1)
                    
            # Dumps the 'documents' list to the pickle file.
            pickle.dump(documents, open(
                'search_indexer/proceesed_data1.pkl', 'wb'))
            progress_bar.close()
            
        return documents

    def preprocess_text(self, text):
        """
        Preprocesses the input text by converting it to lowercase and removing punctuation.
        """
        lemmatizer = WordNetLemmatizer()
        processed_text = text.lower() # convert to lowercase
        processed_text = re.sub(r'[^\w\s]', '', processed_text)  # Removes punctuation
        
        # Over Preprocessing - Less similar results
        # words = nltk.word_tokenize(text)
        # words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]
        # processed_text = ' '.join(words)
        return processed_text

    def build_tfidf_index(self):
        """
        Initializes the TF-IDF vectorizer and transforms the documents into a matrix.
        """
        self.tfidf_vectorizer = TfidfVectorizer()  # Initialize TF-IDF vectorizer
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.documents)  # Transform documents into a matrix

    def build_word2vec_model(self):
        """
        Initializes the Word2Vec model and trains it on the documents.
        """
        self.word2vec_model = Word2Vec(self.documents)  # Initialize Word2Vec model and train it on the documents

    def search_tfidf(self, query):
        """
        Searches for similar documents using the TF-IDF vectorizer.
        If the TF-IDF vectorizer is not initialized, it will raise a ValueError.
        """
        if self.tfidf_vectorizer is None:
            raise ValueError("TF-IDF vectorizer is not initialized")
        
        # Preprocess the input query
        query_text = self.preprocess_text(query)
        
        # Transform the preprocessed query into a vector
        query_vec = self.tfidf_vectorizer.transform([query_text])
        
        # Calculate the cosine similarity between the query vector and the TF-IDF matrix
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)
        
        # Get the indices of the top K similar documents
        top_k_indices = similarities.argsort()[0][-self.k:]
        
        # Load the articles of the top K similar documents from the JSON files
        top_k_documents = [json.load(open(os.path.join(self.data_dir, f"webpage_{i+1}.json"), 'r', encoding='utf8'))['article'] for i in top_k_indices]
        
        return top_k_documents

    def search_word2vec(self, query):
        """
        Searches for similar documents using the Word2Vec model.
        If the Word2Vec model is not initialized, it will raise a ValueError.
        """
        if self.word2vec_model is None:
            raise ValueError("Word2Vec model is not initialized")
        
        # Preprocess the input query
        query_text = self.preprocess_text(query)
        
        # Get the vector representation of the preprocessed query using the Word2Vec model
        query_vec = self.word2vec_model.wv[query_text.split()]
        
        # Find the most similar documents to the query vector
        similar_documents = self.word2vec_model.wv.most_similar(query_vec, topn=self.k)
        
        # Get the articles of the top K similar documents from the JSON files
        top_k_documents = [json.load(open(os.path.join(self.data_dir, f"webpage_{i+1}.json"), 'r', encoding='utf8'))['article'] for i, (doc, sim) in enumerate(similar_documents) if sim >= similar_documents[0][1]]
        
        return top_k_documents


if __name__ == "__main__":
    indexer = DocumentIndexer(r"crawler\data")
    query = "find the deleted messages"

    top_k_tfidf = indexer.search_tfidf(query)
    # top_k_word2vec = indexer.search_word2vec(query)

    print("Top K similar documents (TF-IDF):", top_k_tfidf)
    # print("Top K similar documents (Word2Vec):", top_k_word2vec)
