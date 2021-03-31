import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person"
]

if "responding" not in db.keys():
  db["responding"] = True



def get_joke():
  response = requests.get('https://official-joke-api.appspot.com/jokes/random')

  response = json.loads(response.text)
  
  return response

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  msg = message.content

  if message.author == client.user:
    return
    
  if db["responding"]:

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$joke'):
    joke = get_joke()
    setup = joke['setup']
    punchline = joke['punchline']
    await message.channel.send(setup + '\n' + punchline)

  if message.content.startswith('$math'):
    expression = message.content.split('$math ',1)[1]
    result = eval(expression)
    await message.channel.send(result) 
    
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    starter_encouragements.append(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouraging_message = msg.split("$del ",1)[1]
    if encouraging_message in starter_encouragements:
      starter_encouragements.remove(encouraging_message)
    await message.channel.send("Encouragement removed")
        

  if msg.startswith("$list"):
    await message.channel.send(starter_encouragements)

  if msg.startswith("$responding"):
    try:
      value = msg.split("$responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")
    except IndexError:
      await message.channel.send("Format is - $responding true/false")

  if msg.startswith("$help"):
    await message.channel.send('$inspire - get an inspiration quote. \n \n $joke - get a joke. \n \n $math ~your expression here~ - solves a basic math expression. \n \n $responding ~true/false~ - enable or disable replies by the bot to trigger words such as sad,depressed,unhappy etc. \n \n $new ~new encouragement message~ - add a new possible reply to the trigger words. \n \n $list - returns a list of all the encouraging messages. \n \n $del ~encouragement message~ - removes the specified encouraging reply from the possible replies.\n')

keep_alive()
client.run(os.getenv('TOKEN'))