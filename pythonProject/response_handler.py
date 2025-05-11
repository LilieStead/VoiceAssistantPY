import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load training data from intents.json
def load_training_data():
    """Extracts training data from intents.json for ML training."""
    with open("intents.json", "r") as file:
        data = json.load(file)

    training_data = []
    labels = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            training_data.append(pattern.lower())  # Normalize text
            labels.append(intent["tag"])  # Assign a category

    return training_data, labels

# Train TF-IDF model
training_data, labels = load_training_data()
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_data)


def get_best_response(user_input):
    """Finds the most relevant response based on text similarity or returns a fallback message."""
    responses = load_training_data()  # Load intents

    user_vec = vectorizer.transform([user_input.lower()])
    similarities = cosine_similarity(user_vec, X).flatten()

    best_match_idx = similarities.argmax()
    best_intent = labels[best_match_idx]

    # Ensure confidence threshold is met
    confidence_score = similarities[best_match_idx]
    print(f"🔍 Match Confidence: {confidence_score:.2f}")

    if confidence_score < 0.55:  # Adjust threshold as needed
        return "I'm not too sure about your question, try rephrase the question!"

    # Retrieve the response from intents.json
    with open("intents.json", "r") as file:
        data = json.load(file)

    for intent in data["intents"]:
        if intent["tag"] == best_intent:
            return intent["responses"][0]

    return "I'm not too sure about your question, try rephrase the question!"