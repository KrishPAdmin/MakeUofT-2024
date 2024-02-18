import subprocess

def get_recording():
    record_command = ["arecord", "-D", "plughw:3,0", "--duration=5", "speech.wav"]
    subprocess.run(record_command)

def play_speaker():
    play_speaker = ["vlc", "speech.wav"]
    subprocess.run(play_speaker)

def stop_speaker():
    stop_speaker = ["pkill", "vlc"]
    subprocess.run(stop_speaker)