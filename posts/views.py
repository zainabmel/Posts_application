#This file will contain all endpoints

from django.shortcuts import render,redirect 
from django.http import JsonResponse
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import User

def index(request):
    
    return render(request,"index.html")


#Get all the posts, serialize them, and return json
@api_view(['GET', 'POST'])
def post_list(request, format=None): #format used when user type .json in url

    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])  
def post_detail(request, postID, authorID, format=None): #the id sends through the url

    try:
        post = Post.objects.get(pk=postID,author=authorID) # gets a post by its id
        user=User.objects.get(pk=authorID) # gets the user by its id
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data=request.data
        data["author"]=authorID
        data["author_name"]=user.name
        serializer = PostSerializer(post, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)