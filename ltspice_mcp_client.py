"""
LTspice MCP Client Bridge
------------------------
Enables direct JSON-RPC communication with the official ADI ltspice-mcp-bridge.exe.
Provides Pythonic access to schematic management, simulation control, and raw waveform data extraction.
"""

import json
import os
import subprocess
import sys


class LTspiceMCPClient:
    def __init__(self, bridge_path=r"C:\Program Files\ADI\LTspice\ltspice-mcp-bridge.exe"):
        if not os.path.exists(bridge_path):
            raise FileNotFoundError(f"LTspice MCP bridge not found at: {bridge_path}")
        
        self.proc = subprocess.Popen(
            [bridge_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        self.msg_id = 1
        self._initialize()

    def _initialize(self):
        init_req = {
            "jsonrpc": "2.0",
            "id": self.msg_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "antigravity-ltspice-client", "version": "1.0"}
            }
        }
        self.proc.stdin.write(json.dumps(init_req) + "\n")
        self.proc.stdin.flush()
        self.proc.stdout.readline()

        notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        self.proc.stdin.write(json.dumps(notif) + "\n")
        self.proc.stdin.flush()

    def call_tool(self, tool_name, arguments=None):
        self.msg_id += 1
        req = {
            "jsonrpc": "2.0",
            "id": self.msg_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()

        while True:
            line = self.proc.stdout.readline()
            if not line:
                return None
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            if msg.get("id") == self.msg_id:
                res = msg.get("result", {})
                content = res.get("content", [])
                if content and isinstance(content, list) and "text" in content[0]:
                    try:
                        return json.loads(content[0]["text"])
                    except json.JSONDecodeError:
                        return content[0]["text"]
                return res

    def list_reference_docs(self):
        return self.call_tool("list_ltspice_reference_docs")

    def get_reference_doc(self, name):
        return self.call_tool("get_ltspice_reference", {"name": name})

    def get_raw_info(self, raw_path):
        return self.call_tool("get_raw_info", {"path": os.path.abspath(raw_path)})

    def read_waveforms(self, raw_path, signals, max_values=100000):
        return self.call_tool("read_raw_waveforms", {
            "path": os.path.abspath(raw_path),
            "signals": signals,
            "max_values": max_values
        })

    def get_spice_log(self, path=None):
        args = {"path": os.path.abspath(path)} if path else {}
        return self.call_tool("get_spice_log", args)

    def close(self):
        try:
            self.proc.terminate()
            self.proc.wait(timeout=2)
        except Exception:
            pass


if __name__ == "__main__":
    client = LTspiceMCPClient()
    docs = client.list_reference_docs()
    print("LTspice MCP Client connected successfully!")
    print(f"Available reference docs: {len(docs.get('docs', []))}")
    client.close()
