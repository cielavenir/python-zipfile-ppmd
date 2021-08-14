For zipfile-xz information, see xz branch.

# zipfile-ppmd
[![PyPI](https://img.shields.io/pypi/v/zipfile-ppmd)](https://pypi.org/project/zipfile-ppmd/)

Monkey patch the standard `zipfile` module to enable PPMd support.

Based on [`zipfile-deflate64`](https://github.com/brianhelba/zipfile-deflate64) and [`zipfile-zstandard`](https://github.com/taisei-project/python-zipfile-zstd), which provides similar functionality but for the `deflate64` algorithm. Unlike `zipfile-deflate64`, this package supports both compression and decompression.

Requires [`pyppmd`](https://github.com/miurahr/pyppmd) for ppmd bindings. Note that 0.16.0+ is required, which is not released yet. Please do `python3 -m pip install git+https://github.com/miurahr/pyppmd`.

Note: if you need Python2, use [zipfile39](https://github.com/cielavenir/zipfile39) instead (it is also compatible with Python3).

## Installation
```bash
pip install zipfile-ppmd
```

## Usage
Anywhere in a Python codebase:
```python
import zipfile_ppmd  # This has the side effect of patching the zipfile module to support PPMd
```

Alternatively, `zipfile_ppmd` re-exports the `zipfile` API, as a convenience:
```python
import zipfile_ppmd as zipfile

zipfile.ZipFile(...)
```

Compression example:
```python
import zipfile_ppmd as zipfile

zf = zipfile.ZipFile('/tmp/test.zip', 'w', zipfile.ZIP_PPMD, compresslevel=5)
zf.write('large_file.img')
```

