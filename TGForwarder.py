from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import os
from telethon.sessions import StringSession
import shutil
import random
import time


def random_wait(min_ms, max_ms):
    # 将毫秒转换为秒
    min_sec = min_ms / 1000
    max_sec = max_ms / 1000
    # 生成一个指定范围内的随机浮点数
    wait_time = random.uniform(min_sec, max_sec)
    # 等待随机生成的时间
    time.sleep(wait_time)

def contains(s, kw):
    return any(k in s for k in kw)

def nocontains(s, ban):
    return not any(k in s for k in ban)

async def send(message,target_chat_name,fdown):
    '''
    禁止转发时，主动发送消息
    '''
    if fdown:
        if message.media and isinstance(message.media, MessageMediaPhoto):
            media = await message.download_media(download_folder)
            await client.send_file(target_chat_name, media, caption=message.message)
    else:
        await client.send_message(target_chat_name, message.message)

async def forward_messages(chat_name, target_chat_name):
    try:
        # 获取频道或群组的实体
        chat = await client.get_entity(chat_name)
        # 获取最新的limit条消息
        messages =  client.iter_messages(chat, limit=limit)
        # 遍历消息并发送到目标频道
        async for message in messages:
            # 调用函数，200毫秒到1秒之间随机等待
            random_wait(200, 1000)
            # 是否允许转发
            forwards = message.forwards
            # 如果消息包含多媒体，转发多媒体文件
            if message.media:
                # 视频
                if hasattr(message.document, 'mime_type'):
                    if contains(message.document.mime_type,'video') and nocontains(message.message,ban):
                       await client.forward_messages(target_chat_name, message)
                # 图片+文本关键词
                elif contains(message.message, kw) and message.message and nocontains(message.message,ban):
                    if forwards:
                        await client.forward_messages(target_chat_name, message)
                    else:
                        await send(message, target_chat_name, fdown)
                # 图片+文本非关键词
                elif nokwforwards and message.message and nocontains(message.message,ban):
                    if forwards:
                        await client.forward_messages(target_chat_name, message)
                    else:
                        await send(message, target_chat_name, fdown)
    except Exception as e:
        print(f"Error forwarding messages from {chat_name}: {e}")

async def main():
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    for chat_name in channels_to_monitor + groups_to_monitor:
        print(f"从 {chat_name} 转发资源到 {forward_to_channel}")
        await forward_messages(chat_name, forward_to_channel)

    # 删除下载文件
    if fdown:
        shutil.rmtree(download_folder)


if __name__=='__main__':
    # 监控的频道和群组
    channels_to_monitor = []
    groups_to_monitor = []
    # 自己创建的频道
    forward_to_channel = 'xxx'
    # 转发前5条
    limit = 5
    # 监控关键词
    kw = ['链接', '片名', '名称']
    # 过滤关键词
    ban = ['预告', '预感', 'https://t.me/', '盈利','即可观看']
    # 禁止转发非关键词图文
    nokwforwards = False
    # 当频道禁止转发时，是否下载图片发送消息
    fdown = True
    download_folder = 'downloads'
    api_id = xxxxxx
    api_hash = 'xxxxx'
    string_session = 'xxxxx'
    with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
        client.loop.run_until_complete(main())









