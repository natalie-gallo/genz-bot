import os
import discord
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents().all()
client = discord.Client(intents=intents)  #connection to discord

sad_words = ["depressed", "depression", "sad", "tired", "stressed"]

starter_unhelpful = [
  "aren't we all", "me too dawg", "damn bro", "same", "twins!", "so true",
  "you need help...but same", "get help"
]

#updates 1
rizz_words = ["rizz", "rizzer", "rizzler"]

starter_rizz = [
  "we got a rizz master here", "rizzler", "rizzing it up i see",
  "rizzstraining order", "rizzpecting my women :heymama:"
]

if "responding" not in db.keys():
  db["responding"] = True

manifesting = [
  "manifesting == mentally ill??", "manifesting clear skin",
  "manifesting happiness", "manifesting bank *cha ching*", "you need help",
  "stan loona for clear skin"
]


#helper function to update messages from the database
def update_unhelpful(unhelpful_message):  #db = database
  if "unhelpful" in db.keys():
    unhelpful = db["unhelpful"]
    unhelpful.append(unhelpful_message)
    db["unhelpful"] = unhelpful
  else:
    db["unhelpful"] = [unhelpful_message]


#helper to delete message
def delete_unhelpful(index):
  unhelpful = db["unhelpful"]
  if len(unhelpful) > index:
    del unhelpful[index]
    db["unhelpful"] = unhelpful


#Discord is an async library so things are done with "callbacks"
#a callback is a function that is called when something else happens


#register an event
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


#if bot recieves message
@client.event
async def on_message(message):
  #check if mesage is from user
  if message.author == client.user:
    return

  #check if message starts with a command '/'
  if message.content.startswith('/greet'):
    channel = message.channel
    await channel.send('say "hello" or dont idc')

    def check(m):
      return m.content == 'hello' and m.channel == channel

    msg = await client.wait_for('message', check=check)
    await channel.send(f'hello {msg.author}...*side eye*')

  if message.content.startswith('/slay'):
    await message.channel.send('sleighhhhhhhh')

  if message.content.startswith('/manifest'):
    await message.channel.send(random.choice(manifesting))

  #note- .lower().replace triggered with anything that has the word in it (hiking, working, etc)
  if 'sus' in message.content.lower().replace(' ', ''):
    await message.channel.send('sussy baka *snifffff*')

  if 'yippee' in message.content.lower().replace(' ', ''):
    await message.channel.send('yippee!')

  msg = message.content
  if any(word in msg for word in rizz_words):
    await message.channel.send(random.choice(starter_rizz))

  if db["responding"]:
    options = starter_unhelpful
    if "unhelpful" in db.keys():
      options = options + list(db["unhelpful"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("/new"):  #we want whatever texts comes after
    unhelpful_message = msg.split("/new ", 1)[1]
    # ^ splits array into 2 and gets 2nd element
    update_unhelpful(unhelpful_message)
    await message.channel.send("New Unhelpful Message Added.")

  if msg.startswith("/del"):
    unhelpful = []  #if theres not encouragements it returns empty list/arr
    if "unhelpful" in db.keys():
      index = int(msg.split("/del", 1)[1])
      delete_unhelpful(index)
      unhelpful = db["unhelpful"]
    await message.channel.send(unhelpful)

  if msg.startswith("/list"):
    unhelpful = []
    if "unhelpful" in db.keys():
      unhelpful = db["unhelpful"]
    await message.channel.send(unhelpful)

  if msg.startswith("/responding"):
    value = msg.split("/responding ", 1)[1]

    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


#client token connection
my_secret = os.environ['token']  #connect to discord bot
keep_alive()
client.run(my_secret)
