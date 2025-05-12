from flask import Flask, render_template, request, jsonify
import requests # type: ignore
import logging

app = Flask(__name__)

API_URL = "https://jp-tok.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
API_KEY="2Ldr54qoqT8r59Q--aHqcTwAq5ffLXobzw23gY30vui0"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    """
    Render the home page with an empty output field.
    """
    return render_template('index.html', output="")

@app.route('/predict', methods=['POST'])
def predict():
   
    input_text = request.form.get('inputText', '').strip()
    if not input_text:
        return render_template('index.html', output="Error: Input text cannot be empty.")

    try:
        # Log the input text for debugging
        logging.info(f"Received input text: {input_text}")

        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        payload = {"input": input_text}

        # Make the API request
        logging.info("Sending request to Watsonx API...")
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses

        # Parse the API response
        response_data = response.json()
        output_text = response_data.get("output", "Error: No output from API")

        # Log the output text
        logging.info(f"Received output text: {output_text}")

    except requests.exceptions.Timeout:
        logging.error("Request to Watsonx API timed out.")
        output_text = "Error: The request to the API timed out. Please try again later."
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Watsonx API failed: {e}")
        output_text = f"Error: Failed to connect to the API. Details: {str(e)}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        output_text = f"Error: An unexpected error occurred. Details: {str(e)}"

    # Render the output on the home page
    return render_template('index.html', output=output_text)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Provide an API endpoint for external clients to use the informal-to-formal conversion.
    """
    data = request.get_json()
    input_text = data.get('inputText', '').strip()
    if not input_text:
        return jsonify({"error": "Input text cannot be empty."}), 400

    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        payload = {"input": input_text}

        # Make the API request
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the API response
        response_data = response.json()
        output_text = response_data.get("output", "Error: No output from API")

        return jsonify({"input": input_text, "output": output_text})

    except requests.exceptions.Timeout:
        return jsonify({"error": "The request to the API timed out. Please try again later."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to the API. Details: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred. Details: {str(e)}"}), 500

if __name__ == '__main__':
    logging.info("Starting Flask app...")
    app.run(debug=True)
