from supabase_py import create_client, Client
from dotenv import load_dotenv
import os

assert ".env" in os.listdir("./")
load_dotenv()
url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_PUBLIC")
email, password = os.getenv("USER_EMAIL"), os.getenv("USER_PASSWORD")
assert all([x is not None for x in [url, key, email, password]])

supabase: Client = create_client(url, key)

try:
    user = supabase.auth.sign_up(email=email, password=password)
    assert user["status_code"] == 200
    print("User created")
except:
    try:
        user = supabase.auth.sign_in(email=email, password=password)
        assert user["status_code"] == 200
        print(f"User exists: email/password VALID, {user}")
    except:
        print("User exists: email/password INVALID")
