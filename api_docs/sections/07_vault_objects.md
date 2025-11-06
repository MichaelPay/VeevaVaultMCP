<!-- 
VaultAPIDocs Section: # Vault Objects
Original Line Number: 17642
Generated: August 30, 2025
Part 7 of 38
-->

# Vault Objects

Each Vault is configured with a set of standard objects (`product__v`, `country__v`, `study__v`, etc.). These vary by application and configuration.

Vault is also configured with a set of system objects (`user__sys`, `person__sys`, `locale__sys`, etc.) These are available for all Vault applications and configurations.

Admins may also create custom objects (`region__c`, `agency__c`, `manufacturer__c`, etc.).

Each object can have multiple object records. For example, the `product__v` object may have records for products named `CholeCap`, `Nyaxa`, and `WonderDrug`. All object records are user-defined.

Vault API supports the retrieval of Vault object records and their metadata as well as creating, updating, and deleting object records. It does not support creating or updating Vault objects. This must be done by an Admin in the UI.

Learn about [Vault objects](https://platform.veevavault.help/en/lr/15298) in Vault Help.

## Retrieve Object Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects/product__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "object": {
        "available_lifecycles": [],
        "label_plural": "Products",
        "prefix": "00P",
        "data_store": "standard",
        "description": null,
        "enable_esignatures": false,
        "source": "standard",
        "allow_attachments": false,
        "relationships": [
            {
                "relationship_name": "product_family__vr",
                "relationship_label": "Product Family",
                "field": "product_family__v",
                "relationship_type": "reference_outbound",
                "localized_data": {
                    "relationship_label": {
                        "de": "Produktfamilie",
                        "ru": "Семейство продуктов",
                        "kr": "제품군",
                        "en": "Product Family",
                        "it": "Famiglia di prodotti",
                        "pt_BR": "Família de produtos",
                        "fr": "Famille de produits",
                        "hu": "Termékcsalád",
                        "es": "Familia de productos",
                        "zh": "产品系列",
                        "zh_TW": "產品系列",
                        "th": "ตระกูลผลิตภัณฑ์",
                        "ja": "製品ファミリー",
                        "pl": "Rodzina produktów",
                        "nl": "Productgroep",
                        "tr": "Ürün Ailesi",
                        "pt_PT": "Família do produto"
                    }
                },
                "relationship_deletion": "block",
                "object": {
                    "url": "/api/v25.2/metadata/vobjects/product_family__v",
                    "label": "Product Family",
                    "name": "product_family__v",
                    "label_plural": "Product Families",
                    "prefix": "V95",
                    "localized_data": {
                        "label_plural": {
                            "de": "Produktfamilien",
                            "ru": "Семейства продуктов",
                            "kr": "제품군",
                            "en": "Product Families",
                            "it": "Famiglie di prodotti",
                            "pt_BR": "Famílias de produtos",
                            "fr": "Familles de produits",
                            "hu": "Termékcsaládok",
                            "es": "Familias de productos",
                            "zh": "产品系列",
                            "zh_TW": "產品系列",
                            "th": "ตระกูลผลิตภัณฑ์",
                            "ja": "製品ファミリー",
                            "pl": "Rodziny produktów",
                            "nl": "Productfamilies",
                            "tr": "Ürün Aileleri",
                            "pt_PT": "Famílias de produto"
                        },
                        "label": {
                            "de": "Produktfamilie",
                            "ru": "Семейство продуктов",
                            "kr": "제품군",
                            "en": "Product Family",
                            "it": "Famiglia di prodotti",
                            "pt_BR": "Família de produtos",
                            "fr": "Famille de produits",
                            "hu": "Termékcsalád",
                            "es": "Familia de productos",
                            "zh": "产品系列",
                            "zh_TW": "產品系列",
                            "th": "ตระกูลผลิตภัณฑ์",
                            "ja": "製品ファミリー",
                            "pl": "Rodzina produktów",
                            "nl": "Productgroep",
                            "tr": "Ürün Ailesi",
                            "pt_PT": "Família do produto"
                        }
                    }
                }
            }
        ],
        "urls": {
          "field": "/api/v25.2/metadata/vobjects/product__v/fields/{name}",
          "record": "/api/v25.2/vobjects/product__v/{id}",
          "list": "/api/v25.2/vobjects/product__v",
          "metadata": "/api/v25.2/metadata/vobjects/product__v"
        },
        "role_overrides": false,
        "localized_data": {
            "label_plural": {
              "de": "Produkte",
              "ru": "Продукты",
              "sv": "Produkter",
              "kr": "제품",
              "en": "Products",
              "pt_BR": "Produtos",
              "it": "Prodotti",
              "fr": "Produits",
              "hu": "Termékek",
              "es": "Productos",
              "zh": "产品",
              "zh_TW": "產品",
              "ja": "製品",
              "pl": "Produkty",
              "tr": "Ürünler",
              "nl": "Producten",
              "pt_PT": "Produtos"
            },
            "label": {
              "de": "Produkt",
              "ru": "Продукт",
              "sv": "Produkt",
              "kr": "제품",
              "en": "Product",
              "pt_BR": "Produto",
              "it": "Prodotto",
              "fr": "Produit",
              "hu": "Termék",
              "es": "Producto",
              "zh": "产品",
              "zh_TW": "產品",
              "ja": "製品",
              "pl": "Produkt",
              "tr": "Ürün",
              "nl": "Product",
              "pt_PT": "Produto"
            }
        },
        "object_class": "base",
        "order": 12,
        "allow_types": false,
        "help_content": null,
        "in_menu": true,
        "label": "Product",
        "modified_date": "2020-12-23T04:00:21.000Z",
        "created_by": 1,
        "secure_audit_trail": false,
        "secure_sharing_settings": false,
        "dynamic_security": false,
        "auditable": true,
        "name": "product__v",
        "modified_by": 1,
        "user_role_setup_object": null,
        "secure_attachments": false,
        "prevent_record_overwrite": false,
        "created_date": "2020-05-26T10:19:27.000Z",
        "system_managed": false,
        "fields": [
            {
              "help_content": null,
              "editable": false,
              "lookup_relationship_name": null,
              "description": null,
              "label": "ID",
              "source": "standard",
              "type": "ID",
              "modified_date": "2020-05-26T10:19:27.000Z",
              "created_by": 1,
              "required": false,
              "no_copy": true,
              "localized_data": {
                "label": {
                  "de": "ID",
                  "ru": "Идентификатор",
                  "sv": "ID",
                  "kr": "ID",
                  "en": "ID",
                  "pt_BR": "ID",
                  "it": "ID",
                  "fr": "ID",
                  "hu": "Azonosító",
                  "es": "ID",
                  "zh": "ID",
                  "zh_TW": "識別碼",
                  "ja": "ID",
                  "pl": "Identyfikator",
                  "tr": "Kimlik",
                  "nl": "ID",
                  "pt_PT": "ID"
                }
              },
              "name": "id",
              "list_column": false,
              "modified_by": 1,
              "facetable": false,
              "created_date": "2020-05-26T10:19:27.000Z",
              "lookup_source_field": null,
              "status": [
                "active__v"
              ],
              "order": 0
            }
          ],
          "status": [
            "active__v"
          ],
          "default_obj_type": "base__v"
  }
}
'''

Retrieve all metadata configured on a standard or custom Vault Object.

GET `/api/{version}/metadata/vobjects/{object_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. For example, `product__v`, `country__v`, `custom_object__c`.

#### Query Parameters

Name

Description

`loc`

Set to `true` to retrieve the `localized_data` array, which contains the localized (translated) strings for the `label` and `label_plural` object fields. If omitted, defaults to `false` and localized Strings are not included.

#### Response Details

The response includes all metadata configured on the object, such as:

Name

Description

`in_menu`

When `true`, the object appears in the Vault UI’s _Business Admin_. When configuring objects in the UI, this is the _Display in Business Admin_ setting.

`source`

The source of this object. For example, `standard` objects are Veeva-supplied objects, and `custom` objects are objects created by your organization.

`created_by`

The user ID of the user who created this object. Standard objects are created by System, which is user ID `1`.

`fields`

An array of the fields available on this object. You can [Retrieve Object Field Metadata](#Retrieve_Object_Field_Metadata) with a field’s `name` value.

`facetable`

When `true`, the object is available for use as a faceted filter in the Vault UI.Learn more about [faceted filters in Vault Help](https://platform.veevavault.help/en/lr/1616).

## Retrieve Object Field Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects/product__v/fields/name__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "field": {
        "lookup_relationship_name": null,
        "description": "Do not remove from layout.",
        "start_number": null,
        "source": "standard",
        "type": "String",
        "required": true,
        "list_column": true,
        "facetable": false,
        "format_mask": null,
        "max_length": 128,
        "order": 1,
        "help_content": "The primary name of the product as you wish to see it referenced throughout the system; this may be a brand name or a generic name, but will be visible globally.",
        "editable": true,
        "label": "Product Name",
        "modified_date": "2024-05-15T21:20:44.000Z",
        "created_by": 1,
        "no_copy": false,
        "encrypted": false,
        "system_managed_name": false,
        "value_format": null,
        "unique": true,
        "name": "name__v",
        "modified_by": 133999,
        "created_date": "2023-01-20T19:05:46.000Z",
        "sequential_naming": false,
        "lookup_source_field": null,
        "status": [
            "active__v"
        ]
    }
}
'''

GET `/api/{version}/metadata/vobjects/{object_name}/fields/{object_field_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_field_name}`

The object field `name` value (`id`, `name__v`, `external_id__v`, etc.).

#### Query Parameters

Name

Description

`loc`

Set to `true` to retrieve the `localized_data` array, which contains the localized (translated) strings for the `label` and `label_plural` object fields. If omitted, defaults to `false` and localized Strings are not included.

#### Response Details

The response lists all metadata configured on the specified Vault object field. Note the following field metadata:

Metadata Field

Description

`required`

When `true`, the field value must be set when creating new object records.

`editable`

When `true`, the field value can be defined by the currently authenticated user. When `false`, the field value is read-only or system-managed.

`no_copy`

When `true`, field values are not copied when using the **Make a Copy** action.

`facetable`

