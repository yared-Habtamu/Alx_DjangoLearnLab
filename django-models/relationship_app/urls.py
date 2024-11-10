from django.urls import path
from .views import list_books, LibraryDetailView,register,LiginView,LogoutView,admin_view, librarian_view, member_view,add_book, edit_book, delete_book


urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('admin-view/', admin_view, name='admin_view'), 
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
    path('add/', add_book, name='add_book/'),
    path('edit/<int:pk>/', edit_book, name='edit_book/'),
    path('delete/<int:pk>/', delete_book, name='delete_book/'),
]
