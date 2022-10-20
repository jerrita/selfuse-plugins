from saaya.utils import PluginManager
from saaya.event import GroupMessage

import random

db = {
}

gTarget = 123456789

pre = {}
for i in db:
    pre[i] = ''


def getAns(msg):
    ans = db[msg].split('/')
    look = random.choice(ans)
    if pre[i] == look:
        return getAns(msg)
    else:
        pre[i] = look
        return look


@PluginManager.registerEvent('GroupMessage')
async def rander(event: GroupMessage):
    if event.group.uid == gTarget:
        msg = event.message.getContent()

        if msg == '随机列表':
            ans = []
            for i in db:
                ans.append(i)
            event.group.sendMessage('/'.join(ans))
        elif msg in db:
            event.group.sendMessage(getAns(msg))
