from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Profile

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)
from django.http import HttpResponse

from django.contrib.auth.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer , ProfileList

##auth jwt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

## For individual post user api
from rest_framework import mixins
from rest_framework import generics

#send email
from django.core.mail import send_mail

## Can be uswed to list users  ( but can be harmfull to list all users  )
## Since this mixes list an create  .. go one step back

class Usercreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # def _allowed_methods(self):
    #     return [ 'POST', 'HEAD', 'OPTIONS']
    #
    # ##Alllow get but give out your own response
    # def get(self, request):
    #     response = {'message': 'Create function is not offered in this path.'}
    #     return Response(response, status=HTTP_403_FORBIDDEN)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

## Broken down as this

# class Usercreate(mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

def sending_mail(request):
    print("Sending mail ")

    #testing manager
    print()

    send_mail(
        'Subject here',
        'Here is the message.',
        'expense.vue@gmail.com',
        ['sunilbpoojari@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("HI sunil ")



class Profilelist(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileList
    permission_classes = [IsAdminUser]
