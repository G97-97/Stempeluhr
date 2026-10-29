#!/usr/bin/env python3
"""Baut die Stempeluhr-APK ohne Android-SDK: Manifest/ARSC von Hand, smali-dex, v2-Signatur."""
import hashlib, io, os, struct, sys, zipfile, datetime
from PIL import Image, ImageDraw
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

ROOT = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(ROOT, "app")
KEY_PEM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "signing-key.pem")
CERT_PEM = KEY_PEM.replace("key", "cert")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "Stempeluhr.apk")
VERSION_CODE, VERSION_NAME = 23, "3.2"

# ---------- String pools ----------
def string_pool(strings, utf8):
    data = b""; offsets = []
    for s in strings:
        offsets.append(len(data))
        if utf8:
            b = s.encode("utf-8")
            def ln(n):
                return bytes([n]) if n < 0x80 else bytes([0x80 | (n >> 8), n & 0xFF])
            data += ln(len(s)) + ln(len(b)) + b + b"\x00"
        else:
            u = s.encode("utf-16-le")
            data += struct.pack("<H", len(s)) + u + b"\x00\x00"
    while len(data) % 4: data += b"\x00"
    hdr = 28
    start = hdr + 4 * len(strings)
    body = b"".join(struct.pack("<I", o) for o in offsets) + data
    return struct.pack("<HHIIIIII", 0x0001, hdr, hdr + len(body), len(strings), 0, 0x100 if utf8 else 0, start, 0) + body

# ---------- Binary XML (Manifest) ----------
ANDROID_NS = "http://schemas.android.com/apk/res/android"
ATTR_IDS = {
    "theme": 0x01010000, "label": 0x01010001, "icon": 0x01010002, "name": 0x01010003,
    "exported": 0x01010010, "screenOrientation": 0x0101001e, "configChanges": 0x0101001f,
    "minSdkVersion": 0x0101020c, "versionCode": 0x0101021b, "versionName": 0x0101021c,
    "windowSoftInputMode": 0x0101022b, "targetSdkVersion": 0x01010270, "allowBackup": 0x01010280,
    "hardwareAccelerated": 0x010102d3,
}
T_REF, T_STR, T_DEC, T_HEX, T_BOOL = 0x01, 0x03, 0x10, 0x11, 0x12
TRUE = 0xFFFFFFFF
MANIFEST = ("manifest", [(None, "package", T_STR, "at.stempeluhr.app"),
                         ("a", "versionCode", T_DEC, VERSION_CODE), ("a", "versionName", T_STR, VERSION_NAME)], [
    ("uses-sdk", [("a", "minSdkVersion", T_DEC, 24), ("a", "targetSdkVersion", T_DEC, 34)], []),
    ("application", [("a", "label", T_STR, "Stempeluhr"), ("a", "icon", T_REF, 0x7f010000),
                     ("a", "allowBackup", T_BOOL, TRUE), ("a", "theme", T_REF, 0x0103012c),
                     ("a", "hardwareAccelerated", T_BOOL, TRUE)], [
        ("activity", [("a", "name", T_STR, "at.stempeluhr.app.MainActivity"), ("a", "exported", T_BOOL, TRUE),
                      ("a", "configChanges", T_HEX, 0x0DA0), ("a", "windowSoftInputMode", T_HEX, 0x10),
                      ("a", "screenOrientation", T_DEC, 1)], [
            ("intent-filter", [], [
                ("action", [("a", "name", T_STR, "android.intent.action.MAIN")], []),
                ("category", [("a", "name", T_STR, "android.intent.category.LAUNCHER")], []),
            ]),
        ]),
    ]),
])

