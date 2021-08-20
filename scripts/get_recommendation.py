import sys
sys.path.append("..")

from recommendation.top_score_recommendation import TopScoreRecommendation


if __name__ == "__main__":
	request = 'A Place in the Sun'
	reco = TopScoreRecommendation()
	print(reco.get_top_recos_by_review_weighted_score(request, 3))