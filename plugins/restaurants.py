from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
from time import sleep
from threading import Thread
from operator import itemgetter

class RestaurantPlugin(WillPlugin):

    def __init__(self):
        self.voting = False
        self.votes = {}
        self.person_votes = {}
        self.message = None
        self.onepp = True

    @respond_to("restaurant add (?P<restaurant>.*)")
    def add_restaurant(self, message, restaurant):
        """restaurant add ___: I can add a restaurant to our list!"""
        rlist = self.load("restaurants", [])
        if restaurant not in rlist:
            rlist.append(restaurant)

        self.save("restaurants", rlist)
        self.reply(message, "Got it. '" + restaurant + "' is in our list.")

    @respond_to("restaurant list")
    def list_restaurants(self, message):
        """restaurant list: I can list off all the restaurant we've added!"""
        rlist = self.load("restaurants", [])
        if rlist == []:
            self.reply(message, "The list is empty. Add some with 'restaurant add ____'!")
        else:
            self.reply(message, "The restaurants we have are: \n - " + "\n - ".join(rlist))

    @respond_to("restaurant clear")
    def clear_restaurants(self, message):
        """restaurant clear: I can clear the list of restaurants!"""
        self.save("restaurants", [])
        self.reply(message, "Cleared the list.")

    @respond_to("restaurant remove (?P<restaurant>.*)")
    def remove_restaurant(self, message, restaurant):
        """restaurant remove ___: Made a mistake? We can remove it!"""
        rlist = self.load("restaurants", [])

        if restaurant in rlist:
            rlist.remove(restaurant)
            self.save("restaurants", [])
            self.reply(message, "Successfully removed '" + restaurant + "' from our list.")
        else:
            self.reply(message, "Couldn't find '" + restaurant + "'. Are you sure you capitalized and spelled it correctly?")

    @respond_to("restaurant vote!")
    def vote_restaurant(self, message):
        """restaurant vote!: I can start a poll to decide on a place to have Haoqi buy us lunch from!"""
        self.voting = True
        rlist = self.load("restaurants", [])

        for item in rlist:
            self.votes[item] = 0

        # this has the disadvantage of only being usable in one chatroom or shit gets messed up
        self.message = message
        wait_thread = Thread(target=self.end_voting)
        wait_thread.start()

        self.say("Now collecting votes for 30 seconds! Type the name of the restaurant you want from the list!", message=message)

    def end_voting(self):
        sleep(20)
        self.say("10 seconds left!", message=self.message)
        sleep(10)

        if self.onepp:
            rlist = self.load("restaurants", [])
            rlist2 = [i.lower() for i in rlist]
            for key, value in self.person_votes.iteritems():
                self.votes[rlist[value]] += 1

            self.person_votes = {}

        sorted_votes = sorted(self.votes.items(), key=itemgetter(1), reverse=True)
        self.say("The results!:\n\n - " + "\n - ".join("%s: %s" % (key, value) for key, value in sorted_votes), message=self.message)
        self.voting = False
        self.votes = {}

    @hear("(?P<restaurant>.*)")
    def collect_vote(self, message, restaurant):
        if self.voting == False:
            return
        else:
            rlist = self.load("restaurants", [])
            rlist2 = [i.lower() for i in rlist]
            if self.onepp:
                try:
                    i = rlist2.index(restaurant.lower());
                    self.person_votes[message.sender.nick] = i
                except Exception, e:
                    pass
            else:
                try:
                    i = rlist2.index(restaurant.lower())
                    self.votes[rlist[i]] += 1
                except Exception, e:
                    pass


    @respond_to("restaurant toggle")
    def toggle_vote(self, message):
        """restaurant toggle: switch the voting system between onepp and ctrl+v spam!"""
        self.onepp = not self.onepp

        if self.onepp:
            out_mode = "onepp"
        else:
            out_mode = "ctrl+v spam"
        self.say("Switched mode to " + out_mode + ".", message=message)

