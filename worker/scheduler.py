import asyncio
from datetime import datetime, timezone, timedelta
from core.database import supabase_admin
from worker.poster import send_advertisement

async def run_scheduler():
    print("🚀 Background Advertising Worker Started")
        while True:
                try:
                            # Fetch all active playgrounds
                                        res = supabase_admin.table("playgrounds").select("*").eq("is_active", True).execute()
                                                    playgrounds = res.data
                                                                
                                                                            now = datetime.now(timezone.utc)

                                                                                        for pg in playgrounds:
                                                                                                        next_scheduled = pg.get("next_scheduled_at")
                                                                                                                        
                                                                                                                                        # Check if it's time to post
                                                                                                                                                        if not next_scheduled or datetime.fromisoformat(next_scheduled) <= now:
                                                                                                                                                                            # Run post task asynchronously
                                                                                                                                                                                                result = await send_advertisement(pg)
                                                                                                                                                                                                                    
                                                                                                                                                                                                                                        if result and result.get("rate_limited"):
                                                                                                                                                                                                                                                                wait_time = result.get("retry_after", 10)
                                                                                                                                                                                                                                                                                        next_time = now + timedelta(seconds=wait_time)
                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                    interval = pg.get("manual_interval_seconds", 60)
                                                                                                                                                                                                                                                                                                                                                            next_time = now + timedelta(seconds=interval)

                                                                                                                                                                                                                                                                                                                                                                                supabase_admin.table("playgrounds").update({
                                                                                                                                                                                                                                                                                                                                                                                                        "next_scheduled_at": next_time.isoformat()
                                                                                                                                                                                                                                                                                                                                                                                                                            }).eq("id", pg["id"]).execute()

                                                                                                                                                                                                                                                                                                                                                                                                                                    except Exception as e:
                                                                                                                                                                                                                                                                                                                                                                                                                                                print(f"Scheduler Error: {e}")

                                                                                                                                                                                                                                                                                                                                                                                                                                                        await asyncio.sleep(5)

                                                                                                                                                                                                                                                                                                                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                                                                                                                                            asyncio.run(run_scheduler())