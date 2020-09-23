from ifunny import Client, objects
robot = Client(prefix = "$")
robot.login("email@email.com", 'password')

import discord
from discord.ext import commands
import os.path
from os import path
import requests
import csv
from io import StringIO
from time import strftime, localtime, sleep
from functions import *


@robot.event(name = "on_connect")
def _connected_to_chat(data):
    print("I'm connected")

botOwnerID = "226494896788209665"
description = '''Discord bot to ineract with iFunny.co

Bot owned by Request#0001'''
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description=description, case_insensitive=True)
allowedToGrabIPs = [370730771432079371, 443156642213920779, 414544308805435392, 625719520127877136, 699666917744705718, 386839413935570954, 201895055449915394, 662789287900610585] # Request, Tobi, Yakub, Defy, Bilk, MakeShiftArtist, Da_google

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    robot.start_chat()

@robot.command(name = "echo")
def _reply_with_same(message, args):
    print(f"You said {message.content}")

# User's information
@bot.command()
async def userid(ctx, id: str):
    try:
        user = objects.User(id=id, client=robot)
        last_seen = None
        if (user.can_chat and not user.id == "5d69ed55a5369476372aa2af"):
            for i in user.chat.members:
                if(i.__dict__['id'] == user.id):
                    if(i.__dict__['_sb_data_payload']['last_seen_at']):
                        last_seen = i.__dict__['_sb_data_payload']['last_seen_at']
                        return await ctx.send(embed=createUserEmbed(user, lastSeen = last_seen))
        return await ctx.send(embed=createUserEmbed(user))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Information about user %s failed" % id, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def user(ctx, username: str):
    try:
        user = objects.User.by_nick(username, client=robot)
        last_seen = None
        if (user.can_chat and not user.id == "5d69ed55a5369476372aa2af"):
            for i in user.chat.members:
                if(i.__dict__['id'] == user.id):
                    if(i.__dict__['_sb_data_payload']['last_seen_at']):
                        last_seen = i.__dict__['_sb_data_payload']['last_seen_at']
                        is_active = i.__dict__['_sb_data_payload']['is_active']
                        return await ctx.send(embed=createUserEmbed(user, lastSeen = last_seen, isActive = is_active))
        return await ctx.send(embed=createUserEmbed(user))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Information about user %s failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def ip(ctx, username: str):
    try:
        print(ctx.message.author.id not in allowedToGrabIPs)
        if (ctx.message.author.id not in allowedToGrabIPs):
            raise Exception("You are not allowed to IP grab users. Please ask Request#0002 to grab a user for you.")
        user = objects.User.by_nick(username, client=robot)
        if user.id == "5d69ed55a5369476372aa2af":
            raise Exception("You are not allowed to IP grab this user.")
        if user.id == "5f3174c2ec5740481655d41a":
            raise Exception("You are not allowed to IP grab this user.")
        if(user.can_chat):
            user.chat.send_image_url('http://ip.miyako.rocks:8080/{userid}.png'.format(userid=user.id))
            return await ctx.send(embed=createIPEmbed(user))
        else:
            raise Exception("Unable to chat with user (are their chats set to public?)")
        return await ctx.send(embed=createIPEmbed(user))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="IP grabbing of user %s failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def checkip(ctx, username: str):
    try:
        user = objects.User.by_nick(username, client=robot)
        if user.id == "5d69ed55a5369476372aa2af":
            raise Exception("You are not allowed to IP grab this user.")
        if user.id == "5f3174c2ec5740481655d41a":
            raise Exception("You are not allowed to IP grab this user.")
        if not user.id.isalnum():
            raise Exception("User ID is not alphanumeric. Check logs <@{botOwnerID}>".format(botOwnerID=botOwnerID))
        ippath = "../ipGrabber/ip/{userid}.txt".format(userid=user.id)
        if path.exists(ippath):
            contents = ""
            with open(ippath) as f:
                for line in f.readlines():
                    contents += line
                await ctx.send(contents)
        else:
            raise Exception("I don't have this user's IP address")
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Checking IP of user %s failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

# Subscriptions
@bot.command()
async def subscribe(ctx, username: str):
    try:
        user = objects.User.by_nick(username, client=robot)
        user.subscribe()
        return await ctx.send("subbed lol")
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Subscription to user %s failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def unsubscribe(ctx, username: str):
    try:
        user = objects.User.by_nick(username, client=robot)
        user.unsubscribe()
        return await ctx.send("unsubbed lol")
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Subscription to user %s failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def smileall(ctx, username: str):
    try:
        user = objects.User.by_nick(username, client=robot)
        if user.post_count > 50:
            await ctx.send("Smiling first 50 posts")
        else:
            await ctx.send("Smiling all of {userNick}'s posts".format(userNick=user.nick))
        count = 0
        for i in user.timeline:
            print("Smiling post {url}".format(url=i.link))
            i.smile()
            sleep(.3)
            count = count + 1
            if(count > 50):
                return await ctx.send("Smiling complete.")
        return await ctx.send("Smiling complete.")
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Smiling user %s posts's failed failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

