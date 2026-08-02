# Security Policy

## Supported version

The current public edition is version 1.0.

## Reporting a problem

Do not open a public issue containing credentials, private records, personal information, unreleased prompts, real collection data, or exploit details. Contact the repository owner through the private reporting method configured on the hosting account.

## Security boundary

The included Python utility performs local JSON validation only. It has no network integration, credential store, model connection, external action capability, or file-deletion feature.

Projects that add model calls, web access, plugins, databases, or external actions must perform their own threat model and authorization review.

