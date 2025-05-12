# app.py
from flask import Flask, render_template, request
from model import informal_to_formal

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['inputText']
    output_text = informal_to_formal(input_text)
    return render_template('index.html', output=output_text)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)