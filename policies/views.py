from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Policy, Comment
from .serializers import PolicySerializer, CommentSerializer
from django.core.exceptions import ValidationError
# Create your views here.

@api_view(['GET', 'POST'])
def policies(request):
    if request.method == 'GET':
        try:
            paginator = PageNumberPagination()
            paginator.page_size = 5  # Set page size
            policies = Policy.objects.all()
            result_page = paginator.paginate_queryset(policies, request)
            serializer = PolicySerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            serializer = PolicySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET', 'PUT', 'DELETE'])
def policy(request, policy_id):
    if request.method == 'GET':
        policy = get_object_or_404(Policy, id=policy_id)
        serializer = PolicySerializer(policy)
        return Response(serializer.data)

    elif request.method == 'PUT':
        try:
            policy = get_object_or_404(Policy, id=policy_id)
            serializer = PolicySerializer(policy, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        policy = get_object_or_404(Policy, id=policy_id)
        policy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comments(request, policy_id):
    if request.method == 'GET':
        commnets = Comment.objects.filter(policy=policy_id)         
        serializer = CommentSerializer(commnets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            comment = Comment.objects.create(policy_id=policy_id, comment_text=request.data['comment_text'])
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
