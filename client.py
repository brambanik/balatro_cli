import requests

SERVER = "http://127.0.0.1:12346"

def rpc(method: str, params: dict | None = None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }

    if params is not None:
        payload["params"] = params

    r = requests.post(SERVER, json=payload, timeout = 5)
    r.raise_for_status()

    output = r.json()

    if "error" in output:
        raise RuntimeError(output["error"])
                           
    return output["result"]

def health():
    return rpc("health")

