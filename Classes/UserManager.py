# Standard
import csv

# Community
import discord
from discord.ext import commands

class UserManager():
    """This class handles interaction with the user storage CSV file."""

    def __init__(self, bot, file_name):
        self.bot = bot
        self.file_name = file_name
        self.all_users = []
        self.read_list()
    
    def get_vrc_by_discord(self, discord_id):
        for user in self.all_users:
            if user[0] == discord_id:
                return user[1]
        return None

    def get_discord_by_vrc(self, vrchat_name):
        for user in self.all_users:
            if user[1] == vrchat_name:
                return user[0]
        return None

    def add_user(self, discord_id, vrchat_name):
        self.remove_user(discord_id)

        self.all_users.append([discord_id, vrchat_name])

        self.write_list()
    
    def remove_user(self, discord_id):
        
        i = 0
        while i < len(self.all_users):
            
            if self.all_users[i][0] == discord_id:
                del self.all_users[i]
            else: i += 1
        
        self.write_list()

    def read_list(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as csv_file:
                cursor = csv.reader(csv_file)
                
                self.all_users = []
                for line in cursor:
                    if len(line) == 2:
                        self.all_users.append([int(line[0]), line[1]])
        except FileNotFoundError:
            self.all_users = []

    def write_list(self):
        with open(self.file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerows(self.all_users)