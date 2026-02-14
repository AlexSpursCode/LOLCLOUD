# LOLCLOUD --- Product Requirements Document (PRD)

## 1. Title

**LOLCLOUD** --- A community-driven catalog and investigation framework
for Living Off the Land in Cloud Environments

------------------------------------------------------------------------

## 2. Purpose & Vision

### Problem Statement

Traditional living off the land catalogs focus primarily on endpoint
binaries. However, cloud environments introduce native service abuse via
APIs, CLI tools, identity systems, and control planes that allow
adversaries to operate without malware or traditional artifacts.

### Vision

Create an open-source, structured, searchable catalog of cloud-native
living off the land techniques including identity abuse, control-plane
manipulation, serverless abuse, and CI/CD exploitation --- complete with
detection guidance, telemetry requirements, and risk scoring.

------------------------------------------------------------------------

## 3. Audience & Use Cases

### Primary Users

-   Red Teamers
-   Blue Team Threat Hunters
-   Detection Engineers
-   Cloud Security Architects
-   SOC Analysts

### Core Needs

-   Understand abuse of native cloud primitives
-   Map behaviors to MITRE ATT&CK for Cloud
-   Provide detection guidance & telemetry requirements
-   Enable structured documentation & research collaboration

------------------------------------------------------------------------

## 4. Scope

### In Scope

-   Cloud CLI abuse (awscli, az cli, gcloud)
-   API misuse (STS, Graph API, IAM APIs)
-   Identity abuse (role chaining, token theft)
-   Serverless execution abuse
-   CI/CD runner abuse
-   Control plane manipulation
-   Native data exfil via cloud services

### Out of Scope (MVP)

-   Endpoint LOLBAS techniques
-   Malware frameworks
-   Container workload-only exploits

------------------------------------------------------------------------

## 5. Core Functional Requirements

### 5.1 Catalog Schema

Each entry must include:

-   Name
-   Cloud Provider
-   Technique Description
-   Abuse Category
-   MITRE ATT&CK Mapping
-   Example Command or API Usage
-   Telemetry Requirements
-   Detection Guidance
-   Risk Score
-   Mitigation Recommendations

Example YAML:

``` yaml
name: AWS STS AssumeRole Abuse
provider: AWS
description: Abuse of STS AssumeRole to escalate privileges
attack_vector: Identity Abuse
example: aws sts assume-role --role-arn ...
telemetry:
  - CloudTrail AssumeRole events
detection:
  - unusual role chaining
risk_score: 7/10
mitigation:
  - tighten trust policies
  - require MFA
```

------------------------------------------------------------------------

### 5.2 Searchable Explorer

Filter by: - Provider - Risk Score - Technique Category - ATT&CK
Technique - Telemetry Required

------------------------------------------------------------------------

### 5.3 Telemetry & Detection Guidance

Each entry must define: - Required logs (CloudTrail, Azure AD logs, GCP
audit logs) - Minimum telemetry configuration - Detection blind spots -
False positive considerations

------------------------------------------------------------------------

### 5.4 Risk Scoring Model

Risk model dimensions:

-   Privilege required
-   Ease of abuse
-   Impact
-   Detection likelihood
-   Evasion potential

------------------------------------------------------------------------

## 6. Non-Functional Requirements

-   Machine-readable JSON/YAML
-   GitHub Pages compatible
-   Contribution templates
-   Schema validation for PRs
-   Open source license (MIT or Apache 2.0)

------------------------------------------------------------------------

## 7. Success Criteria

-   50+ catalog entries at MVP
-   All entries contain detection guidance
-   Public GitHub adoption
-   ATT&CK mapping coverage
-   Integration examples with SIEM workflows

------------------------------------------------------------------------

## 8. Risks & Mitigation

**Risk:** Cloud API sprawl\
**Mitigation:** Standardized categorization model

**Risk:** Detection variance per provider\
**Mitigation:** Clear provider-specific telemetry documentation

------------------------------------------------------------------------

## 9. Roadmap

Phase 1 -- Schema + 20 entries\
Phase 2 -- Search UI + JSON export\
Phase 3 -- Detection maturity guidance\
Phase 4 -- Risk scoring engine

------------------------------------------------------------------------

## 10. Governance

-   PR templates
-   Issue templates
-   Security disclosure process
-   Code of conduct
