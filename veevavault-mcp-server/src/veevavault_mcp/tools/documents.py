"""
Document management tools for VeevaVault.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class DocumentsQueryTool(BaseTool):
    """Query documents in Veeva Vault using VQL or filters."""

    @property
    def name(self) -> str:
        return "vault_documents_query"

    @property
    def description(self) -> str:
        return """Query/search documents in Veeva Vault.

Use this to:
- Search for documents by name, type, or status
- List documents matching criteria
- Find specific documents

Supports both VQL queries and simple filters.
Most commonly used tool for document discovery."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "vql": {
                    "type": "string",
                    "description": "Raw VQL query (takes precedence over filters)",
                },
                "name_contains": {
                    "type": "string",
                    "description": "Filter documents by name (partial match)",
                },
                "document_type": {
                    "type": "string",
                    "description": "Document type (e.g., 'protocol__c', 'general_document__c')",
                },
                "lifecycle_state": {
                    "type": "string",
                    "description": "Lifecycle state (e.g., 'draft__c', 'approved__c')",
                },
                "status": {
                    "type": "string",
                    "description": "Document status (active, superseded, etc.)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results per page (default: 100, max: 1000)",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 1000,
                },
                "auto_paginate": {
                    "type": "boolean",
                    "description": "Automatically fetch all pages (default: false). WARNING: May return thousands of results.",
                    "default": False,
                },
            },
            "required": [],
        }

    async def execute(
        self,
        vql: Optional[str] = None,
        name_contains: Optional[str] = None,
        document_type: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        auto_paginate: bool = False,
    ) -> ToolResult:
        """Execute document query."""
        try:
            headers = await self._get_auth_headers()

            # Build VQL query
            if vql:
                query = vql
            else:
                query = self._build_document_query(
                    name_contains=name_contains,
                    document_type=document_type,
                    lifecycle_state=lifecycle_state,
                    status=status,
                    limit=limit,
                )

            # Execute query using POST (required by Vault API)
            path = self._build_api_path("/query")

            # Add Content-Type header for form-encoded data
            query_headers = {
                **headers,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = await self.http_client.post(
                path=path,
                headers=query_headers,
                data={"q": query},
            )

            # Collect all documents
            documents = response.get("data", [])

            # Parse pagination metadata
            pagesize = response.get("pagesize", limit)
            total = response.get("total", len(documents))
            next_page = response.get("next_page")

            # Auto-paginate if requested
            pages_fetched = 1
            if auto_paginate and next_page:
                self.logger.info(
                    "auto_paginating",
                    total_records=total,
                    first_page_count=len(documents),
                )

                # Follow next_page URLs until no more pages
                while next_page:
                    # Extract the full URL from next_page
                    page_response = await self.http_client.post(
                        path=next_page,
                        headers=query_headers,
                        data={},  # Query already in URL
                    )

                    page_data = page_response.get("data", [])
                    documents.extend(page_data)
                    pages_fetched += 1

                    # Get next page URL
                    next_page = page_response.get("next_page")

                    self.logger.debug(
                        "page_fetched",
                        page=pages_fetched,
                        records=len(page_data),
                        total_so_far=len(documents),
                    )

            self.logger.info(
                "documents_queried",
                count=len(documents),
                total_available=total,
                pages_fetched=pages_fetched,
                auto_paginate=auto_paginate,
            )

            return ToolResult(
                success=True,
                data={
                    "documents": documents,
                    "count": len(documents),
                    "total": total,
                    "query": query,
                    "pagination": {
                        "pagesize": pagesize,
                        "pages_fetched": pages_fetched,
                        "total_available": total,
                        "is_complete": auto_paginate or len(documents) >= total,
                    },
                },
                metadata={
                    "query_type": "vql" if vql else "filters",
                    "auto_paginate": auto_paginate,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to query documents: {e.message}",
                metadata={"error_code": e.error_code},
            )

    def _build_document_query(
        self,
        name_contains: Optional[str] = None,
        document_type: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> str:
        """Build VQL query from filter parameters."""
        where_clauses = []

        if name_contains:
            where_clauses.append(f"name__v CONTAINS ('{name_contains}')")
        if document_type:
            where_clauses.append(f"type__v = '{document_type}'")
        if lifecycle_state:
            where_clauses.append(f"state__v = '{lifecycle_state}'")
        if status:
            where_clauses.append(f"status__v = '{status}'")

        where_clause = " AND ".join(where_clauses) if where_clauses else "id > 0"

        query = f"SELECT id, name__v, type__v, subtype__v, classification__v, lifecycle__v, state__v, status__v FROM documents WHERE {where_clause} LIMIT {limit}"

        return query


class DocumentsGetTool(BaseTool):
    """Get detailed information about a specific document."""

    @property
    def name(self) -> str:
        return "vault_documents_get"

    @property
    def description(self) -> str:
        return """Get complete details for a specific Veeva Vault document by ID.

Returns:
- Document metadata (name, type, classification)
- Lifecycle state and version
- Custom fields
- Document properties

Use after documents_query to get full details."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
                "major_version": {
                    "type": "integer",
                    "description": "Major version number (optional, latest if not specified)",
                },
                "minor_version": {
                    "type": "integer",
                    "description": "Minor version number (optional, latest if not specified)",
                },
            },
            "required": ["document_id"],
        }

    async def execute(
        self,
        document_id: int,
        major_version: Optional[int] = None,
        minor_version: Optional[int] = None,
    ) -> ToolResult:
        """Execute document retrieval."""
        try:
            headers = await self._get_auth_headers()

            # Build path with version if specified
            if major_version is not None and minor_version is not None:
                path = self._build_api_path(
                    f"/documents/{document_id}/versions/{major_version}/{minor_version}"
                )
            else:
                path = self._build_api_path(f"/documents/{document_id}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            document_data = response.get("document", response.get("data", {}))

            self.logger.info(
                "document_retrieved",
                document_id=document_id,
                version=f"{major_version}.{minor_version}" if major_version else "latest",
            )

            return ToolResult(
                success=True,
                data=document_data,
                metadata={
                    "document_id": document_id,
                    "version_requested": f"{major_version}.{minor_version}"
                    if major_version
                    else "latest",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsCreateTool(BaseTool):
    """Create a new document in Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_documents_create"

    @property
    def description(self) -> str:
        return """Create a new document in Veeva Vault.

Required fields:
- name: Document name
- type: Document type (e.g., 'protocol__c')
- lifecycle: Lifecycle to use
- title: Document title

Optional fields:
- subtype, classification, study, product
- Any custom fields

Returns the created document ID."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Document name (unique identifier)",
                },
                "type": {
                    "type": "string",
                    "description": "Document type (e.g., 'protocol__c', 'general_document__c')",
                },
                "subtype": {
                    "type": "string",
                    "description": "Document subtype (optional)",
                },
                "classification": {
                    "type": "string",
                    "description": "Document classification (optional)",
                },
                "lifecycle": {
                    "type": "string",
                    "description": "Lifecycle to use",
                },
                "title": {
                    "type": "string",
                    "description": "Document title",
                },
                "product": {
                    "type": "string",
                    "description": "Product name or ID (optional)",
                },
                "study": {
                    "type": "string",
                    "description": "Study number or ID (optional)",
                },
            },
            "required": ["name", "type", "lifecycle", "title"],
        }

    async def execute(
        self,
        name: str,
        type: str,
        lifecycle: str,
        title: str,
        subtype: Optional[str] = None,
        classification: Optional[str] = None,
        product: Optional[str] = None,
        study: Optional[str] = None,
    ) -> ToolResult:
        """Execute document creation."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/documents")

            # Build document data
            doc_data = {
                "name__v": name,
                "type__v": type,
                "lifecycle__v": lifecycle,
                "title__v": title,
            }

            if subtype:
                doc_data["subtype__v"] = subtype
            if classification:
                doc_data["classification__v"] = classification
            if product:
                doc_data["product__v"] = product
            if study:
                doc_data["study__v"] = study

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=doc_data,
            )

            document_id = response.get("data", {}).get("id")

            self.logger.info(
                "document_created",
                document_id=document_id,
                name=name,
                type=type,
            )

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "name": name,
                    "type": type,
                    "lifecycle": lifecycle,
                },
                metadata={"document_id": document_id, "operation": "create"},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to create document: {e.message}",
                metadata={"error_code": e.error_code},
            )


