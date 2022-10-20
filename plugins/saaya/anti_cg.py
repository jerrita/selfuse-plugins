import random

from saaya.utils import CmdManager
from saaya.event import GroupMessage
import re

cg_qq = 123456789


@CmdManager.registerCommand('crawl', alias=['CG爬', 'pa'], help='让 CG 爬')
def crawl(event: GroupMessage, param):
    h = 0
    m = 0
    s = random.randint(1, 600)
    if len(param) > 1:
        ht = re.search(r'[0-9]+h', param[1])
        mt = re.search(r'[0-9]+min', param[1])
        st = re.search(r'[0-9]+s', param[1])
        if ht:
            h = int(ht.group(0)[:-1])
        if mt:
            m = int(mt.group(0)[:-3])
        if st:
            s = int(st.group(0)[:-1])
    res = h * 60 * 60 + m * 60 + s
    event.group.mute(cg_qq, res)
    event.group.sendMessage(f'制裁了 CG {res}s')


@CmdManager.registerCommand('come', alias=['放CG'], help='把 CG 放出来')
def come(event: GroupMessage, param):
    event.group.unmute(cg_qq)
    event.group.sendMessage('口⚽️结束！')
