import re
import threading
import time

from saaya.event import MemberCardChangeEvent, GroupMessage
from saaya.session import Bot
from saaya.utils import PluginManager
from saaya.logger import logger
from saaya.member import GroupMember

from private import wsm, fhr


def filter_emoji(dst, restr=''):
    res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res.sub(restr, dst)


blk_list = [
        'Ireina', '伊蕾娜'
]


def name_filter(ori: str):
    res = filter_emoji(ori)
    for i in blk_list:
        res = res.replace(i, '')
    return res


# @PluginManager.registerEvent('OnLoad')
# def hello(bot: Bot):
#     bot.sendGroupMessage(wsm[0], 'Fhr\'s nameCard listener started')


# Infinite check
def circle_checker(bot: Bot):
    fhr_instance: GroupMember
    while True:
        time.sleep(60)
        try:
            fhr_instance = bot.getMemberInfo(wsm[0], fhr)
            logger.debug(f'Fhr trigger: {name_filter(fhr_instance.name)} <= {fhr_instance.name}')
            if name_filter(fhr_instance.name) != fhr_instance.name:
                fhr_instance.group.sendMessage('[Scheduler]: 探测到 fhr 名称涉嫌发病，尝试更改...')
                bot.changeMemberInfo(fhr_instance.group, fhr_instance.uid, name=name_filter(fhr_instance.name))
        except Exception as e:
            logger.error('Scheduler error: ', e)


@PluginManager.registerEvent('OnLoad')
def fhr_checker(bot: Bot):
    circle_thread = threading.Thread(target=circle_checker, args=(bot,))
    logger.info('Fhr\'s nameCard checker start')
    circle_thread.start()


@PluginManager.registerEvent('GroupMessage')
async def check_fhr_name(event: GroupMessage):
    if event.group.uid in wsm and event.sender.uid == fhr:
        if name_filter(event.sender.name) != event.sender.name:
            event.sender.sendMessage('探测到 fhr 名称涉嫌发病，尝试更改...')
            event.bot.changeMemberInfo(event.group, event.sender.uid, name=name_filter(event.sender.name))


@PluginManager.registerEvent('MemberCardChangeEvent')
async def info(event: MemberCardChangeEvent):
    if event.group.uid in wsm and event.member.uid == fhr:
        if name_filter(event.current) != event.current:
            # event.group.sendMessage(f'探测到 fhr 新昵称涉嫌发病，已过滤')
            # event.bot.changeMemberInfo(event.group, event.member.uid, name=name_filter(event.current))
            pass
        else:
            event.group.sendMessage('fhr 新昵称合规，放行')
