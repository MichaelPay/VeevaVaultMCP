import json
from typing import Dict, Any, Optional, Union, BinaryIO


class BaseDocumentService:
    """
    Base class for all document services in Veeva Vault
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client
