#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import main  # noqa: E402

raise SystemExit(main(sys.argv[1:], False))
