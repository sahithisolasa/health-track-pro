import flask
import pickle
import pandas as pd

app = flask.Flask(
    __name__,
    static_url_path='/static',
    static_folder='templates',   # CSS inside templates
    template_folder='templates'
)

# Load model
with open('model/model.pkl', 'rb') as file:
    pipeline = pickle.load(file)

@app.route('/')
def home():
    return flask.render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = {
            'Age': [int(flask.request.form['Age'])],
            'Gender': [flask.request.form['Gender']],
            'HeartRate': [int(flask.request.form['HeartRate'])],
            'Symptoms': [flask.request.form['Symptoms']],
            'MedicalHistory': [flask.request.form['MedicalHistory']],
            'Smoker': [flask.request.form['Smoker']],
            'Drinker': [flask.request.form['Drinker']],
            'Exercise': [int(flask.request.form['Exercise'])],
            'SleepHours': [int(flask.request.form['SleepHours'])],
            'Weight': [int(flask.request.form['Weight'])],
            'BodyTemperature': [float(flask.request.form['BodyTemperature'])],
            'Lifestyle': [flask.request.form['Lifestyle']],
            'SystolicPressure': [int(flask.request.form['SystolicPressure'])],
            'DiastolicPressure': [int(flask.request.form['DiastolicPressure'])]
        }

        input_df = pd.DataFrame(input_data)

        # Encode categorical values
        input_df['Gender'] = input_df['Gender'].map({'Male': 1, 'Female': 0})
        input_df['Smoker'] = input_df['Smoker'].map({'Yes': 1, 'No': 0})
        input_df['Drinker'] = input_df['Drinker'].map({'Yes': 1, 'No': 0})
        input_df['Lifestyle'] = input_df['Lifestyle'].map({
            'Active': 2,
            'Moderate': 1,
            'Sedentary': 0
        })

        prediction = pipeline.predict(input_df)

        report = prediction[0][0]
        suggestions = prediction[0][1]
        habit = prediction[0][2]
        food = prediction[0][3]

        return flask.render_template(
            'result.html',
            report=report,
            suggestions=suggestions,
            habit=habit,
            food=food,
            systolic=flask.request.form['SystolicPressure'],
            diastolic=flask.request.form['DiastolicPressure'],
            heart_rate=flask.request.form['HeartRate'],
            sleep=flask.request.form['SleepHours']
        )

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)