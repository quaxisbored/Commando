import os
import json
import aiohttp
import requests
import aiofiles
__import__("sys").path.append("..")
#import commando.variables as variables
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

client_id = "921920076473577533"
client_secret = os.environ['CLIENT_SECRET']
auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=921920076473577533&redirect_uri=https%3A%2F%2Fcommando.neodymiumdevelopmentlabs.repl.co%2Frecieve&response_type=code&scope=identify"

class web:
  async def post(url: str = None, data=None, headers=None, json=None):
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="POST",        
        url=url,
        data=data,
        json=json,
        headers=headers
      ) as r:
        data = await r.text()
        try:
          jsonn = await r.json()
          return jsonn
        except:
          return data
      
  async def get(url: str, data=None, headers=None, json=None):
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="GET",        
        url=url,
        data=data,
        json=json,
        headers=headers
      ) as r:
        data = await r.text()
        try:
          jsonn = await r.json()
          return jsonn
        except:
          return data

class configuration:
  def read():
    with open("config.json", encoding="utf-8") as config_file:
      config = json.load(config_file)
      return config

def read_cosmetics():
  item_filename = configuration.read()['files']['items']
  with open(item_filename) as f:
    return json.load(f)

def read_banners():
  item_filename = configuration.read()['files']['banners']
  with open(item_filename) as f:
    return json.load(f)

def get_authenticated_user(request):
  user = request.user
  try:
    return JsonResponse({
      "id": user.id,
      "avatar": user.avatar,
      "discord_tag": user.discord_tag,
      "public_flags": user.public_flags,
      "flags": user.flags,
      "locale": user.locale,
      "mfa_enabled": user.mfa_enabled
    })
  except:
    return JsonResponse({
      "error": "Login First"
    })

async def discord_login(request):
  I = redirect(auth_url_discord)
  return I

def getct(path):
	k = list(os.path.splitext(path))[1][1:]
	exts = {
		"mp4":"video/mp4",
		"mp3":"audio/mp3",
		"wav":"audio/wav",
		"txt":"text/plain",
		"py":"text/plain",
		"json": "text/json",
		"png":"image/png",
		"jpg":"image/jpeg",
		"jpeg":"image/jpeg",
		"html":"text/html"
	}
	return exts.get(k)

def dash_i(request):
  return render(
    request, 
    "test.html"
  )

def guilds(request):
  return HttpResponse(
		"Text only, please.", 
		content_type="text/plain"
	)

def discord_login_redirect(request):
  code = request.GET.get('code')
  if code is None:
    return JsonResponse({"error":"No Code Inputted."})
  user = exchange_code(code)
  discord_user = authenticate(
    request,
    user=user
  )
  discord_user = list(discord_user).pop()
  login(
    request, 
    discord_user
  )
  return redirect("/")

def exchange_code(code: str):
  data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "https://commando.neodymiumdevelopmentlabs.repl.co/recieve",
    "scope": "identify"
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  credentials = requests.post(
    "https://discord.com/api/oauth2/token", 
    data=data, 
    headers=headers
  ).json()
  access_token = credentials['access_token']
  response = requests.get(
    "https://discord.com/api/v6/users/@me", 
    headers={
    'Authorization': 'Bearer %s' % access_token
    }
  ).json()
  return response

def index(request):
  if request.user.is_authenticated:
      return render(
      request, 
      "index.html",
      {'user': request.user}
    )
  else:
    return render(
      render,
      "index_notlogin.html"
    )

def index_html(request):
  return redirect("/")

def render_favicon(request):
  IDATA = open(
    "favicon.png", 
    "rb"
  ).read()
  return HttpResponse(
    IDATA, 
    content_type="image/png"
  )

@login_required
def dash(request):
  return render(
    request, 
    "dash.html",
    {
			'username': request.user.discord_tag.split("#")[0],
			'user': request.user
		}
  )

@login_required
def logouts(request):
  logout(request)
  return redirect("/")