When `true`, the field is available for use as a faceted filter in the Vault UI. Learn more about [faceted filters in Vault Help](https://platform.veevavault.help/en/lr/1616).

`searchable`

Boolean indicating the lookup field is searchable. When `true`, the field is available for filtering and ordering with VQL and in the Vault UI. Only applies to lookup fields. Learn more about [lookup fields on Vault Help](https://platform.veevavault.help/en/lr/34072).

`format_mask`

The format mask expression if it exists on the field. Learn more about format masks in [Vault Help](https://platform.veevavault.help/en/lr/15057#Format_Masks).

`rollup`

When `true`, this field is a Roll-up field, and the response includes related metadata such as `rollup_function` and `rollup_relationship_name`. Learn more about [Roll-up fields in Vault Help](https://platform.veevavault.help/en/lr/15057/#roll-up-fields).

## Retrieve Object Collection

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects?loc=true
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "objects": [
{
           "url": "/api/v25.2/metadata/vobjects/user__sys",
           "label": "User",
           "name": "user__sys",
           "label_plural": "Users",
           "prefix": "V0A",
           "order": 87,
           "in_menu": true,
           "source": "system",
           "status": [
               "active__v"
           ],
           "configuration_state": "STEADY_STATE",
           "localized_data": {
               "label_plural": {
                   "de": "Benutzer",
                   "ru": "Пользователи",
                   "sv": "Användare",
                   "kr": "사용자",
                   "en": "Users",
                   "pt_BR": "Usuários",
                   "it": "Utenti",
                   "fr": "Utilisateurs",
                   "hu": "Felhasználók",
                   "es": "Usuarios",
                   "zh": "用户",
                   "zh_TW": "使用者",
                   "th": "ผู้ใช้",
                   "ja": "ユーザ",
                   "pl": "Użytkownicy",
                   "tr": "Kullanıcılar",
                   "nl": "Gebruikers",
                   "pt_PT": "Utilizadores"
               },
               "label": {
                   "de": "Benutzer",
                   "ru": "Пользователь",
                   "sv": "Användare",
                   "kr": "사용자",
                   "en": "User",
                   "pt_BR": "Usuário",
                   "it": "Utente",
                   "fr": "Utilisateur",
                   "hu": "Felhasználó",
                   "es": "Usuario",
                   "zh": "用户",
                   "zh_TW": "使用者",
                   "th": "ผู้ใช้",
                   "ja": "ユーザ",
                   "pl": "Użytkownik",
                   "tr": "Kullanıcı",
                   "nl": "Gebruiker",
                   "pt_PT": "Utilizador"
               }
           }
       },
{
           "url": "/api/v25.2/metadata/vobjects/country__v",
           "label": "Country",
           "name": "country__v",
           "label_plural": "Countries",
           "prefix": "00C",
           "in_menu": true,
           "source": "standard",
           "status": [
               "active__v"
           ],
           "configuration_state": "STEADY_STATE",
           "localized_data": {
               "label_plural": {
                   "de": "Länder",
                   "ru": "Страны",
                   "sv": "Länder",
                   "kr": "국가",
                   "en": "Countries",
                   "it": "Paesi",
                   "pt_BR": "Países",
                   "fr": "Pays",
                   "hu": "Országok",
                   "es": "Países",
                   "zh": "国家/地区",
                   "zh_TW": "國家/地區",
                   "th": "ประเทศ",
                   "ja": "国",
                   "pl": "Kraje",
                   "tr": "Ülkeler",
                   "nl": "Landen",
                   "pt_PT": "Países"
               },
               "label": {
                   "de": "Land",
                   "ru": "Страна",
                   "sv": "Land",
                   "kr": "국가",
                   "en": "Country",
                   "it": "Paese",
                   "pt_BR": "País",
                   "fr": "Pays",
                   "hu": "Ország",
                   "es": "País",
                   "zh": "国家/地区",
                   "zh_TW": "國家/地區",
                   "th": "ประเทศ",
                   "ja": "国",
                   "pl": "Kraj",
                   "tr": "Ülke",
                   "nl": "Land",
                   "pt_PT": "País"
               }
           }
       }
     ]
   }
'''

Retrieve all Vault objects in the authenticated Vault.

GET `/api/{version}/metadata/vobjects`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`loc`

Set to `true` to retrieve localized (translated) strings for the `label` and `label_plural` object fields. If omitted, defaults to `false` and localized Strings are not included.

#### Response Details

The response includes a summary of key information (`url`, `label`, `name`, `prefix`, `status`, etc.) for all standard and custom Vault Objects configured in your Vault.

Name

Description

`localized_data`

When `loc=true`, this array contains translated field labels for each object. This data is only available at the object and field level, and only if localized Strings have been configured on objects in your Vault.

`configuration_state`

The configuration state of your raw object.

-   `STEADY_STATE`: This object has no pending configuration changes.
-   `IN_DEPLOYMENT`: This object has queued or in-progress configuration changes. While in this state, Vault Admins cannot make further edits to the object configuration, and Vault users continue to interact with the _Active_ object configuration version. In this state, you may also [cancel](#Cancel_HVO) deployment.

## Retrieve Object Records

> Request

'''
curl -L 'myvault.veevavault.com/api/v25.2/query' \
--header 'Authorization: {SESSION_ID}' \
--header 'Accept: application/json' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'q=SELECT id, name__v FROM product__v'
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "pagesize": 1000,
        "pageoffset": 0,
        "size": 26,
        "total": 26
    },
    "data": [
        {
            "id": "00P000000000101",
            "name__v": "WonderDrug"
        },
        {
            "id": "00P000000000102",
            "name__v": "VeevaProm XR"
        },
        {
            "id": "00P000000000201",
            "name__v": "VeevaProm"
        },
        {
            "id": "00P000000000202",
            "name__v": "Cholecap"
        },
        {
            "id": "00P000000000301",
            "name__v": "Restolar"
        },
        {
            "id": "00P000000000303",
            "name__v": "Felinsulin"
        },
        {
            "id": "00P000000000306",
            "name__v": "Labrinone"
        },
        {
            "id": "00P000000000601",
            "name__v": "Nyaxa"
        },
        {
            "id": "00P000000000602",
            "name__v": "Gludacta"
        },
        {
            "id": "00P00000000H002",
            "name__v": "CholeCap"
        }
    ]
}
'''

To retrieve all records for a specific Vault object, use [VQL](#Vault_Query_Language) or the [Direct Data API](/directdata).

For example, the following VQL query will retrieve all records for a specific object:

POST `/api/{version}/query`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. For example,`product__v`, `country__v`, `custom_object__c`.

#### Body Parameters

Name

Description

`q`

`SELECT id, name__v FROM {object_name}` where `{object_name}` is the `name__v` field value of the object to retrieve records.

## Retrieve Object Record

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/0PR0202
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseDetails": {
    "url": "/api/v25.2/vobjects/product__v/00PR0202",
    "object": {
      "url": "/api/v25.2/metadata/vobjects/product__v",
      "label": "Product",
      "name": "product__v",
      "label_plural": "Products",
      "prefix": "00P"
    }
  },
  "data": {
    "external_id__v": "CHO-457",
    "product_family__c": [
      "cholepriol__c"
    ],
    "compound_id__c": "CHO-55214",
    "abbreviation__c": "CHO",
    "therapeutic_area__c": [
      "endocrinology__c"
    ],
    "name__v": "CholeCap",
    "modified_by__v": 12022,
    "modified_date__v": "2016-05-10T21:06:11.000Z",
    "inn__c": null,
    "created_date__v": "2015-07-30T20:55:16.000Z",
    "id": "00PR0202",
    "internal_name__c": null,
    "generic_name__c": "cholepridol phosphate",
    "status__v": [
      "active__v"
    ],
    "created_by__v": 1
  },
  "manually_assigned_sharing_roles": {
    "owner__v": {
      "groups": null,
      "users": [
        12022
      ]
    },
    "viewer__v": {
      "groups": [
        3311303
      ],
      "users": [
        35551,
        48948,
        55002
      ]
    },
    "editor__v": {
      "groups": [
        4411606
      ],
      "users": [
        60145,
        70012,
        89546
      ]
    }
  }
}
'''

Retrieve metadata configured on a specific object record in your Vault.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

#### Response Details

On `SUCCESS`, the response lists all fields and values configured on the object record.

When Custom Sharing Rules have been enabled on the object (`"dynamic_security": true`), the response includes the following additional information:

`manually_assigned_sharing_roles`

-   `owner__v`
-   `viewer__v`
-   `editor__v`

These are the users and groups that have been manually assigned to each role on the object record.

Not all object records will have users and groups assigned to roles. You can update object records to add or remove users and/or groups on each role.

## Create & Upsert Object Records

> Request: Create Object Records

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Object Records\create_object_records.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v
'''

> Response: Create Object Records

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "0PR0771",
                "url": "api/v8.0/vobjects/product__v/0PR0771",
                "event": "created__sys"
            }
        },
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "0PR0772",
                "url": "api/v8.0/vobjects/product__v/0PR0772",
                "event": "created__sys"
            }
        },
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "0PR0773",
                "url": "api/v8.0/vobjects/product__v/0PR0773",
                "event": "created__sys"
            }
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this object record was not created."
                }
            ]
        }
    ]
}
'''

> Request: Upsert Object Records

'''
$ curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Object Records\upsert_object_records.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v?idParam=id
'''

> Response: Upsert Object Records

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "data":{
            "id":"00P00000000M001",
            "url":"/api/v25.2/vobjects/product__v/00P00000000M001",
            "event":"updated__sys",
            "id_param_value":"00P00000000M001"
         }
      },
      {
         "responseStatus":"SUCCESS",
         "data":{
            "id":"00P000000000C01",
            "url":"/api/v25.2/vobjects/product__v/00P000000000C01",
            "event":"updated__sys",
            "id_param_value":"00P000000000C01"
         }
      },
      {
         "responseStatus":"FAILURE",
         "data":{
            "id_param_value":"00P000000000C02"
         },
         "errors":[
            {
               "type":"INVALID_DATA",
               "message":"Invalid id"
            }
         ]
      }
   ]
}
'''

Create or [upsert](#Query_String_Parameters_Upsert_Object_Records) Vault object records in bulk.

You can use this endpoint to create User Tasks or User (`user__sys`) records. Learn more about [User Tasks](https://platform.veevavault.help/en/lr/40757) and the [User & Person Objects](https://platform.veevavault.help/en/lr/46534) in Vault Help.

-   The maximum input file size is 50 MB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   Vault removes XML characters that fall outside of the [character range](https://www.w3.org/TR/xml/#charsets) from the request body.
-   The maximum batch size is 500.

You can only add [relationships on object fields](#Add_Relationships_on_Object_Fields) using ID values or based on a unique field on the target object. This API does not support [object lookup fields](/vql/#Object_Lookup_Fields).

If a `raw` object record encounters a [uniqueness constraint error](https://platform.veevavault.help/en/lr/28740/#defining-uniqueness-in-relationship-objects), the entire batch fails. A `raw` object is a Vault object where the `data_store` attribute is set to `raw`.

POST `/api/{version}/vobjects/{object_name}`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

If set to `true`, Vault allows you to create or update object records in a noninitial state and with minimal validation, create inactive records, and set standard and system-managed fields such as `created_by__v`. Does not bypass record triggers. You must have the Record Migration permission to use this header. Learn more about [Record Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/761685).

`X-VaultAPI-NoTriggers`

If set to `true` and Record Migration Mode is enabled, it bypasses all system, standard, custom SDK triggers, and Action Triggers. Before using this parameter, learn more about [bypassing triggers](https://platform.veevavault.help/en/lr/761685#no-triggers).

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object, for example, `product__v`.

#### Body Parameters

Upload parameters as a JSON or CSV file. The following shows the required standard fields, but an Admin may set other standard or custom object fields as required in your Vault.

If an object has a field default configured, the value you use for that field overrides the default. Learn more about the [order of operations for field defaults in Vault Help](https://platform.veevavault.help/en/lr/42778/#order-of-operations-for-object-field-defaults).

Name

Description

`name__v`required

This field is required unless it is set to system-managed. To find out if an object uses system-managed naming, retrieve its `name__v` field and look for the `system_managed_name` property set to `true` or `false`. Learn more about system-managed naming in [Vault Help](https://platform.veevavault.help/en/lr/30986).

`object_type__v`optional

To create objects of a specific object type, add this field with the `id` of the object type. Requests may include either `object_type__v` or `object_type__v.api_name__v`, but not both.

`object_type__v.api_name__v`optional

To create objects of a specific object type, add this field with the `name` of the object type. Requests may include either `object_type__v` or `object_type__v.api_name__v`, but not both.

`source_record_id`optional

To copy an existing object record, add this field with the `id` of the existing object record. Any values specified for other fields will override the copied values. To perform a deep (hierarchical) copy of a record, see the [Deep Copy](#Deep_Copy_Object_Record) endpoint.

`{field_name}`optional

The name of the object field for which to specify a value. Use the [Object Metadata API](#Retrieve_Object_Metadata) to retrieve all fields configured on objects. You can specify a value for any field with `editable: true`.

`state__v`optional

Specifies the lifecycle state of the record when `X-VaultAPI-MigrationMode` is set to `true`. For example, `draft_state__c`.

`state_label`optional

Specifies the lifecycle state type of the record when `X-VaultAPI-MigrationMode` is set to `true`. Use the format `base:object_lifecycle:` followed by the object state type. For example, `base:object_lifecycle:initial_state_type`. When providing both a state and state type, the `state_label` value must map to the provided `state__v` value. For example, if the `state__v` value is set to `draft_state__c`, the `state_label` value must already be set to draft in the destination Vault.

#### Add Relationships on Object Fields

Many object records have relationships with other object records. For example, the object record details for the _Marketing Campaign_ “CholeCap Campaign” references its parent “CholeCap” _Product_ record. When creating or upserting object records, there are instances where an object field in your input file indicates an object relationship. The API supports the use of reference relationships and parent-child relationships within fields, but not lookup fields. To refer to object relationships in an object field, set the column header in the input file to be a combination of the relationship name and a unique object field, such as `name__v`. For example, `product__vr.name__v` references the name of the related _Product_ record.

#### Create Link Target Records

In PromoMats Vaults, it may sometimes be necessary to create _Claim_ (`annotation_keywords__sys`) records with valid references to anchor annotations (`annotation_types=anchor__sys`). The _Link Target_ (`link_target__sys`) object establishes relationships to documents, anchors, and permalinks and is not visible by default to users in the UI. The API allows you to create _Link Target_ records that reference anchor annotations by providing the annotation ID of the targeted anchor and the corresponding document version ID in the body of a request. Vault then auto-populates the following anchor-related fields on the _Link Target_ record based on the annotation ID provided:

-   _Anchor Id_ (`anchor_id__sys`)
-   _Anchor Title_ (`anchor_title__sys`)
-   _Anchor Page_ (`anchor_page__sys`)
-   _Reference_ (`target__sys`)

The response returns an error if the provided annotation ID does not exist in the authenticated Vault or does not match the provided document version.

##### Body Parameters

Provide the following fields in your input file to create `link_target__sys` records:

Name

Description

`annotation_id__sys`required

The annotation’s ID. Retrieve this value from the `id__ sys` returned from the [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type) request.

`suggestedlink_link_target_type__v`required

The suggested link target type. For example, `anchor__v`.

`document_version_id__v`required

The ID and version number of the document where the annotation appears, in the format `{documentId}_{majorVersion}_{minorVersion}`. For example, `138_2_1`.

#### Add Attachment Fields

To specify a value for an _Attachment_ field, provide the file path on file staging.

The maximum allowed file size for _Attachment_ fields is 100 MB.

#### Upsert Object Records

Upsert is a combination of create and update. With `idParam`, you can identify an object record by any unique object field. This allows you to use one input file to create new object records and update existing records at the same time. If a matching record exists, Vault updates the record with the unique field values specified in the input. If no matching object record exists, Vault creates a new record using the values in the input.

Upsert expects unique `idParam` field values in the request and providing duplicate values will result in a `FAILURE` for the entire batch.

To upsert records in a specific state or state type, use the [Migration Mode](#X-VaultAPI-MigrationMode_header) header. To set or change a record’s object type, include `object_type__v` in the body of the request and use the `X-VaultAPI-MigrationMode` header. Without Migration Mode enabled, update operations for individual records that indicate `object_type__v` will fail. Records can indicate `object_type__v` if the provided value matches the existing value in Vault.

##### Query String Parameters

Name

Description

`idParam`

To upsert object records, add `idParam={field_name}` to the request endpoint. For example, `idParam=external_id__v`. You can use any object field which has `unique` set to `true` in the object metadata. For example, `idParam=external_id__v`.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-object-records.json)

Admin may set other standard or custom object fields to required. Use the Object Metadata API to retrieve all fields configured on objects. You can add any object field with `editable: true`.

Vault does not update records and includes a `responseStatus` of `WARNING` for operations that result in saving a record without making any changes. Learn more about record changes that result in no operation ([no-ops](#No_Ops)).

#### Create User Object Records

To create `user__sys` records, your input file must have all required fields on `user__sys`. You can choose to create new users in pending state and defer welcome emails by setting `activation_date__sys` to a future date.

Use the [Retrieve Object Metadata](#Retrieve_Object_Metadata) endpoint on `user__sys` to retrieve a full list of fields.

This API does not support the following:

-   Creating cross-domain users. To create cross-domain users, use the [Create Single User](#Create_Single_User) endpoint.
-   Adding users to a domain without assigning them to a Vault. To add users to a domain only, use the [Create Single User](#Create_Single_User) endpoint.
-   Adding VeevaID users. To add VeevaID users, use the [Create Single User](#Create_Single_User) endpoint.
-   Changing user passwords.

##### Body Parameters

Provide the following fields in your input file to create `user__sys` records:

Name

Description

`email__sys`required

The user’s email address. For example, `ewoodhouse@email.com` An email address is required to prevent adding duplicate users in error. For example, users John and Jane Smith may both use “jsmith” as a user name. An email address ensures adding the correct user.

`first_name__sys`required

The user’s first name.

`last_name__sys`required

The user’s last name.

`username__sys`required

The user’s Vault user name (login credential). `username__sys` is a multi-part field. To set the user name, provide the entire value. For example, `ewoodhouse@veepharm.com`.

`language__sys`required

The user’s preferred language.

`locale__sys`required

The user’s location.

`timezone__sys`required

The user’s time zone.

`license_type__sys`optional

The user’s license type. If omitted, the default value is `full__v`. If your Vault utilizes user-based licensing, assign application licensing using the fields starting with `license_` on the _User_ (`user__sys`) object obtained from the [Retrieve Object Metadata](#Retrieve_Object_Metadata) endpoint. For example, `license_qualityqdocs__sys` indicates the QualityDocs application license.

`security_profile__sys`required

The user’s security profile.

`status__v`optional

The status of the user.

`source_person_id__v`optional

The person record to be associated with this user. This field is only available in Clinical Operations Vaults. See [Managing the Person & Organization Objects](https://clinical.veevavault.help/en/lr/31637) for more information.

`activation_date__sys`optional

The date the user will first be able to access Vault in `YYYY-MM-DD` format. If excluded, defaults to today’s date.

`send_welcome_email__sys`optional

Set to `true` to defer welcome email until user’s account activation date. Set to `false` to send no welcome email.

`layout_profile__sys`optional

The ID of the layout profile to assign to the user.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-object-records-sample-csv-input.csv)[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-user-objects.json)

Note that when you create, add, or update `user__sys`, Vault synchronizes those changes with `users` across all Vaults to which that user is a member. This includes cross-domain Vaults.

#### Response Details

Vault returns a `responseStatus` for the request:

-   `SUCCESS`: This request executed with no warnings. Individual records may be failures.
-   `WARNING`: When [upserting](#Query_String_Parameters_Upsert_Object_Records) records, this request executed with at least one warning on an individual record. Other individual records may be failures.
-   `FAILURE`: This request failed to execute. For example, an invalid `sessionId`.

On `SUCCESS` or `WARNING`, Vault returns a `responseStatus` for each individual record in the same order provided in the input. The `responseStatus` for each record can be one of the following:

-   `SUCCESS`: Vault successfully updated at least one field value on this record.
-   `WARNING`: When [upserting](#Query_String_Parameters_Upsert_Object_Records) records, Vault successfully evaluated this record and reported a warning. For example, Vault returns a warning for records that process with no changes ([no-op](#No_Ops)).
-   `FAILURE`: This record could not be evaluated and Vault made no field value changes. For example, an invalid or duplicate record ID.

In addition to the record `id` and `url`, the response includes the following information for each record:

Metadata Field

Description

`event`

Whether the record was created (`created__sys`) or updated (`updated__sys`). The response does not return an `event` for failed operations.

`id_param_value`

The value of the field specified by the `idParam` query parameter if provided in an upsert request. For example, if `idparam=external_id__v`, the `id_param_value` returned is the same as the record’s external ID.

In CTMS Vaults, if you do not specify a milestone record ID when creating a new _Monitoring Event_ record, this request automatically creates a new _Milestone_ record. However, the response does not return the `id` of the new _Milestone_ record. Learn more about [automated CTMS object creation in Vault Help](https://clinical.veevavault.help/en/lr/40009).

## Roll-up Fields

You can configure up to 25 Roll-up fields on a parent object to calculate the minimum, maximum, count, or sum of source field values on related child records. [Learn more about Roll-up field calculation in Vault Help](https://platform.veevavault.help/en/lr/15057/#roll-up-fields).

Use the following endpoints to start a full recalculation of all Roll-up fields on a specific object or to check the status of a recalculation. This may be helpful in the following scenarios:

-   When you create a new Roll-up field, Vault does not automatically calculate a value for existing parent records.
-   When you upload a large number of records using Record Migration Mode, Vault bypasses automatic roll-up calculations.

When performing a full recalculation, Vault evaluates all Roll-up fields on an object asynchronously.

### Recalculate Roll-up Fields

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/actions/recalculaterollups
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "SUCCESS"
}
'''

