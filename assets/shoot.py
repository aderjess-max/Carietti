#!/usr/bin/env python3
"""Render banner HTML files to exact 1584x396 PNGs."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
W, H = 1584, 396
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

names = sys.argv[1:] or ["a"]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    for name in names:
        src = HERE / f"{name}.html"
        out = HERE / f"{name}.png"
        page.goto(src.as_uri())
        page.wait_for_timeout(250)
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": W, "height": H})
        print(f"{out.name}  {out.stat().st_size:,} bytes")
    browser.close()
