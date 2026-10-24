from fastapi import APIRouter, HTTPException, Cookie
from core.database import supabase_admin
from web_backend.schemas.pydantic_models import RedeemCodeRequest
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/codes", tags=["Codes"])

@router.post("/redeem")
def redeem_code(payload: RedeemCodeRequest, user_uuid: str = Cookie(None)):
    if not user_uuid:
            raise HTTPException(status_code=401, detail="Unauthorized")

                code_record = supabase_admin.table("redeem_codes").select("*").eq("code", payload.code).eq("is_active", True).execute()
                    if not code_record.data:
                            raise HTTPException(status_code=404, detail="Invalid or inactive code")

                                code_data = code_record.data[0]
                                    if code_data["claimed_by"] is not None:
                                            raise HTTPException(status_code=400, detail="Code already claimed")

                                                duration_type = code_data["duration_type"]
                                                    expires_at = None
                                                        if duration_type == "1m":
                                                                expires_at = datetime.now(timezone.utc) + timedelta(days=30)
                                                                    elif duration_type == "3m":
                                                                            expires_at = datetime.now(timezone.utc) + timedelta(days=90)
                                                                                # lifetime remains None

                                                                                    supabase_admin.table("redeem_codes").update({
                                                                                            "claimed_by": user_uuid,
                                                                                                    "claimed_at": datetime.now(timezone.utc).isoformat(),
                                                                                                            "expires_at": expires_at.isoformat() if expires_at else None
                                                                                                                }).eq("id", code_data["id"]).execute()

                                                                                                                    return {"status": "success", "message": "Code redeemed successfully", "expires_at": expires_at}