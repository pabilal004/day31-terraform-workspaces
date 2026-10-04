# Terraform Workspaces & Environment Management

## Overview

This project demonstrates how Terraform Workspaces can manage multiple environments using one Terraform configuration.

The same configuration is used for:
- dev
- staging
- production

Each workspace has its own Terraform state, providing isolation between environments.

## Prerequisites

- Terraform installed
- Basic Terraform knowledge
- Local Terraform provider

## Configuration

The project uses the Terraform `local` provider to create a text file named after the active workspace.

Example:

```text
Environment: dev
Managed by Terraform Workspace
```

## Commands

Initialize Terraform:

```bash
terraform init
```

Create workspaces:

```bash
terraform workspace new dev
terraform workspace new staging
terraform workspace new production
```

List workspaces:

```bash
terraform workspace list
```

Show the current workspace:

```bash
terraform workspace show
```

Switch environments:

```bash
terraform workspace select dev
terraform workspace select staging
terraform workspace select production
```

Plan and apply:

```bash
terraform plan
terraform apply
```

## Expected Result

When each workspace is applied, Terraform creates a separate output file:

- `dev` -> `dev.txt`
- `staging` -> `staging.txt`
- `production` -> `production.txt`

## Key Concept

**Terraform Workspace = separate Terraform state for the same configuration.**

This allows the same Terraform code to be reused across environments while keeping their states isolated.

## Verification

```bash
terraform workspace list
terraform workspace show
```

The active workspace is marked with `*`.

## Cleanup

To remove resources from the active workspace:

```bash
terraform destroy
```

Repeat for other workspaces if required.

## Git Notes

Terraform state, the `.terraform/` directory, plan files, and generated environment output files are intentionally ignored.

The Terraform dependency lock file `.terraform.lock.hcl` should be committed when generated locally.
