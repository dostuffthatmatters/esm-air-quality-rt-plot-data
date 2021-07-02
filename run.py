from dotenv import load_dotenv
import os

assert('.env' in os.listdir('./'))
load_dotenv()
assert(os.getenv('FIREBASE_KEY_FILE') != None)


if __name__ == '__main__':
    print("running")
    