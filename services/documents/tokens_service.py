from .base_service import BaseDocumentService


class DocumentTokensService(BaseDocumentService):
    """
    Service class for generating document access tokens in Veeva Vault.

    The Document Tokens API allows you to generate document access tokens needed by the
    external viewer to view documents outside of Vault. These tokens can be used to access
    documents through the external viewer without requiring Vault authentication.
    """

    def create_tokens(
        self,
        doc_ids,
        expiry_date_offset=None,
        download_option=None,
        channel=None,
        token_group=None,
        steady_state=None,
    ):
        """
        Generates document access tokens for external viewing.

        Args:
            doc_ids (list or str): Document IDs for which to generate tokens. Can be a list of IDs
                                  or a comma-separated string of IDs.
            expiry_date_offset (int, optional): Number of days after which the tokens will expire.
                                               If not specified, the tokens will expire after 10 years by default.
            download_option (str, optional): Controls what users can download when viewing the document.
                                           Valid values: 'PDF', 'source', 'both', or 'none'.
                                           If not specified, defaults to those set on each document.
            channel (str, optional): Website object record ID value that corresponds to the distribution
                                    channel where the document is being made available.
                                    If not specified, Vault will assume the request is for Approved Email.
            token_group (str, optional): Groups together generated tokens for multiple documents to display
                                        the documents in the same viewer. Accepts alphanumeric strings up to
                                        255 characters in length (with single consecutive underscores allowed).
                                        Documents will be ordered in the sidebar based on their order in doc_ids.
            steady_state (bool, optional): If True, generates tokens for the latest steady state version
                                          of a document. If False or omitted, generates tokens for the
                                          latest version regardless of state.

        Returns:
            dict: Response containing the generated tokens or error information for each document.
            Example:
            {
                "responseStatus": "SUCCESS",
                "tokens": [
                    {
                        "document_id__v": 101,
                        "token__v": "3003-cb6e5c3b-4df9-411c-abc2-6e7ae120ede7"
                    },
                    {
                        "document_id__v": 102,
                        "token__v": "3003-1174154c-ac8e-4eb9-b453-2855de273bec"
                    }
                ]
            }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/tokens"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # Prepare request data
        data = {}

        # Format doc_ids as comma-separated string if provided as a list
        if isinstance(doc_ids, list):
            data["docIds"] = ",".join(str(doc_id) for doc_id in doc_ids)
        else:
            data["docIds"] = doc_ids

        # Add optional parameters if provided
        if expiry_date_offset is not None:
            data["expiryDateOffset"] = expiry_date_offset

        if download_option is not None:
            data["downloadOption"] = download_option

        if channel is not None:
            data["channel"] = channel

        if token_group is not None:
            data["tokenGroup"] = token_group

        if steady_state is not None:
            data["steadyState"] = str(steady_state).lower()

        response = self.client.api_call(url, method="POST", headers=headers, data=data)

        return response