class DocumentsUpdateTool(BaseTool):
    """Update an existing document's metadata."""

    @property
    def name(self) -> str:
        return "vault_documents_update"

    @property
    def description(self) -> str:
        return """Update metadata for an existing Veeva Vault document.

Can update:
- Title, description
- Product, study
- Custom fields
- Classification

Note: Document must be in an editable state."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID to update",
                },
                "title": {
                    "type": "string",
                    "description": "New document title",
                },
                "description": {
                    "type": "string",
                    "description": "New description",
                },
                "product": {
                    "type": "string",
                    "description": "Product name or ID",
                },
                "study": {
                    "type": "string",
                    "description": "Study number or ID",
                },
                "classification": {
                    "type": "string",
                    "description": "New classification",
                },
            },
            "required": ["document_id"],
        }

    async def execute(
        self,
        document_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        product: Optional[str] = None,
        study: Optional[str] = None,
        classification: Optional[str] = None,
    ) -> ToolResult:
        """Execute document update."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}")

            # Build update data
            update_data = {}
            if title:
                update_data["title__v"] = title
            if description:
                update_data["description__v"] = description
            if product:
                update_data["product__v"] = product
            if study:
                update_data["study__v"] = study
            if classification:
                update_data["classification__v"] = classification

            if not update_data:
                return ToolResult(
                    success=False,
                    error="No fields provided for update",
                    metadata={"document_id": document_id},
                )

            response = await self.http_client.put(
                path=path,
                headers=headers,
                json=update_data,
            )

            self.logger.info(
                "document_updated",
                document_id=document_id,
                fields_updated=list(update_data.keys()),
            )

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "updated_fields": list(update_data.keys()),
                },
                metadata={
                    "document_id": document_id,
                    "operation": "update",
                    "fields_updated": len(update_data),
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to update document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsDeleteTool(BaseTool):
    """Delete a document from Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_documents_delete"

    @property
    def description(self) -> str:
        return """Delete a document from Veeva Vault.

WARNING: This permanently deletes the document!
Document must be in a state that allows deletion.

Use with caution."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID to delete",
                },
            },
            "required": ["document_id"],
        }

    async def execute(self, document_id: int) -> ToolResult:
        """Execute document deletion."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}")

            response = await self.http_client.delete(
                path=path,
                headers=headers,
            )

            self.logger.info("document_deleted", document_id=document_id)

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "deleted": True,
                },
                metadata={"document_id": document_id, "operation": "delete"},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to delete document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsLockTool(BaseTool):
    """Lock a document for editing."""

    @property
    def name(self) -> str:
        return "vault_documents_lock"

    @property
    def description(self) -> str:
        return """Lock a Veeva Vault document for editing.

