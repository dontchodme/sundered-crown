"""Shared Playwright harness for The Sundered Crown.

One place that knows how to open the game, trap page errors, and drive the sim
headlessly. verify.py, tune.py, shots.py and render.py all build on this.
"""
from __future__ import annotations

import contextlib
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
GAME = HERE / "sundered-crown.html"


class PageErrors(Exception):
    pass


@contextlib.contextmanager
def game(headless: bool = True, game_path: pathlib.Path | None = None):
    """Yield (page, errors). `errors` accumulates JS errors and console errors.

    Callers should assert it is empty — a silent exception in the sim would
    otherwise read as a clean run with suspicious numbers.
    """
    path = game_path or GAME
    if not path.exists():
        raise FileNotFoundError(path)

    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=headless,
            args=["--disable-frame-rate-limit", "--disable-gpu", "--no-sandbox"],
        )
        page = browser.new_page(viewport={"width": 620, "height": 1000})
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on(
            "console",
            lambda m: errors.append(f"console.{m.type}: {m.text}")
            if m.type == "error"
            else None,
        )
        page.goto(path.as_uri())
        # __fontsReady as well: the artifact embeds Atkinson Hyperlegible Next and
        # Mono as base64 WOFF2, and Canvas draws the FALLBACK face (with the
        # fallback's metrics, silently) for any text measured before they
        # parse. Every capture in this repo goes through here, so this one
        # line is what stops a sheet or a render being of the wrong typeface.
        page.wait_for_function(
            "window.AC && window.AC.WEAPONS && window.__fontsReady !== false",
            timeout=20000)
        try:
            yield page, errors
        finally:
            browser.close()
