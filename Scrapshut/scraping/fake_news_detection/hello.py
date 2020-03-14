from flask import Flask
from flask import request
from flask import json
from flask_cors import CORS
import pandas as pd
# our own packages
from ml import ourModel
from ml import execnet
from rep import mlToOut
from subprocess import call


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# INIT ALL ML
print("loading tensorflow  model")
sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer = ourModel.loadML()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/claims", methods=['POST'])
def foo():
    inputType = json.loads(request.data)
    isURL = inputType['type'] == 'url'
    userInput = inputType['claim']
    sources = []
    if isURL:
        print("Calling webscraper!")
        # sources = webscraper.web_scrape(userInput)
        # result = execnet.call_python_version("2.7", "webscraper", "web_scrape", [userInput])
        # print(result)

        ############# ALL ML #############
        arg1 = userInput
        exit_code = call("python2 watson_scraper.py url " + userInput, shell=True)
        print("Finished")
        # result = execnet.call_python_version("2.7", "webscraper", "web_scrape", [userInput])
        # print(result)

        # Stances = ourModel.runModel(sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)


        newsData = pd.read_csv('url.csv')
        URLs = newsData['url'].tolist()
        SourceName = newsData['source'].tolist()
        BodyID = newsData['id'].tolist()

        # stances is a <List> of 0-3 classifications
        Stances = ourModel.runModel(sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)
        BodyID = range(len(Stances))
        ml_output = pd.DataFrame(
            {'BodyID': BodyID,
            'Stances': Stances,
            'SourceName': SourceName,
            'URL': URLs
        })

        response = ml_output.reset_index(drop=True)
        response = response.to_dict(orient='records')
        final_score = mlToOut.returnOutput(ml_output)
        final_score = (final_score + 1)/2
        print("final score: %d", final_score)

        response[0] = final_score
    else:
        arg1 = userInput
        exit_code = call("python2 watson_scraper.py claim " + userInput, shell=True)
        print("Finished")
        # result = execnet.call_python_version("2.7", "webscraper", "web_scrape", [userInput])
        # print(result)

        # Stances = ourModel.runModel(sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)


        newsData = pd.read_csv('url.csv')
        URLs = newsData['url'].tolist()
        SourceName = newsData['source'].tolist()
        BodyID = newsData['id'].tolist()

        # stances is a <List> of 0-3 classifications
        Stances = ourModel.runModel(sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)
        BodyID = range(len(Stances))
        ml_output = pd.DataFrame(
            {'BodyID': BodyID,
            'Stances': Stances,
            'SourceName': SourceName,
            'URL': URLs
        })

        response = ml_output.reset_index(drop=True)
        response = response.to_dict(orient='records')
        final_score = mlToOut.returnOutput(ml_output)
        final_score = (final_score + 1)/2
        print("final score: %d", final_score)

        response[0] = final_score

    # data = [{'name': "CLAIM!!!", 'agree': "99%", 'disagree': "1%" }, { 'name': "Response #2", 'agree': "55%", 'disagree': "45%"}]
    print(response)
    response = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

    ########### Josh's Algs ############

    # outputs final confidence from 0 to 1
    # response['answer'] = final_score
    # print(response)
    # response['answer']
    return response
if __name__ == '__main__':
    app.run()
