# Builds entry.png: a one-page front page of the world's news on Wednesday 18 November 2026.
# Layout: masthead, region/field bars, day-in-numbers strip, 3 lead cards + 10 cards with
# illustrations (art/*.jpg, made with ChatGPT image generation), a world map
# with numbered pins, an "Also on" list, a date-check box and a sources footer.
# Run: uv run --with pillow python make_front.py
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
ART = HERE / "art"
S = 2                      # supersample factor; drawn at 2048 px, saved at 1024 px
W = H = 1024
FONTS = "C:/Windows/Fonts/"

REGION = {  # region name -> colour
    "Europe": (36, 84, 160), "Middle East": (34, 128, 62), "Asia": (204, 128, 0),
    "Africa": (196, 76, 28), "Americas": (118, 58, 156), "Oceania": (20, 150, 150),
    "World": (85, 85, 85),
}
INK, PAPER, MUTED, RED = (22, 22, 22), (250, 246, 236), (88, 84, 76), (190, 30, 36)

# (region, tag, headline, detail, lon, lat) - every item first reported on 18 Nov 2026
LEADS = [
    ("Asia", "ASIA \u00b7 APEC, CHINA", "Trump, Xi and Putin shake hands at APEC in Shenzhen",
     "Xi met Trump on the tarmac; Putin flew in with nuclear-capable bombers.", 114.1, 22.5),
    ("Middle East", "MIDDLE EAST \u00b7 IRAN WAR", "US strikes Qeshm; Iran fires at Kuwait and Bahrain",
     "Iran fired missiles and drones at Gulf states as peace talks faltered.", 55.9, 26.8),
    ("Middle East", "MIDDLE EAST \u00b7 GAZA", "Israel launches ground operation in central Gaza",
     "Tanks crossed the truce's Yellow Line; families fled their shelters.", 34.4, 31.4),
]
CARDS = [
    ("Americas", "US \u00b7 MARKETS", "Anthropic prices its IPO at $83 a share",
     "Above the expected range, ahead of its stock-market debut.", -74.0, 40.7),
    ("World", "WORLD \u00b7 SPACE", "Voyager 1 is one light-day from Earth",
     "25.9 billion km away, 49 years after its launch.", -118.2, 34.2),
    ("World", "WORLD \u00b7 GAMES", "GTA VI launches to rave reviews",
     "PlayStation's network faltered hours before the release.", None, None),
    ("World", "WORLD \u00b7 HEALTH", "WHO sounds the alarm on antibiotic resistance",
     "Drug-resistant infections are spreading, the agency warns.", 6.1, 46.2),
    ("Americas", "US \u00b7 POLITICS", "Democrats pick Jeffries to be first Black Speaker",
     "House Democrats nominated Hakeem Jeffries for the job.", -77.0, 38.9),
    ("Europe", "EUROPE \u00b7 UKRAINE", "EU proposes a \u20ac45bn loan for Ukraine",
     "Money for 2027 to avert a cash crisis and boost defences.", 4.4, 50.8),
    ("Asia", "ASIA \u00b7 LABOUR", "Bangladesh police clash with garment workers",
     "Workers are demanding a higher minimum wage.", 90.4, 23.8),
    ("Americas", "AMERICAS \u00b7 DEFENCE", "Hegseth signs military deal in Caracas",
     "A surprise visit to Venezuela opens military cooperation.", -66.9, 10.5),
    ("World", "WORLD \u00b7 CLIMATE", "Fossil-fuel exit splits the COP31 talks",
     "OPEC defends oil and gas in Antalya; four more European states join the exit push.", 30.7, 36.9),
    ("Europe", "EUROPE \u00b7 UKRAINE WAR", "Russian strikes kill four in Odesa",
     "Russian strikes hit Ukraine's Black Sea port city overnight.", 30.7, 46.5),
]
# (region, place, text, lon, lat)
BRIEFS = [
    ("Americas", "Haiti", "Bukele confirms airstrike on a gang leader's mansion.", -72.3, 18.5),
    ("Americas", "Florida", "pastor found guilty over the 2021 killing of Haiti's president.", -80.2, 25.8),
    ("Asia", "China", "Xi and Japan's leader meet amid a political feud.", 116.4, 39.9),
    ("Americas", "Canada", "Carney and Trump hold unscheduled trade talks at APEC.", -75.7, 45.4),
    ("Americas", "Canada", "widens tariff relief with China on pork, seafood, metals.", -79.4, 43.7),
    ("Americas", "Colombia", "rejects a joint US plan to target drug gangs.", -74.1, 4.7),
    ("Middle East", "Iraq", "pumps oil to Turkey again after 12 years, bypassing Hormuz.", 44.4, 33.3),
    ("Middle East", "Iraq", "court jails six French Islamic State members for life.", 44.4, 33.3),
    ("Asia", "North Korea", "expanded its uranium enrichment plant, IAEA head says.", 125.8, 39.0),
    ("Middle East", "Lebanon", "US hits Hezbollah with new sanctions.", 35.5, 33.9),
    ("Middle East", "West Bank", "Israel delays settlement contracts after UK sanctions.", 35.2, 31.9),
    ("Africa", "Senegal", "President Faye is excluded from the ruling party.", -17.4, 14.7),
    ("Europe", "UK", "inflation rises to 3.6% as fuel prices hit records.", -0.1, 51.5),
    ("Europe", "UK", "energy bills forecast to rise 26% from January.", -1.5, 52.5),
    ("Europe", "UK-EU", "leaked reset draft covers pet passports and youth mobility.", 4.4, 50.8),
    ("Europe", "Germany", "Merz's coalition agrees an electricity tax cut.", 13.4, 52.5),
    ("Europe", "Berlin", "'Coalition of the Willing' meets on Ukraine.", 13.4, 52.5),
    ("Europe", "Dortmund", "club ends Rheinmetall deal after fan pressure.", 7.5, 51.5),
    ("Europe", "Portugal", "storms Bruna and Charles bring record rain.", -9.1, 38.7),
    ("Europe", "Serbia", "EPP ready to suspend Vu\u010di\u0107's SNS party.", 20.5, 44.8),
    ("Americas", "US", "transport chief blames a contractor for the FAA ground stop.", -77.0, 38.9),
    ("Americas", "US", "Senate panel rejects Trump's pick to lead the NSF.", -77.0, 38.9),
    ("Americas", "US", "lawmakers open a probe into Lutnick over Nvidia.", -77.0, 38.9),
    ("Americas", "California", "alleged Russian agent held for spying on a tech firm.", -122.1, 37.4),
    ("World", "World", "Pew: Muslims to outnumber Christians by 2035.", None, None),
    ("Asia", "South Korea", "AI cheating scandal upends university exams.", 127.0, 37.6),
    ("Asia", "India", "Amazon pledges \u20ac6.3bn for renewable energy.", 77.2, 28.6),
    ("Oceania", "Australia", "data centres a 'climate bomb', report warns.", 151.2, -33.9),
    ("Europe", "Cricket", "Duckett's 133 seals England's ODI series win.", -1.3, 52.6),
]
FIELDS = [("War & security", 11), ("Politics & diplomacy", 10), ("Economy & business", 9),
          ("Society & health", 4), ("Climate & weather", 3), ("Sport & culture", 3), ("Tech & science", 2)]
