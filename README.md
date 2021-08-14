# zipfile-xz
[![PyPI](https://img.shields.io/pypi/v/zipfile-xz)](https://pypi.org/project/zipfile-xz/)

Monkey patch the standard `zipfile` module to enable XZ support.

Based on [`zipfile-deflate64`](https://github.com/brianhelba/zipfile-deflate64) and [`zipfile-zstandard`](https://github.com/taisei-project/python-zipfile-zstd), which provides similar functionality but for the `deflate64` algorithm. Unlike `zipfile-deflate64`, this package supports both compression and decompression.

Note: if you need Python2, use [zipfile39](https://github.com/cielavenir/zipfile39) instead (it is also compatible with Python3).

Note: XZ is based on LZMA2, so the compression ratio will be similar to ZIP_LZMA.

## Installation
```bash
pip install zipfile-xz
```

## Usage
Anywhere in a Python codebase:
```python
import zipfile_xz  # This has the side effect of patching the zipfile module to support XZ
```

Alternatively, `zipfile_ppmd` re-exports the `zipfile` API, as a convenience:
```python
import zipfile_xz as zipfile

zipfile.ZipFile(...)
```

Compression example:
```python
import zipfile_xz as zipfile

zf = zipfile.ZipFile('/tmp/test.zip', 'w', zipfile.ZIP_XZ, compresslevel=6)
zf.write('large_file.img')
```

