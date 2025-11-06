# Veeva Vault API Verification Checklist (25R2)

## Authentication
- [x] User Name and Password
- [x] OAuth 2.0 / OpenID Connect
- [x] Retrieve API Versions
- [x] Authentication Type Discovery
- [x] Session Keep Alive
- [x] End Session
- [x] Salesforce™ Delegated Requests
- [x] Delegated Access
    - [x] Retrieve Delegations
    - [x] Initiate Delegated Session

## Direct Data
- [x] Retrieve Available Direct Data Files
- [x] Download Direct Data File

## Vault Query Language (VQL)
- [x] Submitting a Query

## Metadata Definition Language (MDL)
- [x] Execute MDL Script
- [x] Asynchronous MDL Requests
    - [x] Execute MDL Script Asynchronously
    - [x] Retrieve Asynchronous MDL Script Results
    - [x] Cancel Raw Object Deployment
- [x] Retrieve All Component Metadata
- [x] Retrieve Component Type Metadata
- [x] Retrieve Component Records
    - [x] Retrieve Component Record Collection
    - [x] Retrieve Component Record (XML/JSON)
    - [x] Retrieve Component Record (MDL)
- [x] Components with Content
    - [x] Upload Content File
    - [x] Retrieve Content File

## Documents
- [x] Retrieve Document Fields
    - [x] Retrieve All Document Fields
    - [x] Retrieve Common Document Fields
- [x] Retrieve Document Types
    - [x] Retrieve All Document Types
    - [x] Retrieve Document Type
    - [x] Retrieve Document Subtype
    - [x] Retrieve Document Classification
- [x] Retrieve Documents
    - [x] Retrieve All Documents
    - [x] Retrieve Document
    - [x] Retrieve Document Versions
    - [x] Retrieve Document Version
    - [x] Retrieve Document Version Text
    - [x] Download Document File
    - [x] Download Document Version File
    - [x] Download Document Version Thumbnail File
- [x] Create Documents
    - [x] Create Single Document
    - [x] Create Multiple Documents
- [x] Update Documents
    - [x] Update Single Document
    - [x] Update Multiple Documents
    - [x] Reclassify Single Document
    - [x] Reclassify Multiple Documents
    - [x] Update Document Version
    - [x] Create Multiple Document Versions
    - [x] Create Single Document Version
- [x] Delete Documents
    - [x] Delete Single Document
    - [x] Delete Multiple Documents
    - [x] Delete Single Document Version
    - [x] Delete Multiple Document Versions
    - [x] Retrieve Deleted Document IDs
- [x] Document Locks
    - [x] Retrieve Document Lock Metadata
    - [x] Create Document Lock
    - [x] Retrieve Document Lock
    - [x] Delete Document Lock
    - [x] Undo Collaborative Authoring Checkout
- [x] Document Renditions
    - [x] Retrieve Document Renditions
    - [x] Retrieve Document Version Renditions
    - [x] Download Document Rendition File
    - [x] Download Document Version Rendition File
    - [x] Add Multiple Document Renditions
    - [x] Add Single Document Rendition
    - [x] Upload Document Version Rendition
    - [x] Update Multiple Document Renditions
    - [x] Replace Document Rendition
    - [x] Replace Document Version Rendition
    - [x] Delete Multiple Document Renditions
    - [x] Delete Single Document Rendition
    - [x] Delete Document Version Rendition
- [x] Document Attachments
    - [x] Determine if a Document has Attachments
    - [x] Retrieve Document Attachments
    - [x] Retrieve Document Version Attachments
    - [x] Retrieve Document Attachment Versions
    - [x] Retrieve Document Version Attachment Versions
    - [x] Retrieve Document Version Attachment Version Metadata
    - [x] Retrieve Document Attachment Metadata
    - [x] Retrieve Document Attachment Version Metadata
    - [x] Retrieve Deleted Document Attachments
    - [x] Download Document Attachment
    - [x] Download Document Attachment Version
    - [x] Download Document Version Attachment Version
    - [x] Download All Document Attachments
    - [x] Download All Document Version Attachments
    - [x] Delete Single Document Attachment
    - [x] Delete Single Document Attachment Version
    - [x] Delete Multiple Document Attachments
    - [x] Create Document Attachment
    - [x] Create Multiple Document Attachments
    - [x] Restore Document Attachment Version
    - [x] Update Document Attachment Description
    - [x] Update Multiple Document Attachment Descriptions