Recalculate all Roll-up fields for the specified object. [Learn more about Roll-up fields in Vault Help](https://platform.veevavault.help/en/lr/15057/#roll-up-fields).

When performing a full recalculation, Vault evaluates all Roll-up fields on an object asynchronously.

This endpoint is equivalent to the _Recalculate Roll-up Fields_ action in the Vault UI. While a recalculation is running, Admins cannot start another recalculation using either Vault API or Vault UI.

POST `/api/{version}/vobjects/{object_name}/actions/recalculaterollups`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object on which to start the Roll-up field recalculation.

#### Response Details

Returns `SUCCESS` if the recalculation starts successfully, or `FAILURE` if a recalculation is already running for the specified object.

### Retrieve Roll-up Field Recalculation Status

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/actions/recalculaterollups
'''

> Response

'''
{
    "responseStatus": "SUCCESS", 
    "data": { 
        "status": "RUNNING" 
    }
} 

'''

Determine whether a Roll-up field recalculation is currently running. [Learn more about Roll-up fields in Vault Help](https://platform.veevavault.help/en/lr/15057/#roll-up-fields).

GET `/api/{version}/vobjects/{object_name}/actions/recalculaterollups`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object for which to check the status of a Roll-up field recalculation.

#### Response Details

On `SUCCESS`, the response specifies the status of the Roll-up field recalculation as either `RUNNING` or `NOT_RUNNING`.

## Update Object Records

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-raw 'id,generic_name__vs,product_family__vs,abbreviation__vs,therapeutic_area__vs,manufacturer_name__v,regions__c
00P000000000602,Gluphosphate,gluphosphate__c,GLU,cardiology__vs,Veeva Labs,north_america__c
00P00000000K001,nitroprinaline__c,,NYA,veterinary__c,Veeva Labs,europe__c
00P00000000Q007,veniladrine sulfate,"veniladrine__c,vendolepene__c",VPR,psychiatry__vs,Veeva Labs,"north_america__c,south_america__c"' \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v
'''

> Response

'''
{
   "responseStatus": "WARNING",
   "warnings": [
       {
           "warning_type": "NO_DATA_CHANGES",
           "message": "No changes in values - one or more records not updated"
       }
   ],
   "data": [
       {
           "responseStatus": "SUCCESS",
           "data": {
               "id": "00P000000000602",
               "url": "/api/v25.2/vobjects/product__v/00P000000000602"
           }
       },
       {
           "responseStatus": "WARNING",
           "warnings": [
               {
                   "warning_type": "NO_DATA_CHANGES",
                   "message": "No changes in values - record not updated"
               }
           ],
           "data": {
               "id": "00P00000000K001",
               "url": "/api/v25.2/vobjects/product__v/00P00000000K001"
           }
       },
       {
           "responseStatus": "FAILURE",
           "errors": [
               {
                   "type": "INVALID_DATA",
                   "message": "The resource [00P00000000Q007] does not exist"
               }
           ]
       }
   ]
}
'''

Update Object Records in bulk. You can use this endpoint to update user records (`user__sys`).

-   The maximum input size is 50 MB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   Vault removes XML characters that fall outside of the [character range](https://www.w3.org/TR/xml/#charsets) from the request body.
-   The maximum batch size is 500.

PUT `/api/{version}/vobjects/{object_name}`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

If set to `true`, Vault allows you to update object records in a noninitial state and with minimal validation, create inactive records, and set standard and system-managed fields such as `created_by__v`. Does not bypass record triggers. You must have the Record Migration permission to use this header. Learn more about [Record Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/761685).

`X-VaultAPI-NoTriggers`

If set to `true` and Record Migration Mode is enabled, it bypasses all system, standard, custom SDK triggers, and Action Triggers. Before using this parameter, learn more about [bypassing triggers](https://platform.veevavault.help/en/lr/761685#no-triggers).

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object, for example, `product__v`.

#### Body Parameters

Include parameters as JSON or CSV. The following shows the required standard fields, but an Admin may set other standard or custom object fields as required in your Vault.

Name

Description

`id`required

The object record ID. You can only update an object record ID once per request. If you provide duplicate IDs, the bulk update fails any duplicate records. Instead of `id`, you can use a unique field defined by the `idParam` query parameter.

`{field_name}`optional

The field name to update on this object record. Use the [Object Metadata API](#Retrieve_Object_Metadata) to retrieve all fields configured on objects. You can update any field with `editable: true`.

`state__v`optional

Specifies the lifecycle state of the record when `X-VaultAPI-MigrationMode` is set to `true`. For example, `draft_state__c`.

`state_label`optional

Specifies the lifecycle state type of the record when `X-VaultAPI-MigrationMode` is set to `true`. Use the format `base:object_lifecycle:` followed by the object state type. For example, `base:object_lifecycle:initial_state_type`. When providing both a state and state type, the `state_label` value must map to the provided `state__v` value. For example, if the `state__v` value is set to `draft_state__c`, the `state_label` value must already be set to draft in the destination Vault.

#### Updating Attachment Fields

To update an _Attachment_ field type, provide the file path on file staging. You can also use [Update Attachment Field File](#Update_Attachment_Field_File) to update a single _Attachment_ field for an existing record.

The maximum allowed file size for _Attachment_ fields is 100 MB.

To make no changes to the field, provide the existing attachment’s file handle. To clear the field, leave the value blank.

#### Query Parameters

Name

Description

`idParam`

Optional: To identify objects in your input by a unique field, add `idParam={field_name}` to the request endpoint. You can use any object field that has `unique` set to `true` in the object metadata. For example, `idParam=external_id__v`.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-update-object-records-sample-csv-input.csv)

**Additional Notes**:

-   If an object is a parent in a parent-child relationship with another object, you cannot update its `status__v` field in bulk.
-   If an object has a field default configured, the value you use for that field overrides the default. Learn more about the [order of operations for field defaults in Vault Help](https://platform.veevavault.help/en/lr/42778/#order-of-operations-for-object-field-defaults).
-   If Dynamic Security (Custom Sharing Rules) is configured on an object, you can add or remove users and groups on manually assigned roles. For example, `editor__v.users`. This will overwrite any users currently in the role.
-   You can also use this call to complete user tasks by setting the `complete__v` field to `true`.
-   The _Edit_ permission is required on the object record when updating role assignments. This endpoint only supports updating standard roles (for example, viewer, editor, owner) and not custom roles. We recommend using the [Assign Users & Groups to Roles on Object Records](#Assign_Users_Groups_to_Roles_Objects) and the [Remove Users & Groups from Roles on Object Records](#Remove_Users_Groups_Roles_Objects) endpoints, which support all roles with better performance.
-   When you create, add, or update `user__sys`, Vault synchronizes those changes with users across all Vaults to which that user is a member. This includes cross-domain Vaults.
-   You can use this endpoint to update checkbox fields (_Yes/No_ fields with the _Show as checkbox_ setting) to a `null` value.

#### Response Details

Vault returns a `responseStatus` for the request:

-   `SUCCESS`: This request executed with no warnings. Individual records may be failures.
-   `WARNING`: This request executed with at least one warning on an individual record. Other individual records may be failures.
-   `FAILURE`: This request failed to execute. For example, an invalid `sessionId`.

On `SUCCESS` or `WARNING`, Vault returns a `responseStatus` for each individual record in the same order provided in the input. The `responseStatus` for each record can be one of the following:

-   `SUCCESS`: Vault successfully updated at least one field value on this record.
-   `WARNING`: Vault successfully evaluated this record and reported a warning. For example, Vault returns a warning for records that process with no changes ([no-op](#No_Ops)).
-   `FAILURE`: This record could not be evaluated and Vault made no field value changes. For example, an invalid or duplicate record ID.

In addition to the record `id` and `url`, the response includes the following information for each record:

Metadata Field

Description

`id_param_value`

The value of the field specified by the `idParam` query parameter if provided in the update request. For example, if `idparam=external_id__v`, the `id_param_value` returned is the same as the record’s external ID.

##### About No-Ops

An API call which causes no operation to occur is called a no-op. For example, a call to update values on an object record which already has all of the requested values. The call succeeds and no operation occurs.

When the API processes a record with no changes, Vault:

-   does not update the record’s `last_modified_date`.
-   does not create an entry in the object record audit history.
-   does not execute [SDK triggers](/sdk/#Triggers).

## Delete Object Records

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Object Records\delete_object_records.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "00P000000000607"
            }
        },
     {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "00P00000000O048"
            }
        },
     {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "00P00000000O078"
            }
        }
    ]
}
'''

Delete Object Records in bulk. Admins can also define special deletion rules for objects, which affects how Vault behaves when you attempt to delete an object record. Learn more about [limitations on object record deletion in Vault Help](https://platform.veevavault.help/en/lr/18769#relationships_deletion).

If you need to delete a parent record along with all of its children and grandchildren, use the [Cascade Delete](#Cascade_Delete_Object_Record) endpoint.

Note that you cannot use this API to delete `user__sys` records. Use the [Update Object Records](#Update_Object_Records) endpoint to set the `status__v` field to `inactive`.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

DELETE `/api/{version}/vobjects/{object_name}`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object, for example, `product__v`.

#### Body Parameters

Upload parameters as a JSON or CSV file.

Name

Description

`id`conditional

The system-assigned object record ID to delete. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Instead of `id`, you can use this user-defined document external ID.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying objects in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata. For example, `idParam=external_id__v`.

Admin may set other standard or custom object fields to required. Use the Object Metadata API to retrieve all fields configured on objects. You can update any object field with `editable: true`.

#### Response Details

Vault returns a `responseStatus` for the request:

-   `SUCCESS`: This request executed with no warnings. Individual records may be failures.
-   `FAILURE`: This request failed to execute. For example, an invalid `sessionId`.

On `SUCCESS`, Vault returns a `responseStatus` and record ID for each individual record in the same order provided in the input. The `responseStatus` for each record can be one of the following:

-   `SUCCESS`: Vault successfully deleted the record.
-   `FAILURE`: This record could not be evaluated and Vault did not delete the object record. For example, an invalid or duplicate record ID.

In addition to the record `id` and `url`, the response includes the following information for each record:

Metadata Field

Description

`id_param_value`

The value of the field specified by the `idParam` query parameter if provided in the delete request. For example, if `idparam=external_id__v`, the `id_param_value` returned is the same as the record’s external ID.

## Cascade Delete Object Record

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000302/actions/cascadedelete
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "job_id": 27301,
  "url": "/api/v25.2/services/jobs/27404"
}
'''

This asynchronous endpoint will delete a single parent object record and all related children and grandchildren.

POST `/api/{version}/vobjects/{object_name}/{object_record_id}/actions/cascadedelete`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object to delete.

`{object_record_id}`

The ID of the specific object record to delete.

## Retrieve Results of Cascade Delete Job

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: text/csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/cascadedelete/results/product__v/success/27404
'''

> Response

'''
Source Object, Record Id
product__v, OP0000146
edl__v, OE0000147
edl_item__v, EE123456
'''

After submitting a request to cascade delete an object record, you can query Vault to determine the results of the request. Before submitting this request:

-   You must have previously requested a cascade delete job (via the API) which is no longer active.
-   You must have a valid `job_id value`, retrieved from the response of the cascade delete request.

GET `/api/{version}/vobjects/cascadedelete/results/{object_name}/{job_status}/{job_id}`

#### Headers

Name

Description

`Accept`

`text/csv` (default)

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object which was deleted.

`{job_id}`

The ID of the job, retrieved from the response of the job request.

`{job_status}`

Possible values are `success` or `failure`. Find if your job succeeded or failed by retrieving the job status.

## Merge Object Records

Duplicate records in Vault can happen due to migrations, integrations, or day-to-day activities and may be difficult to resolve. Vault provides a solution to duplicate records by allowing you to merge two records together. You can only initiate record merges through Vault API or [Vault Java SDK](/sdk/#Record_Merges), and you cannot initiate a record merge through the Vault UI.

Your organization may want to create custom [Record Merge Event Handlers](/sdk/#Record_Merge_Event_Handlers) with Vault Java SDK, which can execute custom logic immediately when a record merge begins or after a record merge completes. For example, directly after a merge starts, you can retrieve the field values on the duplicate record. Directly after the merge completes, you can update any desired information from the duplicate record to the main record. This overrides the default merge behavior which does not copy data between the duplicate and main record.

Learn more about [merging records in Vault Help](https://platform.veevavault.help/en/lr/659058).

### Initiate Record Merge

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
--data-binary @"records-to-merge.json" \
https://myvault.veevavault.com/api/v25.2/vobjects/account__v/actions/merge
'''

> Example JSON Request Body

'''
[
   {
       "duplicate_record_id" : "0V0000000000003",
       "main_record_id" : "0V0000000000013"
   },
   {
       "duplicate_record_id" : "0V0000000000004",
       "main_record_id" : "0V0000000000013"
   },
   {
       "duplicate_record_id" : "0V0000000000005",
       "main_record_id" : "0V0000000000010"
   }
]
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": 863204
   }
}

'''

Initiate a record merge operation in bulk. Starts a record merge job. When merging two records together, you must select one record to be the `main_record_id` and one record to be the `duplicate_record_id`. The merging process updates all inbound references (including attachments) from other objects that point to the `duplicate` record and moves those over to the `main` record. Field values on the`main` record are not changed, and when the process is complete, the `duplicate` record is deleted. Record merges do not trigger [record triggers](/sdk/#About_Record_Triggers).

You can only merge two records together in a single operation, one `main` record and one `duplicate` record. This is called a merge set. If you have multiple `duplicate` records you wish to merge into the same`main` record, you need to create multiple merge sets and execute multiple record merges.

-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 10 merge sets.
-   The maximum number of concurrent merge requests is 500.

The object must have **Enable Merges** configured, and the initiating user must have the correct permission such as the _Application: Object: Merge Records_ permission. Learn more about the [configuration required for record merges in Vault Help](https://platform.veevavault.help/en/lr/659058).

In Clinical Operations Vaults, this endpoint does not support merging _Person_ (`person__sys`), _Organization_ (`organization__v`), _Location_ (`location__v`), or _Contact Information_ (`contact_information__clin`) records. Instead, use [Initiate Clinical Record Merge](#Initiate_Clinical_Record_Merge).

POST `/api/{version}/vobjects/{object_name}/actions/merge`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. For example, `account__v`. This object must have **Enable Merges** configured.

#### Body Parameters

Upload parameters as a JSON or CSV file. You can merge up to 10 merge sets at once.

Name

Description

`duplicate_record_id`required

The ID of the `duplicate` record. Each `duplicate_record_id` can only be merged into one `main_record_id` record. When the merging process is complete, Vault deletes this record.

`main_record_id`required

The ID of the `main` record. The merging process updates all inbound references (including attachments) from other objects that point to the `duplicate` record and moves those over to the `main` record. Vault does not change field values on the `main` record.

#### Response Details

On `SUCCESS`, the job has successfully started and the response includes a `job_id`. On `FAILURE`, the job failed to start. There is no partial success.

### Retrieve Record Merge Status

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/merges/863301/status
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "status": "IN_PROGRESS"
    }
}
'''

Given a `job_id` for a merge records job, retrieve the job status.

Before submitting this request:

-   You must have previously requested a record merge job.
-   You must have a valid `job_id` field value returned from the record merge operation.

GET `/api/{version}/vobjects/merges/{job_id}/status`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The `job_id` field value returned from the merge operation. You can start merge operations with the [Initiate Record Merge](#Initiate_Record_Merge) API request or with the [Vault Java SDK](/sdk/#Record_Merges).

#### Response Details

On `SUCCESS`, the merge job may have one of the following statuses:

-   `IN_PROGRESS`: The job is currently running
-   `SUCCESS`: The job completed with no errors; all records were merged
-   `FAILURE`: The job completed with errors; one or more records were not merged

### Retrieve Record Merge Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/merges/863301/results
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "merge_sets": [
           {
               "duplicate_record_id": "0V0000000000003",
               "main_record_id": "0V0000000000013",
               "status": "FAILURE",
               "error": {
                   "type": "INVALID_DATA",
                   "message": "Failed validation. Merge was not attempted."
               }
           }
]
'''

Given a `job_id` for a merge records job, retrieve the job results.

Before submitting this request:

-   You must have previously requested a record merge job which is no longer `IN_PROGRESS`.
-   You must have a valid `job_id` field value returned from the record merge operation.

GET `/api/{version}/vobjects/merges/{job_id}/results`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The `job_id` field value returned from the merge operation. You can start merge operations with the [Initiate Record Merge](#Initiate_Record_Merge) API request or with the [Vault Java SDK](/sdk/#Record_Merges).

#### Response Details

On `SUCCESS`, Vault returns the results of the record `merge_sets` that attempted to merge.

For each of the `merge_sets` that return a `status` of `FAILURE`, Vault may return one of the following error `type`s:

-   `INVALID_DATA`: The merge was not attempted
-   `PROCESSING_ERROR`: The merge was attempted, but failed during processing

### Download Merge Records Job Log

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/merges/873101/log
'''

> Response Headers

'''
Content-Type: application/zip;charset=UTF-8
Content-Disposition: attachment;filename="19523-873101.zip"
'''

> Example Response File: Merge Record Job History Log

'''
2024-03-01T00:50:01.741Z Started processing merge records job [873101]
2024-03-01T00:50:02.116Z Merge sets [Duplicate Record:[OBE000000006005], Main Record:[OBE00000000D002];Duplicate Record:[OBE000000008004], Main Record:[OBE00000000D002];Duplicate Record:[OBE000000000201], Main Record:[OBE00000000D002]] passed validation and will be merged in job [873101]
2024-03-01T00:50:02.116Z Starting distributed work for merge records job [873101]
2024-03-01T00:50:02.632Z Began processing [INBOUND_CHILD_OBJECT] relationship configured on Object [campaign_country_join__c] field [campaign__c] for job [873101]. [0] record(s) will be processed
2024-03-01T00:50:02.640Z Finished processing [INBOUND_CHILD_OBJECT] relationship for job [873101]
2024-03-01T00:50:02.924Z Began processing [INBOUND_OBJECT] relationship configured on Object [review_meeting__c] field [related_campaign__c] for job [873101]. [0] record(s) will be processed
2024-03-01T00:50:02.932Z Finished processing [INBOUND_OBJECT] relationship for job [873101]
2024-03-01T00:50:02.957Z Began processing [INBOUND_DOCUMENT] relationship configured on Document field [related_campaigns__c] for job [873101]. [0] document(s) will be processed
2024-03-01T00:50:02.964Z Finished processing [INBOUND_DOCUMENT] relationship for job [873101]
2024-03-01T00:50:02.965Z Starting to move attachments for job [873101]
2024-03-01T00:50:03.013Z Finished moving attachments for job [873101]
2024-03-01T00:50:03.197Z Completed merge records job [873101]
2024-03-01T00:50:03.197Z Merge Records job [873101] successfully merged Merge Sets: [Duplicate Record:[OBE000000006005], Main Record:[OBE00000000D002];Duplicate Record:[OBE000000008004], Main Record:[OBE00000000D002];Duplicate Record:[OBE000000000201], Main Record:[OBE00000000D002]]
2024-03-01T00:50:03.206Z
2024-03-01T00:50:03.207Z Job Title: AsyncOperation
2024-03-01T00:50:03.207Z Job Type: ASYNC_OPERATION
2024-03-01T00:50:03.207Z Job Subtype: MERGE_RECORDS_JOB
2024-03-01T00:50:03.207Z Job Schedule Time: 2024-03-01T00:50:02.000Z
2024-03-01T00:50:03.207Z Job Queue Time: 2024-03-01T00:50:02.000Z
2024-03-01T00:50:03.207Z Job Execution Time: 2024-03-01T00:50:02.000Z
2024-03-01T00:50:03.208Z Job Finish Time: 2024-03-01T00:50:03.000Z
2024-03-01T00:50:03.208Z Job Completion Status: Success (COMPLETED_WITH_SUCCESS)
'''

Given a `job_id` for a merge records job, retrieve the job history log. The same log is available for download through the Vault UI from **Admin > Operations > Job Status**.

Before submitting this request:

-   You must have previously requested a record merge job which is no longer `IN_PROGRESS`.
-   You must have a valid `job_id` field value returned from the record merge operation.

GET `/api/{version}/vobjects/merges/{job_id}/log`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`. For this request, the `Accept` header controls only the error response. On `SUCCESS`, the response is a file stream (download).

#### URI Path Parameters

Name

Description

`{job_id}`

The `job_id` field value returned from the merge operation. You can start merge operations with the [Initiate Record Merge](#Initiate_Record_Merge) API request or with the [Vault Java SDK](/sdk/#Record_Merges).

#### Response Details

On `SUCCESS`, Vault downloads the job history log for the specified merge record job. The HTTP Response Header `Content-Type` is set to `application/zip`. The HTTP Response Header `Content-Disposition` contains a default filename component which you can use when naming the local file. If you choose to name this file yourself, make sure you add the `.zip` extension. The merge record job history log contains information about the merge, such as the merge start and completion times, relationship processing start and end times, attachment processing start and end times, and more. See the **Example Response File** for details.

## Object Types

Vault Objects can be partitioned into Object Types. For example, a Product object may have two different object types: “Pharmaceutical Product” and “Medical Device Product”. These object types may share some fields but also have fields only used in each object type. By using object types, two product groups can not only manage data specific to their business but also easily report on products in both groups.

### Retrieve Details from All Object Types

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/Objecttype
'''

Retrieve all object types and object type fields in the authenticated Vault.

GET `/api/{version}/configuration/Objecttype`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response

The response lists all object types and all fields configured on each object type. See the next response for details.

### Retrieve Details from a Specific Object

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/Objecttype.bicycle__c.road_bike__c?loc=true
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "localized_data": {
           "label_plural": {
               "en": "Road Bikes",
               "fr": "Vélos de route",
               "es": "Bicicletas de carretera"
           },
           "label": {
               "en": "Road Bike",
               "fr": "Vélo de route",
               "es": "Bicicleta de carretera"
           }
       },
       "name": "road_bike__c",
       "object": "bicycle__c",
       "active": true,
       "description": "This object type is intended for model numbers 400-650. For model numbers 650-900, use the Hybrid Bike object type.",
       "additional_type_validations": [],
       "label_plural": "Road Bikes",
       "type_fields": [
           {
               "required": false,
               "name": "id",
               "source": "standard"
           },
           {
               "required": false,
               "name": "object_type__v",
               "source": "standard"
           },
           {
               "required": false,
               "name": "global_id__sys",
               "source": "system"
           },
           {
               "required": false,
               "name": "link__sys",
               "source": "system"
           },
           {
               "required": true,
               "name": "name__v",
               "source": "standard"
           },
           {
               "required": true,
               "name": "status__v",
               "source": "standard"
           },
           {
               "required": false,
               "name": "created_by__v",
               "source": "standard"
           },
           {
               "required": false,
               "name": "created_date__v",
               "source": "standard"
           },
           {
               "required": false,
               "name": "modified_by__v",
               "source": "standard"
           },
           {
               "required": false,
               "name": "modified_date__v",
               "source": "standard"
           }
       ],
       "label": "Road Bike"
   }
}
'''

Retrieve all object types and object type fields configured on a given object.

GET `/api/{version}/configuration/{object_name_and_object_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name_and_object_type}`

The object name followed by the object type in the format `Objecttype.{object_name}.{object_type}`. For example, `Objecttype.product__v.base__v`.

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by setting `loc` to `true`.

#### Response

The response lists all object types and all fields configured on each object type for the specific object.

### Change Object Type

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: application/json" \
--data-binary @"C:\Vault\Objects\objecttypes.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/actions/changetype
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "00P07710",
                "url": "api/v24.2/vobjects/product__v/00P07710"
            }
        }
    ]
}
'''

Change the object types assigned to object records. Any field values that exist on both the original and new object type will carry over to the new type. All other field values will be removed, as only fields on the new type are valid. You can set field values on the new object type in the CSV input.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the [standard format](https://datatracker.ietf.org/doc/html/rfc4180).
-   The maximum batch size is 500.

POST `/api/{version}/vobjects/{object_name}/actions/changetype`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object.

#### Body Parameters

Upload parameters as a JSON or CSV file.

Name

Description

`id`required

The ID of the object record.

`object_type__v`required

The ID of the new object type.

## Object Roles

Object records can have different roles available to them depending on their type and lifecycles. There are a set of standard roles that ship with Vault: `owner__v`, `viewer__v`, and `editor__v`. In addition, Admins can create custom roles defined per lifecycle. Not all object records will have users and groups assigned to roles. Learn more about roles on object records in [Vault Help](https://platform.veevavault.help/en/lr/36440).

Through the object record role APIs, you can:

-   Retrieve available roles on object records
-   Retrieve who is currently assigned to a role
-   Add additional users and groups to a role
-   Remove users and groups from roles

Note that all user and group information is returned as IDs, so you need to use the Retrieve User or Retrieve Group API to determine the name.

For roles on documents or binders, see [Roles](#Vault_Roles_API_Reference).

### Retrieve Object Record Roles

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/campaign__c/OBE000000000412/roles
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name": "approver__c",
            "users": [
                61583,
                61584,
                86488
            ],
            "groups": [
                3,
                1392631750101
            ],
            "assignment_type": "manual_assignment"
        }
      ]
    }
'''

Retrieve manually assigned roles on an object record and the users and groups assigned to them.

GET `/api/{version}/vobjects/{object_name}/{id}/roles{/role_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object name.

`{id}`

The `id` of the document, binder, or object record.

`{/role_name}`

Optional: Include a role name to filter for a specific role. For example, `owner__v`.

#### Response Details

Even though the `owner__v` role is automatically assigned when you apply Custom Sharing Rules, the `assignment_type` for roles on objects is always `manual_assignment`.

### Assign Users & Groups to Roles on Object Records

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Roles\assign_object_record_roles.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/campaign__c/roles
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "OBE000000000412"
            }
        }
    ]
}
'''

> Example JSON Request Body

'''
[
  {
    "id": "OBE000000000412",
    "roles": [
      {
        "role": "content_creator__c",
        "users": "61590"
      }
      ]
  }
]
'''

Assign users and groups to roles on an object record in bulk.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

Assigning users and groups to roles is additive, and duplicate groups are ignored. For example, if groups 1 and 2 are currently assigned to a particular role and you assign groups 2 and 3 to the same role, the final list of groups assigned to the role will be 1, 2, and 3.

POST `/api/{version}/vobjects/{object_name}/roles`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default), `text/csv`, or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object where you want to update records.

#### Body Parameters

Prepare a JSON or CSV input file. User and group assignments are ignored if they are invalid, inactive, or already exist.

Name

Description

`id`required

The object record ID.

`role__v.users`optional

A string of user `id` values for the new role.

`role__v.groups`optional

A string of group `id` values for the new role.

See Example JSON Request Body in the right-hand column, or click the button below to download a sample CSV input file.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault_assign_object_record_roles.csv)

#### Response Details

On `SUCCESS`, The response includes the object record `id`.

### Remove Users & Groups from Roles on Object Records

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Roles\remove_object_record_roles.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/campaign__c/roles
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "OBE000000000412"
            }
        }
    ]
}
'''

> Example JSON Request Body

'''
[
  {
    "id": "OBE000000000412",
    "roles": [
      {
        "role": "content_creator__c",
        "users": "61590"
      }
      ]
  }
]
'''

Remove users and groups from roles on an object record in bulk.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

DELETE `/api/{version}/vobjects/{object_name}/roles`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default), `text/csv`, or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object where you want to remove roles.

#### Body Parameters

Prepare a JSON or CSV input file. Users and groups are ignored if they are invalid or inactive.

Name

Description

`id`required

The object record ID.

`role__v.users`optional

A string of user `id` values to remove.

`role__v.groups`optional

A string of group `id` values to remove.

See Example JSON Request Body in the right-hand column, or click the button below to download a sample CSV input file.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault_remove_object_record_roles.csv)

#### Response Details

On `SUCCESS`, The response includes the object record `id`.

## Object Record Attachments

### Determine if Attachments are Enabled on an Object

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects/site__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "object": {
        "created_date": "2014-02-03T20:12:29.000Z",
        "created_by": 1,
        "allow_attachments": true,
        "auditable": true,
        "modified_date": "2015-01-06T22:34:15.000Z",
        "status": [
            "active__v"
        ],
        "urls": {
            "field": "/api/v25.2/metadata/vobjects/site__v/fields/{NAME}",
            "record": "/api/v25.2/vobjects/site__v/{id}",
            "attachments": "/api/v25.2/vobjects/site__v/{id}/attachments",
            "list": "/api/v25.2/vobjects/site__v",
            "metadata": "/api/v25.2/metadata/vobjects/site__v"
        },
        "label_plural": "Study Sites",
        "role_overrides": false,
        "label": "Study Site",
        "in_menu": true,
        "help_content": null,
        "source": "standard",
        "order": null,
        "modified_by": 46916,
        "description": null,
        "name": "site__v"
    }
}
'''

