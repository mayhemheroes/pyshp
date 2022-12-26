#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

# Errors
import struct

with atheris.instrument_imports(include=['shapefile']):
    import shapefile


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with fdp.ConsumeMemoryFile(all_data=False, as_bytes=True) as shp, fdp.ConsumeMemoryFile(all_data=False, as_bytes=True) as dbf:
            with shapefile.Reader(shp=shp, dbf=dbf) as spf:
                spf.shapes()
    except (shapefile.ShapefileException, struct.error, UnicodeDecodeError):
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
