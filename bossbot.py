# bot.py
import os
import discord
from dotenv import load_dotenv
import requests
from datetime import datetime
import json
import urllib3

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_voice_state_update(member, before, after):
  chnl = client.get_channel(int(os.getenv('VERBOSE_CHANNEL')))

  #
  if before.channel is None and after.channel is not None:
    if after.channel.id == int(os.getenv('VOICE_TRIGGER_CHANNEL')):
      await chnl.send('Preparing to start MC server...')

      http = urllib3.PoolManager()
      response = http.request('GET','https://api.mcstatus.io/v2/status/java/{svrip}'.format(svrip=os.getenv('SERVER_IP')))
      data = response.data
      jsonData = json.loads(data)

      if not jsonData["online"]:
        response = requests.post('{gatewayapi}/startminecraftserver'.format(gatewayapi=os.getenv('AWS_API_GATEWAY_URL')))
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        await chnl.send('Cloud instance started at {timeLog}. MC server should be available in 30 seconds.'.format(timeLog=current_time))
      else:
        await chnl.send('MC Server Already Started')

      return

  if before.channel is not None and after.channel is None:
    if before.channel.id == int(os.getenv('VOICE_TRIGGER_CHANNEL')):
      await chnl.send('Preparing to stop MC server...')

      #Check if there is still people in the voice channel
      memberInChannel = False
      for memberItr in client.guilds[0].members:
        if not memberItr.voice == None and memberItr.voice.channel.id == int(os.getenv('VOICE_TRIGGER_CHANNEL')):
          memberInChannel = True
          break

      #Close server if voice channel is empty
      if not memberInChannel:
        http = urllib3.PoolManager()
        response = http.request('GET','https://api.mcstatus.io/v2/status/java/{svrip}'.format(svrip=os.getenv('SERVER_IP')))
        data = response.data
        jsonData = json.loads(data)

        if not jsonData["online"]:
          await chnl.send('MC server is already unavailable.')

        response = requests.post('{gatewayapi}/stopminecraftserver'.format(gatewayapi=os.getenv('AWS_API_GATEWAY_URL')))
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        await chnl.send('Closing cloud instance at {timeLog}'.format(timeLog=current_time))
      else:
        await chnl.send('There are still members in the voice channel. MC server will stop when the last member leaves the voice channel.')

client.run(TOKEN)
