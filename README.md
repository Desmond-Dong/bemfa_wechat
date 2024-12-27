# 🔔 Bemfa(巴法云)微信通知插件

> 这是一个用于Home Assistant的自定义插件，可以通过Bemfa(巴法云)平台向微信发送通知消息。
调用巴法云官方接口,官方接口说明如下:
> https://cloud.bemfa.com/docs/src/api_wechat.html

## ✨ 功能特点

- 📱 支持通过Bemfa(巴法云)平台向微信发送文本通知
- 🖥️ 图形化配置界面，无需修改配置文件
- 🔧 可以在Home Assistant的自动化中轻松调用

## 📥 安装方法

1. 在HACS中搜索`Bemfa Wechat`
2. 点击下载安装
3. 重启Home Assistant
4. HACS源可以选择Github或者Gitee

    https://gitee.com/desmond_GT/bemfa_wechat

    https://github.com/djhui/bemfa_wechat

## ⚙️ 配置说明

1. 在Home Assistant的设置页面中，点击**设备与服务**
2. 点击右下角的**添加集成**按钮
3. 搜索`Bemfa`或`巴法云`
4. 输入Bemfa(巴法云)平台获取的用户密钥即可完成配置

## 🚀 使用方法

1. 注册巴法云账号，并获取密钥,关注或者绑定巴法云微信号
2. 在HACS中搜索 `Bemfa Wechat` 安装，或者 clone 此项目，将 `custom_components/Bemfa_Wechat` 目录拷贝至 Home Assistant 配置目录的 `custom_components` 目录下
3. 重启 Home Assistant 服务
4. 在 Home Assistant 的集成页面，搜索 "Bemfa Wechat" 并添加
5. 根据提示输入巴法云密钥后提交

### 📝 调用方法
**Action:** Bemfa WeChat: send_message

**Action data:**

{
"device":"设备",
"message":"消息内容"
}

扫描下面二维码，关注我。有需要可以随时给我留言

![QR Code](https://github.com/djhui/hassio-addons/raw/main/WeChat_QRCode.png)
![QR Code](https://gitee.com/desmond_GT/hassio-addons/raw/main/WeChat_QRCode.png)

扫描上面二维码，关注我。有需要可以随时给我留言