def build_axml():
    # Attributnamen mit Ressourcen-ID zuerst (Reihenfolge = Resource-Map)
    names = []
    def walk(el):
        for ns, n, *_ in el[1]:
            if ns and n not in names: names.append(n)
        for c in el[2]: walk(c)
    walk(MANIFEST)
    names.sort(key=lambda n: ATTR_IDS[n])
    strings = list(names)
    def sidx(s):
        if s not in strings: strings.append(s)
        return strings.index(s)
    for s in ["android", ANDROID_NS]: sidx(s)
    chunks = []
    NO = 0xFFFFFFFF
    def element(el, line=[1]):
        tag, attrs, kids = el
        attrs = sorted(attrs, key=lambda a: ATTR_IDS.get(a[1], 0x7fffffff) if a[0] else 0x7fffffff)
        ab = b""
        for ns, n, t, v in attrs:
            nsi = sidx(ANDROID_NS) if ns else NO
            ni = sidx(n)
            if t == T_STR:
                si = sidx(v); raw, data = si, si
            else:
                raw, data = NO, v
            ab += struct.pack("<IIIHBBI", nsi, ni, raw, 8, 0, t, data)
        ext = struct.pack("<IIHHHHHH", NO, sidx(tag), 20, 20, len(attrs), 0, 0, 0)
        chunks.append(struct.pack("<HHIII", 0x0102, 16, 16 + len(ext) + len(ab), line[0], NO) + ext + ab)
        line[0] += 1
        for k in kids: element(k)
        chunks.append(struct.pack("<HHIIIII", 0x0103, 16, 24, line[0], NO, NO, sidx(tag)))
        line[0] += 1
    element(MANIFEST)
    ns = struct.pack("<II", sidx("android"), sidx(ANDROID_NS))
    start_ns = struct.pack("<HHIII", 0x0100, 16, 24, 1, NO) + ns
    end_ns = struct.pack("<HHIII", 0x0101, 16, 24, 1, NO) + ns
    pool = string_pool(strings, utf8=False)
    rmap = struct.pack("<HHI", 0x0180, 8, 8 + 4 * len(names)) + b"".join(struct.pack("<I", ATTR_IDS[n]) for n in names)
    body = pool + rmap + start_ns + b"".join(chunks) + end_ns
    return struct.pack("<HHI", 0x0003, 8, 8 + len(body)) + body

# ---------- resources.arsc (ein Icon) ----------
ICON_PATH = "res/mipmap-xxxhdpi-v4/ic_launcher.png"
def build_arsc():
    gpool = string_pool([ICON_PATH], utf8=True)
    tpool = string_pool(["mipmap"], utf8=False)
    kpool = string_pool(["ic_launcher"], utf8=False)
    spec = struct.pack("<HHIBBHI", 0x0202, 16, 16 + 4, 1, 0, 0, 1) + struct.pack("<I", 0x100)
    config = bytearray(64)
    struct.pack_into("<I", config, 0, 64)
    struct.pack_into("<H", config, 14, 640)      # density xxxhdpi
    struct.pack_into("<H", config, 24, 4)        # sdkVersion 4 (wie aapt bei -v4)
    entry = struct.pack("<HHI", 8, 0, 0) + struct.pack("<HBBI", 8, 0, T_STR, 0)
    th = 20 + 64
    typ = struct.pack("<HHIBBHII", 0x0201, th, th + 4 + len(entry), 1, 0, 0, 1, th + 4) + bytes(config) + struct.pack("<I", 0) + entry
    name = "at.stempeluhr.app".encode("utf-16-le").ljust(256, b"\x00")
    ph = 288
    pkg_body = tpool + kpool + spec + typ
    pkg = struct.pack("<HHII", 0x0200, ph, ph + len(pkg_body), 0x7f) + name + struct.pack("<IIIII", ph, 1, ph + len(tpool), 1, 0) + pkg_body
    body = gpool + pkg
    return struct.pack("<HHII", 0x0002, 12, 12 + len(body), 1) + body

