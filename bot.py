import discord
import responses
import botLib
import json
import numpy as np
import json
import notifications as nt
import asyncio


# Send messages
async def send_message(message, user_message, botInst, is_private = False):
    try:
        guild = message.guild
        response = responses.handle_response(user_message, botInst, guild, message.author)
        if str(response) != "None" and str(response) != "":
            response = ">>> " + response
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)



class botInstance:
    def __init__(self):
        try:
            f = open("resources\\token.txt", "r")
            TOKEN = f.read()
            f.close()
        except Exception as e:
            print(e)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.client = discord.Client(intents=intents)

        self.settings = {"prefix": "/", "teamPermRoles" : []}
        self.users = {}
        self.practices = []
        self.teams = {}
        self.load()

        @self.client.event
        async def on_ready():
            print(f'{self.client.user} is now running!')
            print(self.settings["prefix"] + " is the current prefix.")
            await nt.handleNotifications(self)
            

        @self.client.event
        async def on_message(message):
            # Make sure bot doesn't get stuck in an infinite loop
            if message.author == self.client.user:
                return

            # Get data about the user
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
            ID = message.author.id

            await send_message(message, user_message, self)
            
        
        self.client.run(TOKEN)

    def savePractices(self):
        with open("resources\\practices.json", "w") as f:
            json.dump(self.practices, f)

    def saveUsers(self):
        with open("resources\\users.json", "w") as f:
            json.dump(self.users, f)

    def saveSettings(self):
        with open("resources\\settings.json", "w") as f:
            json.dump(self.settings, f)

    def saveTeams(self):
        with open("resources\\teams.json", "w") as f:
            json.dump(self.teams, f)

    def load(self):

        #load practices
        try:
            f = open("resources\\practices.json", "r")
            self.practices = json.load(f)
        except Exception as e:
            print(e)

        #load users
        try:
            f = open("resources\\users.json", "r")
            self.users = json.load(f)
        except Exception as e:
            print(e)

        #load settings
        try:
            f = open("resources\\settings.json", "r")
            self.settings = json.load(f)
        except Exception as e:
            print(e)

        #load teams
        try:
            f = open("resources\\teams.json", "r")
            self.teams = json.load(f)
        except Exception as e:
            print(e)

