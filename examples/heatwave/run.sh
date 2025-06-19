#!/bin/bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate as-137
python heatwave.py
