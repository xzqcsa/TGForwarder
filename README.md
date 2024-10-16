# TGForwarder

tgsearch、tgsou需要配置一堆频道群组，完全可以跑个定时任务监控这些频道群组，把资源全都转发到自己的频道，这样只需要配置一个就可以

### 目前功能：
- 支持带关键词的图文、视频转发到自己频道，可以自定义搜索关键词和禁止关键词
- 对于禁止转发的消息可以下载图片以主动发送的方式发布到自己频道

暂不支持：
- 暂时没有加入过滤去重功能，可能会重复转发
思路：先取出来自己频道的历史消息，对比fwd_from里的channel_post，这样同一个频道的转发过的就不转发了。多个频道链接也可能重复，那就对比资源链接。视频文件基本上不会重复，可以对比文件大小
- 有些资源在评论里，暂时无法处理
思路：client.get_replies
```
from telethon import TelegramClient

api_id = '你的api_id'
api_hash = '你的api_hash'
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()
    chat_id = '频道或聊天的ID'  # 替换为你要获取消息的频道或聊天的ID
    message_id = '消息的ID'  # 替换为你要获取评论的消息的ID

    # 获取消息的所有回复
    replies = await client.get_replies(client.get_entity(chat_id), message_id)
    for reply in replies:
        print(f"{reply.id}: {reply.text}")

with client:
    client.loop.run_until_complete(main())
```
- 有些资源有跳转链接，暂时不支持


### 代理参数说明:
- SOCKS5  
proxy = (socks.SOCKS5,proxy_address,proxy_port,proxy_username,proxy_password)
- HTTP  
proxy = (socks.HTTP,proxy_address,proxy_port,proxy_username,proxy_password))
- HTTP_PROXY  
proxy=(socks.HTTP,http_proxy_list[1][2:],int(http_proxy_list[2]),proxy_username,proxy_password)
