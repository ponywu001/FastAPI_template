from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from src.routers.auth import router as auth_router
from src.schemas.basic import TextOnly

app = FastAPI(
    title="Template FastAPI Backend Server",
    description="Template Description",
    version="0.0.1",
    contact={
        "name": "Author Name",
        "email": "example@exmaple.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])

# -------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
# ----------------------------------------------------------------------------------- #
from src.routers.post import router as post_router

app.include_router(post_router, prefix="/post", tags=["post"])
# ----------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------- #

@app.get("/", response_model=TextOnly)
async def root():
    return TextOnly(text="Hello World")


@app.get("/elements", include_in_schema=False)
async def api_documentation(request: Request):
    return HTMLResponse(
"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Elements in HTML</title>

    <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
  </head>
  <body>

    <elements-api
      apiDescriptionUrl="openapi.json"
      router="hash"
    />

  </body>
</html>
"""
)
    
    

# # -------------------------------------------------------------------------------------- #
# # ------------------------------------------------------------------------------------ #
# # ----------------------------------------------------------------------------------- #
# from urllib.parse import urlencode

# LINE_AUTH_URL = "https://access.line.me/oauth2/v2.1/authorize"
# REDIRECT_URI = "https://yourdomain.com/callback"
# CLIENT_ID = "YOUR_CHANNEL_ID"

# def generate_login_url():
#     params = {
#         "response_type": "code",
#         "client_id": CLIENT_ID,
#         "redirect_uri": REDIRECT_URI,
#         "state": "random_string_for_csrf_protection",
#         "scope": "profile openid email",
#     }
#     return f"{LINE_AUTH_URL}?{urlencode(params)}"
  
  
  
  
# from flask import Flask, request, jsonify
# import requests

# app = Flask(__name__)

# CLIENT_SECRET = "YOUR_CHANNEL_SECRET"
# TOKEN_URL = "https://api.line.me/oauth2/v2.1/token"

# @app.route('/callback')
# def callback():
#     code = request.args.get('code')
#     state = request.args.get('state')

#     # 校验 state 以防止 CSRF 攻击

#     # 请求 Access Token
#     payload = {
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': REDIRECT_URI,
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#     }
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}

#     token_response = requests.post(TOKEN_URL, data=payload, headers=headers)
#     token_data = token_response.json()

#     if 'access_token' in token_data:
#         access_token = token_data['access_token']

#         # 使用 Access Token 获取用户信息
#         user_info = requests.get(
#             "https://api.line.me/v2/profile",
#             headers={"Authorization": f"Bearer {access_token}"}
#         ).json()

#         return jsonify(user_info)
#     else:
#         return jsonify({"error": "Failed to get access token", "details": token_data})

# # ----------------------------------------------------------------------------------- #
# # ------------------------------------------------------------------------------------ #
# # ------------------------------------------------------------------------------------- #