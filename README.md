# poe-telegram-bot
Use Poe on Telegram.

## Instructions
1. Set `bot_token` and `allowed_users` in `main.py`.
2. Installation depends on `pip install --upgrade python-telegram-bot poe-api`
3. Run `python main.py`
4. Send `/set_token <token>` to the bot
5. Use Poe on Telegram

## Finding Your Token:
Log into [Poe](https://poe.com) on any web browser, then open your browser's developer tools (also known as "inspect") and look for the value of the `p-b` cookie in the following menus:
 - Chromium: Devtools > Application > Cookies > poe.com
 - Firefox: Devtools > Storage > Cookies
 - Safari: Devtools > Storage > Cookies

## Bot commands
- `/sage` - Sage
- `/gpt4` - GPT-4
- `/claude_plus` - Claude+
- `/neevaai` - NeevaAI
- `/dragonfly` - Dragonfly
- `/chatgpt` - ChatGPT
- `/claude_instant` - Claude-instant
- `/set_token` - Set token
- `/clear_context` - Clear conversation context

# poe-telegram-bot
在 Telegram 上使用 Poe。

## 使用方法
1. 设置`main.py`中的`bot_token`与`allowed_users`。
2. 安装依赖`pip install --upgrade python-telegram-bot poe-api`
3. 运行`python main.py`
4. 向 bot 发送`/set_access_token <token>`
5. 在 Telegram 上使用 Poe

## 找出Token：
在任何网页浏览器上登录[Poe](https://poe.com/)，然后打开浏览器的开发者工具（也称为“检查”），并查找以下菜单中的`p-b` cookie的值：
- Chromium：Devtools > Application > Cookies > poe.com
- Firefox：Devtools > Storage > Cookies
- Safari：Devtools > Storage > Cookies

## 机器人命令
- `/sage` - Sage
- `/gpt4` - GPT-4
- `/claude_plus` - Claude+
- `/neevaai` - NeevaAI
- `/dragonfly` - Dragonfly
- `/chatgpt` - ChatGPT
- `/claude_instant` - Claude-instant
- `/set_token` - 设置 Token
- `/clear_context` - 清除对话上下文