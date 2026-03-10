"""
ATC Flight Strips - Sync Server (Python)
Gebruik: python server.py
Geen extra installatie nodig - alleen Python 3.7+
"""

import asyncio
import json
import socket
import os
import sys
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
import time

# ── Probeer websockets module, anders geef installatie instructie ──
try:
    import websockets
except ImportError:
    print("╔══════════════════════════════════════════╗")
    print("║  websockets module niet gevonden          ║")
    print("║  Voer dit eenmalig uit:                   ║")
    print("║                                           ║")
    print("║  pip install websockets                   ║")
    print("║                                           ║")
    print("╚══════════════════════════════════════════╝")
    sys.exit(1)

# ── Gedeelde state ──────────────────────────────────────────────────
SECTORS = ['Schiphol Approach','Schiphol Departure','Noord','West','Zuid','Oost','Unassigned','Inbound']

shared_state = {
    "flights": {},
    "sectors": {s: [] for s in SECTORS},
    "simStartedAt": None,
    "lastUpdate": int(time.time() * 1000)
}

connected_clients = set()

# ── WebSocket handler ───────────────────────────────────────────────
async def handler(websocket):
    connected_clients.add(websocket)
    ip = websocket.remote_address[0]
    print(f"✓ Controller verbonden ({ip}) — totaal: {len(connected_clients)}")

    try:
        # Stuur huidige state naar nieuwe client
        await websocket.send(json.dumps({"type": "FULL_STATE", "payload": shared_state}))

        async for message in websocket:
            try:
                msg = json.loads(message)
                await handle_message(msg, websocket)
            except json.JSONDecodeError:
                print("Parse error — ongeldige JSON ontvangen")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"Controller verbroken — totaal: {len(connected_clients)}")


async def handle_message(msg, sender):
    global shared_state
    t = msg.get("type")

    if t == "IMPORT_FLIGHTS":
        shared_state["flights"] = msg["payload"]["flights"]
        shared_state["sectors"] = msg["payload"]["sectors"]
        shared_state["lastUpdate"] = int(time.time() * 1000)
        await broadcast({"type": "FULL_STATE", "payload": shared_state}, exclude=sender)
        print(f"✓ {len(shared_state['flights'])} vluchten geïmporteerd")

    elif t == "HANDOFF":
        cs = msg["payload"]["callsign"]
        from_s = msg["payload"]["fromSector"]
        to_s = msg["payload"]["toSector"]
        if cs in shared_state["flights"]:
            shared_state["flights"][cs]["sector"] = to_s
            shared_state["flights"][cs]["status"] = "handoff-received"
            shared_state["flights"][cs]["handoffTime"] = int(time.time() * 1000)
            if cs in shared_state["sectors"].get(from_s, []):
                shared_state["sectors"][from_s].remove(cs)
            if to_s not in shared_state["sectors"]:
                shared_state["sectors"][to_s] = []
            shared_state["sectors"][to_s].append(cs)
            shared_state["lastUpdate"] = int(time.time() * 1000)
            await broadcast({"type": "FULL_STATE", "payload": shared_state})
            print(f"✓ Handoff: {cs} {from_s} → {to_s}")

    elif t == "UPDATE_FLIGHT":
        cs = msg["payload"]["callsign"]
        updates = msg["payload"]["updates"]
        if cs in shared_state["flights"]:
            shared_state["flights"][cs].update(updates)
            shared_state["lastUpdate"] = int(time.time() * 1000)
            await broadcast({"type": "FLIGHT_UPDATE", "payload": {"callsign": cs, "flight": shared_state["flights"][cs]}}, exclude=sender)

    elif t == "ADD_FLIGHT":
        f = msg["payload"]["flight"]
        cs = f["callsign"]
        shared_state["flights"][cs] = f
        sector = f.get("sector", "Unassigned")
        if sector not in shared_state["sectors"]:
            shared_state["sectors"][sector] = []
        shared_state["sectors"][sector].append(cs)
        shared_state["lastUpdate"] = int(time.time() * 1000)
        await broadcast({"type": "FULL_STATE", "payload": shared_state}, exclude=sender)

    elif t == "DELETE_FLIGHT":
        cs = msg["payload"]["callsign"]
        if cs in shared_state["flights"]:
            sector = shared_state["flights"][cs].get("sector", "Unassigned")
            if cs in shared_state["sectors"].get(sector, []):
                shared_state["sectors"][sector].remove(cs)
            del shared_state["flights"][cs]
            shared_state["lastUpdate"] = int(time.time() * 1000)
            await broadcast({"type": "FULL_STATE", "payload": shared_state}, exclude=sender)

    elif t == "SIM_START":
        shared_state["simStartedAt"] = msg["payload"]["startedAt"]
        shared_state["lastUpdate"] = int(time.time() * 1000)
        await broadcast({"type": "SIM_START", "payload": msg["payload"]}, exclude=sender)
        print(f"✓ Simulatie gestart")

    elif t == "SIM_RESET":
        shared_state["simStartedAt"] = None
        shared_state["lastUpdate"] = int(time.time() * 1000)
        await broadcast({"type": "SIM_RESET", "payload": {}}, exclude=sender)
        print(f"✓ Simulatie gereset")

    elif t == "REQUEST_STATE":
        await sender.send(json.dumps({"type": "FULL_STATE", "payload": shared_state}))


async def broadcast(msg, exclude=None):
    if not connected_clients:
        return
    data = json.dumps(msg)
    targets = [c for c in connected_clients if c != exclude]
    if targets:
        await asyncio.gather(*[c.send(data) for c in targets], return_exceptions=True)


# ── HTTP server voor index.html ─────────────────────────────────────
def start_http_server(port=3000):
    # Verander naar de map waar server.py staat
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Geen HTTP logs

    httpd = TCPServer(("", port), QuietHandler)
    httpd.serve_forever()


# ── Main ────────────────────────────────────────────────────────────
async def main():
    PORT_HTTP = 3000
    PORT_WS   = 3001

    # Start HTTP server in aparte thread
    http_thread = threading.Thread(target=start_http_server, args=(PORT_HTTP,), daemon=True)
    http_thread.start()

    # Bepaal lokaal IP
    local_ip = "localhost"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        pass

    print("")
    print("╔══════════════════════════════════════════╗")
    print("║     ATC Flight Strips Server — Actief    ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  Browser:  http://{local_ip}:{PORT_HTTP}        ║")
    print(f"║  WebSocket: ws://{local_ip}:{PORT_WS}          ║")
    print("║                                          ║")
    print("║  Vul in de app in als server IP:         ║")
    print(f"║  {local_ip}:{PORT_WS}                      ║")
    print("╚══════════════════════════════════════════╝")
    print("")
    print("Wachten op controllers... (Ctrl+C om te stoppen)")
    print("")

    async with websockets.serve(handler, "0.0.0.0", PORT_WS):
        await asyncio.Future()  # Draai voor altijd


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer gestopt.")
