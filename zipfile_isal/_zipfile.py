
import zipfile
from isal import isal_zlib
import zlib
import threading
import inspect
import struct

from ._patcher import patch

zipfile.crc32 = isal_zlib.crc32

#@patch(zipfile, '_check_compression')
#def zstd_check_compression(compression):
#    if compression == zipfile.ZIP_DEFLATED:
#        pass
#    else:
#        patch.originals['_check_compression'](compression)


@patch(zipfile, '_get_decompressor')
def zstd_get_decompressor(compress_type):
    if compress_type == zipfile.ZIP_DEFLATED:
        return isal_zlib.decompressobj(-15)
    else:
        return patch.originals['_get_decompressor'](compress_type)


if 'compresslevel' in inspect.signature(zipfile._get_compressor).parameters:
    @patch(zipfile, '_get_compressor')
    def zstd_get_compressor(compress_type, compresslevel=None):
        if compress_type == zipfile.ZIP_DEFLATED:
            if compresslevel is None:
                compresslevel = 6
            if compresslevel<0:
                return isal_zlib.compressobj(-compresslevel, isal_zlib.DEFLATED, -15, 9)
            return zlib.compressobj(compresslevel, zlib.DEFLATED, -15)
        else:
            return patch.originals['_get_compressor'](compress_type, compresslevel=compresslevel)
else:
    @patch(zipfile, '_get_compressor')
    def zstd_get_compressor(compress_type, compresslevel=None):
        if compress_type == zipfile.ZIP_DEFLATED:
            if compresslevel is None:
                compresslevel = 6
            if compresslevel<0:
                return isal_zlib.compressobj(-compresslevel, isal_zlib.DEFLATED, -15, 9)
            return zlib.compressobj(compresslevel, zlib.DEFLATED, -15)
        else:
            return patch.originals['_get_compressor'](compress_type)


