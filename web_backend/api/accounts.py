from fastapi import APIRouter, HTTPException, Cookie
from core.database import supabase_admin
from core.security import encrypt_token, decrypt_token
from web_backend.schemas.pydantic_models import LinkedAccountCreate
import httpx

router = APIRouter(prefix="/accounts", tags=["Linked Accounts"])

@router.get("/")
def get_accounts(user_uuid: str = Cookie(None)):
    if not user_uuid:
            raise HTTPException(status_code=401, detail="Unauthorized")
                accounts = supabase_admin.table("linked_accounts").select("id, account_name, discord_user_id, is_valid, created_at").eq("user_id", user_uuid).execute()
                    return accounts.data

                    @router.post("/")
                    def add_account(payload: LinkedAccountCreate, user_uuid: str = Cookie(None)):
                        if not user_uuid:
                                raise HTTPException(status_code=401, detail="Unauthorized")

                                    # Validate token against Discord API
                                        headers = {"Authorization": payload.token}
                                            with httpx.Client() as client:
                                                    resp = client.get("https://discord.com/api/v10/users/@me", headers=headers)
                                                            if resp.status_code != 200:
                                                                        raise HTTPException(status_code=400, detail="Invalid Discord user token")
                                                                                discord_user = resp.json()

                                                                                    ciphertext, nonce = encrypt_token(payload.token)

                                                                                        new_acc = supabase_admin.table("linked_accounts").insert({
                                                                                                "user_id": user_uuid,
                                                                                                        "discord_user_id": discord_user["id"],
                                                                                                                "account_name": payload.account_name,
                                                                                                                        "token_ciphertext": ciphertext,
                                                                                                                                "token_nonce": nonce,
                                                                                                                                        "is_valid": True
                                                                                                                                            }).execute()

                                                                                                                                                return {"status": "success", "account": new_acc.data[0]}

                                                                                                                                                @router.delete("/{account_id}")
                                                                                                                                                def delete_account(account_id: str, user_uuid: str = Cookie(None)):
                                                                                                                                                    if not user_uuid:
                                                                                                                                                            raise HTTPException(status_code=401, detail="Unauthorized")
                                                                                                                                                                
                                                                                                                                                                    supabase_admin.table("linked_accounts").delete().eq("id", account_id).eq("user_id", user_uuid).execute()
                                                                                                                                                                        return {"status": "success"}