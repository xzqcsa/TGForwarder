from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from telethon.sessions import StringSession
import os
import asyncio
import shutil
import random
import time


class TGForwarder:
    def __init__(self, api_id, api_hash, string_session, channels_to_monitor, groups_to_monitor, forward_to_channel,
                 limit, kw, ban, nokwforwards, fdown, download_folder):
        self.api_id = api_id
        self.api_hash = api_hash
        self.string_session = string_session
        self.channels_to_monitor = channels_to_monitor
        self.groups_to_monitor = groups_to_monitor
        self.forward_to_channel = forward_to_channel
        self.limit = limit
        self.kw = kw
        self.ban = ban
        self.nokwforwards = nokwforwards
        self.fdown = fdown
        self.download_folder = download_folder
        self.client = TelegramClient(StringSession(string_session), api_id, api_hash)

    def random_wait(self, min_ms, max_ms):
        min_sec = min_ms / 1000
        max_sec = max_ms / 1000
        wait_time = random.uniform(min_sec, max_sec)
        time.sleep(wait_time)

    def contains(self, s, kw):
        return any(k in s for k in kw)

    def nocontains(self, s, ban):
        return not any(k in s for k in ban)

    async def send(self, message, target_chat_name):
        if self.fdown and message.media and isinstance(message.media, MessageMediaPhoto):
            media = await message.download_media(self.download_folder)
            await self.client.send_file(target_chat_name, media, caption=message.message)
        else:
            await self.client.send_message(target_chat_name, message.message)

    async def forward_messages(self, chat_name, target_chat_name):
        global total
        try:
            chat = await self.client.get_entity(chat_name)
            messages = self.client.iter_messages(chat, limit=self.limit)
            async for message in messages:
                self.random_wait(200, 1000)
                forwards = message.forwards
                if message.media:
                    if hasattr(message.document, 'mime_type') and self.contains(message.document.mime_type,
                                                                                'video') and self.nocontains(
                            message.message, self.ban):
                        if forwards:
                            await self.client.forward_messages(target_chat_name, message)
                            total += 1
                    elif self.contains(message.message, self.kw) and message.message and self.nocontains(
                            message.message, self.ban):
                        if forwards:
                            await self.client.forward_messages(target_chat_name, message)
                            total += 1
                        else:
                            await self.send(message, target_chat_name)
                            total += 1
                    elif self.nokwforwards and message.message and self.nocontains(message.message, self.ban):
                        if forwards:
                            await self.client.forward_messages(target_chat_name, message)
                            total += 1
                        else:
                            await self.send(message, target_chat_name)
                            total += 1
            print(f"从 {chat_name} 转发资源到 {self.forward_to_channel} total: {total}")
        except Exception as e:
            print(f"从 {chat_name} 转发资源到 {self.forward_to_channel} 失败: {e}")

    async def main(self):
        await self.client.start()
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        for chat_name in self.channels_to_monitor + self.groups_to_monitor:
            global total
            total = 0
            await self.forward_messages(chat_name, self.forward_to_channel)
        await self.client.disconnect()
        if self.fdown:
            shutil.rmtree(self.download_folder)

if __name__ == '__main__':
    channels_to_monitor = []
    groups_to_monitor = []
    forward_to_channel = 'xxxx'
    limit = 2
    kw = ['链接', '片名', '名称']
    ban = ['预告', '预感', 'https://t.me/', '盈利', '即可观看']
    # 禁止转发非关键词图文
    nokwforwards = False
    # 当频道禁止转发时，是否下载图片发送消息
    fdown = True
    download_folder = 'downloads'
    api_id = xxx
    api_hash = 'xxx'
    string_session = 'xxx'

    tg_forwarder = TGForwarder(api_id, api_hash, string_session, channels_to_monitor, groups_to_monitor,
                               forward_to_channel, limit, kw, ban, nokwforwards, fdown, download_folder)
    asyncio.run(tg_forwarder.main())
