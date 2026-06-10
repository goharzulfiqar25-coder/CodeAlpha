"""
CodeAlpha AI Internship - Task 2: Chatbot for FAQs
Author: [Zulfiqar Gauhar]
Description: FAQ Chatbot using NLP (TF-IDF + Cosine Similarity)
"""

import numpy as np
import json
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ─────────────────────────────────────────────
#  FAQ DATASET
# ─────────────────────────────────────────────
FAQ_DATA = [
    {
        "question": "What is CodeAlpha?",
        "answer": "CodeAlpha is a leading software development company dedicated to driving innovation and excellence across emerging technologies. It offers internship programs in AI, Web Development, and more."
    },
    {
        "question": "What tasks are included in the AI internship?",
        "answer": "The AI internship includes 4 tasks:\n1. Language Translation Tool\n2. Chatbot for FAQs\n3. Music Generation with AI\n4. Object Detection and Tracking\nYou need to complete at least 2 or 3 tasks."
    },
    {
        "question": "How many tasks do I need to complete?",
        "answer": "You must complete a minimum of 2 or 3 tasks to be eligible for the internship completion certificate. Submitting only 1 task is considered incomplete."
    },
    {
        "question": "What certificate will I receive?",
        "answer": "You will receive:\n- Internship Offer Letter\n- Completion Certificate (QR Verified)\n- Unique ID Certificate\n- Letter of Recommendation (based on performance)"
    },
    {
        "question": "What are the internship perks and benefits?",
        "answer": "Internship perks include:\n- Offer Letter\n- Completion Certificate (QR Verified)\n- Unique ID Certificate\n- Letter of Recommendation\n- Job Opportunities / Placement Support\n- Resume Building Support"
    },
    {
        "question": "How do I submit my project?",
        "answer": "A submission form will be shared in your WhatsApp group. Submit your completed task only through that form. Follow the instructions carefully to ensure your submission is accepted."
    },
    {
        "question": "Where do I upload my source code?",
        "answer": "Upload your complete source code to GitHub in a repository named: CodeAlpha_ProjectName. Make sure your code is well-documented and includes a README file."
    },
    {
        "question": "What should I post on LinkedIn?",
        "answer": "Share your internship status on LinkedIn tagging @CodeAlpha. After completing your project, post a video explanation with your GitHub repository link."
    },
    {
        "question": "What is the contact information for CodeAlpha?",
        "answer": "Contact CodeAlpha at:\n- Website: www.codealpha.tech\n- WhatsApp: +91 9336576683\n- Email: services@codealpha.tech or services.codealpha@gmail.com"
    },
    {
        "question": "What is Task 1 Language Translation Tool?",
        "answer": "Task 1 requires you to create a user interface where users can enter text and select source and target languages. Use Google Translate API or Microsoft Translator to process the input and display the translated text."
    },
    {
        "question": "What is Task 3 Music Generation with AI?",
        "answer": "Task 3 involves collecting MIDI music data, preprocessing it into note sequences using music21 library, building a deep learning model (RNN/LSTM or GAN), training it on music patterns, and generating new MIDI music sequences."
    },
    {
        "question": "What is Task 4 Object Detection and Tracking?",
        "answer": "Task 4 requires setting up real-time video input using OpenCV, using a pre-trained model like YOLO or Faster R-CNN for object detection, drawing bounding boxes, and applying object tracking algorithms like SORT or Deep SORT."
    },
    {
        "question": "How long is the internship?",
        "answer": "Complete the assigned projects within the mentioned time frame as specified in your internship documents. Check your offer letter or WhatsApp group for specific deadlines."
    },
    {
        "question": "Is the internship paid?",
        "answer": "The internship focuses on skill development and provides certificates, letter of recommendation, and placement support rather than monetary compensation."
    },
    {
        "question": "What technologies are used in the AI internship?",
        "answer": "The AI internship uses technologies like Python, NLTK, SpaCy, TensorFlow, PyTorch, OpenCV, YOLO, music21, Google Translate API, and more depending on the tasks you choose."
    },
]


# ─────────────────────────────────────────────
#  TEXT PREPROCESSING
# ─────────────────────────────────────────────
class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        """Clean and normalize text."""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens
                  if t not in self.stop_words and len(t) > 1]
        return ' '.join(tokens)


# ─────────────────────────────────────────────
#  FAQ CHATBOT ENGINE
# ─────────────────────────────────────────────
class FAQChatbot:
    def __init__(self, faq_data):
        self.faq_data = faq_data
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self._build_index()

    def _build_index(self):
        """Build TF-IDF index from FAQ questions."""
        questions = [f['question'] for f in self.faq_data]
        self.processed_questions = [self.preprocessor.preprocess(q) for q in questions]
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_questions)
        print(f"[INFO] FAQ index built with {len(self.faq_data)} entries.")

    def get_response(self, user_query, threshold=0.1):
        """Find the best matching FAQ for a user query."""
        processed_query = self.preprocessor.preprocess(user_query)
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]

        if best_score >= threshold:
            matched_faq = self.faq_data[best_idx]
            return {
                "answer": matched_faq["answer"],
                "matched_question": matched_faq["question"],
                "confidence": round(float(best_score), 4),
                "found": True
            }
        else:
            return {
                "answer": ("I'm sorry, I couldn't find a relevant answer to your question.\n"
                           "Please contact CodeAlpha directly:\n"
                           "Email: services@codealpha.tech\n"
                           "WhatsApp: +91 9336576683"),
                "matched_question": None,
                "confidence": 0.0,
                "found": False
            }

    def get_all_topics(self):
        """Return list of all FAQ topics."""
        return [f['question'] for f in self.faq_data]


# ─────────────────────────────────────────────
#  COMMAND LINE CHAT INTERFACE
# ─────────────────────────────────────────────
def run_cli_chat(chatbot):
    """Run a simple command-line chatbot interface."""
    print("\n" + "="*60)
    print("   CodeAlpha FAQ Chatbot - AI Internship Assistant")
    print("="*60)
    print("Type your question and press Enter.")
    print("Commands: 'topics' = list all FAQs | 'quit' = exit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Goodbye! Good luck with your internship!")
            break
        if user_input.lower() == 'topics':
            topics = chatbot.get_all_topics()
            print("\nBot: Available topics:")
            for i, t in enumerate(topics, 1):
                print(f"  {i}. {t}")
            print()
            continue

        response = chatbot.get_response(user_input)
        print(f"\nBot: {response['answer']}")
        if response['found']:
            print(f"     [Matched: '{response['matched_question']}' | "
                  f"Confidence: {response['confidence']*100:.1f}%]")
        print()


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    chatbot = FAQChatbot(FAQ_DATA)
    run_cli_chat(chatbot)
