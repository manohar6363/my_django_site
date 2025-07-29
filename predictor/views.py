import cloudpickle
import os
from django.shortcuts import render
from django.conf import settings

# Load model once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR,"predictor","banglore.pkl")
with open(model_path, "rb") as f:
    model = cloudpickle.load(f)

def home(request):
    if request.method == 'POST':
        # Collect data from form
        data = {
            'bedrooms': float(request.POST['bedrooms']),
            'bathrooms': float(request.POST['bathrooms']),
            'sqft_living': float(request.POST['sqft_living']),
            'sqft_lot': float(request.POST['sqft_lot']),
            'sqft_above': float(request.POST['sqft_above']),
            'sqft_basement': float(request.POST['sqft_basement']),
            'yr_built': float(request.POST['yr_built']),
            'yr_renovated': float(request.POST['yr_renovated']),
            'street': request.POST['street'].strip().lower(),
            'city': request.POST['city'].strip().lower()
        }

        # Convert to DataFrame
        import pandas as pd
        df = pd.DataFrame([data])

        # Predict
        prediction = model.predict(df)[0]
        prediction = round(prediction, 2)

        return render(request, 'predictor/home.html', {'prediction': prediction, 'inputs': data})

    return render(request, 'predictor/home.html')