# ---------- Icon ----------
def build_icon(size=192):
    s = 4; S = size * s
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    green, white = (14, 107, 87, 255), (255, 255, 255, 255)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=green)
    cx, cy, r, w = S / 2, S * 0.54, S * 0.27, int(S * 0.055)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=white, width=w)
    d.rounded_rectangle([cx - S * 0.09, S * 0.15, cx + S * 0.09, S * 0.15 + w], radius=w // 2, fill=white)
    d.line([cx, cy - r * 0.62, cx, cy], fill=white, width=w)
    d.line([cx, cy, cx + r * 0.45, cy + r * 0.32], fill=white, width=w)
    d.ellipse([cx - w * 0.75, cy - w * 0.75, cx + w * 0.75, cy + w * 0.75], fill=white)
    im = im.resize((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()

# ---------- Zip mit 4-Byte-Ausrichtung ----------
def build_zip(files):
    buf = io.BytesIO()
    fixed = (1981, 1, 1, 1, 1, 2)
    with zipfile.ZipFile(buf, "w") as z:
        for name, data, store in files:
            zi = zipfile.ZipInfo(name, fixed)
            zi.compress_type = zipfile.ZIP_STORED if store else zipfile.ZIP_DEFLATED
            zi.create_system = 0
            if store:
                off = buf.tell() + 30 + len(name.encode()) + 4
                pad = (-off) % 4
                zi.extra = struct.pack("<HH", 0xD935, pad) + b"\x00" * pad
            z.writestr(zi, data)
    return buf.getvalue()

# ---------- APK Signature Scheme v2 ----------
def lp(b): return struct.pack("<I", len(b)) + b
def find_eocd(apk):
    i = apk.rfind(b"PK\x05\x06")
    cd_size, cd_off = struct.unpack_from("<II", apk, i + 12)
    return i, cd_off, cd_size
def chunked_digest(sections):
    digs = []
    for sec in sections:
        for i in range(0, len(sec), 1 << 20):
            c = sec[i:i + (1 << 20)]
            digs.append(hashlib.sha256(b"\xa5" + struct.pack("<I", len(c)) + c).digest())
    return hashlib.sha256(b"\x5a" + struct.pack("<I", len(digs)) + b"".join(digs)).digest()
def sign_v2(apk, key, cert_der):
    eocd, cd_off, cd_size = find_eocd(apk)
    digest = chunked_digest([apk[:cd_off], apk[cd_off:eocd], apk[eocd:]])
    ALGO = 0x0103  # RSASSA-PKCS1-v1_5 mit SHA2-256
    signed_data = lp(lp(struct.pack("<I", ALGO) + lp(digest))) + lp(lp(cert_der)) + lp(b"")
    sig = key.sign(signed_data, padding.PKCS1v15(), hashes.SHA256())
    pub = key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    signer = lp(signed_data) + lp(lp(struct.pack("<I", ALGO) + lp(sig))) + lp(pub)
    value = lp(lp(signer))
    pair = struct.pack("<Q", 4 + len(value)) + struct.pack("<I", 0x7109871a) + value
    size = len(pair) + 8 + 16
    block = struct.pack("<Q", size) + pair + struct.pack("<Q", size) + b"APK Sig Block 42"
    new_eocd = bytearray(apk[eocd:])
    struct.pack_into("<I", new_eocd, 16, cd_off + len(block))
    return apk[:cd_off] + block + apk[cd_off:eocd] + bytes(new_eocd)

def load_or_make_key():
    if os.path.exists(KEY_PEM) and os.path.exists(CERT_PEM):
        key = serialization.load_pem_private_key(open(KEY_PEM, "rb").read(), None)
        cert = x509.load_pem_x509_certificate(open(CERT_PEM, "rb").read())
        return key, cert
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    nm = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Stempeluhr"), x509.NameAttribute(NameOID.COUNTRY_NAME, "AT")])
    now = datetime.datetime(2026, 10, 14, tzinfo=datetime.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(nm).issuer_name(nm).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=365 * 30)).sign(key, hashes.SHA256()))
    open(KEY_PEM, "wb").write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    open(CERT_PEM, "wb").write(cert.public_bytes(serialization.Encoding.PEM))
    return key, cert

if __name__ == "__main__":
    files = [("AndroidManifest.xml", build_axml(), False),
             ("classes.dex", open(os.path.join(APP, "classes.dex"), "rb").read(), False),
             ("resources.arsc", build_arsc(), True),
             (ICON_PATH, build_icon(), True)]
    adir = os.path.join(APP, "assets")
    for dp, _, fns in os.walk(adir):
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = "assets/" + os.path.relpath(p, adir).replace(os.sep, "/")
            files.append((rel, open(p, "rb").read(), fn.endswith(".woff2")))
    unsigned = build_zip(files)
    key, cert = load_or_make_key()
    apk = sign_v2(unsigned, key, cert.public_bytes(serialization.Encoding.DER))
    open(OUT, "wb").write(apk)
    print("APK", OUT, len(apk), "Bytes")
