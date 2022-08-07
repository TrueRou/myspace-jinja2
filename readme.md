# My Space

## Introduce
A Live stream frontend which provides realtime comments and display of online users.
Also compact with mirai qq bot, bridging with QQ Group

The project is at an early stage which contains lots of low-end codes, forgive me please.
I made this only in a few hours without any modular or readable designs.

## Techniques
- video playback: flv.js (special version to reduce strange lag)
- css framework: bulma (im not good at html css)
- render: jinja2(SSR) mixed with Vue(SPA) for realtime data update
- web: fastapi with uvicorn
- bridge: mirai (yiri-mirai)

## How to use
There are lots of hard coded domains and sites which are bad for you to use it (lol, I don't know why I do put it on GitHub)
You need to have a live backend before you use it. I recommend to use node-media-server with is better than LiveGo or something else.
And then you need to change the domains in the python code, templates, and javascript files.
If you really want to use this project, please contact me directly, lol.

## Others
Thanks for reading my poor English.

## Screenshots
![Imgur](https://i.imgur.com/sPfSQ6Z.png)