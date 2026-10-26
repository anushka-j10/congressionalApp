"""Render labeled synthetic notice facsimiles; never edits existing eval sets."""
import hashlib
import io
import json
from pathlib import Path
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

from .cases import CASES

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parent / 'corpus'
FONT_DIR = Path('/System/Library/Fonts/Supplemental')

def font(size, family='sans', bold=False):
    filename = {'sans': 'Arial Bold.ttf' if bold else 'Arial.ttf',
                'serif': 'Times New Roman Bold.ttf' if bold else 'Times New Roman.ttf',
                'mono': 'Courier New Bold.ttf' if bold else 'Courier New.ttf'}[family]
    candidates = [FONT_DIR / filename,
                  Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold
                       else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    for path in candidates:
        if path.is_file(): return ImageFont.truetype(str(path), size)
    raise RuntimeError('A TrueType font is required.')

def wrapped(draw, text, f, width):
    lines = []
    line = ''
    for word in text.split():
        candidate = (line + ' ' + word).strip()
        if draw.textlength(candidate, font=f) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + ([line] if line else [])

def paragraph(draw, text, x, y, width, size=27, family='sans', bold=False, fill='#141414'):
    f = font(size, family, bold)
    for line in wrapped(draw, text, f, width):
        assert draw.textlength(line, font=f) <= width, 'Text exceeds render width'
        draw.text((x, y), line, font=f, fill=fill)
        y += int(size * 1.38)
    return y + 16

def render(c):
    layout = c['layout']
    receipt = layout == 'receipt'
    panels = layout.startswith('two_panel')
    w,h = (900,1850) if receipt else (1500,1850)
    paper = '#fffef5' if receipt else '#ffffff'
    image = Image.new('RGB',(w,h),paper)
    d = ImageDraw.Draw(image)
    text = ['SYNTHETIC TEST - NOT VALID - DO NOT PAY', c['issuer'], 'PARKING NOTICE']
    y = paragraph(d,text[0],40,25,w-80,22,bold=True,fill='#8a2222')
    y = paragraph(d,'Invented case details. No real debt or vehicle.',40,y,w-80,19)
    family = 'mono' if receipt else 'serif' if layout in {'letter','summons'} else 'sans'
    accent = '#71364d' if layout == 'two_panel_pink' else '#24466e' if panels else '#202020'
    d.rectangle((38,y,w-38,y+138),fill=accent)
    y = paragraph(d,c['issuer'].upper(),60,y+15,w-120,30,family,bold=True,fill='white')
    y = paragraph(d,'PARKING NOTICE',60,y,w-120,26,family,bold=True,fill='white') + 40
    if panels:
        left, right = 48, w//2 + 30
        width = w//2 - 95
        d.line((w//2,y-15,w//2,h-140),fill='#aaaaaa',width=2)
        left_y = paragraph(d,'FRONT - CASE DETAILS',left,y,width,22,bold=True)
        right_y = paragraph(d,'REVERSE - RESPONSE OPTIONS',right,y,width,22,bold=True)
        for label, value in c['rows']:
            left_y = paragraph(d,f'{label}: {value}',left,left_y,width,27,'mono')
            d.line((left,left_y-5,left+width,left_y-5),fill='#bbbbbb')
        for p in c['paragraphs']:
            right_y = paragraph(d,p,right,right_y,width,29)
        y=max(left_y,right_y)
    elif layout in {'schedule','review','summons','hearing'}:
        for i,(label,value) in enumerate(c['rows']):
            left_lines=wrapped(d,label,font(26),540)
            right_lines=wrapped(d,value,font(27,family),w-720)
            rh=max(len(left_lines)*36,len(right_lines)*38)+24
            d.rectangle((50,y,w-50,y+rh),fill='#f0f0f0' if i%2==0 else paper,outline='#777777')
            paragraph(d,label,65,y+10,540,26,bold=True)
            paragraph(d,value,640,y+10,w-720,27,family)
            y+=rh
        y+=35
        for p in c['paragraphs']: y=paragraph(d,p,65,y,w-130,29,family)
    else:
        for label,value in c['rows']: y=paragraph(d,f'{label}: {value}',55,y,w-110,27,family)
        d.line((55,y,w-55,y),fill='#777777',width=2)
        y+=28
        for p in c['paragraphs']: y=paragraph(d,p,55,y,w-110,29,family)
    assert y < h-100, f'{c["id"]}: clipped content at {y}'
    d.line((40,h-90,w-40,h-90),fill='#aaaaaa')
    paragraph(d,'SYNTHETIC / '+c['id']+' / SOFTWARE TEST ONLY',40,h-70,w-80,20,bold=True,fill='#8a2222')
    text += [f'{label}: {value}' for label,value in c['rows']] + c['paragraphs']
    return image, '\n'.join(text)

def degrade(image, seed):
    # Reproducible slant, low resolution, uneven light, mild blur and JPEG loss.
    # All text stays on the photographed page; this is not a cropped/missing-page test.
    rng = random.Random(seed)
    transformed=image.transform(image.size,Image.Transform.AFFINE,(1,.027,-18,.011,1,-7),
        Image.Resampling.BICUBIC,fillcolor='#d3cbbf')
    transformed=transformed.rotate(rng.choice([-2.1,2.1]),Image.Resampling.BICUBIC,expand=True,fillcolor='#d3cbbf')
    x=np.linspace(0,1,transformed.width)[None,:]
    y=np.linspace(0,1,transformed.height)[:,None]
    light=np.clip(158+70*x+20*y,0,255).astype('uint8')
    transformed=ImageChops.multiply(transformed,Image.fromarray(light).convert('RGB'))
    transformed.thumbnail((1100,1400),Image.Resampling.LANCZOS)
    transformed=transformed.filter(ImageFilter.GaussianBlur(.65))
    output=io.BytesIO();transformed.save(output,'JPEG',quality=42)
    return output.getvalue()

def main():
    # Do not overwrite the corpus or change answers after inspecting outputs.
    if DATA.exists(): raise SystemExit('Corpus exists; creation refused.')
    DATA.mkdir()
    manifest={'synthetic':True,'created_on':'2026-10-26','independent_heldout':False,
        'answer_author':'Codex, before pipeline execution; requires AJ review',
        'states':['CT','ME','MA','NH','NJ','NY','PA','RI','VT'],
        'protocol':{'repeats':1,'variants':['clean','degraded'],'today':'2026-10-26',
          'model':'gpt-5.4-mini-2026-03-17','reader':'preprocessed','temperature':0,
          'reasoning_effort':'none','language':'en','human_amount_review':False,
          'ocr_confirmed_unchanged':True,'doc_type_selected':'parking_ticket',
          'note':'Single-field deadline scoring: CT_01 uses earliest printed response date. PA_02 must abstain because conditional deadlines differ. ME_02 must abstain on unsupported hours/weekend arithmetic. Relative dates scored as normalized ISO dates; no raw-rule aliases. Contact may be any declared complete contact channel.'},
        'files':{},'cases':[]}
    for i,c in enumerate(CASES):
        image,text=render(c)
        path=DATA/(c['id']+'-clean.png');image.save(path)
        (DATA/(c['id']+'-degraded.jpg')).write_bytes(degrade(image,700+i))
        entry=dict(c,visible_text=text,variants=[{'name':'clean','image':path.name},
                     {'name':'degraded','image':c['id']+'-degraded.jpg'}])
        (DATA/(c['id']+'.json')).write_text(json.dumps(entry,indent=2)+'\n')
        manifest['cases'].append(c['id']+'.json')
    for p in sorted(DATA.iterdir()):manifest['files'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    (DATA/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # A compact contact sheet for visual review, not pipeline input.
    sheet=Image.new('RGB',(1800,1500),'#dddddd');d=ImageDraw.Draw(sheet)
    for i,c in enumerate(CASES):
        im=Image.open(DATA/(c['id']+'-clean.png'));im.thumbnail((280,435))
        x=(i%6)*300;y=(i//6)*500
        sheet.paste(im,(x+(300-im.width)//2,y+35))
        d.text((x+15,y+5),c['id'],font=font(22),fill='black')
    sheet.save(DATA/'contact-sheet.jpg',quality=90)
    print(f'Created {len(CASES)} notices / {len(CASES)*2} images with predeclared answers.')

if __name__ == '__main__':main()
