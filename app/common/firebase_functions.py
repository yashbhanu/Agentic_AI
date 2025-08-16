import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import requests, json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
FIREBASE_API_KEY = 'AIzaSyDDqVWrqCQXzix63SlVDCARqSBBXaMTSmA'
firebase_admin.initialize_app(cred)
print("initialized")

async def authenticateUsingPhoneNumber(phoneNumber):
    try:
        print(phoneNumber)
        user = auth.get_user_by_phone_number(phoneNumber)
        print(f'Successfully fetched user data: {user.uid}')
        custom_token = auth.create_custom_token(user.uid).decode()
        print("custom_token", custom_token)
        res = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={FIREBASE_API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"token": custom_token, "returnSecureToken": True})
        )
        id_token = res.json()["idToken"]
        decoded_token = auth.verify_id_token(id_token)
        decodedUid = decoded_token['uid']
        print("decoded_uid", decodedUid)
        if(decodedUid == user.uid):
            print("going to agent")
            return decodedUid
        else:
            return False;
    except Exception as e:
        raise
