from recommendation.top_score_recommendation import TopScoreRecommendation


if __name__ == "__main__":
	request = 'A Place in the Sun'
	reco = TopScoreRecommendation()
	print(reco.get_top_recos(request, 3))