GET `/api/{version}/metadata/vobjects/{object_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

#### Response Details

Shown above, “allow\_attachments” is set to `true` for this object and “attachments” is included in the list of urls, indicating that attachments are enabled on the `site__v` object. This means that any of the object records can have attachments.

### Retrieve Object Record Attachments

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 558,
            "filename__v": "Site Contact List.docx",
            "description__v": "Facilities information and contacts",
            "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "size__v": 11450,
            "md5checksum__v": "9c6f61847207898ca98431d3e9ad176d",
            "version__v": 3,
            "created_by__v": 46916,
            "created_date__v": "2015-01-07T21:42:47.772Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558/versions/1"
                },
                {
                    "version__v": 2,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558/versions/2"
                },
                {
                    "version__v": 3,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558/versions/3"
                }
            ]
        },
        {
            "id": 571,
            "filename__v": "Site Area Map.png",
            "format__v": "image/png",
            "size__v": 109828,
            "md5checksum__v": "78b36d9602530e12051429e62558d581",
            "version__v": 1,
            "created_by__v": 46916,
            "created_date__v": "2015-01-16T22:28:44.039Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions/1"
                }
            ]
        }
    ]
}
'''

Retrieve a list of all attachments on a specific object record.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

#### Response Details

Shown above, the `site__v` object record has three versions of attachment `id` 558 and one version of attachment `id` 571. Attachment versioning uses integer numbers beginning with 1 and incrementing sequentially (1, 2, 3,…). There is no concept of major or minor version numbers with attachments.

### Retrieve Object Record Attachment Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 558,
            "filename__v": "Site Contact List.docx",
            "description__v": "Facilities information and contacts",
            "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "size__v": 11450,
            "md5checksum__v": "9c6f61847207898ca98431d3e9ad176d",
            "version__v": 3,
            "created_by__v": 46916,
            "created_date__v": "2015-01-07T21:42:47.772Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558/versions/1"
                },
                {
                    "version__v": 2,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558/versions/2"
                },
                {
                    "version__v": 3,
                    "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/558/versions/3"
                }
            ]
        }
    ]
}
'''

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

#### Response Details

The `md5checksum__v` field is calculated on the latest version of the attachment. If an attachment is added which has the same MD5 checksum value as an existing attachment on a given object record, the new attachment is not added.

### Retrieve Object Record Attachment Versions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "version__v": 1,
            "url": "https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions/1"
        }
    ]
}
'''

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

### Retrieve Object Record Attachment Version Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions/1
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 571,
            "filename__v": "Site Area Map.png",
            "format__v": "image/png",
            "size__v": 109828,
            "md5checksum__v": "78b36d9602530e12051429e62558d581",
            "version__v": 1,
            "created_by__v": 46916,
            "created_date__v": "2015-01-16T22:28:44.039Z"
        }
    ]
}
'''

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

### Retrieve Deleted Object Record Attachments

> Request

'''
curl --location 'https://myvault.veevavault.com/api/v25.2/objects/deletions/vobjects/campaign__c/attachments' \
--header 'Accept: application/json' \
--header 'Authorization: {SESSION_ID}' \
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "OK",
   "responseDetails": {
       "total": 1,
       "size": 1,
       "limit": 1000,
       "offset": 0
   },
   "data": [
       {
           "id": 1501,
           "version": "",
           "date_deleted": "2025-05-17T02:26:49Z",
           "external_id__v": null,
           "record_id": "OBE00000000H001",
           "deletion_type": "attachment__sys"
       }
   ]
}
'''

Retrieve IDs of object attachments deleted within the past 30 days. Learn more about [object record attachments in Vault Help](https://platform.veevavault.help/en/lr/58613).

After object record attachments and attachment versions are deleted, their IDs remain available for retrieval for 30 days. After that, they cannot be retrieved.

This API cannot retrieve attachments in [attachment fields](https://platform.veevavault.help/en/lr/15057).

GET `/api/{version}/objects/deletions/vobjects/{object_name}/attachments`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object from which to retrieve deleted attachments.

#### Query Parameters

Name

Description

`start_date`

Specify a date (no more than 30 days past) after which Vault will look for deleted object record attachments. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`. Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

