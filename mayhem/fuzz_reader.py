#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers
import os

# Errors
import struct

with atheris.instrument_imports(include=['shapefile']):
    import shapefile


def throw_once(err: Exception) -> bool:
    """Throw an exception once"""
    if not os.path.exists('/tmp/errors'):
        os.mkdir('/tmp/errors')
    file_name = err.__class__
    fp = f'/tmp/errors/{file_name}'

    if os.path.exists(fp):
        return False
    else:
        with open(fp, 'w+') as f:
            f.write('raised')
        return True


def handle_single_raise(err: Exception):
    if throw_once(err):
        raise err


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with fdp.ConsumeMemoryFile(all_data=False, as_bytes=True) as shp, \
                fdp.ConsumeMemoryFile(all_data=False, as_bytes=True) as dbf, \
                fdp.ConsumeMemoryFile(all_data=False, as_bytes=True) as shx:
            with shapefile.Reader(shp=shp, dbf=dbf, shx=shx) as spf:
                spf.shapes()
    except (shapefile.ShapefileException, struct.error, UnicodeDecodeError):
        return -1
    except ValueError as e:
        handle_single_raise(e)
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