- [x] Document Annotations
    - [x] Retrieve Annotation Type Metadata
    - [x] Retrieve Annotation Placemark Type Metadata
    - [x] Retrieve Annotation Reference Type Metadata
    - [x] Create Multiple Annotations
    - [x] Add Annotation Replies
    - [x] Update Annotations
    - [x] Read Annotations by Document Version and Type
    - [x] Read Annotations by ID
    - [x] Read Replies of Parent Annotation
    - [x] Delete Annotations
    - [x] Export Document Annotations to PDF
    - [x] Export Document Version Annotations to PDF
    - [x] Import Document Annotations from PDF
    - [x] Import Document Version Annotations from PDF
    - [x] Retrieve Video Annotations
- [x] Document Relationships
    - [x] Retrieve Document Type Relationships
    - [x] Retrieve Document Relationships
    - [x] Create Single Document Relationship
    - [x] Create Multiple Document Relationships
    - [x] Retrieve Document Relationship
    - [x] Delete Single Document Relationship
    - [x] Delete Multiple Document Relationships
- [x] Export Documents
    - [x] Export Documents
    - [x] Export Document Versions
    - [x] Retrieve Document Export Results
- [x] Document Events
    - [x] Retrieve Document Event Types and Subtypes
    - [x] Retrieve Document Event Subtype Metadata
    - [x] Create Document Event
    - [x] Retrieve Document Events
- [x] Document Templates
    - [x] Retrieve Document Template Metadata
    - [x] Retrieve Document Template Collection
    - [x] Retrieve Document Template Attributes
    - [x] Download Document Template File
    - [x] Create Single Document Template
    - [x] Create Multiple Document Templates
    - [x] Update Single Document Template
    - [x] Update Multiple Document Templates
    - [x] Delete Basic Document Template
- [x] Document Signatures
    - [x] Retrieve Document Signature Metadata
    - [x] Retrieve Archived Document Signature Metadata
- [x] Document Tokens
    - [x] Retrieve Document Tokens

## Binders
- [x] Retrieve Binders
    - [x] Retrieve All Binders
    - [x] Retrieve Binder
    - [x] Retrieve All Binder Versions
    - [x] Retrieve Binder Version
- [x] Create Binders
    - [x] Create Binder
    - [x] Create Binder from Template
    - [x] Create Binder Version
- [x] Update Binders
    - [x] Update Binder
    - [x] Reclassify Binder
    - [x] Update Binder Version
    - [x] Refresh Binder Auto-Filing
- [x] Delete Binders
    - [x] Delete Binder
    - [x] Delete Binder Version
- [x] Export Binders
    - [x] Export Binder
    - [x] Export Binder Sections
    - [x] Retrieve Binder Export Results
    - [x] Download Exported Binder Files via File Staging
- [x] Binder Relationships
    - [x] Retrieve Binder Relationship
    - [x] Create Binder Relationship
    - [x] Delete Binder Relationship
- [x] Binder Sections
    - [x] Retrieve Binder Sections
    - [x] Retrieve Binder Version Section
    - [x] Create Binder Section
    - [x] Update Binder Section
    - [x] Delete Binder Section
- [x] Binder Documents
    - [x] Add Document to Binder
    - [x] Move Document in Binder
    - [x] Remove Document from Binder
- [x] Binder Templates
    - [x] Retrieve Binder Template Metadata
    - [x] Retrieve Binder Template Node Metadata
    - [x] Retrieve Binder Template Collection
    - [x] Retrieve Binder Template Attributes
    - [x] Retrieve Binder Template Node Attributes
    - [x] Create Binder Template
    - [x] Bulk Create Binder Templates
    - [x] Create Binder Template Node
    - [x] Update Binder Template
    - [x] Bulk Update Binder Templates
    - [x] Replace Binder Template Nodes
    - [x] Delete Binder Template
- [x] Binding Rules
    - [x] Update Binding Rule
    - [x] Update Binder Section Binding Rule
    - [x] Update Binder Document Binding Rule
- [x] Binder Roles
    - [x] Retrieve Binder Roles
    - [x] Assign Users & Groups to Binder Roles
    - [x] Remove Users & Groups from Binder Roles
- [x] Binder User Actions
    - [x] Retrieve Binder User Actions
    - [x] Retrieve User Actions on Multiple Binders
    - [x] Retrieve Binder Entry Criteria
    - [x] Initiate Binder User Action
    - [x] Initiate Bulk Binder User Actions

