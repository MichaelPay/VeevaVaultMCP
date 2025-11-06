import requests
from typing import Dict, Any, Optional, Union


class DomainService:
    """
    Service class for handling domain-related operations with Veeva Vault
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        :param client: An initialized VaultClient instance
        """
        self.client = client

    def retrieve_domains(self) -> Dict[str, Any]:
        """
        Allows non-domain admins to retrieve a list of all their domains, including the domain of the current Vault.
        This data can be used as a valid domain value when creating a sandbox Vault.

        Endpoint: GET /api/{version}/objects/domains

        Headers:
            - Content-Type: application/x-www-form-urlencoded
            - Accept: application/json (default) or application/xml

        Returns:
            dict: A dictionary containing the response with the following structure:
            {
                "responseStatus": "SUCCESS",
                "responseMessage": "Success",
                "domains": [
                    {
                        "name": "veepharm.com",
                        "type": "Production"
                    },
                    {
                        "name": "veepharm-sbx.com",
                        "type": "Sandbox"
                    }
                ]
            }
        """
        url = (
            f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/objects/domains"
        )

        headers = {
            "Authorization": self.client.sessionId,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def retrieve_domain_information(
        self, include_application: bool = False
    ) -> Dict[str, Any]:
        """
        Allows domain admins to retrieve a list of all Vaults present in their domain.

        Endpoint: GET /api/{version}/objects/domain

        Headers:
            - Content-Type: application/json
            - Accept: application/json (default) or application/xml

        Args:
            include_application (bool): If set to true, the response includes information about
                the Vault application type. Defaults to false.

        Returns:
            dict: A dictionary containing the response with the following structure:
            {
                "responseStatus": "SUCCESS",
                "responseMessage": "Success",
                "domain__v": {
                    "domain_name__v": "veepharm",
                    "domain_type__v": "testvaults",
                    "vaults__v": [
                        {
                            "id": "2000",
                            "vault_name__v": "PromoMats",
                            "vault_status__v": "Active",
                            "vault_application__v": "PromoMats",
                            "vault_family__v": {
                                "name__v": "commercial__v",
                                "label__v": "Commercial"
                            }
                        }
                    ]
                }
            }

        Response Details:
            - domain_name__v: The name of the domain containing the Vaults. This is unique to each
              customer and part of the DNS of each Vault.
            - domain_type__v: The type of domain (Production, Sandbox, Demo, or Test).
            - id: The system-managed numeric ID assigned to each Vault. This is the Vault ID (vault_id__v)
              required in some requests.
            - vault_name__v: The name of each Vault. This may be the same as the application or set
              to something unique.
            - vault_status__v: The current status of each Vault (Active or Inactive). Inactive Vaults
              are inaccessible.
            - vault_application__v: The application of each Vault (PromoMats, MedComms, eTMF, Quality Docs,
              Submissions, RIM Submissions, or Platform). This information only appears if the
              include_application query parameter is set to true.
            - vault_family__v: Contains information about the application family each Vault belongs to
              (Commercial, Clinical Operations, Regulatory, or Quality), such as name and label.
        """
        url = (
            f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/objects/domain"
        )

        headers = {
            "Authorization": self.client.sessionId,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        params = {"include_application": include_application}

        response = requests.get(url, headers=headers, params=params)
        return response.json()
