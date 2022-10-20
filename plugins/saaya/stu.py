from saaya.utils import CmdManager
from saaya.event import GroupMessage
from saaya.message import At
from saaya.permission import Permission
import random

study_list = [123456789]


@CmdManager.registerCommand('study', alias=['学习'], help='滚去学习')
def study(event: GroupMessage, param):
    if event.sender.permission != Permission.MEMBER.value:
        event.sender.sendMessage([At(target=event.sender.uid), ' 管理员禁止搞事'])
        return

    durTime = 60 * int(random.randint(30, 60)) if not list(param) == 2 else int(param[1])
    if event.sender.uid in study_list:
        event.group.mute(target=event.sender.uid, durTime=durTime)
        event.sender.sendMessage([At(target=event.sender.uid), ' 滚去学习！'])
    else:
        maxRange = 60 * 60 * 1
        rate = min(1.0, durTime / maxRange)  # rate 越大越干你
        if rate >= random.random():
            event.group.mute(target=event.sender.uid, durTime=durTime)
            event.group.sendMessage([At(target=event.sender.uid), ' 催🔨，滚去工作！'])
        else:
            shoot = random.choice(study_list)
            event.group.mute(target=shoot, durTime=durTime)
            event.sender.sendMessage([At(target=shoot), ' 滚去学习！'])
