"All seetings to control GSD-AFTER hours wiil exist in this file"

import boto3
import os
from base64 import b64decode

def get_gsd_after_hours_settings():
    "This returns a dictionary of all settings"

    #decrypt environmental variables, webhook URL and Help Desk Channel ID
    kms_client = boto3.client('kms')

    enc_webhook = os.environ['web_hook']
    dec_webhook = kms_client.decrypt(CiphertextBlob=b64decode(enc_webhook))['Plaintext']
    enc_channel_id = os.environ['channel_id']
    dec_channel_id = kms_client.decrypt(CiphertextBlob=b64decode(enc_channel_id))['Plaintext']
    dec_channel_id  = dec_channel_id.decode("utf-8")
    enc_slack_token = os.environ['slack_token']
    dec_slack_token = kms_client.decrypt(CiphertextBlob=b64decode(enc_slack_token))['Plaintext'].decode("utf-8")

    slack_text_to_post = "The Global Service Desk is currently closed. For urgent help call 1-866-GET-SPLUNK #7"

    return  {
        'Monday_start': (os.environ.get('Start', '9:00')),
        'Monday_stop': (os.environ.get('End', '17:00')),
        'Tuesday_start': (os.environ.get('Start', '9:00')),
        'Tuesday_stop': (os.environ.get('End', '17:00')),
        'Wednesday_start': (os.environ.get('Start', '9:00')),
        'Wednesday_stop': (os.environ.get('End', '17:00')),
        'Thursday_start': (os.environ.get('Start', '9:00')),
        'Thursday_stop': (os.environ.get('End', '17:00')),
        'Friday_start': (os.environ.get('Start', '9:00')),
        'Friday_stop': (os.environ.get('End', '17:00')),
        'web_hook_url': dec_webhook,
        'help_desk_channel_id': dec_channel_id,
        'message': slack_text_to_post,
        'slack_token': dec_slack_token
    }
