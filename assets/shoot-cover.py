#!/usr/bin/env python3
"""Render LinkedIn article cover HTML files to exact 1200x644 PNGs."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
W, H = 1200, 644
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

names = sys.argv[1:] or ["cover-guesswork-A", "cover-guesswork-B"]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    for name in names:
        page.goto((HERE / f"{name}.html").as_uri())
        page.wait_for_timeout(250)
        out = HERE / f"{name}.png"
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": W, "height": H})
        print(f"{out.name}  {out.stat().st_size:,} bytes")
    browser.close()