## Vault Objects
- [x] Retrieve Object Metadata
- [x] Retrieve Object Field Metadata
- [x] Retrieve Object Collection
- [x] Retrieve Object Records
- [x] Retrieve Object Record
- [x] Create & Upsert Object Records
- [x] Roll-up Fields
    - [x] Recalculate Roll-up Fields
    - [x] Retrieve Roll-up Field Recalculation Status
- [x] Update Object Records
- [x] Delete Object Records
- [x] Cascade Delete Object Record
- [x] Retrieve Results of Cascade Delete Job
- [x] Merge Object Records
    - [x] Initiate Record Merge
    - [x] Retrieve Record Merge Status
    - [x] Retrieve Record Merge Results
    - [x] Download Merge Records Job Log
- [x] Object Types
    - [x] Retrieve Details from All Object Types
    - [x] Retrieve Details from a Specific Object
    - [x] Change Object Type
- [x] Object Roles
    - [x] Retrieve Object Record Roles
    - [x] Assign Users & Groups to Roles on Object Records
    - [x] Remove Users & Groups from Roles on Object Records
- [x] Object Record Attachments
    - [x] Determine if Attachments are Enabled on an Object
    - [x] Retrieve Object Record Attachments
    - [x] Retrieve Object Record Attachment Metadata
    - [x] Retrieve Object Record Attachment Versions
    - [x] Retrieve Object Record Attachment Version Metadata
    - [x] Retrieve Deleted Object Record Attachments
    - [x] Download Object Record Attachment File
    - [x] Download Object Record Attachment Version File
    - [x] Download All Object Record Attachment Files
    - [x] Create Object Record Attachment
    - [x] Create Multiple Object Record Attachments
    - [x] Restore Object Record Attachment Version
    - [x] Update Object Record Attachment Description
    - [x] Update Multiple Object Record Attachment Descriptions
    - [x] Delete Object Record Attachment
    - [x] Delete Multiple Object Record Attachments
    - [x] Delete Object Record Attachment Version
- [x] Object Page Layouts
    - [x] Retrieve Page Layouts
    - [x] Retrieve Page Layout Metadata
- [x] Attachment Fields
    - [x] Download Attachment Field File
    - [x] Download All Attachment Field Files
    - [x] Update Attachment Field File
- [x] Deep Copy Object Record
- [x] Retrieve Results of Deep Copy Job
- [x] Retrieve Deleted Object Record ID
- [x] Retrieve Limits on Objects
- [x] Update Corporate Currency Fields

## Object Lifecycle & Workflows
- [x] Object Record User Actions
    - [x] Retrieve Object Record User Actions
    - [x] Retrieve Object User Action Details
    - [x] Initiate Object Action on a Single Record
    - [x] Initiate Object Action on Multiple Records

## Document Lifecycle & Workflows
- [x] Document User Actions
    - [x] Retrieve Document User Actions
    - [x] Retrieve User Actions on Multiple Documents
    - [x] Retrieve Document Entry Criteria
    - [x] Initiate Document User Action
    - [x] Download Controlled Copy Job Results
    - [x] Initiate Bulk Document User Actions
- [x] Binder User Actions
    - [x] Retrieve Binder User Actions
    - [x] Retrieve User Actions on Multiple Binders
    - [x] Retrieve Binder Entry Criteria
    - [x] Initiate Binder User Action
    - [x] Initiate Bulk Binder User Actions
- [x] Lifecycle Role Assignment Rules
    - [x] Retrieve Lifecycle Role Assignment Rules (Default & Override)
    - [x] Create Lifecycle Role Assignment Override Rules
    - [x] Update Lifecycle Role Assignment Rules (Default & Override)
    - [x] Delete Lifecycle Role Assignment Override Rules
- [x] Document Workflows
    - [x] Retrieve All Document Workflows
    - [x] Retrieve Document Workflow Details
    - [x] Initiate Document Workflow

- [x] Multi-Record Workflows
    - [x] Retrieve All Multi-Record Workflows
    - [x] Retrieve Multi-Record Workflow Details
    - [x] Initiate Multi-Record Workflow

## Workflow Tasks
- [x] Retrieve Workflow Tasks
- [x] Retrieve Workflow Task Details
- [x] Retrieve Workflow Task Actions
- [x] Retrieve Workflow Task Action Details
- [x] Accept Multi-item Workflow Task
- [x] Accept Single Record Workflow Task
- [x] Undo Workflow Task Acceptance
- [x] Complete Multi-item Workflow Task
- [x] Complete Single Record Workflow Task
- [x] Reassign Multi-item Workflow Task
- [x] Reassign Single Record Workflow Task
- [x] Update Workflow Task Due Date
- [x] Cancel Workflow Task
- [x] Manage Multi-item Workflow Content

