import zlib, struct, os, random
def make_png(w, h, pixels):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            r, g, b, a = pixels[y*w+x]
            raw += bytes((int(r), int(g), int(b), int(a)))
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))
rng = random.Random(211)
pixels = []
for y in range(16):
    for x in range(16):
        if 3 <= x <= 12 and 2 <= y <= 9:
            c = (217, 160, 102)  # 肤色
        elif 4 <= x <= 11 and 10 <= y <= 15:
            c = (0, 168, 168)    # 青衫
        else:
            c = (60, 60, 60)
        if y in (4,5) and x in (5,6): c = (46, 74, 158)
        if y in (4,5) and x in (9,10): c = (46, 74, 158)
        if y == 2 and 6 <= x <= 9: c = (62, 39, 35)  # 头发
        d = (rng.random()-0.5)*10
        def cl(v): return max(0, min(255, int(v)))
        pixels.append((cl(c[0]+d), cl(c[1]+d), cl(c[2]+d), 255))
OUT = os.path.join(os.path.dirname(__file__), '..', 'games', 'minecraft', 'mods', 'mc_ai', 'textures')
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'mc_ai_npc.png'), 'wb').write(make_png(16, 16, pixels))
print('AI 纹理生成完毕')
