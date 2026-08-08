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
rng = random.Random(311)
pixels = []
for y in range(16):
    for x in range(16):
        base = (150, 110, 60) if (2 <= x <= 13 and 3 <= y <= 12) else (90, 65, 35)
        # 边框
        if x in (2, 13) or y in (3, 12):
            base = (110, 80, 45)
        # 锁扣
        if 7 <= x <= 8 and 6 <= y <= 8:
            base = (220, 190, 90)
        d = (rng.random()-0.5)*20
        pixels.append((max(0,min(255,base[0]+d)), max(0,min(255,base[1]+d)), max(0,min(255,base[2]+d)), 255))
OUT = os.path.join(os.path.dirname(__file__), '..', 'games', 'minecraft', 'mods', 'mc_dungeons', 'textures')
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'mc_dungeons_chest.png'), 'wb').write(make_png(16, 16, pixels))
print('箱子纹理生成完毕')
