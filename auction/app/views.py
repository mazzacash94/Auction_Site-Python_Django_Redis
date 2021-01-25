from django.shortcuts import render, redirect
from .forms import *
from .models import Auction, Profile
from django.contrib import messages
import datetime
from datetime import timedelta
import json, redis
from django.contrib.auth.decorators import login_required

client=redis.StrictRedis(host='127.0.0.1', port=6379, password='',db=0)

def home(request):

    auctionsActive = Auction.objects.filter(status=True)
    auctionsExpired = Auction.objects.filter(status=False)
    auctionsLenght = len(auctionsActive)
    currentDate = datetime.datetime.now().strftime("%d %b, %Y %H:%M:%S")

    for auction in auctionsActive:

        if auction.endDate.replace(tzinfo=None) <= datetime.datetime.now():

            if auction.winner == None:

                auction.status = False
                auction.save()
                client.rpush(f"{auction.title}", f"{currentDate} - Nobody won the auction!")

            else:

                auction.status=False
                auction.auctionCompleted(auction.winner,auction.advertiser)
                client.rpush(f"{auction.title}", f"{currentDate} - {auction.winner} wins the auction for {auction.endPrice}$!")

    return render(request, "index.html", {"auctionsActive":auctionsActive,"auctionsExpired":auctionsExpired, "auctionsLenght":auctionsLenght})

@login_required()
def publishAuction(request):

    user=request.user
    form = auctionForm(request.POST, request.FILES)
    currentDate = datetime.datetime.now().strftime("%d %b, %Y %H:%M:%S")

    if request.method=="POST":

        if form.is_valid():

            auction=form.save(commit=False)
            auction.advertiser=user
            auction.startDate=datetime.datetime.now()
            auction.endDate=auction.startDate+timedelta(minutes=2)
            auction.endPrice=request.POST.get("startPrice")
            auction.save()
            client.lpush(f"{auction.title}",f"{currentDate} - Auction starts with the price of {auction.startPrice}$!")
            return redirect("../")

        else:

            form=auctionForm()

    return render(request, "publish.html", {"form":form})

@login_required()
def bid(request, id):

    count = 0
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

                    count+=1
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

    return render(request, "bid.html", {"form":form, "auction":auction, "endDateFormat":endDateFormat})


def profile(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    profiles = Profile.objects.all()

    if request.method == "POST":

        dataAuctions = []

        for profile in profiles:

            data = "User: " + str(profile.user), "Auctions Won: " + profile.auctionsWon, "Auctions Published: " + profile.auctionsPublished
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            dataAuctions.append(data)

        with open("report/report" + timestamp + ".json", "w") as outfile:

            json.dump(dataAuctions, outfile, indent="\t")

    return render(request, "profile.html", {"profile":profile})