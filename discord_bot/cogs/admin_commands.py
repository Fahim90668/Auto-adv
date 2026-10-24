import discord
from discord import app_commands
from discord.ext import commands
from core.config import settings
from core.database import supabase_admin
import secrets
import string

class AdminCommands(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

                def is_admin(interaction: discord.Interaction) -> bool:
                        return str(interaction.user.id) == settings.ADMIN_DISCORD_ID

                            @app_commands.command(name="create-code", description="Create a redeem code for the ad platform")
                                @app_commands.describe(time="Duration type (lifetime, 1m, 3m)", playground="Max playgrounds allowed")
                                    @app_commands.choices(time=[
                                            app_commands.Choice(name="Lifetime", value="lifetime"),
                                                    app_commands.Choice(name="1 Month (30 days)", value="1m"),
                                                            app_commands.Choice(name="3 Months (90 days)", value="3m"),
                                                                ])
                                                                    async def create_code(self, interaction: discord.Interaction, time: str, playground: int):
                                                                            if not self.is_admin(interaction):
                                                                                        await interaction.response.send_message("Unauthorized.", ephemeral=True)
                                                                                                    return

                                                                                                            alphabet = string.ascii_uppercase + string.digits
                                                                                                                    code = ''.join(secrets.choice(alphabet) for _ in range(16))
                                                                                                                            formatted_code = f"AD-{code[:4]}-{code[4:8]}-{code[8:12]}-{code[12:]}"

                                                                                                                                    supabase_admin.table("redeem_codes").insert({
                                                                                                                                                "code": formatted_code,
                                                                                                                                                            "duration_type": time,
                                                                                                                                                                        "max_playgrounds": playground,
                                                                                                                                                                                    "is_active": True
                                                                                                                                                                                            }).execute()

                                                                                                                                                                                                    await interaction.response.send_message(
                                                                                                                                                                                                                f"✅ **Redeem Code Created Successfully!**\n"
                                                                                                                                                                                                                            f"Code: `{formatted_code}`\n"
                                                                                                                                                                                                                                        f"Duration: `{time}`\n"
                                                                                                                                                                                                                                                    f"Max Playgrounds: `{playground}`",
                                                                                                                                                                                                                                                                ephemeral=True
                                                                                                                                                                                                                                                                        )

                                                                                                                                                                                                                                                                            @app_commands.command(name="destroy-code", description="Invalidate an active redeem code")
                                                                                                                                                                                                                                                                                @app_commands.describe(code="The redeem code to destroy")
                                                                                                                                                                                                                                                                                    async def destroy_code(self, interaction: discord.Interaction, code: str):
                                                                                                                                                                                                                                                                                            if not self.is_admin(interaction):
                                                                                                                                                                                                                                                                                                        await interaction.response.send_message("Unauthorized.", ephemeral=True)
                                                                                                                                                                                                                                                                                                                    return

                                                                                                                                                                                                                                                                                                                            res = supabase_admin.table("redeem_codes").update({"is_active": False}).eq("code", code).execute()
                                                                                                                                                                                                                                                                                                                                    if not res.data:
                                                                                                                                                                                                                                                                                                                                                await interaction.response.send_message("Code not found.", ephemeral=True)
                                                                                                                                                                                                                                                                                                                                                            return

                                                                                                                                                                                                                                                                                                                                                                    # Also revoke access or clear linked claims if needed
                                                                                                                                                                                                                                                                                                                                                                            await interaction.response.send_message(f"❌ Code `{code}` has been destroyed and invalidated.", ephemeral=True)

                                                                                                                                                                                                                                                                                                                                                                            async def setup(bot):
                                                                                                                                                                                                                                                                                                                                                                                await bot.add_cog(AdminCommands(bot))