# 学习event broker模式
# 事件代理模式是一种软件设计模式，用于将事件的生产者和消费者解耦。事件代理模式通常用于实现异步编程，例如在Web应用程序中，当用户注册时，可以触发一个事件，然后在后台处理其他逻辑，例如发送电子邮件或记录日志。
from sanic import Sanic
from sanic.response import text
from sanic.log import logger

class EventBroker:
    def __init__(self):
        self.listeners = {}
        self.events = {}

    def add_listener(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def trigger_event(self, event_name, *args, **kwargs):
        callback = self.events.get(event_name)
        if callback is None:
            return
        await callback(*args, **kwargs)

app = Sanic(__name__)
event_broker = EventBroker()

# 添加事件监听器
event_broker.add_listener('user_registered', lambda username: logger.info(f"User registered: {username}"))

@app.route('/register')
async def register_user(request):
    # 假设这里有用户注册的逻辑
    username = "example_user"
    # 触发事件
    await event_broker.trigger_event('user_registered', username)
    return text('User registered successfully')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
