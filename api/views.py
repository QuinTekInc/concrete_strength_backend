
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *
from sklearn.discriminant_analysis import StandardScaler 

from concrete_strength_backend.settings import ML_MODEL_PATH, ML_SCALER_PATH
from .ml_model import prediction_utl

import joblib #responsible for running the ml model
from sklearn.preprocessing import LabelEncoder

from numpy import ndarray

import warnings
warnings.filterwarnings("ignore")



@api_view(['POST'])
def make_prediction(request):

    cement_age = request.data.get('cement_age')
    water_cement_ratio = request.data.get('water_cement_ratio')
    density = request.data.get('density')
    mass = request.data.get('mass')
    cement_type = request.data.get('cement_type')


    inputs_list = [cement_age, water_cement_ratio, density, mass, cement_type]


    # Validate inputs
    if None in inputs_list:
        return Response({'message': f'Missing input data.'}, status=HTTP_400_BAD_REQUEST)



    # feature_columns = [
    #     'age_days',
    #     'water_cement_ratio', 
    #     'density_kg_m3',
    #     'mass_g',
    #     'cement_type_encoded',
    #     # 'age_category_encoded',-to avoid data leakage
    #     # 'strength_to_density_ratio', - to avoid data leakage
    # ]

# {
# "cement_age": 7,
# "water_cement_ratio": 0.45, 
# "density" :14,
# "mass": 27,
#  "cement_type" : "GHACEM"
# }


    model = None
    scaler = None

    try:
        model = joblib.load(ML_MODEL_PATH)
        scaler = joblib.load(ML_SCALER_PATH)

    except Exception as e:
        return Response({'message': 'Model file does not exist.'}, status=HTTP_404_NOT_FOUND)
    

    #todo: vectorize the input features

    encoder = LabelEncoder()
    #encode the cement type
    encoder.fit(['GHACEM', 'SUPACEM'])
    cement_type_encoded = encoder.transform([cement_type])[0]

    feature_values_matrix = [[cement_age, water_cement_ratio, density, mass, cement_type_encoded]]

    x_test = scaler.transform(feature_values_matrix)

    prediction: ndarray = model.predict(x_test)

    prediction_result = list(prediction)[0]
    
    return Response({'prediction_result': prediction_result})

