import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load dataset
mobile_data = pd.read_csv('D:/Project2Mobile/mobile_recommendation_system_dataset.csv')

# Select features and handle missing values
selected_features = ['name', 'ratings', 'price', 'corpus']
for feature in selected_features:
    mobile_data[feature] = mobile_data[feature].fillna(' ')

# Combine features
combined_features = mobile_data['name'] + ' ' + mobile_data['ratings'].astype(str) + ' ' + mobile_data['price'].astype(str) + ' ' + mobile_data['corpus']

# Initialize and fit vectorizer
vectorizer = TfidfVectorizer()
all_vectors = vectorizer.fit_transform(combined_features.tolist())

# Save the vectorizer and mobile data for later use
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('mobile_data.pkl', 'wb') as f:
    pickle.dump(mobile_data, f)
with open('combined_features.pkl', 'wb') as f:
    pickle.dump(combined_features, f)