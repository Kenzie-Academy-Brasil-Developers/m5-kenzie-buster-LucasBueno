from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .permissions import IsEmployee


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployee]

    def post(self, request: Request) -> Response:
        seriazlizer = MovieSerializer(data=request.data)
        seriazlizer.is_valid(raise_exception=True)
        seriazlizer.save(user=request.user)

        return Response(seriazlizer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request, self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployee]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        get_object_or_404(Movie, id=movie_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie, user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
