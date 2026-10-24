import httpx
from datetime import datetime, timezone
from core.database import supabase_admin
from core.security import decrypt_token

async def send_advertisement(playground: dict):
    pg_id = playground["id"]
        account_id = playground["account_id"]
            channel_id = playground["channel_id"]
                message = playground["message"]

                    # Fetch linked account and decrypt token
                        acc_res = supabase_admin.table("linked_accounts").select("*").eq("id", account_id).execute()
                            if not acc_res.data:
                                    log_execution(pg_id, "failed", "Linked account not found")
                                            return None

                                                account = acc_res.data[0]
                                                    token = decrypt_token(account["token_ciphertext"], account["token_nonce"])

                                                        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
                                                            headers = {"Authorization": token, "Content-Type": "application/json"}
                                                                payload = {"content": message}

                                                                    async with httpx.AsyncClient() as client:
                                                                            response = await client.post(url, json=payload, headers=headers)
                                                                                    
                                                                                            if response.status_code == 200:
                                                                                                        log_execution(pg_id, "success", "Message posted successfully")
                                                                                                                    data = response.json()
                                                                                                                                return data
                                                                                                                                        elif response.status_code == 429:
                                                                                                                                                    retry_after = response.json().get("retry_after", 5)
                                                                                                                                                                log_execution(pg_id, "rate_limited", f"Rate limited. Retry after {retry_after}s")
                                                                                                                                                                            return {"rate_limited": True, "retry_after": retry_after}
                                                                                                                                                                                    else:
                                                                                                                                                                                                log_execution(pg_id, "failed", f"HTTP {response.status_code}: {response.text}")
                                                                                                                                                                                                            return None

                                                                                                                                                                                                            def log_execution(playground_id: str, status: str, details: str):
                                                                                                                                                                                                                supabase_admin.table("playground_logs").insert({
                                                                                                                                                                                                                        "playground_id": playground_id,
                                                                                                                                                                                                                                "status": status,
                                                                                                                                                                                                                                        "details": details
                                                                                                                                                                                                                                            }).execute()
                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                    supabase_admin.table("playgrounds").update({
                                                                                                                                                                                                                                                            "last_sent_at": datetime.now(timezone.utc).isoformat()
                                                                                                                                                                                                                                                                }).eq("id", playground_id).execute()