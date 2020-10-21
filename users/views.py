from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from django.contrib.auth.models import User
from users.serializers  import UserSerializer

##auth jwt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN

## For individual post user api
from rest_framework import mixins
from rest_framework import generics

## Can be uswed to list users  ( but can be harmfull to list all users  )
## Since this mixes list an create  .. go one step back

class Usercreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def _allowed_methods(self):
        return [ 'POST', 'HEAD', 'OPTIONS']

    ##Alllow get but give out your own response
    def get(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=HTTP_403_FORBIDDEN)


## Broken down as this

# class Usercreate(mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)