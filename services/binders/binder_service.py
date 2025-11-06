import json
import requests
from .retrieval_service import BinderRetrievalService
from .creation_service import BinderCreationService
from .update_service import BinderUpdateService
from .deletion_service import BinderDeletionService
from .export_service import BinderExportService
from .relationships_service import BinderRelationshipsService
from .sections_service import BinderSectionsService
from .documents_service import BinderDocumentsService
from .templates_service import BinderTemplatesService
from .binding_rules_service import BinderBindingRulesService
from .roles_service import BinderRolesService
from .lifecycle_service import BinderLifecycleService


class BinderService:
    """
    Main service class for handling Veeva Vault binder operations.
    This class aggregates all specialized binder service classes.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client

        # Initialize specialized services
        self.retrieval = BinderRetrievalService(client)
        self.creation = BinderCreationService(client)
        self.update = BinderUpdateService(client)
        self.deletion = BinderDeletionService(client)
        self.export = BinderExportService(client)
        self.relationships = BinderRelationshipsService(client)
        self.sections = BinderSectionsService(client)
        self.documents = BinderDocumentsService(client)
        self.templates = BinderTemplatesService(client)
        self.binding_rules = BinderBindingRulesService(client)
        self.roles = BinderRolesService(client)
        self.lifecycle = BinderLifecycleService(client)