NUMBERS = [("$83", "Anthropic IPO price"), ("\u20ac45bn", "EU loan plan for Ukraine"),
           ("3.6%", "UK inflation"), ("25.9bn km", "Voyager 1 from Earth"),
           ("4", "killed in Odesa"), ("12 yrs", "since Iraq last piped oil to Turkey")]
DATE_CHECK = ("Left out on purpose because they were first reported on 17 Nov, not today: "
              "Ukraine's strike on the Kerch bridge, Nvidia's doubled revenue and Jensen Huang's exit, "
              "the US losing its measles-free status, California's Waymo freeway ban and Trump's arrival in Manila.")


def font(name, size):
    return ImageFont.truetype(FONTS + name, int(size * S))


SERIF_B, SERIF, SANS, SANS_B = "georgiab.ttf", "georgia.ttf", "segoeui.ttf", "segoeuib.ttf"


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width * S or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, f, fill=INK, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)


def rect(d, box, fill=None, outline=None, width=1):
    d.rectangle([v * S for v in box], fill=fill, outline=outline, width=width * S)


def bands(im, axis, min_len):
    """Cut an image at its white gutters along one axis (0 = rows, 1 = columns)."""
    g = im.convert("L")
    w, h = g.size
    n = h if axis == 0 else w
    line = (lambda i: g.crop((0, i, w, i + 1)).resize((64, 1))) if axis == 0 else \
           (lambda i: g.crop((i, 0, i + 1, h)).resize((1, 64)))
    bright = [sum(line(i).getdata()) / 64 > 238 for i in range(n)]
    out, i = [], 0
    while i < n:
        if not bright[i]:
            j = i
            while j < n and not bright[j]:
                j += 1
            if j - i >= min_len:
                out.append(im.crop((0, i, w, j)) if axis == 0 else im.crop((i, 0, j, h)))
            i = j
        i += 1
    return out


