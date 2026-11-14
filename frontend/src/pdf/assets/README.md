# Bundled PDF font

Noto Sans Regular, unchanged upstream TTF encoded as base64 for a static import.
Source: https://github.com/notofonts/noto-fonts/blob/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf
License: SIL Open Font License 1.1, included in OFL.txt.

The font and PDF libraries are bundled with the app. Export makes no font/CDN/API
requests. Unsupported glyphs cause an explicit refusal rather than silent loss;
TXT/copy remain available. The PDF embeds original UTF-8 TXT and validated JSON.

Noto Sans Symbols Regular supplies embedded arrow/math glyphs, under the same
OFL license: https://github.com/notofonts/noto-fonts/blob/main/hinted/ttf/NotoSansSymbols/NotoSansSymbols-Regular.ttf
The asset is subset to U+2190-22FF using `fonttools pyftsubset` (OFL permits
embedding/modification; this license declares no Reserved Font Names).
The inline worker keeps PDF layout off the UI thread and is terminated when a
draft changes. The worker never requests data or persists a report.
