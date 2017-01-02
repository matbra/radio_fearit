import sys
if sys.version_info.major == 2:
    from urllib import urlopen
elif sys.version_info.major == 3:
    from urllib.request import urlopen
else:
    raise("python version maybe not supported.")
from os.path import join, dirname
import wave
import struct
from pymp3decoder import Decoder as Decoder_mp3

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import  *

CHUNK_SIZE = 4096
MODELDIR = join(dirname(__file__), "../sphinx_models/de_DE")

def find_frame_start(buffer):
    buf_conv = struct.unpack_from("B" * len(buffer), buffer)

    if 255 in buf_conv:
        idx_start = buf_conv.index(255)
        if buf_conv[idx_start+1] >= 224:
            return idx_start
        else:
            return None

def streamurl(url):

    # initialize mp3 decoder
    dec_mp3 = Decoder_mp3(20*CHUNK_SIZE)

    u = urlopen(url)

    # open the wave writer
    ww = wave.open("tempout.wav", 'wb')
    ww.setnchannels(1)
    ww.setframerate(44100)
    ww.setsampwidth(2)

    # prepare pocketsphinx
    ps_config = Decoder.default_config()
    ps_config.set_string('-hmm', join(MODELDIR, 'de_DE'))
    ps_config.set_string('-lm', join(MODELDIR, 'voxforge.lm.DMP'))
    ps_config.set_string('-dict', join(MODELDIR, 'voxforge.dic'))
    ps_config.set_string('-logfn', '/dev/null')
    dec_speech = Decoder(ps_config)

    # find the start index
    idx_start = None
    while True:
        while idx_start is None:
            n = u.read(CHUNK_SIZE)
            idx_start = find_frame_start(n)
            # bla = dec.get_tag_length(n[idx_start:])
        print(idx_start)

        try:
            last = bytearray([])
            chunk = n[idx_start:]
            decoded, last = dec_mp3.decode(chunk, last)
            print("started successfully.")
            break
        except:
            print("frame start problem. new try.")
            idx_start = None
            pass

    chunk = n[idx_start:]

    last = bytearray([])
    dec_speech.start_utt()
    in_speech_bf = True
    while True:
        decoded, last = dec_mp3.decode(chunk, last)
        chunk = u.read(CHUNK_SIZE)

        # extract the left channel (wave interleaved format)
        left = b"".join([decoded[_:_+2] for _ in range(0, len(decoded), 4)])
        ww.writeframes(left)

        dec_speech.process_raw(left, False, False)
        try:
            if dec_speech.hyp().hypstr != "":
                print("partial decoding result: ", dec_speech.hyp().hypstr)
        except AttributeError:
            pass

        if dec_speech.get_in_speech():
            pass

        if dec_speech.get_in_speech() != in_speech_bf:
            in_speech_bf = dec_speech.get_in_speech()
            if not in_speech_bf:
                dec_speech.end_utt()
                try:
                    if dec_speech.hyp().hypstr != '':
                        print('Stream decoding result:', dec_speech.hyp().hypstr)
                except AttributeError:
                    pass
                dec_speech.start_utt()

        if chunk == "":
            print("stream ended.")
            break

    ww.close()

if __name__ == "__main__":
    url = "http://dradio_mp3_dlf_m.akacast.akamaistream.net/7/249/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dlf_m"
    # url = "http://www.maninblack.org/demos/WhereDoAllTheJunkiesComeFrom.mp3"
    # url = "http://ndr-ndrinfo-nds-mp3.akacast.akamaistream.net/7/250/273753/v1/gnl.akacast.akamaistream.net/ndr_ndrinfo_nds_mp3"
    streamurl(url)