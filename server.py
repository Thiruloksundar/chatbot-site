from flask import Flask, render_template, request, jsonify
import openai
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERPAPI_KEY")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    if "news" in user_input.lower():
        # Use SerpAPI to get search results
        search = GoogleSearch({
            "q": user_input,
            "location": "India",
            "api_key": SERP_API_KEY
        })
        results = search.get_dict()
        links = []
        if "organic_results" in results:
            for res in results["organic_results"][:5]:
                links.append(res.get("link", ""))
        response = "\n".join(links) if links else "No results found."
        return jsonify({'response': response})
    else:
        # Use ChatGPT
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            reply = completion.choices[0].message['content']
            return jsonify({'response': reply})
        except Exception as e:
            return jsonify({'response': f"Error: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
