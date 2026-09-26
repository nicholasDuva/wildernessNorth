import pandas as pd
from flask import Flask, jsonify, render_template_string, request

# Initialize the Flask application
app = Flask(__name__)


# Default root route
@app.route("/")
def home():
    return jsonify(
        {"message": "Welcome to the Flask backend!", "status": "success"}
    )

@app.route("/orders", methods=["POST"])
def upload_csv():
    

    # Check if a file was sent in the request
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and file.filename.endswith(".csv"):
        try:
            # Read the CSV file directly into memory using pandas
            IN_MEMORY_DATA = pd.read_csv(file)

            # Convert first few rows to dict just to show a preview in the response
            preview = IN_MEMORY_DATA.head(5).to_dict(orient="records")

            return jsonify(
                {
                    "message": "CSV uploaded and Saved"
                }
            ), 200
        except Exception as e:
            return jsonify(
                {"error": f"Failed to parse CSV file: {str(e)}"}
            ), 500

    return jsonify({"error": "Invalid file type. Please upload a CSV."}), 400

if __name__ == "__main__":
    # Run the application in debug mode on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)