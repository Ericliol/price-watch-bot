const Discord = require("discord.js");
const bot = new Discord.Client();

const token = "OTgxNzY2MjU5MTk0NTkzMzcx.GjIuvc.ZnGw17qrludPi9a4Vuyu4OGr1sFlqZ7XitF0K4";

bot.on('ready',() => {
    console.log("BOT ONLINE!");
});

bot.login(token);