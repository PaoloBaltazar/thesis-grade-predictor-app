#!/bin/bash
pip install --upgrade pip
pip install -r requirements.txt

curl https://sh.rustup.rs -sSf | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"
