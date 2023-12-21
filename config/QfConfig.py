# QtFusion, AGPL-3.0 license
"""
QtFusion Configuration Package

This package provides a flexible configuration system for the QtFusion application. It includes the QF_Config class,
which offers a simple interface for managing application settings such as verbosity. The configuration can be easily
adjusted, saved to a file, and loaded from a file, allowing for persistent, customizable settings across application
sessions.

Features:
- Enable or disable verbose output globally.
- Save and load configuration settings to and from a file.
- Reset configuration to default values.

The package is designed to be easy to use and integrate into larger projects or systems that require configurable
settings.
"""

import json


class QF_Config:
    """
    Configuration Manager for QtFusion.

    This class provides methods to manage the configuration settings for the QtFusion application. It allows
    settings like verbosity to be dynamically adjusted during runtime, and also supports saving and loading these
    settings to and from a file for persistence. This is useful for maintaining consistent application behavior
    across different runs or environments.
    """

    VERBOSE = True

    @classmethod
    def set_verbose(cls, mode=True):
        """
        Set the verbosity of the QtFusion package.
        """
        cls.VERBOSE = mode

    @classmethod
    def is_verbose(cls):
        """
        Check if the QtFusion package is in verbose mode.
        """
        return cls.VERBOSE

    @classmethod
    def save_config(cls, file_path):
        """
        Save the current configuration to a file.
        """
        with open(file_path, 'w') as file:
            json.dump({'VERBOSE': cls.VERBOSE}, file)

    @classmethod
    def load_config(cls, file_path):
        """
        Load configuration from a file.
        """
        with open(file_path, 'r') as file:
            config = json.load(file)
            cls.VERBOSE = config.get('VERBOSE', True)

    @classmethod
    def reset_config(cls):
        """
        Reset configuration to default values.
        """
        cls.VERBOSE = True
