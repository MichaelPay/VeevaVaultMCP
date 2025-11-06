import pandas as pd
import re
import requests
import logging

logger = logging.getLogger(__name__)


class QueryService:
    """
    Service class for handling VQL (Vault Query Language) queries in Veeva Vault.

    This service provides methods to execute VQL queries against the Veeva Vault API,
    retrieve data, and handle pagination of results.
    """

    def __init__(self, client):
        """
        Initialize the QueryService with a VaultClient instance.

        Args:
            client: An authenticated VaultClient instance that provides
                   session information and Vault URL details.
        """
        self.client = client

    def query(self, query, describe_query=True, record_properties=None, facets=None):
        """
        Submit a VQL query with advanced options.

        This method provides access to all supported query parameters and headers
        in the Vault API.

        Args:
            query (str): A VQL statement of up to 50,000 characters specifying
                the object to query, the fields to retrieve, and any optional filters.
            describe_query (bool): Set to true to include static field metadata in the
                response for the data record. This includes object metadata (name, label)
                and field metadata (type, required, max_length, etc.).
            record_properties (str, optional): Include the record properties object in the
                response. Possible values are 'all', 'hidden', 'redacted', or 'weblink'.
                If set to 'all', includes ID, field properties, permissions, subquery
                properties, and field additional data for each record.
            facets (list, optional): A list of facetable field names to include in the
                response. The response will include counts of unique values for each field.

        Returns:
            dict: The JSON response containing:
                - responseStatus: Success/failure status
                - queryDescribe: Object and field metadata (if requested)
                - responseDetails: Pagination information (pagesize, pageoffset, size, total)
                - data: The query results as specified in the VQL query
                - facets: Facet information (if requested)
                - record_properties: Record property information (if requested)

        Raises:
            VaultQueryError: If the query fails
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/query"

        headers = {
            "Authorization": self.client.sessionId,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "X-VaultAPI-DescribeQuery": str(describe_query).lower(),
        }

        if record_properties:
            headers["X-VaultAPI-RecordProperties"] = record_properties

        if facets:
            headers["X-VaultAPI-Facets"] = ",".join(facets)

        data = {"q": query}

        response = requests.post(url, headers=headers, data=data).json()

        if response.get("responseStatus") == "FAILURE":
            logger.error(f"VQL query failed: {response}")
            # Import here to avoid circular imports
            from veevavault.exceptions import VaultQueryError
            raise VaultQueryError(f"Query failed: {response.get('errors', response)}")

        logger.debug(f"Query successful: {len(response.get('data', []))} records returned")
        return response

    def bulk_query(self, query):
        """
        Execute a VQL query and return the results as a pandas DataFrame with automatic pagination.

        This method automatically handles pagination by following next_page links and
        concatenates all pages into a single DataFrame.

        Args:
            query (str): VQL query string of up to 50,000 characters.
                If PAGESIZE is specified in the query, only the first page will be retrieved.

        Returns:
            DataFrame: A pandas DataFrame containing all records from all pages of query results.

        Raises:
            VaultQueryError: If the query fails
        """
        # Check if PAGESIZE is in the query
        page_count = None
        if re.search(r"(?i)PAGESIZE", query):
            page_size_match = re.search(r"(?i)PAGESIZE\s+(\d+)", query)
            if page_size_match:
                page_count = int(page_size_match.group(1))
                logger.info(
                    f"PAGESIZE {page_count} detected in query. Only retrieving first page."
                )
        else:
            # Default page size is 1000
            page_count = 1000

        # First page - use query for the initial request
        response = self.query(query, describe_query=True)

        if not response or response.get("responseStatus") == "FAILURE":
            logger.error(f"Bulk query failed: {response}")
            # Import here to avoid circular imports
            from veevavault.exceptions import VaultQueryError
            raise VaultQueryError(f"Bulk query failed: {response}")

        # Convert first page to DataFrame
        output = pd.DataFrame(response.get("data", []))

        # Handle pagination if needed
        try:
            if page_count is None:
                # If we have a paginated result with more pages, fetch them all
                while (
                    "next_page" in response["responseDetails"]
                    and response["responseDetails"]["next_page"]
                ):
                    # For pagination, we need to use the raw requests.get since query uses POST
                    headers = {
                        "X-VaultAPI-DescribeQuery": "true",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json",
                        "Authorization": self.client.sessionId,
                    }
                    response = requests.get(
                        response["responseDetails"]["next_page"], headers=headers
                    ).json()
                    output = pd.concat(
                        [output, pd.DataFrame(response["data"])], ignore_index=True
                    )
        except Exception as e:
            # If pagination fails for any reason, return what we have
            logger.warning(f"Pagination may be incomplete due to: {e}")

        return output
