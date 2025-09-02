import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify
from config.config_entities import MODEL_PATH

app = Flask(__name__)

try:
    with open(MODEL_PATH, "rb") as f:
        loaded_model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("Model file not found. Ensure 'model.pkl' is in the root directory.")

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    try:
        # Extract and validate form data
        lead_time = int(request.form.get("lead_time", 0))
        no_of_special_request = int(request.form.get("no_of_special_request", 0))
        avg_price_per_room = float(request.form.get("avg_price_per_room", 0.0))
        arrival_month = int(request.form.get("arrival_month", 1))
        arrival_date = int(request.form.get("arrival_date", 1))
        market_segment_type = int(request.form.get("market_segment_type", 0))
        no_of_week_nights = int(request.form.get("no_of_week_nights", 0))
        no_of_weekend_nights = int(request.form.get("no_of_weekend_nights", 0))
        type_of_meal_plan = int(request.form.get("type_of_meal_plan", 0))
        room_type_reserved = int(request.form.get("room_type_reserved", 0))

        # Validate input ranges
        if not (0 <= lead_time <= 100):
            return render_template("result.html", error="Lead time must be between 0 and 100 days")
        if not (0 <= no_of_special_request <= 5):
            return render_template("result.html", error="Number of special requests must be between 0 and 5")
        if not (0 <= avg_price_per_room <= 200):
            return render_template("result.html", error="Average price per room must be between 0 and 200")
        if not (0 <= no_of_week_nights <= 8):
            return render_template("result.html", error="Number of week nights must be between 0 and 8")
        if not (0 <= no_of_weekend_nights <= 8):
            return render_template("result.html", error="Number of weekend nights must be between 0 and 8")

        # Prepare features
        features = np.array([[lead_time, no_of_special_request, avg_price_per_room, 
                             arrival_month, arrival_date, market_segment_type, 
                             no_of_week_nights, no_of_weekend_nights, type_of_meal_plan, 
                             room_type_reserved]])

        # Predict
        prediction = loaded_model.predict(features)[0]

        # Pass inputs for display
        inputs = {
            'lead_time': lead_time,
            'arrival_month': arrival_month,
            'arrival_date': arrival_date
        }

        return render_template("result.html", prediction=int(prediction), inputs=inputs)

    except ValueError:
        return render_template("result.html", error="Invalid input format")
    except Exception as e:
        return render_template("result.html", error=str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)