# Utilities
@bot.command()
async def ipinfo(ctx, ip: str):
    try:
        if ip == "":
            raise Exception("Missing IP address")
        if (ip.count('.') != 3):
            if (ip.count(':') != 7):
                raise Exception("Invalid or missing IP address")
        data = requests.get('http://ip-api.com/json/{ip}'.format(ip=ip)).json()
        await ctx.send(embed=createIPLookupEmbed(ip, data))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Lookup for IP %s failed" % ip, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def posts(ctx, username: str):
    try:
        user = objects.User.by_nick(username, client=robot)
        fieldnames = ['url', 'fileURL', 'tags', 'created_at', 'publish_at', 'featured', 'smiles', 'unsmiles', 'republications', 'shares', 'views', 'comments', 'visibility', 'deleted_by_mods']
        if user.post_count > 50:
            await ctx.send("Collecting posts... This may take a while.")
        with open('posts/%s.csv' % user.nick, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in user.timeline:
                postData = i.__dict__['_object_data_payload']
                num = postData['num']
                tagsString = " ".join(postData['tags'])
                print("Adding post %s" % i.link)
                writer.writerow({
                    'url': postData['link'],
                    'fileURL': postData['url'],
                    'tags': tagsString,
                    'created_at': strftime('%Y-%m-%d %H:%M:%S', localtime(postData['date_create'])),
                    'publish_at': strftime('%Y-%m-%d %H:%M:%S', localtime(postData['publish_at'])),
                    'featured': postData['is_featured'],
                    'smiles': num['smiles'],
                    'unsmiles': num['unsmiles'],
                    'republications': num['republished'],
                    'shares': num['shares'],
                    'views': num['views'],
                    'comments': num['comments'],
                    'visibility':  postData['visibility'],
                    'deleted_by_mods': postData['is_abused']
                })
        await ctx.send(ctx.author.mention, file=discord.File('posts/%s.csv' % user.nick))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Posts lookup for %s failed" % username, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def chats(ctx, *passed):
    try:
        name = ' '.join(passed)
        if not all(c.isalnum() or c.isspace() for c in name):
            return await ctx.send(":no_entry: Invalid chat name")
        chats = robot.search_chats(name)
        fieldnames = ['url', 'cover_url', 'title', 'description', 'member_count']
        count = 0
        with open('chats/%s.csv' % name, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for chat in chats:
                count = count + 1
                chatData = chat.__dict__['_object_data_payload']
                if chatData['description']:
                    description = chatData['description']
                else:
                    description = ""
                writer.writerow({
                    'url': chatData['permalink'],
                    'cover_url': chatData['cover_url'],
                    'title': chatData['title'],
                    'description': description,
                    'member_count': chatData['members_count']
                })
        await ctx.send("{mention} I found {count} chats.".format(mention=ctx.author.mention, count=count), file=discord.File('chats/%s.csv' % name))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Searching for chats named %s failed" % name, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def dumpchat(ctx, code: str):
    try:
        chat = objects.Chat.by_link(code=code, client=robot)
        for message in chat.messages:
            print(message.content)
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Searching for chats named %s failed" % chat.name, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def ban(ctx, nick: str, *reason):
    try:
        sleep(0.6)
        embedVar = discord.Embed(title="User Banned", description="User %s has been banned from iFunny" % nick, color=0x00ff00)
        embedVar.add_field(name="Reason", value=' '.join(reason))
        return await ctx.send(embed=embedVar)
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Unable to ban user" % nick, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

@bot.command()
async def smiles(ctx, id: str):
    try:
        if not all(c.isalnum() or c.isspace() for c in id):
            raise Exception("Invalid post ID.")
        post = objects.Post(id, client=robot)
        smile_count = post.smile_count
        if(smile_count > 1000):
           await ctx.send("Collecting smiles, this may take a while.")
        else:
            await ctx.send("Collecting smiles.")
        fieldnames = ['userID', 'nick', 'is_verified', 'is_banned', 'total_posts', 'subscriptions', 'subscribers', 'is_deleted', 'original_nick']
        with open('smiles/%s.csv' % id, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            for user in post.smiles:
                userData = user._object_data
                print(userData)
                count = count + 1
                print("{count}/{smile_count} - {nick}".format(count=count, smile_count=smile_count, nick=user.nick))
                writer.writerow({
                    'userID': userData['id'],
                    'nick': userData['nick'],
                    'is_verified': userData['is_verified'],
                    'is_banned': userData['is_banned'],
                    'total_posts': userData['total_posts'],
                    'subscriptions': userData['num']['subscriptions'],
                    'subscribers': userData['num']['subscribers'],
                    'is_deleted': userData['is_deleted'],
                    'original_nick': userData['original_nick']
                })
        await ctx.send(ctx.author.mention, file=discord.File('smiles/%s.csv' % id))
    except Exception as e:
        embedVar = discord.Embed(title="Failed", description="Grabbing smiles for post %s failed" % id, color=0xFF0000)
        embedVar.add_field(name="Reason", value=str(e))
        return await ctx.send(embed=embedVar)

bot.run('token')

