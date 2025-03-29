import common
from common_pins import AUDIO_UART
from kt403a import KT403A

speaker = None

class Song:
    def __init__(self, f, duration):
        self.file_index = f
        self.volume = duration

SONGS = {
    1: Song(0, 100),
    2: Song(1, 100),
    3: Song(2, 100),
    4: Song(3, 100),
    5: Song(4, 100),
    6: Song(5, 100),
    7: Song(6, 100),
    8: Song(7, 100),
    9: Song(8, 100),
    10: Song(9, 100),
    11: Song(10, 100),
    12: Song(11, 100),
    13: Song(12, 100),
    14: Song(13, 100),
    15: Song(14, 100),
    16: Song(15, 100),
    17: Song(16, 100),
    18: Song(17, 100),
    19: Song(18, 100),
    20: Song(19, 100),
    21: Song(20, 100),
    90: Song(21, 100)
}

def play_by_index(index):
    num = sorted(list(SONGS.keys()))[index]
    play(num)

def play(num):
    song = SONGS[num]
    if speaker.IsPlaying():
        speaker.Stop()
    speaker.SetVolume(song.volume)
    speaker.PlaySpecific(song.file_index)

def stop():
    speaker.Stop()

def init():
    global speaker
    speaker = KT403A(AUDIO_UART, volume=70)
    play(90)
