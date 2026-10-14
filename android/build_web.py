#!/usr/bin/env python3
"""Erzeugt aus stempeluhr-source.html die Offline-Seite für die APK (app/assets) und die installierbare Web-App (web/)."""
import hashlib, io, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import build_icon
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "stempeluhr-source.html")
FONT_CSS = open(os.path.join(ROOT, "fonts.css")).read()

def page(extra_head=""):
    src = open(SRC).read()
    lines = [l for l in src.split("\n") if "fonts.googleapis" not in l and "fonts.gstatic" not in l and "claude:viewport" not in l]
    title, rest = "\n".join(lines).split("\n", 1)
    head = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + title + extra_head +
            '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}\n' + FONT_CSS + '</style>')
    return head + rest.replace('<div class="app">', '</head><body>\n<div class="app">', 1) + "\n</body></html>"

# APK-Assets
open(os.path.join(ROOT, "app/assets/index.html"), "w").write(page())

# Web-App
W = os.path.join(ROOT, "web")
shutil.rmtree(W, ignore_errors=True); os.makedirs(W + "/fonts")
for f in os.listdir(os.path.join(ROOT, "app/assets/fonts")):
    shutil.copy(os.path.join(ROOT, "app/assets/fonts", f), W + "/fonts/" + f)
icon = Image.open(io.BytesIO(build_icon(512)))
icon.save(W + "/icon-512.png"); icon.resize((192, 192), Image.LANCZOS).save(W + "/icon-192.png")
icon.resize((180, 180), Image.LANCZOS).save(W + "/apple-touch-icon.png")
# Maskable: Symbol mit Rand auf vollflächigem Grün
m = Image.new("RGBA", (512, 512), (14, 107, 87, 255)); m.alpha_composite(icon.resize((360, 360), Image.LANCZOS), (76, 76)); m.save(W + "/icon-maskable.png")
json.dump({
    "name": "Stempeluhr", "short_name": "Stempeluhr", "lang": "de", "start_url": "./", "scope": "./",
    "display": "standalone", "orientation": "portrait", "background_color": "#F2F4F1", "theme_color": "#0E6B57",
    "description": "Arbeitszeit stempeln, Abwesenheiten erfassen, Monatsbericht für die Buchhaltung.",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
}, open(W + "/manifest.webmanifest", "w"), ensure_ascii=False, indent=1)
head = ('\n<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon-192.png">'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">'
        '<script>window.STEMPELUHR_OFFLINE=true;if("serviceWorker"in navigator)addEventListener("load",()=>navigator.serviceWorker.register("sw.js"));</script>')
open(W + "/index.html", "w").write(page(head))
files = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-maskable.png", "apple-touch-icon.png"] + ["fonts/" + f for f in sorted(os.listdir(W + "/fonts"))]
h = hashlib.sha256()
for f in files[1:]: h.update(open(os.path.join(W, f), "rb").read())
ver = h.hexdigest()[:10]
open(W + "/sw.js", "w").write(f"""// Stempeluhr Offline-Cache (Version {ver})
const CACHE = "stempeluhr-{ver}";
const FILES = {json.dumps(files)};
self.addEventListener("install", e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); }});
self.addEventListener("activate", e => {{ e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); }});
self.addEventListener("fetch", e => {{
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, {{ ignoreSearch: true }}).then(r => r || fetch(e.request).catch(() => caches.match("index.html"))));
}});
""")
open(W + "/.nojekyll", "w").write("")
print("web", ver, sorted(os.listdir(W)))
