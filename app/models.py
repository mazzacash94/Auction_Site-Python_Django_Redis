from django.db import models
from django.contrib.auth.models import User
from .utils import sendTransaction
import hashlib
from django.urls import reverse

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

    def __str__(self):

        return self.title

# get id of the auction to connect the popup page for bidding in the homepage

    def get_absolute_url(self):

        return reverse("auction_detail", kwargs={"id": self.id})

# write the hash of the auction on the ropsten ethereum blockchain

    def writeOnChain(self, json):

        json.hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(json.hash)
        self.hash = json.hash
        self.save()
