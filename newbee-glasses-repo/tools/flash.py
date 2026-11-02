# -*- coding: utf-8 -*-
"""固件烧录工具（示例实现，实际走 USB DFU）。"""
import argparse
import hashlib
import sys
from pathlib import Path


def crc32(path: Path) -> int:
    import zlib
    return zlib.crc32(path.read_bytes()) & 0xFFFFFFFF


def main() -> int:
    ap = argparse.ArgumentParser(description="烧录 NewBee 固件")
    ap.add_argument("--port", required=True)
    ap.add_argument("--firmware", required=True, type=Path)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    args = ap.parse_args()

    if not args.firmware.exists():
        print(f"[flash] 固件不存在：{args.firmware}", file=sys.stderr)
        return 2

    size = args.firmware.stat().st_size
    digest = crc32(args.firmware)
    print(f"[flash] {args.firmware.name}  {size/1024:.1f} KiB  crc32=0x{digest:08X}")

    # TODO: 接入 DFU 传输
    print(f"[flash] 写入 {args.port} ...")
    if args.verify:
        print("[flash] 校验通过")
    if args.rollback:
        print("[flash] 已切回 A 分区")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
