import json
import boto3
import os
import time
import dateutil.tz
import logging
from config import get_gsd_after_hours_settings
from botocore.vendored import requests
from datetime import datetime

gsd_settings = get_gsd_after_hours_settings()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#return challenge to Slack if requested
def return_challenge_to_slack(challenge):
    return {'challenge': challenge}
# Verify Slack Request
def verify_slack_request(token):
    if token == gsd_settings.get('slack_token'):
        return True
    else:
        logger.warning("Verification failed.")
        return False

#function to check if message was posted to the help desk channel
def is_help_channel(event):
    if event['event']['channel'] == gsd_settings.get('help_desk_channel_id'):
        return True
    return False

#Function to check if time is during working hours
def is_working_hours():
    "Get current time"
    pacific_time = dateutil.tz.gettz('US/Pacific')
    now = datetime.now(tz=pacific_time)
    "Check current date and time"
    day_of_week = now.strftime("%A")
    time_of_day = now.strftime("%H:%M")

    time_of_day_datetime = datetime.strptime(time_of_day, '%H:%M')
    work_datetime_start = datetime.strptime(gsd_settings.get(day_of_week + '_start'), '%H:%M')
    work_datetime_end = datetime.strptime(gsd_settings.get(day_of_week + '_stop'), '%H:%M')

    if day_of_week == "Saturday" or day_of_week == "Sunday":
        return False
    if time_of_day_datetime < work_datetime_start or time_of_day_datetime > work_datetime_end:
        return False
    else:
        return True

#This function post to Help Desk Channel if a message is received after
def lambda_handler(event, context):
    # TODO implement
    try:
        if 'challenge' in event and 'url_verification' in event['type']:
            return return_challenge_to_slack(event['challenge'])

        # Verify Slack Request Authenticity
        if not verify_slack_request(event['token']) and "url_verification" in event['type']:
            logger.error('Bad request.')
        #time.sleep(1)
        slack_msg = {}

        #Verify that the message came from Slack
        #Check if message was posted to Help-Desk Channel and During non business hours
        if is_help_channel(event) and is_working_hours() == False:
            #Check if the last message was posted by a user, ignore if it was posted by a Slack bot
            if 'user' in event['event']:
                #Check if message was posted during business hours and reply with message if outside of business hours
                slack_msg = {
                    'text': '<@' + event['event']['user'] + '>' + gsd_settings.get('message')
                }
                #Post the reply message as a Thread of the message from the user
                if 'thread_ts' not in event['event']:
                    slack_msg['thread_ts'] = event['event']['ts']
                requests.post(gsd_settings.get('web_hook_url'), data=json.dumps(slack_msg))

    except Exception as e:
        raise Exception(e)

    return {
        'statusCode': 200,
        'body': json.dumps(slack_msg)
    }
