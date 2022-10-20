from saaya.utils import CmdManager, PluginManager
from saaya.event import GroupMessage
from saaya.message import At, Plain
from saaya.session import Bot
from saaya.permission import Permission
from saaya.logger import logger
import re

from typing import List, Set

# Members should be managed and controlled
jail: Set[int] = set()


def filter_emoji(dst, restr=''):
    res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res.sub(restr, dst)


@PluginManager.registerEvent('OnLoad')
def purify_register(bot: Bot):
    logger.info('Jail Initializing... ')
    jail.add(123456789)


@PluginManager.registerEvent('GroupMessage')
async def purify_handler(event: GroupMessage):
    if event.sender.uid in jail:
        msg = event.message.getContent()
        if filter_emoji(msg) != msg:
            ori_msg = event.message.chain
            new_msg = []
            for i in ori_msg:
                if type(i) is Plain:
                    new_msg.append(Plain(filter_emoji(i.getContent())))
                else:
                    new_msg.append(i)
            event.bot.recall(event.message.source.messageId)
            event.sender.sendMessage([f'Purified: {event.sender.name}({event.sender.uid})', *new_msg])


# todo: Permission check
@CmdManager.registerCommand('purify', alias=['净水器'], help='群聊净化器', permission=Permission.ADMINISTRATOR)
def purify(event: GroupMessage, param):
    try:
        if param[1] == 'list':
            event.sender.sendMessage('---- Jail List ----\n' + '\n'.join([
                f'{i[0]}: {i[1]}' for i in enumerate(jail)
            ]) + '\n------- End -------')
        if param[1] == 'add':
            target: At = event.message.chain[1]
            qq = target.target
            jail.add(qq)
            event.sender.sendMessage(f'Jail added: {qq}')
        if param[1] == 'del':
            event.sender.sendMessage('Unimplemented')

    except Exception as e:
        event.sender.sendMessage(f'[{e}]\nUsage: purify add/del/list [at: member]')
