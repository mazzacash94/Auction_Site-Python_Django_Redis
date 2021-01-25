from django.db import models
from django.contrib.auth.models import User
from api.utils import sendTransaction
import hashlib
from django.urls import reverse
import json

# Create your models here.

class Auction(models.Model):

    advertiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_advertiser', null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_winner', null=True)
    title = models.CharField(max_length=30)
    text = models.TextField()
    startPrice = models.FloatField(null=True)
    endPrice = models.FloatField()
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/')
    startDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)
    json = models.TextField(default="")

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse("auction_detail", kwargs={"id":self.id})

    def auctionCompleted(self,winner,advertiser):

        jsonOrder = json.dumps({
            "Advertiser": str(self.advertiser),
            "Winner": str(self.winner),
            "Title": self.title,
            "Text": self.text,
            "startPrice": self.startPrice,
            "endPrice": self.endPrice,
            "startDate": str(self.startDate),
            "endDate": str(self.endDate),
        })
        self.json += jsonOrder
        profileWinner = Profile.objects.get(user=winner)
        profileAdvertiser = Profile.objects.get(user=advertiser)
        profileWinner.auctionsWon += jsonOrder
        profileAdvertiser.auctionsPublished += jsonOrder
        profileWinner.save()
        profileAdvertiser.save()
        self.save()
        self.writeOnChain(jsonOrder)

    def writeOnChain(self,json):

        self.hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        jsonHash = hashlib.sha256(json.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(jsonHash)
        self.json += " Json Hash : " + jsonHash
        self.save()

class Profile(models.Model):


    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auctionsWon = models.TextField()
    auctionsPublished = models.TextField()

    def __str__(self):

        return self.user








