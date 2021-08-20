from flask import Flask, request, render_template
from recommendation.top_score_recommendation import TopScoreRecommendation
from recommendation.genre_recommendation import GenreRecommendation

app = Flask(__name__)


def recommend(request):
	"""
	Returns top 3 recommendations given `request`.
	:param request: string with input drama, e.g.: 'A Place in the Sun'.
	:return: list of recommended drama names
	"""
	# score_recommender = TopScoreRecommendation()
	# drama_list = score_recommender.get_top_recos_by_review_weighted_score(request, 3)
	
	genre_recommender = GenreRecommendation()
	drama_list = genre_recommender.get_genre_recommendation(request, 3)
	return drama_list


@app.route("/")
def index():
	return render_template('index.html')


@app.route("/", methods=['POST'])
def my_form_post():
	text = request.form['text']
	recos = recommend(text)
	return render_template('query_results.html', input=text, recos=recos)


if __name__ == '__main__':
	app.run(debug=True)
