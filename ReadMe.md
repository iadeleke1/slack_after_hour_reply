Auto Respond to After Hour Post to Help Desk Slack Channel

##Requirments
-python3
-Slack Channel ID
-Slack Channel Webhook
-AWS Lambda

## Does the Bot reply as a thread
Yes, replies from the Bot are posted as a thread which invokes the username.

## How do I change the Channel ID to monitor
Change the Channel ID in Environmental Variable

## What happens if a message is posted during business hours
Nothing happens

## What if I need to change the Business Hours
Change the Day start and stop times as necessary in config.python3

## How do I change the message that is posted in the thread
Change slack_text_to_post variable in config.py

## How long would it take the Bot to respond
Immediately

## Does the Bot reply to Bot messages
No, only replies to User posts