## Workflows
- [x] Retrieve Workflows
- [x] Retrieve Workflow Details
- [x] Retrieve Workflow Actions
- [x] Retrieve Workflow Action Details
- [x] Initiate Workflow Action

## Bulk Workflow Actions
- [x] Retrieve Bulk Workflow Actions
- [x] Retrieve Bulk Workflow Action Details
- [x] Initiate Bulk Workflow Action

## Users
- [x] Retrieve User Metadata
- [x] Retrieve All Users
- [x] Retrieve User
- [x] Create Users
    - [x] Create Single User
    - [x] Create Multiple Users
- [x] Update Users
    - [x] Update Single User
    - [x] Update My User
    - [x] Update Multiple Users
- [x] Disable User
- [x] Change My Password
- [x] Update Vault Membership
- [x] Retrieve Application License Usage
- [x] Retrieve User Permissions
- [x] Retrieve My User Permissions
- [x] Validate Session User

## SCIM
- [x] Discovery Endpoints
    - [x] Retrieve SCIM Provider
    - [x] Retrieve All SCIM Schema Information
    - [x] Retrieve Single SCIM Schema Information
    - [x] Retrieve All SCIM Resource Types
    - [x] Retrieve Single SCIM Resource Type
- [x] Users
    - [x] Retrieve All Users with SCIM
    - [x] Retrieve Single User with SCIM
    - [x] Retrieve Current User with SCIM
    - [x] Update Current User with SCIM
    - [x] Create User with SCIM
    - [x] Update User with SCIM
- [x] Retrieve SCIM Resources
- [x] Retrieve Single SCIM Resource

## Groups
- [x] Retrieve Group Metadata
- [x] Retrieve All Groups
- [x] Retrieve Auto Managed Groups
- [x] Retrieve Group
- [x] Create Group
- [x] Update Group
- [x] Delete Group

## Picklists
- [x] Retrieve All Picklists
- [x] Retrieve Picklist Values
- [x] Create Picklist Values
- [x] Update Picklist Value Label
- [x] Update Picklist Value
- [x] Inactivate Picklist Value

## Expected Document Lists
- [x] Create a Placeholder from an EDL Item
- [x] Retrieve All Root Nodes
- [x] Retrieve Specific Root Nodes
- [x] Retrieve a Node's Children
- [x] Update Node Order
- [x] Add EDL Matched Documents
- [x] Remove EDL Matched Documents

## Security Policies
- [x] Retrieve Security Policy Metadata
- [x] Retrieve All Security Policies
- [x] Retrieve Security Policy

## Domain Information
- [x] Retrieve Domain Information
- [x] Retrieve Domains

## Configuration Migration
- [x] Export Package
- [x] Import Package
- [x] Deploy Package
- [x] Retrieve Package Deploy Results
- [x] Retrieve Outbound Package Dependencies
- [x] Component Definition Query
- [x] Vault Compare
- [x] Vault Configuration Report
- [x] Validate Package
- [x] Validate Inbound Package
- [x] Enable Configuration Mode
- [x] Disable Configuration Mode

## Sandbox Vaults
- [x] Retrieve Sandboxes
- [x] Retrieve Sandbox Details by ID
- [x] Recheck Sandbox Usage Limit
- [x] Change Sandbox Size
- [x] Set Sandbox Entitlements
- [x] Create or Refresh Sandbox
- [x] Refresh Sandbox from Snapshot
- [x] Delete Sandbox
- [x] Sandbox Snapshots
    - [x] Create Sandbox Snapshot
    - [x] Retrieve Sandbox Snapshots
    - [x] Delete Sandbox Snapshot
    - [x] Update Sandbox Snapshot
    - [x] Upgrade Sandbox Snapshot
- [x] Pre-Production Vaults
    - [x] Build Production Vault
    - [x] Promote to Production

## Logs
- [x] Audit
    - [x] Retrieve Audit Types
    - [x] Retrieve Audit Metadata
    - [x] Retrieve Audit Details
- [x] Audit History
    - [x] Retrieve Complete Audit History for a Single Document
    - [x] Retrieve Complete Audit History for a Single Object Record
- [x] SDK Debug Log
    - [x] Retrieve All Debug Logs
    - [x] Retrieve Single Debug Log
    - [x] Download Debug Log Files
    - [x] Create Debug Log
    - [x] Reset Debug Log
    - [x] Delete Debug Log