def load_art():
    """3 lead pictures, then 10 card pictures in card order."""
    leads = [Image.open(ART / f"{n}.jpg").convert("RGB") for n in ("lead1_apec", "lead2_gulf", "lead3_gaza")]
    cards = [Image.open(ART / f"{n}.jpg").convert("RGB")
             for n in ("card04_ipo", "card05_voyager", "card06_gta", "card07_lab", "card08_capitol")]
    sheet = Image.open(ART / "cards09_13_sheet.jpg").convert("RGB")
    for band in bands(sheet, 0, 150):          # two rows of two, then one wide panel
        cards += bands(band, 1, 150)
    assert len(cards) == 10, len(cards)
    return leads, cards


def cover(im, w, h):
    """Scale and centre-crop an illustration to fill w x h (in output pixels)."""
    w, h = int(w * S), int(h * S)
    r = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * r)), max(h, round(im.height * r))), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def badge(d, x, y, n, size=15):
    rect(d, (x, y, x + size, y + size), fill=RED)
    text(d, (x + size / 2, y + size / 2 + 0.5), str(n), font(SANS_B, size * 0.62), (255, 255, 255), "mm")


def card(img, d, x, y, w, ih, n, story, art, hl_size, det_size, lead=False):
    region, tag, head, detail = story[:4]
    img.paste(cover(art, w, ih), (int(x * S), int(y * S)))
    badge(d, x, y, n, 17 if lead else 14)
    ty = y + ih + 4
    tf = font(SANS_B, 7.6 if not lead else 8.4)
    tw = d.textlength(tag, font=tf) / S + 8
    rect(d, (x, ty, x + tw, ty + 11), fill=REGION[region])
    text(d, (x + 4, ty + 5.8), tag, tf, (255, 255, 255), "lm")
    hf = font(SERIF_B, hl_size)
    ly = ty + 14
    for line in wrap(d, head, hf, w)[:2]:
        text(d, (x, ly), line, hf)
        ly += hl_size * 1.12
    df = font(SANS, det_size)
    ly += 1.5
    for line in wrap(d, detail, df, w)[:2]:
        text(d, (x, ly), line, df, MUTED)
        ly += det_size * 1.25


def world_map(img, d, x, y, w, h):
    rect(d, (x, y, x + w, y + h), fill=(214, 230, 240))
    land = json.loads((ART / "land110.geojson").read_text(encoding="utf8"))
    lat_top, lat_bot = 80, -58

    def pt(lon, lat):
        return ((x + (lon + 180) / 360 * w) * S, (y + (lat_top - lat) / (lat_top - lat_bot) * h) * S)

    for feat in land["features"]:
        geo = feat["geometry"]
        polys = geo["coordinates"] if geo["type"] == "MultiPolygon" else [geo["coordinates"]]
        for poly in polys:
            ring = [pt(lon, max(lat_bot, min(lat_top, lat))) for lon, lat in poly[0]]
            d.polygon(ring, fill=(236, 230, 214), outline=(176, 168, 150))
    for region, place, _t, lon, lat in BRIEFS:
        if lon is not None:
            px, py = pt(lon, lat)
            r = 2.6 * S
            d.ellipse([px - r, py - r, px + r, py + r], fill=REGION[region])
    for n, st in enumerate(LEADS + CARDS, 1):
        if st[4] is None:
            continue
        px, py = pt(st[4], st[5])
        r = 6.2 * S
        d.ellipse([px - r, py - r, px + r, py + r], fill=REGION[st[0]], outline=(255, 255, 255), width=S)
        d.text((px, py + 0.5 * S), str(n), font=font(SANS_B, 7), fill=(255, 255, 255), anchor="mm")
    rect(d, (x, y, x + w, y + h), outline=(150, 150, 150))