def asset_render(request):
    args = request.GET.get('path')
    path = f"assets/{args}"
    IDATA = open(
      path, 
      "rb"
    ).read()
    if ".png" in path.lower():
      IDATA = open(
        path, 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
    elif ".jpg" in path.lower() or ".jpeg" in path.lower():
      IDATA = open(
        path, 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
    else:
      return HttpResponse(
        IDATA, 
        content_type="text/plain"
      )

def page_render(request):
    args = request.GET.get('path')
    path = f"pages/{args}"
    IDATA = open(
      path, 
      "rb"
    ).read()
    return HttpResponse(
      IDATA, 
      content_type="text/plain"
    )

async def banner_render(request, id):
  print(id)
  try:
    items = read_banners()
    item = None
    for cos in items:
      if cos['id'].lower() == id.lower():
        item = cos
        pass
      else:
        continue
    if item is None:
      return JsonResponse({"error": "Item Does Not Exist"})
    if os.path.isfile(f"banners/{id.lower()}.png"):
      IDATA = open(
        f"banners/{id.lower()}.png", 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
    else:
      async with aiohttp.ClientSession() as session:
        async with session.get(f'{item["images"]["icon"]}') as resp:
          f = await aiofiles.open(
            f"banners/{item['id'].lower()}.png", 
            mode='wb'
          )
          await f.write(await resp.read())
          await f.close()
      IDATA = open(
        f"banners/{id.lower()}.png", 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
  except:
    return JsonResponse({'error': 'Item Does Not Exist'})

async def normal_image_render(request, id):
  print(id)
  try:
    items = read_cosmetics()
    item = None
    for cos in items:
      if cos['id'].lower() == id.lower():
        item = cos
        pass
      else:
        continue
    if item is None:
      return JsonResponse({"error": "Item Does Not Exist"})
    if os.path.isfile(f"images/{id.lower()}.png"):
      IDATA = open(
        f"images/{id.lower()}.png", 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
    else:
      async with aiohttp.ClientSession() as session:
        async with session.get(f'{item["images"]["icon"]}') as resp:
          f = await aiofiles.open(
            f"images/{item['id'].lower()}.png", 
            mode='wb'
          )
          await f.write(await resp.read())
          await f.close()
      IDATA = open(
        f"images/{id.lower()}.png", 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
  except:
    return JsonResponse({'error': 'Item Does Not Exist'})


async def files(
	request
):
	path = request.GET.get('path')
	if path:
		if os.path.isdir(f"{path}"):
			files = os.listdir(path)
			text = ""
			text += "<title>CommandoCDN By Pirxcy</title>"
			for file in files:
				if "." in file:
					text += f'<a href="/files?path={path}/{file}">{file} (File)</a><br>'
				else:
					text += f'<a href="/files?path={file}">{file} (Folder)</a><br>'
			return HttpResponse(
				text, 
			)
		elif os.path.isfile(path):
			content_type = getct(path)
			IDATA = open(
				path, 
				"rb"
			).read()
			return HttpResponse(
				IDATA, 
				content_type=content_type
			)
		else:
			return JsonResponse({"error": "File Not Found"})
	else:
			files = os.listdir()
			text = ""
			text += "<title>CommandoCDN By Pirxcy</title>"
			for file in files:
				if "." in file:
					text += f'<a href="/files?path={file}">{file} (File)</a><br>'
				else:
					text += f'<a href="/files?path={file}">{file} (Folder)</a><br>'
			return HttpResponse(
				text, 
			)

async def variant_image_render(
	request, 
	id,
	channel,
	material
):
  try:
    items = read_cosmetics()
    item = None
    for cos in items:
      if cos['id'].lower() == id.lower():
        item = cos
        pass
      else:
        continue
    if item is None:
      return JsonResponse({"error": "Item Does Not Exist"})
    if os.path.isfile(f"variantimages/{id.lower()}{channel.lower()}{material.lower()}.png"):
      IDATA = open(
        f"variantimages/{id.lower()}{channel.lower()}{material.lower()}.png", 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
    else:
      async with aiohttp.ClientSession() as session:
        async with session.get(f'https://fortnite-api.com/images/cosmetics/br/{id}/variants/{channel}/{material}.png') as resp:
          f = await aiofiles.open(
            f"variantimages/{id.lower()}{channel.lower()}{material.lower()}.png", 
            mode='wb'
          )
          await f.write(await resp.read())
          await f.close()
      IDATA = open(
        f"variantimages/{id.lower()}{channel.lower()}{material.lower()}.png", 
        "rb"
      ).read()
      return HttpResponse(
        IDATA, 
        content_type="image/png"
      )
  except:
    return JsonResponse({'error': 'Item Does Not Exist'})