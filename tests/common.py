""" Common methods for clearing out test stuff """

from pynpoint.config import Config


def reset_config():
    # Reset config
    Config._Config__shared_state.clear()
