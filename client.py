import requests

SERVER = "http://127.0.0.1:12346"

def rpc(method: str, params: dict | None = None, timeout: float = 5.0):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }

    if params is not None:
        payload["params"] = params

    class RpcTimeout(RuntimeError):
        pass

    try:
        r = requests.post(SERVER, json=payload, timeout = timeout)
    except requests.exceptions.ReadTimeout as e:
        raise RpcTimeout(f"Timed out waiting for '{method}'...")
    r.raise_for_status()

    output = r.json()

    if "error" in output:
        raise RuntimeError(output["error"])
                           
    return output["result"]

def health():
    return rpc("health")

