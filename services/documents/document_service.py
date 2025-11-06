import os
import json
import requests
import pandas as pd
from typing import List, Dict, Any, Optional, Union, BinaryIO
from .fields_service import DocumentFieldsService
from .types_service import DocumentTypesService
from .retrieval_service import DocumentRetrievalService
from .creation_service import DocumentCreationService
from .update_service import DocumentUpdateService
from .deletion_service import DocumentDeletionService
from .locks_service import DocumentLocksService
from .renditions_service import DocumentRenditionsService
from .attachments_service import DocumentAttachmentsService
from .annotations_service import DocumentAnnotationsService
from .relationships_service import DocumentRelationshipsService
from .exports_service import DocumentExportsService
from .events_service import DocumentEventsService
from .templates_service import DocumentTemplatesService
from .signatures_service import DocumentSignaturesService
from .tokens_service import DocumentTokensService
from .roles_service import DocumentRolesService


class DocumentService:
    """
    Main service class for managing documents in Veeva Vault.
    This class delegates to specialized services for different document management operations.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self._client = client

        # Initialize specialized service instances
        self.fields = DocumentFieldsService(client)
        self.types = DocumentTypesService(client)
        self.retrieval = DocumentRetrievalService(client)
        self.creation = DocumentCreationService(client)
        self.update = DocumentUpdateService(client)
        self.deletion = DocumentDeletionService(client)
        self.locks = DocumentLocksService(client)
        self.renditions = DocumentRenditionsService(client)
        self.attachments = DocumentAttachmentsService(client)
        self.annotations = DocumentAnnotationsService(client)
        self.relationships = DocumentRelationshipsService(client)
        self.exports = DocumentExportsService(client)
        self.events = DocumentEventsService(client)
        self.templates = DocumentTemplatesService(client)
        self.signatures = DocumentSignaturesService(client)
        self.tokens = DocumentTokensService(client)
        self.roles = DocumentRolesService(client)
