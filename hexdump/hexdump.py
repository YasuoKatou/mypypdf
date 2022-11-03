from pathlib import Path
import argparse
import re

def path_check(fp):
    p = Path(fp)
    assert p.exists(), 'file not found ({}) '.format(fp)
    assert p.is_file(), 'path is not data file ({})'.format(fp)
    print('dump file : {}, ({:,} bytes)'.format(p.resolve(), p.stat().st_size))
    return p

def hexArray(b):
    s = re.split('(..)', b.hex())[1::2]
    if len(b) == 16:
        return ' '.join(s)
    else:
        return ' '.join(s) + '   ' * (16 - len(b))

_MIN_ASCII_CHAR = int('0x20', 16)
_MAX_ASCII_CHAR = int('0x7f', 16)

def ascii(b):
    r = []
    for x in b:
        if x < _MIN_ASCII_CHAR:
            r.append('.')
        elif x > _MAX_ASCII_CHAR:
            r.append('.')
        else:
            r.append(chr(x))
    return ''.join(r)

def dump01(p, limit=-1, offset=-1, plain_text=''):
    dp_size = 0
    with p.open(mode='rb') as f:
        if offset > 0:
            f.seek(offset)
        while True:
            b = f.read(16)
            if not b:
                break
            if plain_text:
                print(b.decode(plain_text, errors='ignore'), end='')
            else:
                print(hexArray(b) + '   ' + ascii(b))
            if limit > 0:
                dp_size += len(b)
                if limit <= dp_size:
                    break
    if plain_text:
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='file dump')
    parser.add_argument('--file-path', type=str, help='file path', required=True)
    parser.add_argument('--limit', type=int, default=-1, help='dump size (bytes)')
    parser.add_argument('--offset', type=int, default=-1, help='offset (bytes)')
    parser.add_argument('--plain-text', type=str, default='utf-8', help='plain text')
    args = parser.parse_args()
    #print(args)
    #file_path = '../pdf/pdfrw01/sample001_pdf.pdf'
    p = path_check(args.file_path)
    dump01(p, args.limit, args.offset, args.plain_text)
    #dump01(p, offset=16595)
#[EOF]