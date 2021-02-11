from django.shortcuts import render, redirect
from .forms import *
from .models import Auction
from django.contrib import messages
from datetime import timedelta
from rest_framework import viewsets
from .serializers import AuctionSerializer
from django.http import HttpResponse
import datetime
import redis

# connect to redis server


client = redis.StrictRedis(host='127.0.0.1', port=6379, password='', db=0)

# serializes all the queryset and converts into JSON


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all().order_by("-endDate")
    serializer_class = AuctionSerializer

# get specified auction by enter id in the url or error 404 if it doesn't exist


def auctionDetail(request, id):

    try:
        auction = Auction.objects.get(id=id)
    except Auction.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = AuctionSerializer(auction)
        return serializer.data

# shows active/expired orders and automatically ends and does operations if an auction becomes expired


def home(request):

    auctionsActive = Auction.objects.filter(status=True)
    auctionsExpired = Auction.objects.filter(status=False)
    auctionsLenght = len(auctionsActive)
    currentDate = datetime.datetime.now().strftime("%d %b, %Y %H:%M:%S")
    user = request.user
    form = auctionForm(request.POST, request.FILES)

    for auction in auctionsActive:

        if auction.endDate.replace(tzinfo=None) <= datetime.datetime.now():

            if auction.winner is None:

                auction.status = False
                auction.save()
                client.rpush(f"{auction.title}", f"{currentDate} - Nobody won the auction!")

            else:

                auction.status = False
                json = AuctionSerializer(auction)
                auction.writeOnChain(json.data)
                client.rpush(f"{auction.title}", f"{currentDate} - {auction.winner} wins the auction for {auction.endPrice}$!")

    if request.method == "POST":

        if form.is_valid():

            auction = form.save(commit=False)
            auction.advertiser = user
            auction.startDate = datetime.datetime.now()
            auction.endDate = auction.startDate+timedelta(seconds=30)
            auction.endPrice = request.POST.get("startPrice")
            auction.save()
            client.lpush(f"{auction.title}", f"{currentDate} - Auction starts with the price of {auction.startPrice}$!")
            return redirect("../")

        else:

            form = auctionForm()

    return render(request, "index.html", {"form": form, "auctionsActive": auctionsActive, "auctionsExpired": auctionsExpired, "auctionsLenght": auctionsLenght})

# popup page where you can bid for auction and different kind of message if you don't comply certain conditions


def bid(request, id):

    auction = Auction.objects.get(id=id)
    endDate = auction.endDate + timedelta(hours=1)
    endDateFormat = endDate.strftime("%d %b, %Y %H:%M:%S")
    user = request.user
    form = bidForm(request.POST or None)
    currentDate = datetime.datetime.now().strftime("%d %b, %Y %H:%M:%S")

    if request.method == "POST":

        bid = request.POST.get("endPrice")

        if form.is_valid():

            if auction.advertiser != user and auction.winner != user:

                if float(bid) > auction.endPrice:

                    auction.winner = user
                    auction.endPrice = bid
                    auction.save()
                    client.rpush(f"{auction.title}", f"{currentDate} - {auction.winner} bids {bid}$!")

                else:

                    messages.warning(request, "You have to bid an higher amount than the actual one!")

            elif auction.winner == user:

                messages.warning(request, "You have already placed your offer!")

            elif auction.advertiser == user:

                messages.error(request, "You are the advertiser of the auction!")

        else:

            form = bidForm()

    return render(request, "bid.html", {"form": form, "auction": auction, "endDateFormat": endDateFormat})
