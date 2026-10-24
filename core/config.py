from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str
        SUPABASE_KEY: str
            SUPABASE_SERVICE_ROLE_KEY: str
                ENCRYPTION_KEY: str  # 32-byte hex or base64 for AES-256-GCM
                    DISCORD_CLIENT_ID: str
                        DISCORD_CLIENT_SECRET: str
                            DISCORD_REDIRECT_URI: str
                                DISCORD_BOT_TOKEN: str
                                    ADMIN_DISCORD_ID: str

                                        model_config = SettingsConfigDict(env_file=".env", extra="ignore")

                                        settings = Settings()