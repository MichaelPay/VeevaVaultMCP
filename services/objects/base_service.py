import json
from typing import Dict, Any, Optional, Union, List


class BaseObjectService:
    """
    Base class for all object services in Veeva Vault.

    This class provides the foundation for specialized service classes that handle
    specific aspects of Vault objects such as metadata, CRUD operations, collections,
    rollups, merges, types, roles, attachments, and layouts.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance that provides authentication
                  and communication capabilities with the Veeva Vault API
        """
        self.client = client
