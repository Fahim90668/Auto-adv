from fastapi import APIRouter, HTTPException, Cookie
from core.database import supabase_admin
from web_backend.schemas.pydantic_models import PlaygroundCreate, PlaygroundUpdate

router = APIRouter(prefix="/playgrounds", tags=["Playgrounds"])

@router.get("/")
def get_playgrounds(user_uuid: str = Cookie(None)):
    if not user_uuid:
            raise HTTPException(status_code=401, detail="Unauthorized")
                res = supabase_admin.table("playgrounds").select("*").eq("user_id", user_uuid).execute()
                    return res.data

                    @router.post("/")
                    def create_playground(payload: PlaygroundCreate, user_uuid: str = Cookie(None)):
                        if not user_uuid:
                                raise HTTPException(status_code=401, detail="Unauthorized")

                                    # Check active code limits for user
                                        claimed_code = supabase_admin.table("redeem_codes").select("*").eq("claimed_by", user_uuid).eq("is_active", True).execute()
                                            if not claimed_code.data:
                                                    raise HTTPException(status_code=403, detail="Active redeem code required to create playgrounds")
                                                        
                                                            max_pg = claimed_code.data[0]["max_playgrounds"]
                                                                existing_pg = supabase_admin.table("playgrounds").select("id", count="exact").eq("user_id", user_uuid).execute()
                                                                    if existing_pg.count >= max_pg:
                                                                            raise HTTPException(status_code=400, detail=f"Playground limit reached (Max allowed: {max_pg})")

                                                                                new_pg = supabase_admin.table("playgrounds").insert({
                                                                                        "user_id": user_uuid,
                                                                                                "account_id": payload.account_id,
                                                                                                        "name": payload.name,
                                                                                                                "server_id": payload.server_id,
                                                                                                                        "channel_id": payload.channel_id,
                                                                                                                                "message": payload.message,
                                                                                                                                        "timing_mode": payload.timing_mode,
                                                                                                                                                "manual_interval_seconds": payload.manual_interval_seconds,
                                                                                                                                                        "is_active": False
                                                                                                                                                            }).execute()

                                                                                                                                                                return {"status": "success", "playground": new_pg.data[0]}

                                                                                                                                                                @router.patch("/{playground_id}")
                                                                                                                                                                def update_playground(playground_id: str, payload: PlaygroundUpdate, user_uuid: str = Cookie(None)):
                                                                                                                                                                    if not user_uuid:
                                                                                                                                                                            raise HTTPException(status_code=401, detail="Unauthorized")

                                                                                                                                                                                update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
                                                                                                                                                                                    res = supabase_admin.table("playgrounds").update(update_data).eq("id", playground_id).eq("user_id", user_uuid).execute()
                                                                                                                                                                                        return {"status": "success", "playground": res.data}

                                                                                                                                                                                        @router.delete("/{playground_id}")
                                                                                                                                                                                        def delete_playground(playground_id: str, user_uuid: str = Cookie(None)):
                                                                                                                                                                                            if not user_uuid:
                                                                                                                                                                                                    raise HTTPException(status_code=401, detail="Unauthorized")
                                                                                                                                                                                                        supabase_admin.table("playgrounds").delete().eq("id", playground_id).eq("user_id", user_uuid).execute()
                                                                                                                                                                                                            return {"status": "success"}