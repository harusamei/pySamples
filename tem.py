from sanic import Sanic
from sanic.response import json
import asyncio

app = Sanic(__name__)
ip_freq = {}

async def background_task():
    while True:
        print("Running background task, clear ip_mem")
        # ip 记数清零
        for key in ip_freq:
            ip_freq[key] = 0

        print(ip_freq)
        await asyncio.sleep(5)

@app.listener('before_server_start')
async def setup_background_task(app, loop):
    loop.create_task(background_task())

@app.listener('after_server_stop')
async def notify_server_stopped(app, loop):
    print(ip_freq)
    print("Server stopped!")


@app.route('/')
async def index(request):
    ip_address = request.ip

    if ip_address in ip_freq:
        ip_freq[ip_address] += 1
    else:
        ip_freq[ip_address] = 1
    print(ip_freq)

    if ip_freq[ip_address] > 5:
        return json({"message": "You have made too many requests"})
    else:   
        return json({"message": "Hello, Sanic!"})

if __name__ == '__main__':
    
    # 启动Sanic应用
    app.run(host='0.0.0.0', port=8000)
