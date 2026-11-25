#!/usr/bin/env python3
"""Create small WebP versions of the images used by the generated homepage."""
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent


class HomepageImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attributes):
        if tag == 'img':
            source = dict(attributes).get('src', '')
            if source.startswith('assets/'):
                self.sources.append(source)


def main():
    page = HomepageImages()
    page.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    for source in dict.fromkeys(page.sources):
        path = Path(source)
        original = (ROOT / path).resolve()
        if not original.is_relative_to(ROOT / 'assets') or not original.is_file():
            raise ValueError(f'Invalid local image: {source}')
        output = ROOT / path.parent / 'thumbs' / (path.stem + '.webp')
        output.parent.mkdir(parents=True, exist_ok=True)
        portrait = source == 'assets/portrait.jpg'
        max_width, quality = (480, 85) if portrait else (1000, 90)
        with Image.open(original) as opened:
            image = ImageOps.exif_transpose(opened)
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGBA' if 'transparency' in image.info else 'RGB')
            image.thumbnail((max_width, 10000), Image.Resampling.LANCZOS)
            image.save(output, format='WEBP', quality=quality, method=6)
        print(f'{source} -> {output.relative_to(ROOT)}: {original.stat().st_size} -> {output.stat().st_size} bytes')


if __name__ == '__main__':
    main()
