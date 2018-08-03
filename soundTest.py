from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file('sounds/birdsong.wav')
play(sound)
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

# slow_sound = speed_change(sound, 0.75)
# fast_sound = speed_change(sound, 2.0)


# play(slow_sound)