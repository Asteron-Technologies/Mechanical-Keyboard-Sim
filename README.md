Mechanical Keyboard Engine

A high-performance, low-latency keyboard sound emulator built with Python 3.13 compatibility. This engine transforms your standard typing experience into an auditory journey with real-time audio processing.
Key Features

   - Spatial Audio Panning: Sounds are dynamically panned from left to right based on the key's physical position on a QWERTY layout.

   - Dynamic Velocity: Volume and texture scale based on your typing speed—the faster you type, the more intense the feedback.

   - Humanization Layer: Includes micro-timing jitter and pitch variations to prevent the robotic effect of repetitive samples.

   - Built-in Limiter: A real-time software limiter prevents audio clipping during rapid-fire typing sessions.

   - Python 3.13 Ready: Uses audioop-lts to ensure compatibility with the latest Python releases where the original audioop was deprecated.

Quick Start
1. Prerequisites

Ensure you have Python 3.8 or higher installed.
2. Installation

Clone the repository and install the required dependencies:
Bash

pip install -r requirements.txt

3. Audio Setup

4. Running the Engine

Simply run the script. It works globally—you do not need to keep the terminal focused to hear the sounds.
Bash

python keyboard_engine.py

Press ESC at any time to stop the engine.
Configuration

You can tweak the performance and feel of the engine inside the EngineConfig class:
Setting	Description
SAMPLE_RATE	Default 44100Hz for high-fidelity audio.
BUFFER	Set to 256 for ultra-low latency. Increase if you hear crackling.
HUMANIZE_VOLUME	How much the volume varies per keystroke.
HUMANIZE_TIMING	Adds milliseconds of random delay for a human feel.
CHANNELS	Supports 64 simultaneous sounds (prevents cutting off long tails).
License

MIT License - Feel free to use this for your own projects or custom sound packs.
