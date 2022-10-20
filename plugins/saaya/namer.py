from saaya.utils import CmdManager
from saaya.event import GroupMessage
from saaya.message import At


@CmdManager.registerCommand('rename', alias=['重命名'], help='群名片重命名')
def namer(event: GroupMessage, params):
    if len(params) < 2:
        event.sender.sendMessage('Usage: rename [name] ([target])')
    elif len(params) == 2:
        event.bot.changeMemberInfo(event.group, event.sender.uid, " ".join(params[1:]))
        event.sender.sendMessage(f'Change {event.sender.uid} => {" ".join(params[1:])}')
    else:
        target: At = event.message.chain[1]
        event.bot.changeMemberInfo(event.group, target.target, " ".join(params[1:]))
        event.sender.sendMessage(f'Change {target.display}({target.target}) => {" ".join(params[1])}')
