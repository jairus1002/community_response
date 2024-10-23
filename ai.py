from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API key
api_key = "AIzaSyB0exgFLLDaljxqXN2qPtQ2AVdDDRLoQaw"
genai.configure(api_key=api_key)

@app.route('/')
def index():
    return render_template('ai.html', generated_text=None)  # Pass None initially

@app.route('/get_disease_info', methods=['GET', 'POST'])  # Allow GET and POST methods
def get_disease_info():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        prompt = f"Explain the symptoms of a poultry disease: {symptoms} and try to summarize the main points only; make the characters not exceed 200."
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-exp-0827")
        
        # Generate text using the model
        response = model.generate_content(prompt)
        generated_text = response.text  # Get the generated text
        
        return render_template("ai.html", generated_text=generated_text)  # Pass the generated text to the template
    
    # If GET request, render the form
    return render_template('ai.html', generated_text=None)  # Adjust as needed

if __name__ == '__main__':
    app.run(debug=True)