Prevents other users from editing while you work on it.
Must unlock when done or document remains locked to you."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID to lock",
                },
            },
            "required": ["document_id"],
        }

    async def execute(self, document_id: int) -> ToolResult:
        """Execute document lock."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}/lock")

            response = await self.http_client.post(
                path=path,
                headers=headers,
            )

            self.logger.info("document_locked", document_id=document_id)

            return ToolResult(
                success=True,
                data={"document_id": document_id, "locked": True},
                metadata={"document_id": document_id, "operation": "lock"},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to lock document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsUnlockTool(BaseTool):
    """Unlock a document after editing."""

    @property
    def name(self) -> str:
        return "vault_documents_unlock"

    @property
    def description(self) -> str:
        return """Unlock a Veeva Vault document after editing.

Allows other users to edit the document.
Use after completing edits on a locked document."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID to unlock",
                },
            },
            "required": ["document_id"],
        }

    async def execute(self, document_id: int) -> ToolResult:
        """Execute document unlock."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}/lock")

            response = await self.http_client.delete(
                path=path,
                headers=headers,
            )

            self.logger.info("document_unlocked", document_id=document_id)

            return ToolResult(
                success=True,
                data={"document_id": document_id, "unlocked": True},
                metadata={"document_id": document_id, "operation": "unlock"},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to unlock document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsDownloadFileTool(BaseTool):
    """Download the source file from a document."""

    @property
    def name(self) -> str:
        return "vault_documents_download_file"

    @property
    def description(self) -> str:
        return """Download the source file from a Veeva Vault document.

Downloads the actual file content (PDF, Word, Excel, etc.) from a document.
Returns file metadata and download information.

Use this to:
- Download document files for review
- Extract document content for processing
- Archive document files locally
- Verify document file integrity

