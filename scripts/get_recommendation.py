import sys
import os
sys.path.append(os.path.abspath('.'))
print(sys.path)
# from recommendation.top_score_recommendation import TopScoreRecommendation
from recommendation.genre_recommendation import GenreRecommendation


if __name__ == "__main__":
	request = 'A Place in the Sun'
	# review_score_reco = TopScoreRecommendation()
	# print("Top dramas in the same genre by review score", review_score_reco.get_top_recos_by_review_weighted_score(request, 3))
	
	genre_reco = GenreRecommendation()
	print("Top dramas by genre similarity", genre_reco.get_genre_recommendation(request))