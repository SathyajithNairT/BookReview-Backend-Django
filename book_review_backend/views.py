from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import BookDetails, Review
from .serializers import (
    UserRegisterSerializer, 
    LoginSerializer,
    BookSerializer,
    ReviewSerializer,
    )
from rest_framework import views
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegisterApiView(views.APIView):
    def post(self, request):
        email = request.data.get('email')

        if User.objects.filter(email = email).exists():
            return Response({'error': 'Email already exists.'}, status= status.HTTP_400_BAD_REQUEST)
        
        serializer = UserRegisterSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():

            print(serializer.validated_data)

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username = username, password = password)

            # print(f'User: {user}')

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_name': user.username,
                    'admin': user.is_staff,
                    'userID': user.id
                })
            else:
                return Response({'error':'Invalid Credentials.'}, status= status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','POST', 'PUT', 'DELETE'])
def manage_book(request, userID = None, bookID = None):

    def is_admin(userID):
        try:
            user = User.objects.get(id = userID)
            return user.is_staff
        except User.DoesNotExist:
            return False

    if request.method == 'GET':
        books = BookDetails.objects.all()
        serializer = BookSerializer(books, many = True)

        return Response(serializer.data, status= status.HTTP_200_OK)
    
    if is_admin(userID):
        if request.method == 'POST':    
            book = BookDetails(
                title = request.data.get('title'),
                author = request.data.get('author')
            )

            book.save()
            
            return Response({'Message': 'Book created successfully.'})
        
        if request.method == 'PUT':
            try:
                book = BookDetails.objects.get(id = bookID)

                book.title = request.data.get('title', book.title)
                book.author = request.data.get('author', book.author)

                book.save()

                return Response({'message': 'Book updated successfully.'})
            except BookDetails.DoesNotExist:
                return Response({'error': 'Book not found.'}, status= status.HTTP_404_NOT_FOUND)
            
        if request.method == 'DELETE':
            try:
                book = BookDetails.objects.get(id = bookID)
                book.delete()

                return Response({'message': 'Book deleted successfully.'})
            except BookDetails.DoesNotExist:
                return Response({'error': 'Book not found.'}, status= status.HTTP_404_NOT_FOUND)
        

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def manage_reviews(request, userID = None, bookID = None, reviewID = None):
    def get_review_user(reviewID):
        review = Review.objects.get(id = reviewID)
        return review.userID

    if request.method == 'GET':
        reviews = Review.objects.filter(bookID = bookID)
        serializer = ReviewSerializer(reviews, many = True)

        return Response(serializer.data, status= status.HTTP_200_OK)

    if request.method == 'POST':
        user = User.objects.get(id = userID)
        book = BookDetails.objects.get(id = bookID)

        review = Review(
            userID = user,
            bookID = book,
            review = request.data.get('review')
        )

        review.save()

        return Response({'message': 'Review Submission Successfull.'})
    
    if userID == get_review_user(reviewID):
        if request.method == 'PUT':
            try:
                review = Review.objects.get(id = reviewID)
                review.review = request.data.get('review', review.review)
                review.save()

                return Response({'message': 'Review updated successfully.'})
            except Review.DoesNotExist:
                return Response({'error': 'Review does not exist.'}, status= status.HTTP_404_NOT_FOUND)
            
        if request.method == 'DELETE':
            review = Review.objects.get(id = reviewID)
            review.delete()

            return Response({'message': 'Review deleted successfully.'}, status= status.HTTP_404_NOT_FOUND)
    
    