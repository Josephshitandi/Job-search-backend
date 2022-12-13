from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import viewsets,status,generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from django.http import HttpResponse, Http404
import json
from rest_framework import filters  
from rest_framework.generics import ListAPIView
# from filer.models import mixins
from rest_framework import mixins

# Create your views here.



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = UserSignupSerializer
#     queryset = User.objects.all()
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated,IsCustomerOrMerchantOrAdmin]
    serializer_class = UserSignupSerializer
    
class SignupAPIView(generics.GenericAPIView):
    serializer_class = UserSignupSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSignupSerializer(user,context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]
        })

class LogoutAPIView(generics.CreateAPIView):
    serializer_class=LogoutSerializer
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token=request.data.get('refresh_token')
        error_message={
            "error":"Token is invalid or expired"
        }
        success_message={
            "success":"Logout successfully"
        }        
        try:
            token=RefreshToken(token)
            token.blacklist()
        except TokenError as error:
            return Response(error_message,status=status.HTTP_400_BAD_REQUEST)
        return Response(success_message,status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing profile instances.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = ProfileSerializer(user.profile)
        return Response(profile_serializer.data)
    
    
class ProfileList(APIView):
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        
class JobViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing job instances.
    """
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    
class JobsViewSet(APIView):
    def get(self, request, format=None):      
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        permission_classes = [IsAuthenticated]
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)