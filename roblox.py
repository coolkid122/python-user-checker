import time, requests
from threading import Thread

webhook = "your_webhook_here"

def send_embed(desc, color):
    data = {
        "embeds": [{
            "description": desc,
            "color": color
        }]
    }
    try:
        requests.post(webhook, json=data)
    except:
        pass

def start():
    try:
        with open("usernames.txt", "r", encoding="utf-8", errors="ignore") as f:
            names = f.read().splitlines()
    except:
        print("usernames.txt not found")
        return

    if not names:
        print("no usernames")
        return

    print(f"loaded {len(names)} usernames")
    send_embed("Starting...", 0x00ff00)

    count = 0
    begin = time.time()

    def get_status(code):
        if code == 0: return "valid"
        if code == 1: return "taken"
        if code == 2: return "invalid"
        if code == 3: return "moderated"
        return "unknown"

    def check_username(username):
        nonlocal count
        try:
            r = requests.get(f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01", timeout=10)
            code = r.json().get("code")
            result = get_status(code)
            print(f"{result}: {username}")
            if result == "valid":
                with open("valid.txt", "a") as f:
                    f.write(username + "\n")
                send_embed(f"Found: `{username}`", 0x3498db)
        except:
            print(f"err: {username}")
        count += 1

    def loop():
        try:
            while True:
                for username in names:
                    check_username(username)
                    time.sleep(0.05)
                elapsed = time.time() - begin
                print(f"checked {count} in {elapsed:.2f}s ({count/elapsed:.2f}/s)")
                send_embed("Ending...", 0xff0000)
        except:
            send_embed("Ending...", 0xff0000)

    Thread(target=loop, daemon=True).start()

start()
