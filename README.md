# zipfile-isal
[![PyPI](https://img.shields.io/pypi/v/zipfile-isal)](https://pypi.org/project/zipfile-isal/)

Monkey patch the standard `zipfile` module to enable accelerated deflate support via isal.

Based on [`zipfile-deflate64`](https://github.com/brianhelba/zipfile-deflate64) and [`zipfile-zstandard`](https://github.com/taisei-project/python-zipfile-zstd), which provides similar functionality but for the `deflate64` algorithm. Unlike `zipfile-deflate64`, this package supports both compression and decompression.

Requires [`isal`](https://github.com/pycompression/python-isal).

Note: if you need Python2, use [zipfile39](https://github.com/cielavenir/zipfile39) instead (it is also compatible with Python3).

## Installation
```bash
pip install zipfile-isal
```

## Usage
Anywhere in a Python codebase:
```python
import zipfile_isal  # This has the side effect of patching the zipfile module to support isal
```

Alternatively, `zipfile_isal` re-exports the `zipfile` API, as a convenience:
```python
import zipfile_isal as zipfile

zipfile.ZipFile(...)
```

Compression example:
```python
import zipfile_isal as zipfile

zf = zipfile.ZipFile('/tmp/test.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=-2)
zf.write('large_file.img')
```

