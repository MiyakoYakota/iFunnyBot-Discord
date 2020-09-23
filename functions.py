from discord import Embed
from ifunny import objects
from time import strftime, gmtime
import timeago, datetime

def ifunnyuser(data):
    user = objects.User.by_nick(data, client=robot)
    if user == None:
        userid = objects.User(id=data, client=robot)
        user = userid
    return user

def props(cls):
  return [i for i in cls.__dict__.keys() if i[:1] != '_']


def createUserEmbed(user, lastSeen=None, isActive=None):
    userData = user._object_data
    embedVar = Embed(title=user.nick, description=user.about, color=0x00ff00)
    if (user.profile_image):
        embedVar.set_thumbnail(url=user.profile_image.url)
    else:
        embedVar.set_thumbnail(url="https://cdn.miyako.rocks/iFunny/nopfp.png")
    if (user.cover_image):
        embedVar.set_image(url=user.cover_image.url)
    else:
        embedVar.set_image(url="https://cdn.miyako.rocks/iFunny/nopfp.png")
    embedVar.add_field(name="User ID", value=userData['id'], inline=True)
    embedVar.add_field(name="Post Count", value='{:,}'.format(userData['num']['created']), inline=True)
    embedVar.add_field(
        name="Rating", value= "{level} ({days} Days)".format(
            level=userData['meme_experience']['rank'],
            days='{:,}'.format(userData['meme_experience']['days'])), 
        inline=True)
    embedVar.add_field(name="Feature Count", value='{:,}'.format(userData['num']['featured']), inline=True)
    embedVar.add_field(name="Smile Count", value='{:,}'.format(userData['num']['total_smiles']), inline=True)
    embedVar.add_field(name="Subscriber Count", value='{:,}'.format(userData['num']['subscribers']), inline=True)
    embedVar.add_field(name="Subscription Count", value='{:,}'.format(userData['num']['subscriptions']), inline=True)
    embedVar.add_field(name="Verified", value=str(userData['is_verified']), inline=True)
    embedVar.add_field(name="Chat Privacy", value=userData['messaging_privacy_status'].capitalize(), inline=True)
    embedVar.add_field(name="Visit Profile", value="[Click Here](%s)" % userData['web_url'])
    if lastSeen:
        date = datetime.datetime.now()
        embedVar.add_field(
            name="Last Seen",
            value="{time} ({ago})".format(
                time=strftime("%b %d %Y %H:%M:%S", gmtime(lastSeen/1000)),
                ago=timeago.format(lastSeen/1000, date)
            )
        )
    if isActive:
        embedVar.add_field(name="Is Active", value=str(isActive), inline=True)
    embedVar.set_footer(text="Bot made by Request#0002")
    return embedVar

def createIPEmbed(user, description=""):
    embedVar = Embed(title=user.nick, description=user.about, color=0x00ff00)
    if (user.profile_image):
        embedVar.set_thumbnail(url=user.profile_image.url)
    else:
        embedVar.set_thumbnail(url="https://cdn.miyako.rocks/iFunny/nopfp.png")
    embedVar.add_field(name="User ID", value=user.id, inline=True)
    embedVar.add_field(name="IP", value="Once the target views the image their ip will show [here]({iplink}).".format(iplink="http://ip.miyako.rocks:8080/ip/{userid}.txt".format(userid=user.id)), inline=True)
    embedVar.set_footer(text="Bot made by Request#0002")
    return embedVar

def createIPLookupEmbed(ip, data):
    embedVar = Embed(title=ip, description="Infromation about {}".format(ip), color=0x00ff00)
    for result in data:
        embedVar.add_field(name=result, value=data[result], inline=True)
        embedVar.set_footer(text="Bot made by Request#0002")
    return embedVar