`end_date`

SSpecify a date (no more than 30 days past) before which Vault will look for deleted object record attachments. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`. Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

`limit`

Paginate the results by specifying the maximum number of deleted attachments to display per page in the response. This can be any value between `0` and `5000`. If omitted, defaults to `1000`.

#### Response Details

Name

Description

`total`

The total number of deleted object record attachments or attachment versions.

`id`

The ID of this deleted object record attachment or attachment version.

`version`

The version of this deleted object record attachment. If all versions of the attachment were deleted, this value is blank (`""`).

`date_deleted`

The date and time this object record attachment or attachment version was deleted.

`external_id__v`

The external ID of this deleted object record attachment or attachment version. May be `null` if no external ID was set for this attachment.

`global_id__sys`

The global ID of this deleted object record attachment or attachment version.

`global_version_id__sys`

The global version ID of this deleted object record or version. If all versions of the document were deleted, this value is `null`.

`deletion_type`

Describes how this object record attachment or attachment version was deleted.

-   this object record attachment was deleted in full, including all versions. For example, this document attachment was deleted with the Delete user action in the Vault UI, or with Vault API.
-   `attachment_version__sys`: this object record attachment version was deleted. For example, this attachment version was deleted with the [Delete Single Object Record Attachment Version](#Delete_Object_Record_Attachment_Version) API.

### Download Object Record Attachment File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/file
'''

> Response Headers

'''
Content-Type: application/pdf;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Downloads the latest version of the specified attachment from the object record.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/file`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

