from pydantic import BaseModel, Field
from typing import Optional

class RedeemCodeRequest(BaseModel):
    code: str

    class LinkedAccountCreate(BaseModel):
        account_name: str
            token: str

            class PlaygroundCreate(BaseModel):
                account_id: str
                    name: str
                        server_id: str
                            channel_id: str
                                message: str
                                    timing_mode: str = Field(..., pattern="^(manual|auto_slowmode)$")
                                        manual_interval_seconds: Optional[int] = 60

                                        class PlaygroundUpdate(BaseModel):
                                            name: Optional[str] = None
                                                server_id: Optional[str] = None
                                                    channel_id: Optional[str] = None
                                                        message: Optional[str] = None
                                                            timing_mode: Optional[str] = None
                                                                manual_interval_seconds: Optional[int] = None
                                                                    is_active: Optional[bool] = None