
import zipfile
import pyppmd
import threading
import inspect
import struct

from ._patcher import patch


zipfile.ZIP_PPMD = 98
zipfile.compressor_names[zipfile.ZIP_PPMD] = 'ppmd'
zipfile.PPMD_VERSION = 63

class PPMDCompressor(object):

    def __init__(self, level=None):
        self._comp = None
        self._level = level
        if self._level is None:
            self._level = 5
        if self._level < 1:
            self._level = 1
        if self._level > 9:
            self._level = 9

    def _init(self):
        ### level interpretation ###
        # https://github.com/jinfeihan57/p7zip/blob/v17.04/CPP/7zip/Compress/PpmdZip.cpp#L155
        # by the way, using numeric parameter is not covered by LGPL (according to clause 3).
        order = 3 + self._level
        sasize = 1 << min(self._level, 8)
        restore_method = 0 if self._level < 7 else 1
        ### level interpretation end ###

        prop = (order-1) | (sasize-1)<<4 | (restore_method)<<12;
        self._comp = pyppmd.Ppmd8Encoder(order, sasize<<20, restore_method=restore_method, endmark=False)
        return struct.pack('<H', prop)

    def compress(self, data):
        if self._comp is None:
            return self._init() + self._comp.encode(data)
        return self._comp.compress(data)

    def flush(self):
        if self._comp is None:
            return self._init() + self._comp.flush()
        return self._comp.flush()

class PPMDDecompressor(object):

    def __init__(self):
        self._decomp = None
        self._unconsumed = b''
        self.eof = False

    def decompress(self, data):
        if self._decomp is None:
            self._unconsumed += data
            if len(self._unconsumed) <= 2:
                return b''
            prop, = struct.unpack('<H', self._unconsumed[:2])
            order = (prop&0x000f)+1
            sasize = ((prop&0x0ff0)>>4)+1
            restore_method = (prop&0xf000)>>12

            self._decomp = pyppmd.Ppmd8Decoder(order, sasize<<20, restore_method=restore_method, endmark=False)
            data = self._unconsumed[2:]
            del self._unconsumed

        result = self._decomp.decode(data)
        self.eof = self._decomp.eof
        return result

@patch(zipfile, '_check_compression')
def zstd_check_compression(compression):
    if compression == zipfile.ZIP_PPMD:
        pass
    else:
        patch.originals['_check_compression'](compression)


@patch(zipfile, '_get_decompressor')
def zstd_get_decompressor(compress_type):
    if compress_type == zipfile.ZIP_PPMD:
        return PPMDDecompressor()
    else:
        return patch.originals['_get_decompressor'](compress_type)


if 'compresslevel' in inspect.signature(zipfile._get_compressor).parameters:
    @patch(zipfile, '_get_compressor')
    def zstd_get_compressor(compress_type, compresslevel=None):
        if compress_type == zipfile.ZIP_PPMD:
            if compresslevel is None:
                compresslevel = 5
            return PPMDCompressor(compresslevel)
        else:
            return patch.originals['_get_compressor'](compress_type, compresslevel=compresslevel)
else:
    @patch(zipfile, '_get_compressor')
    def zstd_get_compressor(compress_type, compresslevel=None):
        if compress_type == zipfile.ZIP_PPMD:
            if compresslevel is None:
                compresslevel = 5
            return PPMDCompressor(compresslevel)
        else:
            return patch.originals['_get_compressor'](compress_type)


@patch(zipfile.ZipInfo, 'FileHeader')
def zstd_FileHeader(self, zip64=None):
    if self.compress_type == zipfile.ZIP_PPMD:
        self.create_version = max(self.create_version, zipfile.PPMD_VERSION)
        self.extract_version = max(self.extract_version, zipfile.PPMD_VERSION)
    return patch.originals['FileHeader'](self, zip64=zip64)


