from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration de la clé API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message', '')
    file = request.files.get('file')

    try:
        # Si un fichier est envoyé, vous pouvez le traiter ici
        if file:
            # Par exemple, enregistrer le fichier
            file.save(os.path.join('uploads', file.filename))
            # Vous pouvez également ajouter une logique pour traiter le fichier

        # Appel à l'API OpenAI avec le message de l'utilisateur
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extraction de la réponse
        ai_response = response.choices[0].message.content
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        print(f"Erreur: {str(e)}")  # Ajout d'un log pour déboguer
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 