# The client is the public entry point of the boundary layer, so re-export it:
#   from ai.content import ContentClient
from .content_client import ContentClient

__all__ = ['ContentClient']
