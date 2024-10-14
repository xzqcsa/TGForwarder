# TGForwarder

tgsearch、tgsou需要配置一堆频道群组，完全可以跑个定时任务监控这些频道群组，把资源全都转发到自己的频道，这样只需要配置一个就可以

### 目前功能：
- 支持带关键词的图文、视频转发到自己频道，可以自定义搜索关键词和禁止关键词
- 对于禁止转发的消息可以下载图片以主动发送的方式发布到自己频道

暂时没有加入过滤去重功能，可能会重复转发

### 代理参数说明:
- SOCKS5
proxy = (socks.SOCKS5,proxy_address,proxy_port,proxy_username,proxy_password)
- HTTP
proxy = (socks.HTTP,proxy_address,proxy_port,proxy_username,proxy_password))
- HTTP_PROXY
proxy=(socks.HTTP,http_proxy_list[1][2:],int(http_proxy_list[2]),proxy_username,proxy_password)