Note: Returns file metadata. Actual file download happens via returned URL."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
                "save_path": {
                    "type": "string",
                    "description": "Optional local path to save file",
                },
            },
            "required": ["document_id"],
        }

    async def execute(
        self, document_id: int, save_path: Optional[str] = None
    ) -> ToolResult:
        """Execute document file download."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}/file")

            # Get file metadata first
            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            # Extract file information from response
            # Vault API returns file metadata and download URL
            file_info = {
                "document_id": document_id,
                "download_url": path,
                "response": response,
            }

            self.logger.info(
                "document_file_retrieved",
                document_id=document_id,
            )

            return ToolResult(
                success=True,
                data=file_info,
                metadata={
                    "document_id": document_id,
                    "operation": "download_file",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to download file for document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsDownloadVersionFileTool(BaseTool):
    """Download a specific version of a document file."""

    @property
    def name(self) -> str:
        return "vault_documents_download_version_file"

    @property
    def description(self) -> str:
        return """Download file from a specific document version.

Downloads the source file from a particular version of a document.
Useful for accessing historical versions of documents.

Returns file metadata and download information for the specified version."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
                "major_version": {
                    "type": "integer",
                    "description": "Major version number",
                },
                "minor_version": {
                    "type": "integer",
                    "description": "Minor version number",
                },
            },
            "required": ["document_id", "major_version", "minor_version"],
        }

    async def execute(
        self, document_id: int, major_version: int, minor_version: int
    ) -> ToolResult:
        """Execute version file download."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(
                f"/documents/{document_id}/versions/{major_version}/{minor_version}/file"
            )

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            file_info = {
                "document_id": document_id,
                "version": f"{major_version}.{minor_version}",
                "download_url": path,
                "response": response,
            }

            self.logger.info(
                "document_version_file_retrieved",
                document_id=document_id,
                version=f"{major_version}.{minor_version}",
            )

            return ToolResult(
                success=True,
                data=file_info,
                metadata={
                    "document_id": document_id,
                    "version": f"{major_version}.{minor_version}",
                    "operation": "download_version_file",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to download file for document {document_id} version {major_version}.{minor_version}: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "document_id": document_id,
                    "version": f"{major_version}.{minor_version}",
                },
            )


class DocumentsBatchCreateTool(BaseTool):
    """Create multiple documents in a single API call."""

    @property
    def name(self) -> str:
        return "vault_documents_batch_create"

    @property
    def description(self) -> str:
        return """Create multiple Veeva Vault documents in a single operation.

Batch creation is 10-100x faster than creating documents individually.
Use this for:
- Bulk document imports
- Data migrations
- Mass document generation
- Efficient document creation workflows

