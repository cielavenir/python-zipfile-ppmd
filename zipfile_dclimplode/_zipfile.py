
import zipfile
import dclimplode
import threading
import inspect
import struct

from ._patcher import patch


zipfile.ZIP_DCLIMPLODED = 10
zipfile.ZIP_PKIMPLODED = 10
if zipfile.ZIP_DCLIMPLODED not in zipfile.compressor_names:
    zipfile.compressor_names[zipfile.ZIP_DCLIMPLODED] = 'dclimplode'
zipfile.DCLIMPLODED_VERSION = 25

@patch(zipfile, '_check_compression')
def zstd_check_compression(compression):
    if compression == zipfile.ZIP_DCLIMPLODED:
        pass
    else:
        patch.originals['_check_compression'](compression)


@patch(zipfile, '_get_decompressor')
def zstd_get_decompressor(compress_type):
    if compress_type == zipfile.ZIP_DCLIMPLODED:
        return dclimplode.decompressobj()
    else:
        return patch.originals['_get_decompressor'](compress_type)


if 'compresslevel' in inspect.signature(zipfile._get_compressor).parameters:
    @patch(zipfile, '_get_compressor')
    def zstd_get_compressor(compress_type, compresslevel=None):
        if compress_type == zipfile.ZIP_DCLIMPLODED:
            if compresslevel is None:
                compresslevel = 3
            compressmethod = compresslevel//10
            compresslevel = compresslevel%10
            return dclimplode.compressobj(compressmethod, 1<<(9+compresslevel))
        else:
            return patch.originals['_get_compressor'](compress_type, compresslevel=compresslevel)
else:
    @patch(zipfile, '_get_compressor')
    def zstd_get_compressor(compress_type, compresslevel=None):
        if compress_type == zipfile.ZIP_DCLIMPLODED:
            if compresslevel is None:
                compresslevel = 3
            compressmethod = compresslevel//10
            compresslevel = compresslevel%10
            return dclimplode.compressobj(compressmethod, 1<<(9+compresslevel))
        else:
            return patch.originals['_get_compressor'](compress_type)


@patch(zipfile.ZipInfo, 'FileHeader')
def zstd_FileHeader(self, zip64=None):
    if self.compress_type == zipfile.ZIP_DCLIMPLODED:
        self.create_version = max(self.create_version, zipfile.DCLIMPLODED_VERSION)
        self.extract_version = max(self.extract_version, zipfile.DCLIMPLODED_VERSION)
    return patch.originals['FileHeader'](self, zip64=zip64)
