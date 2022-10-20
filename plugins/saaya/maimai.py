from saaya.utils import PluginManager
from saaya.event import GroupMessage
from saaya.message import Image, Quote, At
from utils.mailib import generate
from utils.mailib_50 import generate50
from utils.mailib_image import image_to_base64


@PluginManager.registerEvent('GroupMessage')
async def b40_mai(event: GroupMessage):
    param = event.message.getContent().strip().split(' ')
    if param[0] not in ['b40', 'b50']:
        return

    username = ''
    if len(param) > 1:
        username = param[1]

    query_q = 0
    for msg in event.message.chain:
        if type(msg) is At:
            msg: At
            query_q = msg.target

    if username == "":
        payload = {'qq': str(event.sender.uid)}
    elif query_q:
        payload = {'qq': str(query_q)}
    else:
        payload = {'username': username}

    event.sender.sendMessage(['查询中，请稍等...'])
    if '40' in param[0]:
        img, success = await generate(payload)
    else:
        img, success = await generate50(payload)

    if success == 400:
        event.sender.sendMessage("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。")
    elif success == 403:
        event.sender.sendMessage("该用户禁止了其他人获取数据。")
    else:
        event.sender.sendMessage([Image(
            source={},
            ignoreId=True,
            base64=str(image_to_base64(img), encoding='utf-8'))])
