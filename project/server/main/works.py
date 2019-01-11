# project/server/main/tasks.py

import time
from rq import get_current_job
from project.server import create_app

app = create_app()
app.app_context().push()


def _set_task_progress(task):
    job = get_current_job()
    if job:
        job.meta['progress'] = task.export()
        job.save_meta()


def long_work(tsk):
    tsk.executeAll(_set_task_progress)