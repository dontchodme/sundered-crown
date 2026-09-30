"""THE EDIT: one table both the picture (trailer_cut.py) and the sound (trailer_mix.py) read.

Grid: 128 BPM, a bar is 1.875s, 30.0s = 16 bars. Every cut lands on a beat of
trailer_music.py's score, so the table is written in bars and beats, not seconds.
"""
BPM = 128.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
FPS = 60
DUR = 30.0


def tb(bar, beat=0.0):
    return round(bar * BAR + beat * BEAT, 6)


# relic id -> (display name, school, ultimate name), as the build names them
RELIC = {
    'duskreave': ('Duskreave', 'umbral', 'Scour'),
    'cindercleave': ('Cindercleave', 'dwarven', 'Breach'),
    'thornshear': ('Thornshear', 'verdant', 'The Winnowing'),
    'crozier': ('Crozier', 'sanctified', 'Radiance'),
    'culverin': ('Culverin', 'dwarven', 'Ironfall'),
    'bloodmirror': ('Bloodmirror', 'bloodsworn', 'Bloodletting'),
    'vesper': ('Vesper', 'vigil', 'Sentinel'),
    'starwarden': ('Starwarden', 'vigil', 'Corona'),
    'ravelbone': ('Ravelbone', 'bloodsworn', 'Garrote'),
    'paradox': ('Paradox', 'runic', 'Stasis Field'),
    'cipher': ('Cipher', 'runic', 'Convergence'),
    'shroudmaul': ('Shroudmaul', 'umbral', 'Grasp'),
    'lastlight': ('Lastlight', 'sanctified', 'Harrowing'),
    'briarwand': ('Briarwand', 'verdant', 'Bloom'),
    'nightglass': ('Nightglass', 'umbral', 'Backlash'),
    'gloamwire': ('Gloamwire', 'umbral', 'Crossweave'),
}

# FOOTAGE. (t0, t1, clip dir, source in-point s, options)
#   hero   relic to label (2-beat cuts only get a label)
#   z      (zoom at start, zoom at end), about (cx, cy) in source pixels
#   punch  extra zoom that decays over the first 0.18s of the cut
#   flash  white flash strength on the first frames
#   speed  source seconds per output second
#   dim    multiply the picture (graphics sit on dimmed footage)
#   sfx    clip-audio gain in dB
F = []


def seg(t0, t1, clip, s, **o):
    o.setdefault('z', (1.0, 1.05)); o.setdefault('c', (540, 1040)); o.setdefault('punch', 0.06)
    o.setdefault('flash', 0.0); o.setdefault('speed', 1.0); o.setdefault('dim', 1.0)
    o.setdefault('sfx', 0.0); o.setdefault('hero', None); o.setdefault('shake', 0.0)
    F.append(dict(t0=t0, t1=t1, clip=clip, s=s, **o))


# B) bars 2-3: four two-beat cuts, each labelled
seg(tb(2, 0), tb(2, 2), 'duskreave', 1.30, hero='duskreave', flash=0.6, c=(560, 1040), z=(1.10, 1.16))
seg(tb(2, 2), tb(3, 0), 'cindercleave', 1.00, hero='cindercleave', z=(1.06, 1.12))
seg(tb(3, 0), tb(3, 2), 'thornshear', 1.25, hero='thornshear', z=(1.06, 1.12))
seg(tb(3, 2), tb(4, 0), 'bloodmirror', 1.25, hero='bloodmirror', z=(1.22, 1.28), c=(650, 1500))
# C) bars 4-7
seg(tb(4, 0), tb(4, 3), 'starwarden', 0.00, dim=0.32, z=(1.02, 1.10), punch=0.0, sfx=-8, flash=0.55)    # under 16 GROUPS
seg(tb(4, 3), tb(5, 0), 'culverin', 0.85, flash=0.3, z=(1.28, 1.34), c=(600, 860))
seg(tb(5, 0), tb(5, 3), 'vesper', 0.75, dim=0.30, z=(1.02, 1.08), punch=0.0, sfx=-8, flash=0.4)        # under ONE KNOCKOUT
seg(tb(5, 3), tb(6, 0), 'crozier', 0.78, flash=0.3, z=(1.30, 1.36), c=(640, 920))
seg(tb(6, 0), tb(6, 2), 'vesper', 1.95, hero='vesper', flash=0.5, z=(1.08, 1.14), c=(600, 1150))                              # WIN OR GO HOME
seg(tb(6, 2), tb(7, 0), 'starwarden', 1.55, hero='starwarden', z=(1.28, 1.36), c=(470, 1150))
seg(tb(7, 0), tb(7, 2), 'ravelbone', 0.35, hero='ravelbone', z=(1.24, 1.30), c=(430, 1600))
seg(tb(7, 2), tb(8, 0), 'paradox', 1.00, hero='paradox', z=(1.24, 1.30), c=(560, 1350))
# D) bars 8-9: one beat each, the gap is the last half beat
D_CUTS = [('cipher', 2.55, {}), ('shroudmaul', 0.55, dict(z=(1.30, 1.36), c=(650, 1250))),
          ('lastlight', 0.55, dict(z=(1.12, 1.18), c=(620, 900))), ('briarwand', 1.98, {}), ('nightglass', 2.62, dict(z=(1.10, 1.16), c=(600, 1250))),
          ('culverin', 1.25, dict(z=(1.28, 1.34), c=(600, 900))), ('duskreave', 2.6, {})]
