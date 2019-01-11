# project/server/main/works.py

import time
from rq import get_current_job
from project.server import create_app

app = create_app()
app.app_context().push()


def _set_task_progress(task):
    """
    This method will update the job progress using the task object
    :param task : Task
    :return:
    """
    job = get_current_job()
    if job:
        job.meta['progress'] = task.export()
        job.save_meta()


def long_work(tsk):
    """
    This method will start uploading the images provided by the tsk object
    :param tsk:
    :return:
    """
    tsk.executeAll(_set_task_progress)