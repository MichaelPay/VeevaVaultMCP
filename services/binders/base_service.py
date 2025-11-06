import json
from typing import Dict, Any, Optional, Union, BinaryIO


class BaseBinderService:
    """
    Base class for all binder services in Veeva Vault
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client
