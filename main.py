import os
import sys
import time
import math
import random
import threading
from collections import deque

# Python 3.13 audio compatibility
try:
    import audioop
except ImportError:
    pass

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

try:
    import pygame
    from pynput import keyboard
except ImportError:
    print("Missing libraries. Run:")
    print("python -m pip install pygame pynput audioop-lts")
    sys.exit(1)


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
class EngineConfig:
    SAMPLE_RATE = 44100
    BUFFER = 256
    CHANNELS = 64

    BASE_VOLUME = 0.9
    HUMANIZE_VOLUME = 0.25
    HUMANIZE_TIMING = 0.006
    HUMANIZE_PITCH = 0.015

    LIMITER_THRESHOLD = 0.95
    LIMITER_RELEASE = 0.01

    AUDIO_FOLDERS = ["audio files", "audio"]


# ------------------------------------------------------------
# AUDIO ENGINE
# ------------------------------------------------------------
class AudioEngine:
    def __init__(self, config: EngineConfig):
        self.cfg = config
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        pygame.mixer.pre_init(
            self.cfg.SAMPLE_RATE,
            -16,
            2,
            self.cfg.BUFFER,
        )
        pygame.mixer.init()
        pygame.init()

        pygame.mixer.set_num_channels(self.cfg.CHANNELS)

        self.audio_path = self._find_audio_folder()
        self.special = {}
        self.pool = []

        self.last_times = deque(maxlen=32)
        self.pan_map = self._generate_pan_map()

        self._load_assets()

        self.limiter_gain = 1.0
        self.lock = threading.Lock()

    # --------------------------------------------------------

    def _find_audio_folder(self):
        for name in self.cfg.AUDIO_FOLDERS:
            p = os.path.join(self.script_dir, name)
            if os.path.exists(p):
                return p
        return None

    # --------------------------------------------------------

    def _generate_pan_map(self):
        rows = [
            ("1234567890", -0.9, 0.9),
            ("qwertyuiop", -0.8, 0.8),
            ("asdfghjkl", -0.7, 0.7),
            ("zxcvbnm", -0.6, 0.6),
        ]

        pans = {}
        for chars, start, end in rows:
            step = (end - start) / (len(chars) - 1)
            for i, c in enumerate(chars):
                pans[c] = start + step * i
        return pans

    # --------------------------------------------------------

    def _load_assets(self):
        if not self.audio_path:
            print("Audio folder not found.")
            return

        specials = {"space": "space.wav", "enter": "enter.wav", "cmd": "cmd.wav"}

        for k, f in specials.items():
            p = os.path.join(self.audio_path, f)
            if os.path.exists(p):
                self.special[k] = pygame.mixer.Sound(p)

        for i in range(1, 25):  # expanded pool
            p = os.path.join(self.audio_path, f"key{i}.wav")
            if os.path.exists(p):
                self.pool.append(pygame.mixer.Sound(p))

        print(f"Loaded {len(self.special) + len(self.pool)} sounds.")

    # --------------------------------------------------------
    # Humanization
    # --------------------------------------------------------

    def _typing_velocity(self):
        now = time.time()
        self.last_times.append(now)

        if len(self.last_times) < 2:
            return 0.5

        dt = now - self.last_times[-2]
        speed = max(0.001, min(0.3, dt))

        return 1.0 - (speed / 0.3)

    def _volume(self, velocity):
        base = self.cfg.BASE_VOLUME
        human = random.uniform(-self.cfg.HUMANIZE_VOLUME, self.cfg.HUMANIZE_VOLUME)
        return max(0.0, min(1.0, base * velocity + human))

    def _pan(self, char):
        return self.pan_map.get(str(char).lower(), 0.0)

    def _pitch_variation(self):
        return random.uniform(-self.cfg.HUMANIZE_PITCH, self.cfg.HUMANIZE_PITCH)

    # --------------------------------------------------------
    # Limiter
    # --------------------------------------------------------

    def _apply_limiter(self, vol):
        with self.lock:
            if vol > self.cfg.LIMITER_THRESHOLD:
                self.limiter_gain *= 0.9
            else:
                self.limiter_gain += (1.0 - self.limiter_gain) * self.cfg.LIMITER_RELEASE

            return vol * self.limiter_gain

    # --------------------------------------------------------
    # Playback
    # --------------------------------------------------------

    def play(self, char, name):
        sound = self.special.get(name)

        if not sound and self.pool:
            sound = random.choice(self.pool)

        if not sound:
            return

        velocity = self._typing_velocity()
        vol = self._volume(velocity)
        vol = self._apply_limiter(vol)

        pan = self._pan(char)

        left = max(0.0, min(1.0, (1 - pan) * vol))
        right = max(0.0, min(1.0, (1 + pan) * vol))

        channel = pygame.mixer.find_channel()
        if not channel:
            return

        # micro-timing jitter
        jitter = random.uniform(0, self.cfg.HUMANIZE_TIMING)
        time.sleep(jitter)

        channel.set_volume(left, right)
        channel.play(sound)


# ------------------------------------------------------------
# KEYBOARD LISTENER
# ------------------------------------------------------------
class KeyboardController:
    def __init__(self, audio: AudioEngine):
        self.audio = audio

    def on_press(self, key):
        try:
            char = key.char if hasattr(key, "char") else None
            name = key.name if hasattr(key, "name") else str(key)

            self.audio.play(char, name)

        except Exception:
            pass

        if key == keyboard.Key.esc:
            return False

    def run(self):
        print("Insane Keyboard Engine running. Press ESC to quit.")
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    cfg = EngineConfig()
    audio = AudioEngine(cfg)
    kb = KeyboardController(audio)
    kb.run()


if __name__ == "__main__":
    main()
