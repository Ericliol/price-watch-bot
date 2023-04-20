from codecs import ignore_errors
from nextcord.ext import commands
from getPrice import get_price_single_url
import discord
import json

bot = commands.Bot(command_prefix="!")

def add_url_to_db(userid:str, url:str, price:float) -> None:
    """add transaction returned from bot to db"""
    with open('program/database/user_request_db.json', 'r') as f:
        db = json.load(f)

    user_transtactions = db["user_transtactions"]
    try:
        transaction = user_transtactions[str(userid)]
        url_list= transaction["url_list"]
        if url not in url_list:
            url_list.append(url)
    except:
        transaction = {}
        url_list = []
        transaction["notification method"] = "discord"
        transaction["url_list"] = url_list
        if url not in url_list:
            url_list.append(url)
    user_transtactions[str(userid)] = transaction
    db["user_transtactions"]= user_transtactions
    
    url_dict = db["url_on_watch"]
    if url in url_dict.keys():
        if str(price) != str(url_dict[url]["price"]):
            print(price,"error accur price not")
        if userid not in url_dict[url]["user on watch"]:
            url_dict[url]["user on watch"].append(userid)
    else:
        url_detial = {}
        url_detial["price"] = price
        url_detial["user on watch"] = [userid]
        url_dict[url] = url_detial
    db["url_on_watch"] = url_dict

    db = json.dumps(db, indent=4)
    with open('program/database/user_request_db.json', 'w') as outfile:
        outfile.write(db)
    print("bd update with",url, price)
    return None

# print(add_url_to_db("hehe","test2",10))


@bot.command(name="hi")
async def SendMassage(ctx):
    print(ctx.message.author.mention)
    await ctx.send("Hello")

@bot.command(name="check")
async def SendMassage(ctx,url:str):
    price = get_price_single_url(url)
    # print(price)
    await ctx.send(f"Hi{ctx.message.author.mention} I found the price as: {price}")

@bot.command(name="track")
async def SendMassage(ctx,url:str):
    price = get_price_single_url(url)
    # print(price)
    add_url_to_db(ctx.message.author.id,url,price)
    await ctx.send(f"Hi{ctx.message.author.mention} I found the price as: {price} Url has added to the database and u will be notified if the price has changed")

@bot.command(name="untrack")
async def SendMassage(ctx,url:str):
    await ctx.send("function unable")

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")


if __name__=='__main__':
    bot.run("OTgxNzY2MjU5MTk0NTkzMzcx.GHAGss.c8Ej1WmMcqzPe7age7yd4XgBHqJ7R1pLlbxQpo")