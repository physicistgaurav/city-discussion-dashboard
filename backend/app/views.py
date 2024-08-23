from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from src.fetch_news_topic import fetch_top_news_topic
from src.fetch_reddit_discussion import fetch_comments_for_topic
from src.analyze_gathered_info import getAnalyzedReport

@api_view(["GET"])
def health_check(request):
    return Response({"status": "api working successfully"})

@api_view(["GET"])
def fetch_news(request):
    city = request.query_params.get('city')
    if not city:
        return Response({"error": "City name is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Call the function to fetch top news topics
        top_news = fetch_top_news_topic(city)
        return Response({"top_news": top_news}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def fetch_comments(request):
    topic = request.data.get('topic')
    city = request.data.get('city')


    if not topic:
        return Response({"error": "Topic is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not city:
        return Response({"error": "city is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comments = fetch_comments_for_topic(topic, city)
        discussions = [f"Main News Topic: {comment['newsTopic']} | Reddit-Post on this news: {comment['PostTitle']} | Comment on this post by people: {comment['CommentBody']}" for comment in comments]
        summary,sentiment, actionable_needs = getAnalyzedReport(discussions)
        data = {"comments": comments,
                "summary": summary,
                "sentiment": sentiment,
                "actionable_needs": actionable_needs}
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
