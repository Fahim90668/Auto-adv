from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web_backend.api import auth, codes, accounts, playgrounds

app = FastAPI(title="Discord Auto-Advertising Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
        allow_origins=["http://localhost:3000"],
            allow_credentials=True,
                allow_methods=["*"],
                    allow_headers=["*"],
                    )

                    app.include_router(auth.router)
                    app.include_router(codes.router)
                    app.include_router(accounts.router)
                    app.include_router(playgrounds.router)

                    @app.get("/")
                    def root():
                        return {"status": "running", "service": "Discord Ad Platform API"}