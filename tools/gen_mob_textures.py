#!/usr/bin/env python3
"""生成怪物像素纹理 PNG"""
import zlib, struct, os, random

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

def make_16(fn):
    pixels = [fn(x, y) for y in range(16) for x in range(16)]
    return make_png(16, 16, pixels)

def zombie():
    rng = random.Random(101)
    def f(x, y):
        # 绿皮肤
        base = (78, 140, 66)
        if 3 <= x <= 12 and 2 <= y <= 9:  # 脸
            c = base
        elif 4 <= x <= 11 and 10 <= y <= 15:  # 身体
            c = (66, 124, 56)
        else:
            c = (50, 95, 45)
        # 眼睛
        if y in (4, 5) and x in (5, 6):
            c = (20, 20, 20)
        if y in (4, 5) and x in (9, 10):
            c = (20, 20, 20)
        # 嘴
        if y == 8 and 6 <= x <= 9:
            c = (30, 40, 30)
        d = (rng.random()-0.5)*16
        return (c[0]+d, c[1]+d, c[2]+d, 255)
    return f

def skeleton():
    rng = random.Random(107)
    def f(x, y):
        base = (200, 200, 200)
        if 3 <= x <= 12 and 2 <= y <= 9:
            c = base
        elif 4 <= x <= 11 and 10 <= y <= 15:
            c = (170, 170, 170)
        else:
            c = (150, 150, 150)
        if y in (4, 5) and x in (5, 6):
            c = (10, 10, 10)
        if y in (4, 5) and x in (9, 10):
            c = (10, 10, 10)
        d = (rng.random()-0.5)*14
        return (c[0]+d, c[1]+d, c[2]+d, 255)
    return f

def creeper():
    rng = random.Random(113)
    def f(x, y):
        base = (70, 150, 70)
        if 3 <= x <= 12 and 2 <= y <= 9:
            c = base
        elif 4 <= x <= 11 and 10 <= y <= 15:
            c = (56, 128, 60)
        else:
            c = (45, 105, 50)
        # 苦力怕脸：眼睛 + 嘴
        if y in (4, 5) and (x == 5 or x == 10):
            c = (20, 20, 20)
        if y == 7 and x in (6, 7, 8, 9):
            c = (20, 20, 20)
        if y in (8, 9) and x in (4, 5, 10, 11):
            c = (20, 20, 20)
        d = (rng.random()-0.5)*20
        return (c[0]+d, c[1]+d, c[2]+d, 255)
    return f

def spider():
    rng = random.Random(127)
    def f(x, y):
        base = (40, 40, 40)
        if 3 <= x <= 12 and 2 <= y <= 9:
            c = base
        elif 4 <= x <= 11 and 10 <= y <= 15:
            c = (30, 30, 30)
        else:
            c = (50, 20, 20)
        if y in (4, 5) and x in (5, 6):
            c = (200, 30, 30)
        if y in (4, 5) and x in (9, 10):
            c = (200, 30, 30)
        d = (rng.random()-0.5)*12
        return (c[0]+d, c[1]+d, c[2]+d, 255)
    return f

def iron_sword():
    img = [[(0,0,0,0) for _ in range(16)] for _ in range(16)]
    for i in range(10):
        img[i][14-i] = (200, 200, 200, 255)
        img[i][13-i] = (230, 230, 230, 255)
    for i in range(3):
        img[11+i][10-i] = (120, 80, 40, 255)
        img[11+i][9-i] = (150, 100, 50, 255)
    flat = [p for row in img for p in row]
    return lambda x, y: flat[y*16+x]

def apple():
    img = [[(0,0,0,0) for _ in range(16)] for _ in range(16)]
    for y in range(5, 13):
        for x in range(5, 11):
            img[y][x] = (220, 40, 40, 255)
    for y in range(6, 12):
        img[y][5] = (180, 30, 30, 255)
    img[4][8] = (90, 60, 30, 255)
    img[4][9] = (60, 130, 60, 255)
    flat = [p for row in img for p in row]
    return lambda x, y: flat[y*16+x]

TEXTURES = {
    'zombie': zombie,
    'skeleton': skeleton,
    'creeper': creeper,
    'spider': spider,
    'iron_sword': iron_sword,
    'apple': apple,
}

OUT = os.path.join(os.path.dirname(__file__), '..', 'games', 'minecraft', 'mods', 'mc_mobs', 'textures')
os.makedirs(OUT, exist_ok=True)
for name, fn in TEXTURES.items():
    f = fn()
    png = make_16(f)
    with open(os.path.join(OUT, f'mc_mobs_{name}.png'), 'wb') as fh:
        fh.write(png)
    print(f'生成 mc_mobs_{name}.png')
print('怪物纹理完毕')
