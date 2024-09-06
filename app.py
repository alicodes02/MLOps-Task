from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

def train_model():
    
    datasets = pd.read_csv('Salary_Data.csv')
    X = datasets.iloc[:, :-1].values
    Y = datasets.iloc[:, 1].values
    

    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=1/3, random_state=0)
    
    regressor = LinearRegression()
    regressor.fit(X_Train, Y_Train)
    
    return regressor

model = train_model()

@app.route('/predict', methods=['GET'])
def predict_salary():
    try:

        years_of_experience = float(request.args.get('years_of_experience'))

        input_data = np.array([[years_of_experience]])
        
        predicted_salary = model.predict(input_data)
        
        return jsonify({'years_of_experience': years_of_experience, 'predicted_salary': predicted_salary[0]})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
