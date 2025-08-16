from fastapi import FastAPI
from .firebase_functions import authenticateUsingPhoneNumber

def create_app(agent):
    app = FastAPI()

    @app.get("/")
    def health():
        return {"message": "Hello world"}

    @app.post("/run")
    async def run(payload: dict):
        try:
            authenticated_uid = await authenticateUsingPhoneNumber(payload['phoneNumber'])
            print("authenticated", authenticated_uid)
            if authenticated_uid:
                return await agent.execute(payload, authenticated_uid)
            else:
                return {"error": "Cannot Authenticate your phone number"}
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print("Error occurred:", error_msg)
            return {"error": error_msg}
    
    return app