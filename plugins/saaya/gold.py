from saaya.utils import CmdManager
from saaya.event import GroupMessage
from saaya.message import At


@CmdManager.registerCommand('gold', alias=['抽卡'], help='测试 tjj 的 bot')
def gold(event: GroupMessage, params):
    for i in range(9):
        event.group.sendMessage([At(target=123456789), ' 十连'])
