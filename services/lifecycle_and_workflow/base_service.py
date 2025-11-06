from typing import Dict, Any, Optional, Union, List


class BaseLifecycleWorkflowService:
    """
    Base class for all lifecycle and workflow services in Veeva Vault.

    This class provides the foundation for specialized service classes that handle
    specific aspects of Vault lifecycles and workflows such as document lifecycles,
    object lifecycles, and associated workflows.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance that provides authentication
                  and communication capabilities with the Veeva Vault API
        """
        self.client = client
