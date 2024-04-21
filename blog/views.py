from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from blog.models import Article
from blog.serializers import ArticleSerializer


# Create your views here.
class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):

        MINIMUM_MATCH_SCORE = 0.025
        search_qry = request.query_params.get("search_qry", None)
        if not search_qry:
            return Response({"message": "Search query is missing"}, status=400)

        # basic full-text search
        # articles_obj = Article.objects.filter(title__search=search_qry)

        """
            pass the model fields in the SearchVector
            against you want to perform search
            I am passing only title field
        """
        vector = SearchVector("title")
        # Encapsulate the search query parameter
        search_qry = SearchQuery(search_qry)

        articles_obj = (
            Article.objects.annotate(
                score=SearchRank(vector=vector, query=search_qry)
            ).filter(score__gte=MINIMUM_MATCH_SCORE).order_by("-score")
        )
        articles = ArticleSerializer(articles_obj, many=True)
        return Response(articles.data, status=200)
