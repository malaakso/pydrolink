"""Simple CLI for pydrolink library.

Usage examples:
  pydrolink-cli login USER PASS
  pydrolink-cli list-meters USER PASS
  pydrolink-cli current USER PASS <meter_id>
"""
from __future__ import annotations

import argparse
import asyncio
from typing import Any

from .client import HydrolinkClient, AuthenticationError
import sys


def _print(obj: Any) -> None:
    import json

    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(prog="pydrolink-cli")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("login")
    sub.add_parser("list-meters")
    current = sub.add_parser("current")
    current.add_argument("meter_id", nargs="?")
    sub.add_parser("alarms")

    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()

    client = HydrolinkClient(username=args.username, password=args.password)

    async def _run():
        if args.cmd == "login":
            token = await client.login()
            _print({"token": token})
        elif args.cmd == "list-meters":
            meters = await client.list_meters()
            _print(meters)
        elif args.cmd == "current":
            if args.meter_id:
                meters = await client.create_water_meter_instances()
                m = next((x for x in meters if x.id == int(args.meter_id)), None)
                if not m:
                    print("meter not found")
                    return
                r = await m.current_reading()
                _print(r)
            else:
                _print(await client.get_current_readings())
        elif args.cmd == "alarms":
            _print(await client.get_alarms())
        else:
            parser.print_help()

    try:
        asyncio.run(_run())
    finally:
        try:
            asyncio.run(client.close())
        except Exception:
            pass

    # top-level error handling for authentication failures
    if False:
        pass

def _main_wrapper():
    try:
        main()
    except AuthenticationError as e:
        print("Authentication failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    _main_wrapper()

