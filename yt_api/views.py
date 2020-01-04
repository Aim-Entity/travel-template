from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import VideoSerializer, RatingSerializer, UserSerializer
from .models import Video, Rating
from django.contrib.auth.models import User


def index(request):
    return render(request, "home/index.html", {})


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(methods=["POST"], detail=True)
    def rate_video(self, request, pk=None):
        if "stars" in request.data:
            video=Video.objects.get(id=pk)
            stars = request.data["stars"]
            comments = request.data["comments"]
            user = request.user
            try:
                rating = Rating.objects.get(user=user.id, video=video.id)
                rating.stars = stars
                rating.comment = comments
                rating.save()

                serializer = RatingSerializer(rating, many=False)
                response = {"message": "Rating has been updated", "results": serializer.data}
                return Response(response, status=HTTP_200_OK)

            except:
                rating = Rating.objects.create(user=user, video=video, stars=stars, comments=comments)
                serializer = RatingSerializer(rating, many=False)
                response = {"message": "Rating created", "result": serializer.data}
                return Response(response, status=HTTP_200_OK)

        else:
            response = {"message": "Enter stars"}
            return Response(response, status=HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        response = {"message": "Rating cannot be updated like this"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )