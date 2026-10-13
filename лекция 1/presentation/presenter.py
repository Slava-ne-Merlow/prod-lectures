"""Local slide controller: python3 presenter.py; OBS URL http://127.0.0.1:8767/?obs=1."""
import json
import re
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
NOTES = ROOT.parent / 'books_app_video_1_part_1_theses_v2.md'
STATE = {'slide': 0}

def notes():
    return re.split(r'\n\s*-----\s*\n', NOTES.read_text().strip())

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'dist'), **kwargs)

    def reply(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/presenter-state':
            self.reply(STATE)
        elif path == '/presenter-notes':
            self.reply({'slides': notes()})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != '/presenter-state':
            self.reply({'error': 'Not found'}, 404)
            return
        if self.headers.get('Origin') not in (None, 'http://127.0.0.1:8767', 'http://localhost:8767'):
            self.reply({'error': 'Origin not allowed'}, 403)
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size < 1024:
                raise ValueError()
            slide = json.loads(self.rfile.read(size))['slide']
            if type(slide) is not int or not 0 <= slide < len(notes()):
                raise ValueError()
        except (ValueError, KeyError, TypeError):
            self.reply({'error': 'Invalid slide'}, 400)
            return
        STATE['slide'] = slide
        self.reply(STATE)

    def log_message(self, *args):
        pass

if __name__ == '__main__':
    print('Notes: http://127.0.0.1:8767/speaker.html', flush=True)
    print('OBS browser source: http://127.0.0.1:8767/?obs=1', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8767), Handler).serve_forever()
