import sys
from os.path import join, dirname
import wave
import struct
# sys.path.append(join(dirname(__file__), "build", "lib", "python3.3", "site-packages", "pymp3decoder-0.0.1-py3.3-linux-x86_64.egg"))
# sys.path.append(join(dirname(__file__), "build", "lib", "python3.3", "site-packages", "pymp3decoder-0.0.1-py3.3-linux-x86_64.egg", "pymp3decoder"))

import numpy as np
from scipy.signal import resample

from pymp3decoder import Decoder as Decoder_mp3

# sys.path.append(join(dirname(__file__), "build", "lib", "python3.3", "site-packages", "pocketsphinx-0.0.9-py3.3-linux-x86_64.egg"))
# sys.path.append(join(dirname(__file__), "build", "lib", "python3.3", "site-packages", "pocketsphinx-0.0.9-py3.3-linux-x86_64.egg", "pocketsphinx"))
# sys.path.append(join(dirname(__file__), "build", "lib", "python3.3", "site-packages", "pocketsphinx-0.0.9-py3.3-linux-x86_64.egg", "sphinxbase"))
# sys.path.append(join(dirname(__file__), "build", "lib", "python3.3", "site-packages", "sphinxbase"))

#sys.path.append(join(dirname(__file__), "build", "lib")

if sys.version_info.major == 2:
    from urllib import urlopen
elif sys.version_info.major == 3:
    from urllib.request import urlopen
else:
    raise("python version maybe not supported.")

#import peewee
from models import Words


from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import  *

CHUNK_SIZE = 1024
MODELDIR = join(dirname(__file__), "./sphinx_models/de_DE")

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
    dec_mp3 = Decoder_mp3(15*CHUNK_SIZE)

    u = urlopen(url)

    fs_source = 44100
    fs_target = 16000 # required by sphinx


    b_write_wave_file = True

    if b_write_wave_file:
        # open the wave writer
        ww = wave.open("tempout.wav", 'wb')
        ww.setnchannels(1)
        ww.setframerate(fs_target)
        ww.setsampwidth(2)

    # prepare pocketsphinx
    ps_config = Decoder.default_config()
    ps_config.set_string('-hmm', join(MODELDIR, 'de_DE'))
    ps_config.set_string('-lm', join(MODELDIR, 'voxforge.lm.DMP'))
    ps_config.set_string('-dict', join(MODELDIR, 'voxforge.dic'))
    ps_config.set_string('-logfn', '/dev/null')

    if True:
        # set some more parameters from the README.md accompanying the language model
        # ps_config.set_int("-lw", 10)
        ps_config.set_string("-feat", "1s_c_d_dd")
        ps_config.set_float("-beam", 1e-80)
        ps_config.set_float("-wbeam", 1e-40)
        # ps_config.set_float("-maxwpf", 40)
        ps_config.set_float("-wip", 0.2)
        ps_config.set_string("-agc", "none")
        ps_config.set_string("-varnorm", "no")
        ps_config.set_string("-cmn", "current")
        ps_config.set_int("-ds", 1)

        # ps_config.set_int("-vad_postspeech", 5)
        # ps_config.set_int("-vad_prespeech", 2)
        # ps_config.set_int("-vad_startspeech", 1)
        # ps_config.set_int("-vad_threshold", 1)

    dec_speech = Decoder(ps_config)

    # initialize the database connection
    # db = MySQLDatabase('radio_fearit', user="radio_fearit", passwd="Unf17m4*")


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
    in_speech_bf = False
    while True:
        decoded, last = dec_mp3.decode(chunk, last)
        chunk = u.read(CHUNK_SIZE)

        # extract the left channel (wave interleaved format)
        left = b"".join([decoded[_:_+2] for _ in range(0, len(decoded), 4)])

        # resample the pcm data
        if False:
            # most basic approach: every other two bytes (leave one sample outand accept aliasing)
            left = b"".join([left[_:_+2] for _ in range(0, len(left), 6)])
        elif True:
            # convert byte data to numpy array
            left_np = np.fromstring(left, dtype=np.int16)
            # print(left_np)
            left = resample(left_np, int(fs_target/fs_source  * len(left_np))).astype(np.int16).tobytes()

        if b_write_wave_file:
            ww.writeframes(left)

        dec_speech.process_raw(left, False, False)

        if False:
            try:
                if dec_speech.hyp().hypstr != "":
                    print("partial decoding result: ", dec_speech.seg())
            except AttributeError:
                pass

        # if dec_speech.get_in_speech():
        #     pass

        if dec_speech.get_in_speech() != in_speech_bf:
            in_speech_bf = dec_speech.get_in_speech()
            if not in_speech_bf:
                dec_speech.end_utt()
                segment = [seg.word for seg in dec_speech.seg()]
                try:
                    if segment != '':
                        print('Stream decoding result:', segment)
                        new_entries = [{'word': _} for _ in segment]
                        Words.insert_many(new_entries).execute()
                        # for word in segment:
                        #     new_word = Words.create(word=word)
                        #     new_word.save()
                except AttributeError:
                    pass
                dec_speech.start_utt()

        if chunk == "":
            print("stream ended.")
            break

    if b_write_wave_file:
        ww.close()

if __name__ == "__main__":
    # url = "http://dradio_mp3_dlf_m.akacast.akamaistream.net/7/249/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dlf_m"
    url = "http://dradio_mp3_dlf_s.akacast.akamaistream.net/7/251/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dlf_s"
    # url = "http://www.maninblack.org/demos/WhereDoAllTheJunkiesComeFrom.mp3"
    # url = "http://ndr-ndrinfo-nds-mp3.akacast.akamaistream.net/7/250/273753/v1/gnl.akacast.akamaistream.net/ndr_ndrinfo_nds_mp3"
    streamurl(url)
