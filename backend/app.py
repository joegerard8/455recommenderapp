from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

import numpy as np

app = Flask(__name__)
CORS(app)

def get_cf_recommendations(user_id, user_item_matrix, user_similarity_df, n=5):
    if user_id not in user_similarity_df.index:
        return {}

    user_similarities = user_similarity_df.loc[user_id].drop(user_id)
    user_items = user_item_matrix.loc[user_id]
    user_items = user_items[user_items > 0].index.tolist()

    recommendations = {}

    for similar_user, similarity in user_similarities.items():
        if similarity <= 0:
            continue

        similar_user_items = user_item_matrix.loc[similar_user]
        similar_user_items = similar_user_items[similar_user_items > 0].index.tolist()

        new_items = [item for item in similar_user_items if item not in user_items]

        for item in new_items:
            recommendations[item] = recommendations.get(item, 0) + similarity

    recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n]
    return {item_id: score for item_id, score in recommendations}

print("🔄 Starting Flask app and loading models...")

# === Load Models and Data ===
try:
    collab_model = joblib.load(os.path.join('models', 'collaborative_filtering_model.sav'))
    content_model = joblib.load(os.path.join('models', 'content_model.sav'))
    user_item_matrix = joblib.load(os.path.join('models', 'user_item_matrix.sav'))
    articles_df = pd.read_csv('shared_articles.csv')

    # Force types to match expected
    collab_model.index = collab_model.index.astype(int)
    collab_model.columns = collab_model.columns.astype(int)
    articles_df['contentId'] = articles_df['contentId'].astype(int)

    print("✅ Models and article data loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    collab_model = None
    content_model = None
    articles_df = None

# === Home route for sanity check ===
@app.route('/')
def home():
    return jsonify({'message': 'Backend is running'})

# === Collaborative Filtering Route (USER-BASED) ===
@app.route('/api/recommendations/collaborative', methods=['POST'])
def collaborative_recommendations():
    data = request.get_json()
    person_id = data.get('person_id')

    if not person_id:
        return jsonify({'error': 'person_id is required'}), 400

    try:
        person_id = np.int64(person_id)

        if person_id not in collab_model.index:
            return jsonify({'error': f'Person ID {person_id} not found in model'}), 404

        recs = get_cf_recommendations(
            user_id=person_id,
            user_item_matrix=user_item_matrix,
            user_similarity_df=collab_model
        )

        # Build enriched results
        results = []
        for content_id in recs.keys():
            article = articles_df[articles_df['contentId'] == content_id]
            if not article.empty:
                title = article.iloc[0]['title']
                results.append({
                    'contentId': int(content_id),
                    'title': title
                })
            else:
                results.append({
                    'contentId': int(content_id),
                    'title': 'Unknown Article'
                })

        return jsonify({'recommendations': results})


    except Exception as e:
        print("❌ Error in collaborative filtering:", e)
        return jsonify({'error': str(e)}), 500

# === Content-Based Filtering Route ===
@app.route('/api/recommendations/content', methods=['POST'])
def content_recommendations():
    data = request.get_json()
    item_id = data.get('item_id')
    item_id = np.int64(data.get('item_id'))  # Ensure item_id is treated as int

    if not item_id:
        return jsonify({'error': 'item_id is required'}), 400

    try:
        item_id = int(item_id)

        print(f"🛬 Incoming item_id: {item_id}")
        print("🔍 Checking against content IDs:", articles_df['contentId'].head().tolist())

        if item_id not in articles_df['contentId'].values:
            return jsonify({'error': f'Item ID {item_id} not found in articles'}), 404

        idx = articles_df[articles_df['contentId'] == item_id].index[0]
        sim_scores = list(enumerate(content_model[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
        top_indices = [i[0] for i in sim_scores]

        recommendations = []

        for i in top_indices:
            article = articles_df.iloc[i]
            recommendations.append({
                'contentId': int(article['contentId']),
                'title': article['title']
            })

        return jsonify({'recommendations': recommendations})

    except Exception as e:
        print("❌ Error in content-based filtering:", e)
        return jsonify({'error': str(e)}), 500

# === Run the App ===
if __name__ == '__main__':
    print("✅ Running Flask app on http://localhost:5000")
    app.run(port=5000, debug=True)
