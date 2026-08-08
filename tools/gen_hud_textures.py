#!/usr/bin/env python3
import zlib, struct, os

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

def bar_tex(r1, g1, b1, r2, g2, b2, bg=False):
    pixels = []
    for y in range(16):
        for x in range(16):
            if bg:
                pixels.append((30, 30, 30, 120))
            else:
                t = x / 15.0
                pixels.append((int(r1 + (r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t), 255))
    return make_png(16, 16, pixels)

OUT = os.path.join(os.path.dirname(__file__), '..', 'games', 'minecraft', 'mods', 'mc_levels', 'textures')
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'mc_levels_exp_bar.png'), 'wb') as f:
    f.write(bar_tex(255, 213, 79, 255, 152, 0))  # 金→橙
with open(os.path.join(OUT, 'mc_levels_exp_bg.png'), 'wb') as f:
    f.write(bar_tex(0, 0, 0, 0, 0, 0, bg=True))
print('HUD 纹理生成完毕')
