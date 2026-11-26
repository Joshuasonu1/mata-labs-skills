"""Overlay platform safe zones on a cover export so text and faces can be checked.
usage: python safe_zone_preview.py <cover.png> <facebook|x|linkedin|linkedin_company> [out.png]
Red = avatar/logo overlap (keep clear). Blue bands = cropped on mobile or some displays.
Green box = recommended message zone. Zones are fractions of the canvas (from platforms/*.md)."""
import sys
from PIL import Image, ImageDraw

ZONES = {
    # avatar: (cx, cy, r) as fractions of width/height/width; crops: list of rects (x0,y0,x1,y1) fractions
    'facebook': dict(avatars=[(0.135, 0.98, 0.11)], crops=[(0, 0, 0.16, 1), (0.84, 0, 1, 1)],
                     msg=(0.20, 0.08, 0.82, 0.85)),
    'x': dict(avatars=[(0.095, 0.93, 0.085)], crops=[(0, 0, 1, 0.12), (0, 0.88, 1, 1)],
              msg=(0.21, 0.13, 0.98, 0.87)),
    'linkedin': dict(avatars=[(0.14, 0.95, 0.115), (0.5, 1.02, 0.12)], crops=[(0, 0, 0.04, 1), (0.96, 0, 1, 1)],
                     msg=(0.63, 0.12, 0.97, 0.78)),
    'linkedin_company': dict(avatars=[(0.095, 0.80, 0.08)], crops=[(0, 0, 0.22, 1), (0.94, 0, 1, 1)],
                             msg=(0.23, 0.13, 0.94, 0.86)),
}

def main():
    src, plat = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else src.rsplit('.', 1)[0] + f'_{plat}_safezone.png'
    z = ZONES[plat]
    im = Image.open(src).convert('RGBA'); W, H = im.size
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x0, y0, x1, y1 in z['crops']:
        d.rectangle([x0 * W, y0 * H, x1 * W, y1 * H], fill=(40, 120, 255, 70))
    for cx, cy, r in z['avatars']:
        R = r * W
        d.ellipse([cx * W - R, cy * H - R, cx * W + R, cy * H + R], fill=(255, 40, 40, 90), outline=(255, 40, 40, 255), width=3)
    m = z['msg']; d.rectangle([m[0] * W, m[1] * H, m[2] * W, m[3] * H], outline=(40, 220, 90, 255), width=3)
    Image.alpha_composite(im, ov).convert('RGB').save(out)
    print(out)

if __name__ == '__main__':
    main()
