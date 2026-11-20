"""Собирает страницу-редактор для одного запроса (набора постов).

python3 tools/make_batch.py posts/2026-11-20/batch.json out.html

batch.json: {"id": "...", "title": "...", "items": [{"name", "image" (путь от batch.json),
  "fTitle", "fBody", "fLabel", "pDesc", "pFlavors", "pPrice", "pWhere", "pTags",
  "post" (готовый текст, txt-файл или строка), "scale", "cx", "cy", "rot", ...}]}
"""
import base64, io, json, os, re, sys
from PIL import Image

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, out = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(src))
batch = json.load(open(src, encoding='utf-8'))

def data_uri(path, max_h=900):
    im = Image.open(path).convert('RGBA')
    if im.height > max_h:
        im = im.resize((round(im.width * max_h / im.height), max_h), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

for it in batch['items']:
    img = it.pop('image', None)
    if img: it['src'] = data_uri(os.path.join(base, img))
    post = it.get('post')
    if post and post.endswith('.txt'):
        it['post'] = open(os.path.join(base, post), encoding='utf-8').read()

html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
# страница публикуется как артефакт: убираем свою обёртку документа
html = re.sub(r'^<!doctype html>.*?<head>\s*(<meta[^>]*>\s*)*', '', html, flags=re.S | re.I)
html = html.replace('</head>\n<body>', '').replace('\n</body>\n</html>\n', '\n')
html = re.sub(r'<title>.*?</title>', '<title>' + batch['title'] + '</title>', html, count=1)
data = json.dumps(batch, ensure_ascii=False).replace('</', '<\\/')
html = html.replace('<script>\n(function(){', '<script>window.TABACHOK_BATCH=' + data + ';</script>\n<script>\n(function(){', 1)
open(out, 'w', encoding='utf-8').write(html)
print(out, len(html) // 1024, 'KB')
