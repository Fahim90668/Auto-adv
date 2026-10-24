from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse
import httpx
from core.config import settings
from core.database import supabase_admin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login")
def login_discord():
    discord_auth_url = (
            f"https://discord.com/api/oauth2/authorize?client_id={settings.DISCORD_CLIENT_ID}"
                    f"&redirect_uri={settings.DISCORD_REDIRECT_URI}&response_type=code&scope=identify%20email"
                        )
                            return RedirectResponse(discord_auth_url)

                            @router.get("/callback")
                            def discord_callback(code: str, response: Response):
                                token_url = "https://discord.com/api/oauth2/token"
                                    data = {
                                            "client_id": settings.DISCORD_CLIENT_ID,
                                                    "client_secret": settings.DISCORD_CLIENT_SECRET,
                                                            "grant_type": "authorization_code",
                                                                    "code": code,
                                                                            "redirect_uri": settings.DISCORD_REDIRECT_URI,
                                                                                }
                                                                                    headers = {"Content-Type": "application/x-www-form-urlencoded"}
                                                                                        
                                                                                            with httpx.Client() as client:
                                                                                                    resp = client.post(token_url, data=data, headers=headers)
                                                                                                            if resp.status_code != 200:
                                                                                                                        raise HTTPException(status_code=400, detail="Failed to authenticate with Discord")
                                                                                                                                token_data = resp.json()
                                                                                                                                        access_token = token_data.get("access_token")

                                                                                                                                                user_resp = client.get(
                                                                                                                                                            "https://discord.com/api/users/@me",
                                                                                                                                                                        headers={"Authorization": f"Bearer {access_token}"}
                                                                                                                                                                                )
                                                                                                                                                                                        if user_resp.status_code != 200:
                                                                                                                                                                                                    raise HTTPException(status_code=400, detail="Failed to fetch Discord user profile")
                                                                                                                                                                                                            discord_user = user_resp.json()

                                                                                                                                                                                                                discord_id = discord_user["id"]
                                                                                                                                                                                                                    username = discord_user["username"]
                                                                                                                                                                                                                        email = discord_user.get("email")
                                                                                                                                                                                                                            avatar = f"https://cdn.discordapp.com/avatars/{discord_id}/{discord_user.get('avatar')}.png" if discord_user.get('avatar') else None

                                                                                                                                                                                                                                # Upsert user in Supabase
                                                                                                                                                                                                                                    existing = supabase_admin.table("users").select("*").eq("discord_id", discord_id).execute()
                                                                                                                                                                                                                                        if not existing.data:
                                                                                                                                                                                                                                                new_user = supabase_admin.table("users").insert({
                                                                                                                                                                                                                                                            "discord_id": discord_id,
                                                                                                                                                                                                                                                                        "username": username,
                                                                                                                                                                                                                                                                                    "email": email,
                                                                                                                                                                                                                                                                                                "avatar": avatar
                                                                                                                                                                                                                                                                                                        }).execute()
                                                                                                                                                                                                                                                                                                                user_record = new_user.data[0]
                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                            user_record = existing.data[0]
                                                                                                                                                                                                                                                                                                                                    supabase_admin.table("users").update({"username": username, "email": email, "avatar": avatar}).eq("id", user_record["id"]).execute()

                                                                                                                                                                                                                                                                                                                                        response.set_cookie(key="user_uuid", value=user_record["id"], httponly=True, secure=False, samesite="lax")
                                                                                                                                                                                                                                                                                                                                            return RedirectResponse(url="http://localhost:3000/dashboard", status_code=303)