for i, (clip, s, o) in enumerate(D_CUTS):
    o = dict(dict(punch=0.08, flash=0.25, z=(1.03, 1.08)), **o)
    seg(tb(8, i), tb(8, i + 1), clip, s, **o)
# (tb(9,3) .. tb(10,0): black -- the score's gap)
# E) bar 10: the kill, slowed further, impact on the downbeat
seg(tb(10, 0), tb(11, 0), 'kill_gloamwire', 1.90, speed=0.62, z=(1.0, 1.10), flash=0.9, punch=0.10, sfx=2,
    shake=18)
# F) bars 11-12: six beats, then four half beats
F_CUTS = [('cindercleave', 0.0, dict(flash=0.75)), ('thornshear', 0.5, {}), ('vesper', 2.9, dict(z=(1.10, 1.16), c=(700, 1250))),
          ('lastlight', 1.05, dict(z=(1.12, 1.18), c=(620, 1000))), ('starwarden', 0.02, {}),
          ('kill_duskreave', 1.2, dict(sfx=1, z=(1.45, 1.55), c=(540, 1060)))]
for i, (clip, s, o) in enumerate(F_CUTS):
    o = dict(dict(punch=0.10, flash=0.35, z=(1.04, 1.10), shake=6), **o)
    seg(tb(11, i), tb(11, i + 1), clip, s, **o)
for i, (clip, s) in enumerate([('kill_gloamwire', 1.1), ('ravelbone', 1.8), ('duskreave', 3.2), ('paradox', 1.7)]):
    seg(tb(12, 2 + i / 2), tb(12, 2.5 + i / 2), clip, s, punch=0.12, flash=0.45, z=(1.06, 1.12), shake=8)

# VOICE. (file, onset seconds). Files are Kokoro bm_lewis at speed 1.0.
VO = [
    ('l1_100.wav', 0.28),   # Forty-nine fighters.
    ('l2_100.wav', tb(1, 0.3)),   # One crown.
    ('l3_100.wav', tb(4, 0.1)),   # Sixteen groups.
    ('l4_100.wav', tb(5, 0.1)),   # One knockout.
    ('l5_100.wav', tb(6, 0.1)),   # Win, or go home.
    ('l6_100.wav', tb(10, 0.55)),  # Who takes the crown?
    ('l7_100.wav', tb(13, 0.35)),  # The Super Weapon Ball World Cup.
    ('l8_100.wav', tb(14, 1.9)),   # Follow, so you don't miss a match.
]

# CAPTIONS (the stakes band). (t0, t1, text, y, h, size)
BANDS = [
    (0.30, tb(1, 0) - 0.02, '49 FIGHTERS', 250, 200, 124),
    (tb(1, 0.25), tb(2, 0) - 0.12, 'ONE CROWN', 1010, 200, 124),
    (tb(4, 0.05), tb(4, 3), '16 GROUPS', 300, 200, 124),
    (tb(5, 0.05), tb(5, 3), 'ONE KNOCKOUT', 300, 200, 124),
    (tb(6, 0.05), tb(7, 0) - 0.05, 'WIN OR GO HOME', 300, 200, 112),
    (tb(10, 0.5), tb(11, 0) - 0.04, 'WHO TAKES THE CROWN?', 300, 200, 100),
]
TITLE_T0 = tb(13, 0)
FOLLOW = (tb(14, 1.7), DUR, "FOLLOW SO YOU DON'T MISS A MATCH")