#### Response Details

The HTTP Response Header `Content-Type` is set to the MIME type of the file. For example, if the attachment is a PNG image, the `Content-Type` is image/png. If we cannot detect the MIME file type, `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. When downloading attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachments (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download Object Record Attachment Version File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions/1/file
'''

> Response Headers

'''
Content-Type: application/pdf;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Downloads the specified version of the attachment from the object record.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}/file`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the specified version of the attachment from the object record. The file name is the same as the attachment file name.

The HTTP Response Header `Content-Type` is set to the MIME type of the file. For example, if the attachment is a PNG image, the `Content-Type` is image/png. If we cannot detect the MIME file type, `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. When downloading attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachments (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download All Object Record Attachment Files

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/file
'''

> Response Headers

'''
Content-Type: application/zip;charset=UTF-8
Content-Disposition: attachment;filename="Product CholeCap - attachments.zip"
'''

Downloads the latest version of all attachments from the specified object record.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/file`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the latest version of all attachments from the object record. The attachments are packaged in a ZIP file with the file name: {object type label} {object record name} - attachments.zip.

The HTTP Response Header `Content-Type` is set to `application/zip;charset=UTF-8`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. When downloading attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachment downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Create Object Record Attachment

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=my_attachment_file.png" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data":
    [{
        "id": "558",
        "version__v": 3
    }]
}
'''

Create a single object record attachment. If the attachment already exists, Vault uploads the attachment as a new version of the existing attachment. Learn more about [attachment versioning in Vault Help](https://platform.veevavault.help/en/lr/24287#version-specific).

POST `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB.

If an attachment is added which has the same filename as an existing attachment on a given object record, the new attachment is added as a new version of the existing attachment. If an attachment is added which _is_ exactly the same (same MD5 checksum value) as an existing attachment on a given object record, the new attachment is not added.

The following attribute values are determined based on the file in the request: `filename__v`, `format__v`, `size__v`.

### Create Multiple Object Record Attachments

> Request

'''
curl -X POST  -H 'Authorization: {SESSION_ID}\
-H 'Accept: text/csv' \
-H 'Content-Type: text/csv' \
--data-binary @"create_attachments.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/veterinary_patient__c/attachments/batch
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "SUCCESS",
           "id": 140,
           "version": 1
       },
       {
           "responseStatus": "SUCCESS",
           "id": 141,
           "version": 1
       }
   ]
}
'''

You can create object record attachments in bulk with a JSON or CSV input file. You must first load the attachments to [file staging](/docs/#FTP). If the attachment already exists in your Vault, Vault uploads it as a new version of the existing attachment. Learn more about [attachment versioning in Vault Help](https://platform.veevavault.help/en/lr/24287#version-specific).

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the [standard format](https://datatracker.ietf.org/doc/html/rfc4180).
-   The maximum batch size is 500.

POST `/api/{version}/vobjects/{object_name}/attachments/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Prepare a CSV or JSON input file.

Name

Description

`id`required

The `id` of the object record to which to add the attachment.

`filename__v`required

The name for the new attachment. This name must include the file extension, for example, `MyAttachment.pdf`. If an attachment with this name already exists, it is added as a new version. Cannot exceed 218 bytes.

`file`required

The filepath of the attachment on file staging.

`description__v`optional

Description of the attachment. Maximum 1,000 characters.

`external_id__v`optional

The external ID value of the attachment.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-object-attachments.json)

### Restore Object Record Attachment Version

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions/2?restore=true
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data":
    {
        "id": "571",
        "version__v": 2
    }
}
'''

