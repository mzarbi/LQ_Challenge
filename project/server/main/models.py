import ast
import datetime
import json
from base64 import b64encode
import requests

IMGUR_BASE = "https://api.imgur.com"


class Task:
    def __init__(self):
        """

        :rtype: object
        """
        self.queue = list()
        self.pending = []
        self.complete = []
        self.failed = []
        self.url_map = {}
        self.created = datetime.datetime.now().isoformat()
        self.finished = None
        self.status = "pending"
        self.credentials = None

    def initialize(self, param, cred):
        """

        :rtype: object
        """
        for i in param:
            self.enqueue(i)
            self.pending.append(i)
        clean = str(cred).replace('b\"', '').replace('\"', '').replace("'", '"')
        self.credentials = ast.literal_eval(clean)

    def export(self):
        """

        :rtype: object
        """
        return {
            "created": self.created,
            "finished": self.finished,
            "status": self.status,
            "uploaded": {
                "pending": self.pending,
                "complete": self.complete,
                "failed": self.failed
            }
        }

    def executeAll(self, _set_task_progress):
        """

        :rtype: object
        """
        _set_task_progress(self)
        self.status = 'in-progress'
        _set_task_progress(self)
        while self.size() != 0:
            val = self.dequeue()
            if self.executeOne(val):
                self.pending.remove(val)
                self.complete.append(self.url_map[val])
                _set_task_progress(self)
            else:
                self.pending.remove(val)
                self.failed.append(val)
                _set_task_progress(self)
        self.status = 'complete'
        self.finished = datetime.datetime.now().isoformat()
        _set_task_progress(self)

    def executeOne(self, val):
        """

        :rtype: object
        """
        v,url = self.upload_image(path=None, url=val, title=None, description=None, album=None)
        if v:
            self.url_map.update({val: url})
            return True
        else:
            self.url_map.update({val: url})
            return False

    # Adding elements to queue
    def enqueue(self, data):
        """

        :rtype: object
        """
        # Checking to avoid duplicate entry (not mandatory)
        if data not in self.queue:
            self.queue.insert(0, data)
            return True
        return False

    # Removing the last element from the queue
    def dequeue(self):
        """

        :rtype: object
        """
        if len(self.queue) > 0:
            return self.queue.pop()
        return ("Queue Empty!")

    # Getting the size of the queue
    def size(self):
        """

        :rtype: object
        """
        return len(self.queue)

    def upload_image(self, path=None, url=None, title=None, description=None,
                     album=None):
        """

        :rtype: object
        """
        if bool(path) == bool(url):
            raise LookupError("Either path or url must be given.")
        if path:
            with open(path, 'rb') as image_file:
                binary_data = image_file.read()
                image = b64encode(binary_data)
        else:
            image = url
        payload = {'album_id': "58tq5Nw", 'image': image,
                   'title': title, 'description': description}

        #token = ast.literal_eval(str(self.credentials))["access_token"]
        token = self.credentials["access_token"]
        authentication = {'Authorization': 'Bearer {0}'.format(token)}
        verify = True
        resp = requests.post(IMGUR_BASE + "/3/image", payload, headers=authentication, verify=verify)
        if 'error' in json.loads(resp.content)["data"]:
            return False, json.loads(resp.content)["data"]["error"]
        else:
            return True, json.loads(resp.content)["data"]["link"]


