from django.urls import path
from .views import RegisterApiView, LoginView, manage_book, manage_reviews



urlpatterns = [
    path('register-user/', RegisterApiView.as_view(), name = 'register-user'),
    path('user-login/', LoginView.as_view(), name= 'user-login'),
    path('manage-book/', manage_book, name= 'manage-book-get-books'),
    path('manage-book/<int:userID>/', manage_book, name='manage-book-add-book'),
    path('manage-book/<int:userID>/<int:bookID>/', manage_book, name= 'manage-book-edit-book'),
    path('manage-book/<int:userID>/<int:bookID>/', manage_book, name= 'manage-book-delete-book'),
    path('manage-review/<int:bookID>/', manage_reviews, name= 'manage-review-get'),
    path('manage-review/<int:userID>/<int:bookID>/', manage_reviews, name= 'manage-review-post'),
    path('manage-review/<int:userID>/<int:bookID>/<int:reviewID>/', manage_reviews, name= 'manage-review-put'),
    path('manage-review/<int:userID>/<int:bookID>/<int:reviewID>/', manage_reviews, name= 'manage-review-delete'),
]