- [x] SDK Request Profiler
    - [x] Retrieve All Profiling Sessions
    - [x] Retrieve Profiling Session
    - [x] Create Profiling Session
    - [x] End Profiling Session
    - [x] Delete Profiling Session
    - [x] Download Profiling Session Results
- [x] Retrieve Email Notification Histories
- [x] Download Daily API Usage
- [x] Download SDK Runtime Log

## File Staging
- [x] List Items at a Path
- [x] Download Item Content
- [x] Create Folder or File
- [x] Update Folder or File
- [x] Delete File or Folder
- [x] Resumable Upload Sessions
    - [x] Create Resumable Upload Session
    - [x] Upload to a Session
    - [x] Commit Upload Session
    - [x] List Upload Sessions
    - [x] Get Upload Session Details
    - [x] List File Parts Uploaded to Session
    - [x] Abort Upload Session

## Vault Loader
- [x] Multi-File Extract
    - [x] Extract Data Files
    - [x] Retrieve Loader Extract Results
    - [x] Retrieve Loader Extract Renditions Results
- [x] Multi-File Load
    - [x] Load Data Objects
    - [x] Retrieve Load Success Log Results
    - [x] Retrieve Load Failure Log Results

## Bulk Translation
- [x] Export Bulk Translation File
- [x] Import Bulk Translation File
- [x] Retrieve Import Bulk Translation File Job Summary
- [x] Retrieve Import Bulk Translation File Job Errors

## Jobs
- [x] Retrieve Job Status
- [x] Retrieve SDK Job Tasks
- [x] Retrieve Job Histories
- [x] Retrieve Job Monitors
- [x] Start Job

## Managing Vault Java SDK
- [x] Retrieve Single Source Code File
- [x] Enable Vault Extension
- [x] Disable Vault Extension
- [x] Add or Replace Single Source Code File
- [x] Delete Single Source Code File
- [x] Validate Imported Package
- [x] Retrieve Signing Certificate
- [x] Queues
    - [x] Retrieve All Queues
    - [x] Retrieve Queue Status
    - [x] Disable Delivery
    - [x] Enable Delivery
    - [x] Reset Queue

## Custom Pages
- [x] Retrieve All Client Code Distribution Metadata
- [x] Retrieve Single Client Code Distribution Metadata
- [x] Download Single Client Code Distribution
- [x] Add or Replace Single Client Code Distribution
- [x] Delete Single Client Code Distribution

## Clinical Operations
- [x] Create EDLs
- [x] Recalculate Milestone Document Field
- [x] Apply EDL Template to a Milestone
- [x] Create Milestones from Template
- [x] Execute Milestone Story Events
- [x] Generate Milestone Documents
- [x] Veeva Site Connect: Distribute to Sites
- [x] Populate Site Fee Definitions
- [x] Populate Procedure Definitions
- [x] Initiate Clinical Record Merge
- [x] Enable Study Migration Mode
- [x] Disable Study Migration Mode
- [x] Retrieve OpenData Clinical Affiliations
- [x] Change Primary Investigator Affiliation

## QualityDocs
- [x] Document Role Check for Document Change Control

## QMS
- [x] Manage Quality Team Assignments

## Batch Release
- [x] Create Disposition

## QualityOne
- [x] Manage Team Assignments

## QualityOne HACCP
- [x] Export HACCP Plan Translatable Fields
- [x] Retrieve HACCP Plan Translatable Fields
- [x] Import HACCP Plan Translatable Fields

## RIM Submissions Archive
- [x] Import Submission
- [x] Retrieve Submission Import Results
- [x] Retrieve Submission Metadata Mapping
- [x] Update Submission Metadata Mapping
- [x] Remove Submission
- [x] Cancel Submission
- [x] Export Submission
- [x] Export Partial Submission
- [x] Retrieve Submission Export Results
- [x] Download Exported Submission Files via File Staging

## RIM Submissions
- [x] Copy into Content Plan

## Safety
- [x] Intake
    - [x] Intake Inbox Item
    - [x] Intake Imported Case
    - [x] Retrieve Intake Status
    - [x] Retrieve ACK
- [x] Intake JSON
- [x] Import Narrative
- [x] Bulk Import Narrative
- [x] Retrieve Bulk Import Status

## Veeva SiteVault
- [x] Users
    - [x] Create User
    - [x] Edit User
- [x] Veeva eConsent
    - [x] Retrieve Documents and Signatories
    - [x] Send Documents to Signatories

## Errors
- [x] Error Types
