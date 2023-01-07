import json
from datetime import datetime,date,timedelta
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime
from django.core.serializers import serialize
from django.core.paginator import Paginator

from .models import User, Group, Card


def index(request):
    user = request.user
    groups = Group.objects.all()

    if user.is_authenticated:
        context = {
            'groups': groups.filter(user_id=user)
        }
        return render(request, "app/index.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


@login_required
def card(request, id):
    deck_group = Group.objects.get(id=id).id
    deck_cards = Card.objects.filter(group__id=deck_group)
    deck_name = Group.objects.get(id=id)
    context = {
        'cards': deck_cards,
        'deck': deck_name
    }
    return render(request, 'app/cards.html', context)


@login_required
def newcard(request):
    if request.method == "POST":
        front = request.POST["front"]
        back = request.POST["back"]
        group = request.POST["group"]
        group_id = Group.objects.get(id=group).id
        revision = datetime.now()

        Card.objects.create(front=front, back=back,
                            group_id=group_id, revision=revision)

        context = {
            'cards': Card.objects.filter(group__id=group_id),
            'deck': Group.objects.get(id=group_id)
        }
        return render(request, 'app/cards.html', context)
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def remove_card(request, id):
    group_id = Card.objects.get(id=id).group.id
    rem_car = Card.objects.get(id=id)
    rem_car.delete()
    context = {
        "cards": Card.objects.filter(group__id=group_id),
        "deck": Group.objects.get(id=group_id)
    }
    return render(request, 'app/cards.html', context)


@login_required
def remove_deck(request, id):
    rem_car = Group.objects.get(id=id)
    rem_car.delete()
    return HttpResponseRedirect(reverse("index"))


@login_required
def newdeck(request):
    if request.method == "POST":
        user = request.user
        group = request.POST["group"]
        description = request.POST["description"]
        Group.objects.create(user=user, group=group, description=description)
    return HttpResponseRedirect(reverse("index"))


@login_required
def review(request):
    user = request.user
    deck_list = Group.objects.filter(user=user)
    context = {
        "decks": deck_list
    }
    return render(request, 'app/review.html', context)


@login_required
def review_table(request,id):
    cards = Card.objects.filter(group_id=id)
    data = serialize("json", cards, fields=('front', 'back','revision'))
    return JsonResponse(data, safe=False)


@login_required
def review_deck(request,id):
    today_date = date.today()
    card_deck = Card.objects.filter(group_id=id)
    filtered_deck = card_deck.filter(revision__lte=today_date)

    paginator = Paginator(filtered_deck, 1)
    card_number = request.GET.get('page')
    all_cards = paginator.get_page(card_number)

    context={
        "today_date" : today_date,
        "all_cards" : all_cards

    }
    return render(request,'app/reviewCards.html',context)



@login_required
def review_deck_update(request,id):
    if request.method == "POST":
        factor = request.POST["factor"]
        revision_date = Card.objects.get(id=id).revision
        revision_date = revision_date + timedelta(days=int(factor))

        Card_to_update = Card.objects.get(id=id)
        Card_to_update.revision = revision_date
        Card_to_update.save()

    group_id = Card.objects.get(id=id).group.id
    today_date = date.today()
    card_deck = Card.objects.filter(group_id=group_id)
    filtered_deck = card_deck.filter(revision__lt=today_date)

    paginator = Paginator(filtered_deck, 1)
    card_number = request.GET.get('page')
    all_cards = paginator.get_page(card_number)

    context={
        "today_date" : today_date,
        "all_cards" : all_cards

    }
    return render(request,'app/reviewCards.html',context)