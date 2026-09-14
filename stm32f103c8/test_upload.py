import urllib.request
import os
import json

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
filename = "bai02_gpio_structure.svg"
filepath = os.path.join(r"F:\Advance_C\stm32f103c8\images", filename)
data = open(filepath, "rb").read()

body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
    f"Content-Type: image/svg+xml\r\n\r\n"
).encode("utf-8") + data + f"\r\n--{boundary}--\r\n".encode("utf-8")

req = urllib.request.Request(
    "https://embedded-aiot.com/api/upload",
    data=body,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as r:
        res = r.read().decode("utf-8")
        print("Upload response:", res)
        parsed = json.loads(res)
        url = "https://embedded-aiot.com" + parsed["url"]
        
        # Test loading uploaded URL
        with urllib.request.urlopen(url, timeout=5) as r2:
            print(f"Fetch uploaded URL {url} -> Status: {r2.status} Length: {len(r2.read())}")
except Exception as e:
    print("Upload error:", e)
