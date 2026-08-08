#!/usr/bin/env python3
"""生成 Minecraft 风格 16x16 像素纹理 PNG（Luanti mod 用）"""
import zlib, struct, os, math, random

def make_png(w, h, pixels):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            r, g, b, a = pixels[y * w + x]
            raw += bytes((int(r), int(g), int(b), int(a)))
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))

def noise(base, amt, seed):
    rng = random.Random(seed)
    def gen(x, y):
        d = (rng.random() - 0.5) * 2 * amt * 60
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return gen

def solid(c, seed=1):
    return noise(c, 0.1, seed)

def grass_top():
    g = solid((124, 189, 107), 7)
    def f(x, y):
        p = g(x, y)
        if y >= 13:  # 边缘一圈深绿
            return (94, 158, 70, 255)
        return p
    return f

def grass_side():
    g = solid((139, 106, 69), 8)
    gt = solid((124, 189, 107), 9)
    def f(x, y):
        if y < 4:
            return gt(x, y)
        if y == 4:
            return (80, 61, 40, 255)
        return g(x, y)
    return f

def wood_side():
    base = (107, 75, 42)
    rng = random.Random(11)
    def f(x, y):
        if x % 4 == 0 or x % 4 == 1:
            return (80, 56, 31, 255)
        d = (rng.random()-0.5)*20
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def planks():
    base = (184, 148, 95)
    rng = random.Random(13)
    def f(x, y):
        if y % 4 == 0:
            return (147, 118, 76, 255)
        d = (rng.random()-0.5)*16
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def leaves():
    base = (62, 122, 36)
    rng = random.Random(17)
    def f(x, y):
        d = (rng.random()-0.5)*40
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def cobble():
    base = (125, 125, 125)
    rng = random.Random(19)
    def f(x, y):
        bx, by = x//4, y//4
        off = (bx % 2) * 2
        ry = (y + off) % 4
        if ry == 0 or x % 4 == 0:
            return (88, 88, 88, 255)
        d = (rng.random()-0.5)*24
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def ore(base, spot, seed):
    rng = random.Random(seed)
    spots = []
    for _ in range(5):
        spots.append((rng.randint(1,13), rng.randint(1,13), 2))
    def f(x, y):
        for (sx, sy, sz) in spots:
            if abs(x-sx) < sz and abs(y-sy) < sz:
                return (spot[0], spot[1], spot[2], 255)
        d = (rng.random()-0.5)*18
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def sand():
    base = (219, 211, 160)
    rng = random.Random(23)
    def f(x, y):
        d = (rng.random()-0.5)*16
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def water():
    base = (63, 118, 228)
    rng = random.Random(29)
    def f(x, y):
        d = (rng.random()-0.5)*16
        return (base[0]+d, base[1]+d, base[2]+d, 180)
    return f

def bedrock():
    base = (90, 90, 90)
    rng = random.Random(31)
    def f(x, y):
        d = (rng.random()-0.5)*50
        return (base[0]+d, base[1]+d, base[2]+d, 255)
    return f

def diamond_sword_icon():
    # 16x16 钻石剑图标（白色剑刃 + 青握手）
    img = [[(0,0,0,0) for _ in range(16)] for _ in range(16)]
    # 剑刃（对角）
    for i in range(10):
        img[i][14-i] = (180, 240, 240, 255)
        img[i+1][14-i] = (140, 220, 230, 255)
        img[i][13-i] = (200, 250, 250, 255)
    # 握手
    for i in range(3):
        img[11+i][10-i] = (90, 60, 30, 255)
        img[11+i][9-i] = (120, 85, 45, 255)
    flat = [p for row in img for p in row]
    return lambda x, y: flat[y*16+x]

def pick_icon():
    img = [[(0,0,0,0) for _ in range(16)] for _ in range(16)]
    # 镐头（弧形）
    for i in range(5):
        img[4+i][3+i] = (120, 120, 120, 255)
        img[4+i][4+i] = (150, 150, 150, 255)
        img[8+i][8+i] = (120, 120, 120, 255)
    # 木柄
    for i in range(8):
        img[8+i][7] = (120, 85, 45, 255)
        img[8+i][8] = (140, 100, 55, 255)
    flat = [p for row in img for p in row]
    return lambda x, y: flat[y*16+x]

TEXTURES = {
    'grass_top': grass_top,
    'grass_side': grass_side,
    'dirt': lambda: solid((139, 106, 69), 3),
    'stone': lambda: solid((126, 126, 126), 5),
    'cobble': cobble,
    'wood_side': wood_side,
    'wood_top': lambda: solid((107, 75, 42), 12),
    'planks': planks,
    'leaves': leaves,
    'sand': sand,
    'iron_ore': lambda: ore((126,126,126), (216,175,147), 41),
    'gold_ore': lambda: ore((126,126,126), (252,232,77), 43),
    'diamond_ore': lambda: ore((126,126,126), (74,237,217), 47),
    'coal_ore': lambda: ore((126,126,126), (42,42,42), 53),
    'water': water,
    'bedrock': bedrock,
    'diamond_sword': diamond_sword_icon,
    'pick': pick_icon,
}

OUT = os.path.join(os.path.dirname(__file__), '..', 'games', 'minecraft', 'mods', 'mc_base', 'textures')
os.makedirs(OUT, exist_ok=True)

for name, fn in TEXTURES.items():
    f = fn()
    pixels = [f(x, y) for y in range(16) for x in range(16)]
    png = make_png(16, 16, pixels)
    with open(os.path.join(OUT, f'mc_base_{name}.png'), 'wb') as fh:
        fh.write(png)
    print(f'生成 mc_base_{name}.png ({len(png)} bytes)')
print('全部纹理生成完毕')
