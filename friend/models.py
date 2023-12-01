from django.db import models
from django.conf import settings
from django.utils import timezone

# friend file added by bo (remove if needed)

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")

    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        
        #add new friend
        if not account in self.friends.all():
            self.friends.add(account)
            #self.save()
        
    def remove_friend(self, account):

        #remove friend
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):

        #action of unfriending
        remover_friends_list = self #person who unfriends

        remover_friends_list.remove_friend(removee) #removes friend from person who initiated the unfriending

        friends_list = FriendList.objects.get(user=removee) #removes person who initiated unfriending from the friend that was just unfriended or something idk
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):

        #is friend?
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    #Friend request has two parts
        #Sender - the human who sends the request
        #Reciever - the human who gets the request

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

    #function defines if friend request is currently active
    is_active = models.BooleanField(blank = True, null = False, default = True)

    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        #accept the friend request
        #updates both sender and receiver

        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        #decline a request
        #it's declined by setting 'is_active' field to False

        self.is_active = False
        self.save()


    def cance(self):
        #cancel sent friend request by sender
        #it's canceled by setting 'is_active' field to False
        #the only difference between this and declining the request is the notification that is generated

        self.is_active = False
        self.save()