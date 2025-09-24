# Maibot-AstrBot-Plugin-Compatibility-Layer
用于兼容AstrBot插件的MaiBot插件兼容层

## TODO
- [ ] 基础部分
    - [x] 插件发现
    - [x] API暴露为顶层
    - [ ] 插件注册
- [ ] 兼容部分
    - [ ] AstrBot消息段转换
    - [ ] AstrBot注册转换
    - [ ] AstrBot消息事件转换
- [ ] 测试部分
    - [ ] 样例测试
- [ ] Adapter支持
    - [ ] Napcat Adapter 管理员权限查询

## WARNING
由于现有的MaiBot层限制，无法进行视频消息解析。

部分涉及管理员的功能亦无法使用。

另外，在有 WeChat Adapter 之前，无法进行WeChat支持，其所有的消息事件均无效，且**会抛出异常**。

支持情况如下：
| 类型 | 收 | 发 | 解析 |
| ---- | -- | -- | -- |
| 视频 | NO | NO | NO |
| 语音 | YES | YES| YES |
| 管理员 | NO | NO | NO |
| 直接调用Adapter API | 无 | 部分* | 无 |

\* 仅部分适配器支持直接调用API，现在仅有 MaiBot Napcat Adapter 支持。支持列表详见 MaiBot-Napcat-Adapter 的`command_args.md`文件。