Supports partial success - some documents may succeed while others fail.
Returns detailed results for each document."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "documents": {
                    "type": "array",
                    "description": "Array of document objects to create",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "lifecycle": {"type": "string"},
                            "title": {"type": "string"},
                            "subtype": {"type": "string"},
                            "classification": {"type": "string"},
                        },
                        "required": ["name", "type", "lifecycle", "title"],
                    },
                },
            },
            "required": ["documents"],
        }

    async def execute(self, documents: list[dict]) -> ToolResult:
        """Execute batch document creation."""
        try:
            headers = await self._get_auth_headers()
            headers["Content-Type"] = "application/json"
            path = self._build_api_path("/documents")

            # Convert document data to Vault API format
            vault_documents = []
            for doc in documents:
                vault_doc = {
                    "name__v": doc["name"],
                    "type__v": doc["type"],
                    "lifecycle__v": doc["lifecycle"],
                    "title__v": doc["title"],
                }
                if "subtype" in doc:
                    vault_doc["subtype__v"] = doc["subtype"]
                if "classification" in doc:
                    vault_doc["classification__v"] = doc["classification"]
                if "product" in doc:
                    vault_doc["product__v"] = doc["product"]
                if "study" in doc:
                    vault_doc["study__v"] = doc["study"]
                vault_documents.append(vault_doc)

            # Vault API expects array in JSON body
            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=vault_documents,
            )

            # Parse batch response
            results = response.get("data", [])
            success_count = sum(
                1 for r in results if r.get("responseStatus") == "SUCCESS"
            )
            failure_count = len(results) - success_count

            self.logger.info(
                "batch_documents_created",
                total=len(documents),
                successes=success_count,
                failures=failure_count,
            )

            return ToolResult(
                success=failure_count == 0,  # All must succeed
                data={
                    "total": len(documents),
                    "successes": success_count,
                    "failures": failure_count,
                    "results": results,
                },
                metadata={
                    "operation": "batch_create",
                    "batch_size": len(documents),
                    "success_rate": success_count / len(documents) if documents else 0,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Batch document creation failed: {e.message}",
                metadata={"error_code": e.error_code, "batch_size": len(documents)},
            )


class DocumentsBatchUpdateTool(BaseTool):
    """Update multiple documents in a single API call."""

    @property
    def name(self) -> str:
        return "vault_documents_batch_update"

    @property
    def description(self) -> str:
        return """Update multiple Veeva Vault documents in a single operation.

Batch updates are 10-100x faster than updating documents individually.
Use this for:
- Bulk metadata changes
- Mass status updates
- Efficient data synchronization
- Large-scale document management

Supports partial success - returns detailed results for each document."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "updates": {
                    "type": "array",
                    "description": "Array of document updates (id + fields)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "product": {"type": "string"},
                            "study": {"type": "string"},
                            "classification": {"type": "string"},
                        },
                        "required": ["id"],
                    },
                },
            },
            "required": ["updates"],
        }

    async def execute(self, updates: list[dict]) -> ToolResult:
        """Execute batch document update."""
        try:
            headers = await self._get_auth_headers()
            headers["Content-Type"] = "application/json"
            path = self._build_api_path("/documents")

            # Convert updates to Vault API format
            vault_updates = []
            for update in updates:
                vault_update = {"id": update["id"]}
                if "title" in update:
                    vault_update["title__v"] = update["title"]
                if "description" in update:
                    vault_update["description__v"] = update["description"]
                if "product" in update:
                    vault_update["product__v"] = update["product"]
                if "study" in update:
                    vault_update["study__v"] = update["study"]
                if "classification" in update:
                    vault_update["classification__v"] = update["classification"]
                vault_updates.append(vault_update)

            response = await self.http_client.put(
                path=path,
                headers=headers,
                json=vault_updates,
            )

            # Parse batch response
            results = response.get("data", [])
            success_count = sum(
                1 for r in results if r.get("responseStatus") == "SUCCESS"
            )
            failure_count = len(results) - success_count

            self.logger.info(
                "batch_documents_updated",
                total=len(updates),
                successes=success_count,
                failures=failure_count,
            )

            return ToolResult(
                success=failure_count == 0,
                data={
                    "total": len(updates),
                    "successes": success_count,
                    "failures": failure_count,
                    "results": results,
                },
                metadata={
                    "operation": "batch_update",
                    "batch_size": len(updates),
                    "success_rate": success_count / len(updates) if updates else 0,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Batch document update failed: {e.message}",
                metadata={"error_code": e.error_code, "batch_size": len(updates)},
            )


class DocumentsGetActionsTool(BaseTool):
    """Get available workflow actions for a document."""

    @property
    def name(self) -> str:
        return "vault_documents_get_actions"

    @property
    def description(self) -> str:
        return """Get available workflow/lifecycle actions for a document.

Returns list of actions that can be performed on the document:
- Workflow state changes
- Lifecycle state transitions
- User actions (Approve, Reject, etc.)

Use before executing actions to discover what's available."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
            },
            "required": ["document_id"],
        }

    async def execute(self, document_id: int) -> ToolResult:
        """Execute get actions."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}/actions")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            actions = response.get("lifecycle_actions__v", [])

            self.logger.info(
                "document_actions_retrieved",
                document_id=document_id,
                action_count=len(actions),
            )

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "actions": actions,
                    "count": len(actions),
                },
                metadata={"document_id": document_id},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get actions for document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class DocumentsExecuteActionTool(BaseTool):
    """Execute a workflow action on a document."""

    @property
    def name(self) -> str:
        return "vault_documents_execute_action"

    @property
    def description(self) -> str:
        return """Execute a workflow/lifecycle action on a document.

Common actions:
- Change state (e.g., Draft → Review → Approved)
- Assign reviewers
- Add signatures
- Update workflow

Use get_actions first to discover available actions."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
                "action_name": {
                    "type": "string",
                    "description": "Action name (from get_actions response)",
                },
                "action_data": {
                    "type": "object",
                    "description": "Action-specific parameters (optional)",
                    "additionalProperties": True,
                },
            },
            "required": ["document_id", "action_name"],
        }

    async def execute(
        self, document_id: int, action_name: str, action_data: Optional[dict] = None
    ) -> ToolResult:
        """Execute workflow action."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/documents/{document_id}/actions/{action_name}")

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=action_data or {},
            )

            self.logger.info(
                "document_action_executed",
                document_id=document_id,
                action_name=action_name,
            )

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "action_name": action_name,
                    "result": response,
                },
                metadata={
                    "document_id": document_id,
                    "action_name": action_name,
                    "operation": "workflow_action",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to execute action {action_name} on document {document_id}: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "document_id": document_id,
                    "action_name": action_name,
                },
            )
