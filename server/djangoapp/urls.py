# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path('register', views.registration, name='register'),
    # path for login
    path(route='login', view=views.login_user, name='login'),
    path('logout', views.logout_view, name='logout'),
    # path for dealer reviews view

    # path for add a review view
    path(route='add_review', view=views.add_review, name='add_review'),
    #path for get_cars
    path('get_cars', views.get_cars, name='getcars'),

    # path for get dealerships
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # path for getting a single dealer's details
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),

    # path for getting dealer reviews
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)