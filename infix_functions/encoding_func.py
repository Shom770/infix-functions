import codecs
import encodings
from io import StringIO

from transforms_code import transform_source


utf_8_encoding = encodings.search_function("utf-8")


def decode(source, encoding="utf-8", errors="strict"):
    """Base function that `infix_decoding` will use to decode the source and transform the source to allow infix functions."""
    return transform_source(bytes(source).decode(encoding, errors))


def infix_decoding(source, errors="strict"):
    """Decodes source and transforms the source to allow infix functions."""
    code, length_code = utf_8_encoding.decode(source, errors)

    return transform_source(code), length_code


def transform_stream(stream):
    """Reads the stream and transforms the stream (file provided with the encoding)."""
    return StringIO(transform_source(stream.read()))


class InfixDecoder(codecs.BufferedIncrementalDecoder):
    """
    Decodes file with `infix-function` encoding.

    Uses buffered incremental decoder because it may encode at different times and isn't at once.
    """
    def _buffer_decode(self, source, errors="strict", final=False):
        if final:
            return infix_decoding(source, errors)

        else:
            return "", 0


class InfixStreamReader(utf_8_encoding.streamreader):
    """Reads the stream (current file)."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.stream = transform_stream(self.stream)


def search_function(encoding):
    """Used to register the codec"""
    if encoding != "infix-functions":
        return

    return codecs.CodecInfo(
        name="infix-functions",
        encode=utf_8_encoding.encode,
        decode=infix_decoding,
        incrementalencoder=utf_8_encoding.incrementalencoder,
        incrementaldecoder=InfixDecoder,
        streamreader=InfixStreamReader,
        streamwriter=utf_8_encoding.streamwriter,
    )


codecs.register(search_function)