POST `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}?restore=true`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

### Update Object Record Attachment Description

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "description__v=This is my description for this attachment." \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

PUT `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}`

#### Headers

Name

Description

`Content-Type`

`application/json` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

#### Body Parameters

Name

Description

`description__v`required

This is the only editable field. The maximum length is 1000 characters.

### Update Multiple Object Record Attachment Descriptions

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H 'Accept: text/csv' \
-H 'Content-Type: text/csv' \
--data-binary @"create_attachments.csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/veterinary_patient__c/attachments/batch
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "SUCCESS",
           "id": 140,
           "version": 1
       },
       {
           "responseStatus": "SUCCESS",
           "id": 141,
           "version": 1
       }
   ]
}
'''

Update object record attachments in bulk with a JSON or CSV input file. You can only update the latest version of an attachment.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the [standard format](https://datatracker.ietf.org/doc/html/rfc4180).
-   The maximum batch size is 500.

PUT `/api/{version}/vobjects/{object_name}/attachments/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Prepare a CSV or JSON input file.

Name

Description

`id`required

The `id` of the object record to which to add the attachment.

`attachment_id`required

The `id` of the attachment you are updating on the record.

`external_id__v`optional

Identify attachments by their external `id`. You must also add the `idParam=external_id__v` query parameter.

`description__v`required

Description of the attachment. 1000 characters maximum.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-update-object-attachments.json)

#### Query Parameters

Name

Description

`idParam`

If you’re identifying attachments in your input by external id, add `idParam=external_id__v` to the request endpoint.

### Delete Object Record Attachment

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

DELETE `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

### Delete Multiple Object Record Attachments

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-d '[
{
"id": "V15000000000305",
"attachment_id": "141"
}
]'
https://myvault.veevavault.com/api/v25.2/vobjects/veterinary_patient__c/attachments/batch
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "SUCCESS",
           "id": 141
       }
   ]
}
'''

Delete object record attachments in bulk with a JSON or CSV input file. You can only delete the latest version of an attachment.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the [standard format](https://datatracker.ietf.org/doc/html/rfc4180).
-   The maximum batch size is 500.

DELETE `/api/{version}/vobjects/{object_name}/attachments/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Prepare a CSV or JSON input file.

Name

Description

`id`conditional

The `id` of the object record to which to add the attachment. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Identify attachments by their external `id`. You must also add the `idParam=external_id__v` query parameter.

`attachment_id`required

The `id` of the attachment being updated.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying attachments in your input by external id, add `idParam=external_id__v` to the request endpoint.

### Delete Object Record Attachment Version

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/site__v/1357752909483/attachments/571/versions/1
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

DELETE `/api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

`{object_record_id}`

The object record `id` field value.

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

## Object Page Layouts

Object page layouts are defined at the object or object-type level and control the information displayed to a user on the object record detail page. Objects that include multiple object types can define a different layout for each type. Learn more about [configuring object page layouts in Vault Help](https://platform.veevavault.help/en/lr/26387).

The page layout APIs consider the authenticated user’s permissions, so fields which are hidden from the authenticated user will not be included in the API response. For example, field-level security, object controls, and other object-level permissions are considered. Record-level permissions such as atomic security are not considered. Layout rules are not applied, but instead have their configurations returned as metadata. Both active and inactive fields are included in the response.

### Retrieve Page Layouts

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects/product__v/page_layouts
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "name": "product_detail_page_layout__c",
           "label": "Product Detail Page Layout",
           "object_type": "base__v",
           "url": "/api/v25.2/metadata/vobjects/product__v/page_layouts/product_detail_page_layout__c",
           "active": true,
           "description": "General layout for any product",
           "default_layout": true,
           "display_lifecycle_stages": false
       },
       {
           "name": "otc_product_layout__c",
           "label": "OTC Product Layout",
           "object_type": "base__v",
           "url": "/api/v25.2/metadata/vobjects/product__v/page_layouts/otc_product_layout__c",
           "active": true,
           "description": "New layout for OTC products",
           "default_layout": false,
           "display_lifecycle_stages": false
       },
       {
           "name": "generic_product_layout__c",
           "label": "Generic Product Layout",
           "object_type": "base__v",
           "url": "/api/v25.2/metadata/vobjects/product__v/page_layouts/generic_product_layout__c",
           "active": true,
           "description": "Layout for generics",
           "default_layout": false,
           "display_lifecycle_stages": false
       }
   ]
}
'''

Given an object, retrieve all page layouts associated with that object. You can use this data to [retrieve specific page layout metadata](#Retrieve_Page_Layout_Metadata).

GET `/api/{version}/metadata/vobjects/{object_name}/page_layouts`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The `name` of the object from which to retrieve page layouts.

#### Response Details

On `SUCCESS`, the response lists all layouts associated with the specified object. Each layout includes:

Name

Description

`name`

The name of the layout.

`label`

The label of the layout as it appears in the Vault UI.

`object_type`

The object type where the layout is available.

`active`

The active or inactive status of the layout.

`description`

A description of the layout.

`default_layout`

If `true`, this layout is assigned to all users unless another layout is specified in their assigned Layout Profile.

`display_lifecycle_stages`

For objects with lifecycle stages configured, if `true`, Vault displays the Lifecycle Stages Chevron panel on all views for the object.

### Retrieve Page Layout Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects/my_object__c/page_layouts/my_object_detail_page_layout__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "my_object_detail_page_layout__c",
        "label": "My Object Detail Page Layout",
        "object": "my_object__c",
        "object_type": "base__v",
        "active": true,
        "description": "",
        "default_layout": true,
        "display_lifecycle_stages": false,
        "created_date": "2023-12-04T21:11:32.000Z",
        "last_modified_date": "2023-12-04T23:44:56.000Z",
        "layout_rules": [
            {
                "evaluation_order": 100,
                "status": "active__v",
                "fields_to_hide": [],
                "sections_to_hide": [
                    "my_related_objects__c"
                ],
                "controls_to_hide": [],
                "hide_layout": false,
                "hidden_pages": [],
                "displayed_as_readonly_fields": [
                    "link__sys"
                ],
                "displayed_as_required_fields": [
                    "my_related_object__c"
                ],
                "focus_on_layout": true,
                "expression": "IsBlank(my_related_object__c)"
            }
        ],
        "sections": [
            {
                "name": "details__c",
                "title": "Details",
                "type": "detail",
                "help_content": null,
                "show_in_lifecycle_states": [],
                "properties": {
                    "layout_type": "One-Column",
                    "items": [
                        {
                            "type": "field",
                            "reference": "name__v",
                            "status": "active__v"
                        },
                        {
                            "type": "field",
                            "reference": "status__v",
                            "status": "active__v"
                        },
                        {
                            "type": "field",
                            "reference": "created_date__v",
                            "status": "active__v"
                        }
                    ]
                }
            },
            {
                "name": "my_related_objects__c",
                "title": "My Related Objects",
                "type": "related_object",
                "help_content": null,
                "show_in_lifecycle_states": [],
                "properties": {
                    "relationship": "my_related_objects__cr",
                    "related_object": "my_related_object__c",
                    "prevent_record_create": false,
                    "modal_create_record": false,
                    "criteria_vql": null,
                    "columns": [
                        {
                            "reference": "name__v",
                            "width": "200",
                            "status": "active__v"
                        },
                        {
                            "reference": "my_object__c",
                            "width": "200",
                            "status": "active__v"
                        }
                    ]
                }
            }
        ]
    }
}
'''

