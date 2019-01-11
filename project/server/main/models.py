import ast
import datetime
import json
from base64 import b64encode
import requests

IMGUR_BASE = "https://api.imgur.com"


class Task:
    """
    A class used to represent a job
    ...

    Attributes
    ----------
    queue : list
        the list of all urls
    pending : list
        the name of all pending urls
    complete : list
        the name of all completed urls
    failed : list
        the name of all failed urls
    url_map : dict
        a dictionary that maps provided urls with imgur urls
    created:
        date created
    finished:
        date finished
    status:
        the job status
    credentials:
        the access token and other useful objects

    """
    def __init__(self):
        """
        Create the object
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

    def initialize(self, urls, cred):
        """
        Initialize the object with parameters urls and cred
        :param urls : list > the list of urls
        :param cred : dict > the client credentials
        :rtype: object
        """
        for i in urls:
            self.enqueue(i)
            self.pending.append(i)
        clean = str(cred).replace('b\"', '').replace('\"', '').replace("'", '"')
        self.credentials = ast.literal_eval(clean)

    def export(self):
        """

        :rtype: dict
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
        Sequentially upload images and update job progress
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
        Upload a unique image
        :rtype: object
        """
        v,url = self.upload_image(path=None, url=val, title=None, description=None, album=None)
        if v:
            self.url_map.update({val: url})
            return True
        else:
            self.url_map.update({val: url})
            return False


    def enqueue(self, data):
        """
        Adding elements to queue
        :rtype: object
        """
        # Checking to avoid duplicate entry (not mandatory)
        if data not in self.queue:
            self.queue.insert(0, data)
            return True
        return False


    def dequeue(self):
        """
        Adding elements to queue
        :rtype: object
        """
        if len(self.queue) > 0:
            return self.queue.pop()
        return ("Queue Empty!")


    def size(self):
        """
        Getting the size of the queue
        :rtype: object
        """
        return len(self.queue)

    def upload_image(self, path=None, url=None, title=None, description=None,
                     album=None):
        """
        Upload image to the imgur server and returns the new url
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

        token = ast.literal_eval(str(self.credentials))["access_token"]

        authentication = {'Authorization': 'Bearer {0}'.format(token)}
        verify = True
        resp = requests.post(IMGUR_BASE + "/3/image", payload, headers=authentication, verify=verify)
        if 'error' in json.loads(resp.content)["data"]:
            return False, json.loads(resp.content)["data"]["error"]
        else:
            return True, json.loads(resp.content)["data"]["link"]


