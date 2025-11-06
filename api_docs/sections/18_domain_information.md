<!-- 
VaultAPIDocs Section: # Domain Information
Original Line Number: 32900
Generated: August 30, 2025
Part 18 of 38
-->

# Domain Information

The following endpoints allow Admins to retrieve information about the domain of the authenticated Vault and domains accessible to the authenticated user. Learn more about [Vault domains in Vault Help](https://platform.veevavault.help/en/lr/14691).

## Retrieve Domain Information

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/domain?include_application=true
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "domain__v": {
        "domain_name__v": "veepharm",
        "domain_type__v": "Test",
        "vaults__v": [
            {
                "id": 19523,
                "vault_name__v": "PromoMats",
                "vault_status__v": "Active",
                "vault_family__v": {
                    "name__v": "commercial__v",
                    "label__v": "Commercial"
                },
                "vault_application__v": [
                    {
                        "name": "pm_promomats__v",
                        "label": "PM: PromoMats"
                    },
                    {
                        "name": "pm_multichannel__v",
                        "label": "PM: Multichannel"
                    }
                ]
            }
        ]
    }
}
'''

Domain Admins can use this request to retrieve a list of all Vaults currently in their domain.

GET `/api/{version}/objects/domain`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`include_application`

To include Vault application type information in the response, set `include_application` to `true`. If omitted, defaults to `false` and application information is not included.

#### Response Details

Name

Description

`domain_name__v`

The name of the domain containing the Vaults. This is unique to each customer and part of the DNS of each Vault.

`domain_type__v`

The type of domain (Production, Sandbox, Demo, or Test).

`id`

The system-managed numeric ID assigned to each Vault. This is the **Vault ID** (`vault_id__v`) required in some requests.

`vault_name__v`

The name of each Vault. This may be the same as the application or set to something unique.

`vault_status__v`

The current status of each Vault (Active or Inactive). Inactive Vaults are inaccessible.

`vault_family__v`

Contains information about the application family each Vault belongs to.

`vault_application__v`

Contains information about the application of each Vault, such as `name` and `label`. This information only appears if the `include_application` query parameter is set to `true`.

## Retrieve Domains

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/objects/domains
'''

> Response

'''
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
'''

Non-domain Admins can use this request to retrieve a list of all their domains, including the domain of the current Vault. You can use this data as a valid `domain` value when [creating a sandbox Vault](#Create_Refresh_Sandbox).

GET `/api/{version}/objects/domains`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`
