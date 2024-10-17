# TGForwarder

tgsearch、tgsou需要配置一堆频道群组，完全可以跑个定时任务监控这些频道群组，把资源全都转发到自己的频道，这样只需要配置一个就可以

### 提醒
不要过度采集，有人反馈limit设置过高导致自建频道被官方强制删除了

### 目前功能：
- 支持带关键词的图文、视频转发到自己频道，可以自定义搜索关键词和禁止关键词
- 对于禁止转发的消息可以下载图片以主动发送的方式发布到自己频道
- 支持根据链接和视频大小去重，已经存在的资源不再转发

暂不支持：
- 有些资源有跳转链接，暂时不支持，这种由他去吧，我也不想搞
- 有些资源在评论里，暂时无法处理  
思路：使用client.get_replies
- 自动加入群组


### 代理参数说明:
- SOCKS5  
proxy = (socks.SOCKS5,proxy_address,proxy_port,proxy_username,proxy_password)
- HTTP  
proxy = (socks.HTTP,proxy_address,proxy_port,proxy_username,proxy_password))
- HTTP_PROXY  
proxy=(socks.HTTP,http_proxy_list[1][2:],int(http_proxy_list[2]),proxy_username,proxy_password)
