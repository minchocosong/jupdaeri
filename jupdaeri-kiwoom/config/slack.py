import requests
import json


class Slack():
    def __init__(self):
        self.token = 'Bearer xoxb-1816264673378-1816509713683-LVN8T90qDM1UdLu9zHOamxLA'

    def notification(self, pretext=None, title=None, fallback=None, text=None):
        attachments_dict = dict()
        attachments_dict['pretext'] = pretext
        attachments_dict['title'] = title
        attachments_dict['fallback'] = fallback
        attachments_dict['text'] = text

        attachments = [attachments_dict]

        url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        data = {"channel": "#jupjup", "attachments": attachments}

        requests.post(url, data=json.dumps(data), headers=headers)
