
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("card/<str:id>", views.card, name="card"),
    path("newcard", views.newcard, name="newcard"),
    path("remove_card/<str:id>", views.remove_card, name="remove_card"),
    path("remove_deck/<str:id>", views.remove_deck, name="remove_deck"),
    path("review", views.review, name="review"),
    path("newdeck", views.newdeck, name="newdeck"),
    path("review_deck/<str:id>", views.review_deck, name="review_deck"),
    path("review_deck_update/<str:id>", views.review_deck_update, name="review_deck_update"),

    #API
    path("review_table/<str:id>", views.review_table, name="review_table"),
]
