"""Simple CLI for pydrolink library.

Usage examples:
  pydrolink-cli list USER PASS
  pydrolink-cli current USER PASS
  pydrolink-cli alarms USER PASS
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
from dataclasses import asdict, is_dataclass
from typing import Any, cast

from .client import HydrolinkClient, AuthenticationError
from .service import WaterMeterService
import sys


def _print(obj: Any) -> None:
    import json

    def to_jsonable(value: Any) -> Any:
        if is_dataclass(value) and not isinstance(value, type):
            return to_jsonable(asdict(cast(Any, value)))
        if isinstance(value, datetime):
            return value.isoformat(sep=" ")
        if isinstance(value, dict):
            return {
                str(key): to_jsonable(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [to_jsonable(item) for item in value]
        return value

    print(json.dumps(to_jsonable(obj), indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(prog="pydrolink-cli")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("login")
    sub.add_parser("list")
    sub.add_parser("current")
    sub.add_parser("alarms")

    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()

    client = HydrolinkClient(username=args.username, password=args.password)
    service = WaterMeterService(client)

    async def _run():
        if args.cmd == "login":
            token = await client.login()
            _print({"token": token})
        elif args.cmd == "list":
            meters = await service.list_meters()
            _print(meters)
        elif args.cmd == "current":
            _print(await service.get_readings())
        elif args.cmd == "alarms":
            _print(await service.get_alarms())
        else:
            parser.print_help()

    try:
        asyncio.run(_run())
    finally:
        try:
            asyncio.run(client.close())
        except Exception:
            pass


def _main_wrapper():
    try:
        main()
    except AuthenticationError as e:
        print("Authentication failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    _main_wrapper()
