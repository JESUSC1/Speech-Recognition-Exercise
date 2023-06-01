#!/bin/bash

# Install Homebrew if not already installed
command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew..."; /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; }

# Install PortAudio
brew install portaudio

# Install Python packages
pip install -r requirements.txt
