import json
from datetime import datetime, timedelta
from typing import Any

from mirai import HTTPAdapter, Plain, GroupMessage, Image

from fastapi import FastAPI, Form
from mirai.asgi import ASGI
from mirai import Mirai
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from timeloop import Timeloop


def save_data():
    with open("./data.json", "w") as f:
        json.dump(data, f)


def read_data():
    with open("./data.json", "r") as f:
        return json.load(f)


async def set_data(key: str, content: str, id: int):
    data[key] = content
    save_data()
    await bot.send_group_message(id, [Plain(f'设置成功: {key} = {content}')])


def decode_command(msg: str) -> []:
    first = ''
    second = ''
    try:
        if msg.startswith('!') and ' ' in msg:
            first = msg.split(' ')[0][1:]
            second = msg.replace(f'!{first} ', '', 1)
    except:
        pass
    return [first, second]


def redirect(path: str):
    response = RedirectResponse(f"{domain}{path}")
    response.status_code = 302
    return response


bot = Mirai(qq=3188609629, adapter=HTTPAdapter(verify_key='miraiturou', host='localhost', port=7000))
owners = [1822974018]
templates = Jinja2Templates(directory="templates")
data: dict[str, Any] = read_data()
msg_history = []
online_users = []
app = FastAPI()
timeloop = Timeloop()
app.add_middleware(SessionMiddleware, secret_key="iyshdfgkajsvcsf5fs4dsfisd2c")
domain = "http://trou.ltd:8000/"
last_group = 0

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get('/')
async def main_page(request: Request):
    if request.session.get('username') is None:
        request.session['username'] = request.client.host
    user = {
        "username": request.session['username'],
        "last_active": datetime.now()
    }
    append = True
    for item in online_users:
        if item['username'] == request.session['username']:
            append = False
            break
    if append:
        online_users.append(user)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data,
        "username": request.session['username']
    })


@app.get('/comment')
async def comment(request: Request, msg: str):
    msgrich = {
        "username": request.session.get('username'),
        "msg": msg,
        "datetime": datetime.now()
    }
    msg_history.append(msgrich)
    await bot.send_group_message(765415165, [Plain(request.session.get('username') + ": " + msg)])
    return redirect('')


@app.post('/username')
async def set_username(request: Request, username: str = Form()):
    old_name = request.session['username']
    request.session['username'] = username
    for index, user in enumerate(online_users):
        if user['username'] == username:
            return redirect('')
        if user['username'] == old_name:
            online_users[index]['username'] = username
    for index, msg in enumerate(msg_history):
        if msg['username'] == old_name:
            msg_history[index]['username'] = username
    return redirect('')


@app.get('/status')
async def status(request: Request):
    for index, user in enumerate(online_users):
        if user['username'] == request.session.get('username'):
            online_users[index]['last_active'] = datetime.now()
    msgs = []
    for item in msg_history[::-1]:
        msgs.append(item['datetime'].strftime("%H:%M") + " " + item['username'] + ": " + item['msg'])
    return {
        'online_users': online_users,
        "msgs": msgs
    }


@timeloop.job(interval=timedelta(seconds=10))
def check_online():
    for index, user in enumerate(online_users):
        last_active = user['last_active']
        if last_active + timedelta(seconds=30) < datetime.now():
            online_users.pop(index)


@bot.on(GroupMessage)
async def on_friend_message(event: GroupMessage):
    id = event.sender.group.id
    if event.sender.id in owners:
        command, content = decode_command(str(event.message_chain))
        if command == 'set_title':
            await set_data('title', content, id)
        if command == 'set_info':
            await set_data('info', content, id)
        if command == 'set_image':
            images = event.message_chain.get((Image, 1))
            if len(images) == 1:
                await images[0].download(filename='./images/pic.png', determine_type=False)
        if command == 'begin':
            await bot.send_group_message(id, [
                Plain(f"直播已开始: http://live.trou.ltd/ \n 标题: {data['title']} \n 简介: {data['info']}"),
                Image(path=str('./images/pic.png'))])

ASGI().mount('/web', app).mount('/static', StaticFiles(directory="static"))
timeloop.start()
bot.run(host='127.0.0.1', port=8080)
