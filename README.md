# mcbossbot
Discord bot to start and stop our family Minecraft server hosted on an AWS EC2 instance.

## Behavior
1. When the trigger-voice-channel is empty and a member enters the channel, the bot lauches the EC2 instance if the server is not already available.
2. When the last member leaves the trigger-voice-channel and the trigger-voice-channel is now empty, the bot stops the EC2 instance.
3. The bot provides information on the verbose-channel

![Phase1 Diagram](media\Phase1-diagram.PNG "Phase1 Diagram")




