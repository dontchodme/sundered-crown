"""Contact sheet of a clip: a frame every STEP frames, timestamped.  python trailer_sheet.py clip.mp4 out.png 6"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
clip, out = sys.argv[1], sys.argv[2]
step = int(sys.argv[3]) if len(sys.argv) > 3 else 6
W, H = 162, 288
p = subprocess.run(['ffmpeg','-v','error','-i',clip,'-vf',f"select='not(mod(n\\,{step}))',scale={W}:{H}",'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'], capture_output=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3)
cols = 12; rows = (len(fr)+cols-1)//cols
sheet = Image.new('RGB', (cols*W, rows*(H+14)), (20,20,20))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(fr):
    x, y = (i%cols)*W, (i//cols)*(H+14)
    sheet.paste(Image.fromarray(f), (x, y+14)); d.text((x+3, y+1), f"{i*step/60:.2f}s", fill=(255,255,0))
sheet.save(out); print(len(fr), 'frames sampled')
