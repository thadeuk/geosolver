import vlc
import time

def play_sound(file_path):
    player: vlc.MediaPlayer = vlc.MediaPlayer(file_path) # type: ignore
    player.play()
    return player

if __name__ == "__main__":
    print("Playing sound...")
    player = play_sound("wakeup.mp3")
    print(player.is_playing())
    print(player.get_state())
    while player.is_playing() or player.get_state() != vlc.State.Ended:
        print("Playing...", player.get_state())
        time.sleep(0.1)
