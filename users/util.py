from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib  # For ML model loading

model = joblib.load('path_to_model.pkl')

@api_view(['POST'])
def predict_fraud(request):
    data = request.data
    # Extract features and predict
    features = [data['amount'], data['location'], data['ip_address']]
    prediction = model.predict([features])
    return Response({'fraud': bool(prediction[0])})
