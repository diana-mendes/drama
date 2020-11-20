from flask import Flask, jsonify
from recommendation.top_score_recommendation import TopScoreRecommendation

app = Flask(__name__)


def prepare_output(request, drama_list):
	formatted_drama_list = str(", ".join(drama_list))
	output = "If you liked " + request + ", checkout " + "\n" + formatted_drama_list
	return output


@app.route("/")  # decorator that tells Flask what URL should trigger the function defined as hello()
def recommend():
	request = 'A Place in the Sun'
	recommender = TopScoreRecommendation()
	drama_list = recommender.get_top_recos(request, 3)
	return prepare_output(request, drama_list)


if __name__ == '__main__':
	app.run(debug=True)
