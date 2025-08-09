from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the pre-trained vectorizer and data
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('mobile_data.pkl', 'rb') as f:
    mobile_data = pickle.load(f)
with open('combined_features.pkl', 'rb') as f:
    combined_features = pickle.load(f)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    name = request.form['name']
    rating = request.form['rating']
    price = request.form['price']
    corpus = request.form['corpus']
    
    # Combine user input
    user_input = f"{name} {rating} {price} {corpus}"
    
    # Get all features including user input
    all_mobiles = combined_features.tolist() + [user_input]
    
    # Transform features to vectors
    all_vectors = vectorizer.transform(all_mobiles)
    
    # Separate user vector and mobile vectors
    user_vector = all_vectors[-1]
    book_vectors = all_vectors[:-1]
    
    # Calculate similarities
    similarities = cosine_similarity(user_vector, book_vectors).flatten()
    
    # Get top 5 recommendations
    N = 5
    top_indices = similarities.argsort()[-N:][::-1]
    
    # Prepare recommendations
    recommendations = []
    for i, index in enumerate(top_indices, start=1):
        name = mobile_data.iloc[index]['name']
        recommendations.append(f"{i}. {name}")
    
    return render_template('output.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)