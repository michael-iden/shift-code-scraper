import os
from typing import List

import tweepy
import re
import slack

from shift_code_scraper.shift_code_client import ShiftCodeClient
from shift_code_scraper.user_builder import build_users

shift_code_pattern = re.compile("^[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}$")
slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


def is_borderlands_3_code(tweet_lines):
    status_line = tweet_lines[0].upper()
    if "SHIFT CODE" in status_line and "NOT" not in status_line:
        game_line = tweet_lines[1].upper()
        return "BORDERLANDS 3" in game_line


def extract_shift_code(tweet_lines):
    for line in tweet_lines:
        if shift_code_pattern.match(line):
            return line


def send_code_to_slack(code):
    slack_client.chat_postMessage(
        channel='#shift-codes',
        text=code
    )


def send_redemptions_to_slack(successful_submissions: List[str], failed_submissions: List[str]):
    success_message = f"Submission successful: {', '.join(successful_submissions)}\n" if successful_submissions else ''
    failure_message = f"Submission failure: {', '.join(failed_submissions)}" if failed_submissions else ''

    message = f"{success_message}{failure_message}"

    slack_client.chat_postMessage(
        channel='#shift-codes',
        text=message
    )


def get_shift_code_from_tweet(status):
    if not hasattr(status, 'retweeted_status'):
        tweet_lines = status.text.splitlines()

        if is_borderlands_3_code(tweet_lines):
            return extract_shift_code(tweet_lines)

    return None


def redeem_code(shift_code):
    successful_submissions = []
    failed_submissions = []

    for user in build_users():
        try:
            ShiftCodeClient(user, shift_code).submit_shift_code()
            successful_submissions.append(user.name)
        except Exception as e:
            print(e)
            failed_submissions.append(user.name)

    send_redemptions_to_slack(successful_submissions, failed_submissions)


class ShiftCodeStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        shift_code = get_shift_code_from_tweet(tweet)
        if shift_code:
            print(shift_code, flush=True)
            send_code_to_slack(shift_code)
            redeem_code(shift_code)

    def on_error(self, status_code):
        print(status_code, flush=True)
        return

    def on_exception(self, exception):
        print(exception, flush=True)
        return