def main():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)
    M = 12  # page margin
    # top line
    text(d, (M, 6), "THE WORLD'S NEWS IN ONE PICTURE", font(SANS_B, 9.5))
    k1, k2 = "42 STORIES", " \u00b7 7 REGIONS \u00b7 7 FIELDS \u00b7 13 ILLUSTRATED \u00b7 ALL FROM WEDNESDAY 18 NOVEMBER"
    kf = font(SANS_B, 9.5)
    k2w = d.textlength(k2, font=kf) / S
    text(d, (W - M - k2w, 6), k2, kf)
    text(d, (W - M - k2w, 6), k1, kf, RED, "ra")
    # masthead, fitted to the page width
    size = 80
    while d.textlength("Wednesday 18 November 2026", font=font(SERIF_B, size)) / S > W - 2 * M - 10:
        size -= 1
    text(d, (W / 2, 52), "Wednesday 18 November 2026", font(SERIF_B, size), INK, "mm")
    rect(d, (M, 88, W - M, 89.5), fill=INK)
    # region bar
    counts = {r: 0 for r in REGION}
    for st in LEADS + CARDS + BRIEFS:
        counts[st[0]] += 1
    total = sum(counts.values())
    bx, by = M, 93
    for r, c in counts.items():
        if not c:
            continue
        bw = max(58, (W - 2 * M) * c / total)
        if r == "World":
            bw = W - M - bx
        rect(d, (bx, by, bx + bw, by + 13), fill=REGION[r])
        text(d, (bx + bw / 2, by + 6.8), f"{r.upper()} {c}", font(SANS_B, 8.2), (255, 255, 255), "mm")
        bx += bw
    # field bar
    rect(d, (M, 108, W - M, 121), fill=INK)
    fx = M + 8
    text(d, (fx, 114.5), "BY FIELD:", font(SANS_B, 8.2), (255, 255, 255), "lm")
    fx += 52
    for name, c in FIELDS:
        s1 = f"{name} "
        text(d, (fx, 114.5), s1, font(SANS, 8.2), (255, 255, 255), "lm")
        fx += d.textlength(s1, font=font(SANS, 8.2)) / S
        text(d, (fx, 114.5), str(c), font(SANS_B, 8.2), (250, 196, 60), "lm")
        fx += d.textlength(str(c), font=font(SANS_B, 8.2)) / S + 14
    # day in numbers
    rect(d, (M, 124, W - M, 139), fill=(240, 232, 212), outline=(205, 195, 170))
    nx = M + 6
    text(d, (nx, 131.5), "THE DAY IN NUMBERS:", font(SANS_B, 8.2), INK, "lm")
    nx += 102
    for big, small in NUMBERS:
        text(d, (nx, 131.5), big, font(SANS_B, 9.2), RED, "lm")
        nx += d.textlength(big, font=font(SANS_B, 9.2)) / S + 3
        text(d, (nx, 131.5), small, font(SANS, 8.2), INK, "lm")
        nx += d.textlength(small, font=font(SANS, 8.2)) / S + 13
    # lead cards
    leads_art, cards_art = load_art()
    gap = 8
    lw = (W - 2 * M - 2 * gap) / 3
    for i, st in enumerate(LEADS):
        card(img, d, M + i * (lw + gap), 145, lw, 128, i + 1, st, leads_art[i], 17.5, 9.6, lead=True)
    cw = (W - 2 * M - 4 * gap) / 5
    for i, st in enumerate(CARDS):
        row, col = divmod(i, 5)
        card(img, d, M + col * (cw + gap), 352 + row * 160, cw, 78, i + 4, st, cards_art[i], 12.6, 8.4)
    # bottom: map + date check (left), also-on list (right)
    by = 676
    rect(d, (M, by, W - M, by + 1.2), fill=INK)
    text(d, (M, by + 5), "WHERE IT HAPPENED", font(SERIF_B, 12.5))
    mw = 318
    world_map(img, d, M, by + 23, mw, 172)
    ly = by + 200
    lx = M
    for r, c in counts.items():
        lab = r if r != "Middle East" else "Mid-East"
        d.ellipse([(lx) * S, (ly + 1) * S, (lx + 7) * S, (ly + 8) * S], fill=REGION[r])
        text(d, (lx + 9, ly - 0.5), lab, font(SANS, 7.6))
        lx += 12 + d.textlength(lab, font=font(SANS, 7.6)) / S + 2
    text(d, (M, ly + 11), "Numbered pins = cards 1-13 \u00b7 dots = briefs 14-42", font(SANS, 7.6), MUTED)
    # date check box
    dy = by + 225
    rect(d, (M, dy, M + mw, H - 30), fill=(252, 232, 232), outline=(214, 150, 150))
    rect(d, (M, dy, M + 3, H - 30), fill=RED)
    text(d, (M + 8, dy + 5), "DATE CHECK", font(SANS_B, 8.6), RED)
    yy = dy + 17
    for line in wrap(d, DATE_CHECK, font(SANS, 9.2), mw - 14):
        text(d, (M + 8, yy), line, font(SANS, 9.2))
        yy += 11.6
    print("date check ends at y", round(yy))
    # also on
    ax = M + mw + 16
    text(d, (ax, by + 5), "ALSO ON WEDNESDAY 18 NOVEMBER", font(SERIF_B, 12.5))
    colw = (W - M - ax - 2 * 12) / 3
    per = (len(BRIEFS) + 2) // 3
    bf, bfb = font(SANS, 9.4), font(SANS_B, 9.4)
    bottom = 0
    for ci in range(3):
        yy = by + 26
        for j, (region, place, t, _lo, _la) in enumerate(BRIEFS[ci * per:(ci + 1) * per]):
            n = 14 + ci * per + j
            cx = ax + ci * (colw + 12)
            num = f"{n} "
            text(d, (cx, yy), num, bfb, REGION[region])
            px = cx + d.textlength(num, font=bfb) / S
            lead_w = d.textlength(place + ": ", font=bfb) / S
            text(d, (px, yy), place + ":", bfb)
            words = t.split()
            first = ""
            while words and d.textlength(first + " " + words[0], font=bf) / S <= colw - (px - cx) - lead_w:
                first = (first + " " + words.pop(0)).strip()
            text(d, (px + lead_w, yy), first, bf)
            yy += 12.0
            for line in wrap(d, " ".join(words), bf, colw - (px - cx)) if words else []:
                text(d, (px, yy), line, bf)
                yy += 12.0
            yy += 4.6
        bottom = max(bottom, yy)
    print("also-on list ends at y", round(bottom))
    # footer
    rect(d, (M, H - 25, W - M, H - 24), fill=INK)
    foot = ("Every story here happened or was first reported on Wednesday 18 November 2026. Contested claims are "
            "attributed. Sources: BBC, Guardian, NYT, Al Jazeera, DW, France 24, Euronews, NPR, Sky, CNA, ABC. "
            "Illustrations: ChatGPT.")
    text(d, (W / 2, H - 13), foot, font(SANS, 7.9), INK, "mm")
    out = img.resize((W, H), Image.LANCZOS)
    out.save(HERE / "entry_full.png", optimize=True)
    out.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(
        HERE / "entry.png", optimize=True)
    print("saved", (HERE / "entry.png").stat().st_size, "bytes")


if __name__ == "__main__":
    main()
