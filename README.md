# zipfile-dclimplode
[![PyPI](https://img.shields.io/pypi/v/zipfile-dclimplode)](https://pypi.org/project/zipfile-dclimplode/)

Monkey patch the standard `zipfile` module to enable DCL Implode support.

DCL stands for `PKWARE(R) Data Compression Library`.

Based on [`zipfile-deflate64`](https://github.com/brianhelba/zipfile-deflate64) and [`zipfile-zstandard`](https://github.com/taisei-project/python-zipfile-zstd), which provides similar functionality but for the `deflate64` algorithm. Unlike `zipfile-deflate64`, this package supports both compression and decompression.

Requires [`dclimplode`](https://github.com/cielavenir/dclimplode) for dclimplode bindings.

Note: if you need Python2, use [zipfile39](https://github.com/cielavenir/zipfile39) instead (it is also compatible with Python3).

## Installation
```bash
pip install zipfile-dclimplode
```

## Usage
Anywhere in a Python codebase:
```python
import zipfile_dclimplode  # This has the side effect of patching the zipfile module to support DCL Implode
```

Alternatively, `zipfile_dclimplode` re-exports the `zipfile` API, as a convenience:
```python
import zipfile_dclimplode as zipfile

zipfile.ZipFile(...)
```

Compression example:
```python
import zipfile_dclimplode as zipfile

zf = zipfile.ZipFile('/tmp/test.zip', 'w', zipfile.ZIP_DCLIMPLODED, compresslevel=3)
zf.write('large_file.img')
```

compresslevel: 1,2,3 (binary) 11,12,13 (ascii)
