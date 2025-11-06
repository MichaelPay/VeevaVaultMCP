from typing import Dict, Any, Optional, Union, List


class BaseWorkflowService:
    """
    Base class for all workflow services in Veeva Vault.

    This class provides the foundation for specialized service classes that handle
    specific aspects of Vault workflows such as workflows, tasks, and bulk actions.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance that provides authentication
                  and communication capabilities with the Veeva Vault API
        """
        self.client = client
