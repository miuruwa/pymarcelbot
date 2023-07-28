"""
Copyright 2023 kensoi
"""

from .require_args import requires_arguments


def init(definition):
    if not requires_arguments(definition):
        return definition()
    
    return definition
