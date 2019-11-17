#!/usr/bin/python
import discord
import os.path
from discord.ext import commands
from googleapiclient.discovery import build

#Assign values to unique variables
TOKEN = 'YOUR BOT TOKEN'
my_api_key = "YOUR API KEY"
my_cse_id = "YOUR CSE ID"

#Function to search for file and update search history, if not found, create
def add_history(cmd):
    if os.path.exists('history.txt'):
        file = open('history.txt','a+')
        file.write(f'{cmd}\n')
    else:
        file = open('history.txt','a+')
        file.write(f'{cmd}\n')

#Function to trigger Custom Google Search and return raw data
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

client = commands.Bot(command_prefix = '')

#Handling Events

@client.event
async def on_ready():
    print('Bot is  ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')

@client.event
async def on_message(message):

    #To send Hey if user input hi or Hi or HI
    if message.content == 'hi' or message.content == 'Hi' or message.content == 'HI' :
        await message.channel.send('Hey')
        in_cmd = message.content


    #To filter out data and pass the search term to function google_search() and print links from raw data received
    elif message.content[:7] == '!google':
        await message.channel.send(f'Top 5 search result for {message.content[7:]} are:')
        in_cmd = message.content
        results = google_search(
            message.content[7:], my_api_key, my_cse_id, num=5)
        for result in results:
            link = result.get('link')
            await message.channel.send(f'{link}\n')
        add_history(in_cmd)


    #Defining recent functionality 
    elif message.content[:7] == '!recent':
        search_term = message.content[7:]
        if search_term.lstrip() == '':
            await message.channel.send('Please mention what you are looking for like \n!recent google')
        if search_term.lstrip() != '':
            with open("history.txt","r") as search_file:
                for search_line in search_file:
                    if search_term in search_line:
                        await message.channel.send(f'{search_line[7:]} \n')

client.run(TOKEN)