Given a page layout `name`, retrieve the metadata for that specific page layout.

The page layout APIs consider the authenticated user’s permissions, so fields that are hidden from the authenticated user will not be included in the API response. For example, field-level security, object controls, and other object-level permissions are considered. Record-level permissions such as atomic security are not considered. Both active and inactive fields are included in the response.

This endpoint returns metadata without layout rules applied, instead returning layout rule configurations as metadata. If a layout rule references a token, this endpoint returns the unresolved token instead of resolving it in the response.

GET `/api/{version}/metadata/vobjects/{object_name}/page_layouts/{layout_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The `name` of the object from which to retrieve page layout metadata.

`{layout_name}`

The `name` of the page layout from which to retrieve metadata.

#### Response Details

On `SUCCESS`, returns metadata for the specified page layout, including the `object_type`, `layout_rules`, and `sections`.

## Attachment Fields

_Attachment_ fields allow you to attach a file to a field on an object record. The value of an _Attachment_ field is the file handle for the file. Learn more about [Attachment fields in Vault Help](https://platform.veevavault.help/en/lr/15057).

You must download an _Attachment_ field file in order to view or edit its content. You can use the following endpoints to download or update _Attachment_ field files.

### Download Attachment Field File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000202/attachment_fields/file__c/file
'''

> Response Headers

'''
Content-Type: application/pdf;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Download the specified _Attachment_ field file from an object record.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/{attachment_field_name}/file`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. For example, `product__v`.

`{object_record_id}`

The object record `id` field value.

`{attachment_field_name}`

The name of the _Attachment_ field from which to retrieve the file.

#### Response Details

On `SUCCESS`, Vault retrieves the file from the specified _Attachment_ field from the object record. The file name is the same as the _Attachment_ field file name.

The HTTP Response Header `Content-Type` is set to the MIME type of the file. For example, if the file is a PNG image, the `Content-Type` is `image/png`. If we cannot detect the MIME file type, `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. When downloading files with very small file size, the HTTP Response Header `Content-Length` is set to the size of the file. For most _Attachment_ fields (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download All Attachment Field Files

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000202/attachment_fields/file
'''

> Response Headers

'''
Content-Type: application/zip;charset=UTF-8
Content-Disposition: attachment;filename="Product - Cholecap - attachment fields.zip"
'''

Download all _Attachment_ field files from the specified object record.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/file`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. For example, `product__v`.

`{object_record_id}`

The object record id field value.

#### Response Details

On `SUCCESS`, Vault retrieves the file from the specified _Attachment_ field from the object record. The files are packaged in a ZIP file with the file name: `{object label} {object record name} - attachment fields.zip`. When extracted, it will include a subfolder for each _Attachment_ field included in the response.

The HTTP Response Header `Content-Type` is set to `application/zip;charset=UTF-8`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. When downloading files with very small file size, the HTTP Response Header `Content-Length` is set to the size of the file. For most _Attachment_ field downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Update Attachment Field File

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000202/attachment_fields/file__c/file \
--form 'file=@"Cholecap Prescribing Information.doc"'
'''

> Response Headers

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "data": {
                "id": "00P000000000202",
                "url": "/api/v25.2/vobjects/product__v/00P000000000202"
            }
        }
    ]
}
'''

Update an _Attachment_ field by uploading a file. If you need to update more than one _Attachment_ field, it is best practice to update in bulk with [Update Object Records](#Update_Object_Records).

POST `/api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/{attachment_field_name}/file`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. For example, `product__v`.

`{object_record_id}`

The object record `id` field value.

## Deep Copy Object Record

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000202/actions/deepcopy
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "job_id": 26001,
  "url": "/api/v25.2/services/jobs/26001"
}
'''

> Example: Deep Copy with Override

'''
[{"name__v":"Copied record 1","external_id__v":""}]
'''

Deep Copy copies an object record, including all of the record’s related child and grandchild records. Each deep (hierarchical) copy can copy a maximum of 10,000 related records at a time.

See [Copying Object Records](https://platform.veevavault.help/en/lr/32218) for details on required access permissions.

POST `/api/{version}/vobjects/{object_name}/{object_record_ID}/actions/deepcopy`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the parent object to copy. For example, `product__v`.

`{object_record_ID}`

The ID of the specific object record to copy.

#### Body

In the request body, you can include field names to override field values in the source record. For example, including `external_id__v` removes the field value in the copy while leaving the source record unchanged.

If the input is formatted as CSV, only a single data line is accepted. If the input is formatted as JSON, only one in the list is accepted.

## Retrieve Results of Deep Copy Job

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: text/csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/deepcopy/results/product__v/failure/26901
'''

> Response

'''
line number,vobject,sourceRecordId,errors
1,product__v,00P000000000301,"""PARAMETER_REQUIRED|Missing required parameter [internal_name__c]"",""OPERATION_NOT_ALLOWED|Another resource already exists with [name__v=WonderDrug]"""
'''

After submitting a request to deep copy an object record, you can query Vault to determine the results of the request. Before submitting this request:

-   You must have previously requested a deep copy job (via the API) which is no longer active.
-   You must have a valid `job_id` value, retrieved from the response of the deep copy request.

GET `/api/{version}/vobjects/deepcopy/results/{object_name}/{job_status}/{job_id}`

#### Headers

Name

Description

`Accept`

`text/csv` (default)

#### URI Path Parameters

Name

Description

`object_name`

The name of the deep copied object.

`job_id`

The ID of the job, retrieved from the response of the job request.

`job_status`

Possible values are `success` or `failure`. Find if your job succeeded or failed by retrieving the job status.

## Retrieve Deleted Object Record ID

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/deletions/vobjects/product__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "OK",
    "responseDetails": {
        "total": 3,
        "size": 3,
        "limit": 1000,
        "offset": 0
    },
    "data": [
        {
            "id": "V29000000002001",
            "date_deleted": "2022-06-22T15:24:27Z"
        },
        {
            "id": "V29000000003001",
            "date_deleted": "2022-06-23T21:16:25Z"
        },
        {
            "id": "V29000000003002",
            "date_deleted": "2022-06-23T21:16:30Z"
        }
    ]
}
'''

Retrieve the IDs of object records that have been deleted from your Vault within the past 30 days. After object records are deleted from a Vault, their IDs are still available for retrieval for 30 days. After that, they cannot be retrieved. You can use the optional request parameters below to narrow the results to a specific date and time range within the past 30 days.

GET `/api/{version}/objects/deletions/vobjects/{object_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value (`product__v`, `country__v`, `custom_object__c`, etc.).

#### Query Parameters

Name

Description

`start_date`

Specify a date (no more than 30 days past) after which Vault will look for deleted object records. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`

`end_date`

Specify a date (no more than 30 days past) before which Vault will look for deleted object records. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`

`limit`

Paginate the results by specifying the maximum number of records per page in the response. This can be any value between `0` and `5000`. If omitted, defaults to `1000`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the entry returned. For example, if you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=50`. If omitted, defaults to `0`.

Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

## Retrieve Limits on Objects

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/limits
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "name": "custom_objects",
      "remaining": 7,
      "max": 20
    }
  ]
}
'''

Retrieve the limit on the number of custom objects that can be created in the authenticated Vault.

GET `/api/{version}/limits`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

Field Name

Description

`custom_objects`

The maximum number of custom objects that can be created in the Vault and the number remaining.

## Update Corporate Currency Fields

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-d "id=00P000000000301" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/actions/updatecorporatecurrency
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "job_id": 81603,
    "url": "/api/v25.2/services/jobs/81603"
}
'''

Currency is a field type available on all Vault objects. Whenever a user populates a local currency field value, Vault automatically populates the related corporate currency field value, except in the following scenarios:

-   Admins change the Corporate Currency setting for the vault
-   Admins update the Rate setting for the local currency used by a record

This endpoint updates the `field_corp__sys` field values of an object record based on the Rate of the currency, denoted by the `local_currency__sys` field of the specified record. Learn more about [Currency Fields](https://platform.veevavault.help/en/lr/50532) in Vault Help.

PUT `/api/{version}/vobjects/{object_name}/actions/updatecorporatecurrency`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value, for example, `product__v`.

#### Body Parameters

Name

Description

`id`optional

The object record `id` field value. If you don’t provide an `id`, Vault updates corporate fields of all records for the object.
