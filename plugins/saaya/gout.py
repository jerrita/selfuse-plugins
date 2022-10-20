from saaya.utils import CmdManager
from saaya.event import GroupMessage, FriendMessage
from private import ehall
from utils import gout_new
from typing import Union


@CmdManager.registerCommand('gout', alias=['离校', '出校'], help='一键快速离校')
def gout(event: Union[GroupMessage, FriendMessage], param):
    if event.sender.uid in ehall:
        event.sender.sendMessage(gout_new(event.sender.sendMessage, ehall[event.sender.uid]))
    else:
        event.sender.sendMessage('不存在此用户的预制模板，请联系管理员添加！')

# @CmdManager.registerCommand('cheat', alias=['秘技'], help='自动离返校')
# def cheat(event: Union[GroupMessage, FriendMessage], param):
#     if event.sender.uid in we:
#         if len(param) != 2 or param[1] not in ['离', '返']:
#             event.sender.sendMessage('Usage: cheat [离/返]')
#         else:
#             event.sender.sendMessage(cqupt_cheat(we[event.sender.uid], param[1]))
#     else:
#         event.sender.sendMessage('不存在此用户的预制模板，请联系管理员添加！')
