# importing necessary dependencies
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import sklearn

app = Flask(__name__)  # initializing a flask application


@app.route("/")  # route to display the home page
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/predict", methods = ['POST','GET']) # route to display predicted results in a web UI
@cross_origin()
def index():
    """'Try to read the data inputs given by the user and predict the
        result by using the loaded model(pickle file) and showing the
        result through a web UI """
    if request.method == 'POST':
        try:
            gre_score = float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']

            if is_research == 'yes':
                research = 1
            else:
                research = 0

            file = 'model.pickle'
            loaded_model = pickle.load(open(file, 'rb'))

            prediction = loaded_model.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
            print('prediction is', prediction)
            return render_template("results.html", prediction=round(prediction[0]*100, 2))
        except Exception as err:
            print('The exception is : ', err)
            return "something is wrong"

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
