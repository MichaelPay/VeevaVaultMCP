# Veeva Vault API v25.2 Endpoint Tracking

**Last Updated:** November 6, 2025
**API Version:** v25.2
**Implementation Status:** ✅ 100% Complete (70/70 endpoints)

---

## Table of Contents

1. [SCIM (13 endpoints)](#scim)
2. [Groups (7 endpoints)](#groups)
3. [Picklists (6 endpoints)](#picklists)
4. [Expected Document Lists (7 endpoints)](#expected-document-lists-edl)
5. [File Staging (12 endpoints)](#file-staging)
6. [Vault Loader (6 endpoints)](#vault-loader)
7. [Clinical Operations (14 endpoints)](#clinical-operations)
8. [Safety (8 endpoints)](#safety)
9. [SiteVault (4 endpoints)](#sitevault)
10. [Summary](#summary)

---

## SCIM

**Service File:** `/services/scim/scim.py`
**Implementation Status:** ✅ 13/13 (100%)
**API Version:** v25.2

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | GET | `/api/v25.2/scim/v2/ServiceProviderConfig` | `retrieve_scim_provider()` | SCIM 2.0 compliance |
| ✅ | GET | `/api/v25.2/scim/v2/Schemas` | `retrieve_all_scim_schemas()` | Schema discovery |
| ✅ | GET | `/api/v25.2/scim/v2/Schemas/{schema_id}` | `retrieve_single_scim_schema()` | Schema details |
| ✅ | GET | `/api/v25.2/scim/v2/ResourceTypes` | `retrieve_all_scim_resource_types()` | Resource discovery |
| ✅ | GET | `/api/v25.2/scim/v2/ResourceTypes/{resource_type}` | `retrieve_single_scim_resource_type()` | Resource type details |
| ✅ | GET | `/api/v25.2/scim/v2/Users` | `retrieve_all_users()` | User listing with filters |
| ✅ | GET | `/api/v25.2/scim/v2/Users/{user_id}` | `retrieve_single_user()` | User details |
| ✅ | GET | `/api/v25.2/scim/v2/Me` | `retrieve_current_user()` | Current user context |
| ✅ | PUT | `/api/v25.2/scim/v2/Me` | `update_current_user()` | Self-service updates |
| ✅ | POST | `/api/v25.2/scim/v2/Users` | `create_user()` | User provisioning |
| ✅ | PUT | `/api/v25.2/scim/v2/Users/{user_id}` | `update_user()` | User management |
| ✅ | GET | `/api/v25.2/scim/v2/{resource_type}` | `retrieve_scim_resources()` | Generic resource retrieval |
| ✅ | GET | `/api/v25.2/scim/v2/{resource_type}/{resource_id}` | `retrieve_single_scim_resource()` | Generic resource details |

**Key Features:**
- Full SCIM 2.0 specification compliance
- Support for filtering, sorting, and pagination
- Attribute selection with `attributes` parameter
- Patch operations for partial updates

---

## Groups

**Service File:** `/services/groups/groups.py`
**Implementation Status:** ✅ 7/7 (100%)
**API Version:** v25.2

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | GET | `/api/v25.2/metadata/objects/groups` | `retrieve_group_metadata()` | Metadata schema |
| ✅ | GET | `/api/v25.2/objects/groups` | `retrieve_all_groups()` | `includeImplied` parameter |
| ✅ | GET | `/api/v25.2/objects/groups/auto` | `retrieve_auto_managed_groups()` | Pagination support |
| ✅ | GET | `/api/v25.2/objects/groups/{group_id}` | `retrieve_group()` | `includeImplied` parameter |
| ✅ | POST | `/api/v25.2/objects/groups` | `create_group()` | Delegation control |
| ✅ | PUT | `/api/v25.2/objects/groups/{group_id}` | `update_group()` | Additive/removal operations |
| ✅ | DELETE | `/api/v25.2/objects/groups/{group_id}` | `delete_group()` | User-defined groups only |

**Key Features:**
- `includeImplied` parameter to show users added via security profiles
- Auto-managed groups for Dynamic Access Control (DAC)
- Group nesting support
- Additive and removal operations for members

---

## Picklists

**Service File:** `/services/picklists/picklist_service.py`
**Implementation Status:** ✅ 6/6 (100%)
**API Version:** v25.2

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | GET | `/api/v25.2/objects/picklists` | `retrieve_all_picklists()` | System-managed indicator |
| ✅ | GET | `/api/v25.2/objects/picklists/{picklist_name}` | `retrieve_picklist_values()` | Dependency information |
| ✅ | POST | `/api/v25.2/objects/picklists/{picklist_name}` | `create_picklist_values()` | Auto-generated names |
| ✅ | PUT | `/api/v25.2/objects/picklists/{picklist_name}` | `update_picklist_value_label()` | Label-only update |
| ✅ | PUT | `/api/v25.2/objects/picklists/{picklist_name}/{picklist_value_name}` | `update_picklist_value()` | Status management |
| ✅ | DELETE | `/api/v25.2/objects/picklists/{picklist_name}/{picklist_value_name}` | `inactivate_picklist_value()` | Soft delete |

**Key Features:**
- System-managed picklist support
- Picklist dependencies with controlling picklists
- CSV bulk operations
- Active/Inactive status management

---

## Expected Document Lists (EDL)

**Service File:** `/services/edl/edl.py`
**Implementation Status:** ✅ 7/7 (100%)
**API Version:** v25.2

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/vobjects/edl_item__v/actions/createplaceholder` | `create_placeholder_from_edl_item()` | Asynchronous job |
| ✅ | GET | `/api/v25.2/composites/trees/{hierarchy_or_template}` | `retrieve_all_root_nodes()` | Hierarchy support |
| ✅ | POST | `/api/v25.2/composites/trees/{hierarchy_or_template}/actions/listnodes` | `retrieve_specific_root_nodes()` | Batch retrieval (1000 max) |
| ✅ | GET | `/api/v25.2/composites/trees/{hierarchy_or_template}/{parent_node_id}/children` | `retrieve_node_children()` | Hierarchical navigation |
| ✅ | PUT | `/api/v25.2/composites/trees/{hierarchy_or_template}/{parent_node_id}/children` | `update_node_order()` | Order management |
| ✅ | POST | `/api/v25.2/objects/edl_matched_documents/batch/actions/add` | `add_edl_matched_documents()` | Version locking |
| ✅ | POST | `/api/v25.2/objects/edl_matched_documents/batch/actions/remove` | `remove_edl_matched_documents()` | Locked removal support |

**Key Features:**
- EDL Hierarchy (`edl_hierarchy__v`) and EDL Template (`edl_template__v`) support
- Specific version locking with `lock` parameter
- Batch operations for matched documents
- Tree node ordering capabilities

---

## File Staging

**Service File:** `/services/file_staging/file_staging.py`
**Implementation Status:** ✅ 12/12 (100%)
**API Version:** v25.2

### Basic File Operations (5 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | GET | `/api/v25.2/services/file_staging/items/{item}` | `list_items_at_path()` | Recursive listing, pagination |
| ✅ | GET | `/api/v25.2/services/file_staging/items/content/{item}` | `download_item_content()` | Resumable downloads (Range header) |
| ✅ | POST | `/api/v25.2/services/file_staging/items` | `create_folder_or_file()` | 50MB limit, overwrite support |
| ✅ | PUT | `/api/v25.2/services/file_staging/items/{item}` | `update_folder_or_file()` | Move/rename operations |
| ✅ | DELETE | `/api/v25.2/services/file_staging/items/{item}` | `delete_file_or_folder()` | Recursive deletion |

### Resumable Upload Session Management (7 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/services/file_staging/upload` | `create_resumable_upload_session()` | 500GB max file size |
| ✅ | PUT | `/api/v25.2/services/file_staging/upload/{upload_session_id}` | `upload_to_session()` | 5-50MB parts, 2000 parts max |
| ✅ | POST | `/api/v25.2/services/file_staging/upload/{upload_session_id}` | `commit_upload_session()` | Asynchronous assembly |
| ✅ | GET | `/api/v25.2/services/file_staging/upload` | `list_upload_sessions()` | Active sessions only |
| ✅ | GET | `/api/v25.2/services/file_staging/upload/{upload_session_id}` | `get_upload_session_details()` | Progress tracking |
| ✅ | GET | `/api/v25.2/services/file_staging/upload/{upload_session_id}/parts` | `list_file_parts_uploaded_to_session()` | Pagination support |
| ✅ | DELETE | `/api/v25.2/services/file_staging/upload/{upload_session_id}` | `abort_upload_session()` | Purges all parts |

**Key Features:**
- Files up to 500GB via resumable uploads
- MD5 checksum validation with `Content-MD5` header
- Resumable downloads with Range header
- CSV export format for large directory listings (1000+ items)
- Inbox directory support for external integrations

---

## Vault Loader

**Service File:** `/services/vault_loader/vault_loader.py`
**Implementation Status:** ✅ 6/6 (100%)
**API Version:** v25.2

### Extract Operations (3 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/services/loader/extract` | `extract_data_files()` | 10 objects max, rendition support |
| ✅ | GET | `/api/v25.2/services/loader/{job_id}/tasks/{task_id}/results` | `retrieve_loader_extract_results()` | CSV output |
| ✅ | GET | `/api/v25.2/services/loader/{job_id}/tasks/{task_id}/results/renditions` | `retrieve_loader_extract_renditions_results()` | Rendition paths |

### Load Operations (3 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/services/loader/load` | `load_data_objects()` | 10 objects max, migration modes |
| ✅ | GET | `/api/v25.2/services/loader/{job_id}/tasks/{task_id}/successlog` | `retrieve_load_success_log()` | CSV format |
| ✅ | GET | `/api/v25.2/services/loader/{job_id}/tasks/{task_id}/failurelog` | `retrieve_load_failure_log()` | Error details |

**Key Features:**
- Up to 10 data objects per extract/load request
- Record Migration Mode (`recordmigrationmode`, `notriggers`)
- Document Migration Mode (`documentmigrationmode`)
- Extended object types support
- Email notification on completion

---

## Clinical Operations

**Service File:** `/services/applications/clinical_operations/clinical_operations_service.py`
**Implementation Status:** ✅ 14/14 (100%)
**API Version:** v25.2
**Code Quality:** ⚠️ Fixed duplicate methods (removed lines 470-647)

### EDL and Milestones (6 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/vobjects/study__v/{study_id}/actions/etmfcreateedl` | `create_edls()` | `applyWhereEdlItemsExist` |
| ✅ | POST | `/api/v25.2/objects/documents/milestones/actions/recalculate` | `recalculate_milestone_document_field()` | 500 max batch |
| ✅ | POST | `/api/v25.2/vobjects/milestone__v/{milestone_id}/actions/etmfcreateedl` | `apply_edl_template_to_milestone()` | Template mapping |
| ✅ | POST | `/api/v25.2/vobjects/{object_name}/{object_record_id}/actions/createmilestones` | `create_milestones_from_template()` | Asynchronous job |
| ✅ | POST | `/api/v25.2/app/clinical/milestone/{object_name}/actions/applytemplate` | `execute_milestone_story_events()` | 500 max batch |
| ✅ | POST | `/api/v25.2/app/clinical/milestone/actions/generatemilestonedocuments` | `generate_milestone_documents()` | 500 max milestones |

### Safety and Payments (3 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/app/clinical/safety_distributions/{id}/actions/send` | `distribute_to_sites()` | Safety distribution |
| ✅ | POST | `/api/v25.2/app/clinical/payments/populate-site-fee-definitions` | `populate_site_fee_definitions()` | Template/study source |
| ✅ | POST | `/api/v25.2/app/clinical/ctms/populate-procedure-definitions` | `populate_procedure_definitions()` | Procedure template |

### Study Management (3 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/app/clinical/objects/{object_name}/actions/merge` | `initiate_clinical_record_merge()` | 10 merge sets max |
| ✅ | POST | `/api/v25.2/app/clinical/studies/actions/enable_migration_mode` | `enable_study_migration_mode()` | 500 studies max |
| ✅ | POST | `/api/v25.2/app/clinical/studies/actions/disable_migration_mode` | `disable_study_migration_mode()` | 500 studies max |

### OpenData Clinical (2 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | GET | `/api/v25.2/app/clinical/opendata/{object_name}/{record_id}/affiliations` | `retrieve_opendata_clinical_affiliations()` | 100 record limit |
| ✅ | POST | `/api/v25.2/app/clinical/opendata/person__sys/primary_affiliations` | `change_primary_investigator_affiliation()` | 100 records max |

**Key Features:**
- Study Migration Mode for clinical data migrations
- OpenData Clinical integration for investigator affiliations
- Clinical record merge for Global Directory (person__sys, organization__v, location__v, contact_information__clin)
- Milestone automation with template support
- Site Connect integration for safety distributions

---

## Safety

**Service File:** `/services/applications/safety/safety_service.py`
**Implementation Status:** ✅ 8/8 (100%)
**API Version:** v25.2

### Intake Operations (5 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/app/safety/intake/inbox-item` | `intake_inbox_item()` | E2B R2/R3 support |
| ✅ | POST | `/api/v25.2/app/safety/intake/imported-case` | `intake_imported_case()` | Multi-format support |
| ✅ | GET | `/api/v25.2/app/safety/intake/status` | `retrieve_intake_status()` | Multi-ICSR support |
| ✅ | GET | `/api/v25.2/app/safety/intake/ack` | `retrieve_ack()` | E2B acknowledgment |
| ✅ | POST | `/api/v25.2/app/safety/ai/intake` | `intake_json()` | JSON format support |

### Narrative Operations (3 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/app/safety/import-narrative` | `import_narrative()` | 100k character limit |
| ✅ | POST | `/api/v25.2/app/safety/import-narrative/batch` | `bulk_import_narrative()` | 500 max, 200k chars each |
| ✅ | GET | `/api/v25.2/app/safety/import-narrative/batch/{import_id}` | `retrieve_bulk_import_status()` | Progress tracking |

**Key Features:**
- E2B (R2) and E2B (R3) format support
- Transmission Profile for automated case promotion
- JSON intake with optional source documents
- `X-VaultAPI-IntegrityCheck` header for enhanced validation
- `X-VaultAPI-MigrationMode` header for localized case verification
- Vault Document Archive integration

---

## SiteVault

**Service File:** `/services/applications/site_vault/site_vault_service.py`
**Implementation Status:** ✅ 4/4 (100%)
**API Version:** v25.2

### User Administration (2 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | POST | `/api/v25.2/app/sitevault/useradmin/persons` | `create_user()` | Organization context |
| ✅ | PUT | `/api/v25.2/app/sitevault/useradmin/persons/{person_id}` | `edit_user()` | Assignment management |

### eConsent (2 endpoints)

| Status | Method | Endpoint | Python Method | v25.2 Features |
|--------|--------|----------|---------------|----------------|
| ✅ | GET | `/api/v25.2/app/sitevault/econsent/participant/{participant_id}` | `retrieve_documents_and_signatories()` | Valid blank ICFs |
| ✅ | POST | `/api/v25.2/app/sitevault/econsent/send` | `send_documents_to_signatories()` | Bulk sending |

**Key Features:**
- Person/User differentiation (person__sys vs user__sys)
- Automatic inactive record reactivation
- Nested permission structure (org → site → study assignments)
- Investigator designation support
- eConsent participant document management

---

## Summary

### Overall Implementation Metrics

| Metric | Value |
|--------|-------|
| **Total API Sections Reviewed** | 9 |
| **Total Endpoints Documented** | 70 |
| **Total Endpoints Implemented** | 70 |
| **Implementation Coverage** | 100% |
| **API Version** | v25.2 ✅ |
| **Missing Endpoints** | 0 |
| **Endpoints Needing Updates** | 0 |

### Implementation Status by Section

| Section | Endpoints | Status | Coverage |
|---------|-----------|--------|----------|
| SCIM | 13 | ✅ Complete | 100% |
| Groups | 7 | ✅ Complete | 100% |
| Picklists | 6 | ✅ Complete | 100% |
| Expected Document Lists | 7 | ✅ Complete | 100% |
| File Staging | 12 | ✅ Complete | 100% |
| Vault Loader | 6 | ✅ Complete | 100% |
| Clinical Operations | 14 | ✅ Complete | 100% |
| Safety | 8 | ✅ Complete | 100% |
| SiteVault | 4 | ✅ Complete | 100% |

### Recent Code Quality Improvements

1. ✅ **Fixed Duplicate Methods** (Nov 6, 2025)
   - Removed duplicate method definitions in Clinical Operations service (lines 470-647)
   - File reduced from 647 to 469 lines
   - Impact: Improved code maintainability

2. ✅ **API Version Update** (Nov 6, 2025)
   - Updated from v25.1 to v25.2
   - All endpoints now use correct API version

3. ✅ **Exception Handling** (Nov 6, 2025)
   - Added comprehensive custom exceptions
   - Better error messages with status codes and Vault errors

4. ✅ **Logging Support** (Nov 6, 2025)
   - Added centralized logging throughout
   - Configurable log levels

### v25.2 Key Features Implemented

✅ **SCIM 2.0 Compliance**
- Full SCIM 2.0 specification support
- Resource filtering, sorting, pagination

✅ **Resumable File Uploads**
- Files up to 500GB
- Part-based uploads (2000 parts max)
- MD5 checksum validation

✅ **Clinical Operations Enhancements**
- Study Migration Mode
- OpenData Clinical integration
- Clinical record merge capabilities

✅ **Safety API Enhancements**
- E2B R2 and R3 support
- JSON intake format
- Bulk narrative import (500 max)

✅ **EDL Hierarchy Support**
- Tree-based navigation
- Node ordering
- Matched document versioning

✅ **Migration Modes**
- Record migration mode
- Document migration mode
- Study migration mode

---

## Maintenance Notes

### Last Review: November 6, 2025

**Actions Taken:**
1. Comprehensive endpoint inventory created
2. All 70 endpoints verified against v25.2 documentation
3. Duplicate methods removed from Clinical Operations service
4. API version updated from v25.1 to v25.2
5. Exception handling and logging added

**Next Review Recommended:**
- When Veeva releases API v25.3 or v26.1
- Quarterly verification of endpoint signatures
- Annual comprehensive audit

### Contributing

When adding new endpoints:
1. Update this tracking document
2. Add endpoint to appropriate service file
3. Include comprehensive docstrings with:
   - Endpoint URL
   - Parameters
   - Return type
   - v25.2-specific features
4. Add unit tests
5. Update changelog

---

**Document Version:** 1.0
**Created:** November 6, 2025
**Last Modified:** November 6, 2025
