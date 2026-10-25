import struct, zlib

extra = open('_img0.png', 'rb').read()[38962:]

def valid_chunk(data, pos, limit_types=(b'IHDR', b'IDAT', b'tEXt', b'iTXt', b'zTXt', b'PLTE', b'tRNS', b'IEND', b'tIME', b'sRGB', b'pHYs', b'gAMA', b'bKGD', b'pCAL', b'sCAN')):
    if pos + 12 > len(data):
        return None
    ln = struct.unpack('>I', data[pos:pos+4])[0]
    typ = data[pos+4:pos+8]
    if pos + 12 + ln > len(data):
        return None
    if not (0 <= ln <= 100_000_000) or typ not in limit_types:
        return None
    crc = struct.unpack('>I', data[pos+8+ln:pos+12+ln])[0]
    if zlib.crc32(data[pos+4:pos+8+ln]) & 0xFFFFFFFF != crc:
        return None
    return typ, ln, pos + 12 + ln

# scan start offsets, walk chunks forward, must end exactly at IEND
for s in range(0, min(8192, len(extra))):
    pos = s
    chunks = []
    ok = True
    while pos < len(extra):
        r = valid_chunk(extra, pos)
        if r is None:
            ok = False
            break
        typ, ln, pos = r
        chunks.append((typ.decode(), ln))
        if typ == b'IEND':
            break
    if ok and pos == len(extra) and chunks and chunks[-1][0] == 'IEND' and len(chunks) > 1:
        print('start offset', s, 'chunks:', chunks)
        break
