from celery import shared_task
from celery.schedules import crontab
from turtle_dove.celery import app
from util.ansible_api import ANSRunner
from .models import Tasks, AdHocTasks
# from celery import add_periodic_task
import json

@shared_task
def run_play_book(pk, playbook_path):
    rbt = ANSRunner()
    rbt.run_playbook(playbook_path)
    res = rbt.get_playbook_result()
    result = [
        {"name":"skipped", "num": len(res.get('skipped'))},
        {"name":"failed", "num": len(res.get('failed'))},
        {"name":"ok", "num": len(res.get('ok'))},
        {"name":"status", "num": len(res.get('status'))},
        {"name":"unreachable", "num": len(res.get('unreachable'))},
        {"name":"changed", "num": len(res.get('changed'))}
    ]
    data = json.dumps(res, indent=4)
    Tasks.objects.filter(pk=pk).update(detail_result=data, result_view=result, status='Y')


@shared_task
def run_adhoc_task(pk, host_list, module_name, module_args):
    rbt = ANSRunner()
    rbt.run_model(host_list, module_name, module_args)
    res = rbt.get_model_result()

    result = [
        {"name":"success", "num": len(res.get('success'))},
        {"name":"failed", "num": len(res.get('failed'))},
        {"name":"unreachable", "num": len(res.get('unreachable'))},
    ]
    data = json.dumps(res, indent=4)
    AdHocTasks.objects.filter(pk=pk).update(detail_result=data, result_view=result, status='Y')
