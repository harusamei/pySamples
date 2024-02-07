# 使用sanic框架，实现一个简单的时间格式规范化服务

from sanic import Request, response,Sanic, json,text
from sanic.response import html
import asyncio

from timeProcess import DateTimeProc
from changeHtml import addNewDiv
from urllib.parse import unquote

app = Sanic("DateNormalize")
dp=DateTimeProc()

ip_freq = {}
tags = [
    {"url": "/zh", "name": "规范中文时间格式"},
    {"url": "/en", "name": "规范英文时间格式"},
    {"url": "/home", "name": "规范中文数字格式"}
]

with open("form.html", "r",encoding='utf-8') as f:
    html_form = f.read()

def isHighFreqIp(request):
    ip_address = request.ip
    print(f"Received request from {ip_address}")  

    if ip_address in ip_freq:
        ip_freq[ip_address] += 1
    else:
        ip_freq[ip_address] = 1

    if ip_freq[ip_address] > 5:
        return True
       
    return False

async def background_task():
    while True:
        print("Running background task, clear ip_mem")
        # ip 记数清零
        for key in ip_freq:
            ip_freq[key] = 0
        await asyncio.sleep(5)

async def callTimeProc(query, lang):
    return dp.parseDateTime(query, lang)

@app.listener('before_server_start')
async def setup_background_task(app, loop):
    loop.create_task(background_task())

@app.listener('after_server_stop')
async def notify_server_stopped(app, loop):
    print(ip_freq)
    print("Server stopped!")

# 所有请求都会调用这个中间件
@app.middleware('request')
async def print_on_request(request):
    # 如果请求频率过高，返回错误信息，不再处理
    if isHighFreqIp(request):
        return json({'message': 'Too many requests from your IP address!'})
    print("A request is coming")

@app.route("/",name="root")
@app.route("/home",name="home")
async def home(request : Request):
    
    temStr = unquote(request.query_string)
    temVal = dp.str2val(temStr)
    return text(f"{temVal}")

# curl "http://localhost:8000/zh?2019年三月七日下午10点差五分"
@app.route("/zh")
async def zh_CN(request):
    temStr = unquote(request.query_string)
    temVal = await callTimeProc(temStr, "zh_CN")
    return text(f"{temVal}")

# curl "http://localhost:8000/en?January 2019"
@app.route("/en")
async def en_US(request):
    temStr = unquote(request.query_string)
    temVal = await callTimeProc(temStr, "en_US")
    return text(f"{temVal}")

@app.get("/help")
async def help(request: Request):
   
    print(request.args)
    return json(tags)

@app.get("/showForm")
async def showForm(request: Request):

    return html(html_form)

@app.route("/submit", methods=["POST"])
async def submit(request):
    user_name = request.form.get("user_name")
    temStr =""
    if user_name:
        temStr = f"Hello, {user_name}! Your form is submitted successfully."
    else:
        temStr = "Please enter your name."
    
    return html(addNewDiv(html_form, temStr))

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000)

