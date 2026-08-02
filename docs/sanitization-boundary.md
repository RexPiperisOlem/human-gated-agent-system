# Sanitization Boundary

This public edition was rebuilt from architectural principles rather than copied from a production system.

## Included

- Twelve-agent role separation.
- Human-gated dispatch, intake, work-order, quality, provenance, and patch loops.
- A generic collection-management branch.
- A generic voice-and-style routing shell.
- Neutral record templates, fictional examples, validation code, and repository checks.

## Excluded

- Private operating manuals and source documents.
- Brand names, doctrine, slogans, imagery, and proprietary creative systems.
- Personal identity, health, accessibility, location, relationship, or financial information.
- Personal voice models, real writing samples, and private calibration rules.
- Real products, recipes, campaigns, customers, collaborators, collection objects, images, identifiers, and storage locations.
- Live storefront, email, platform, account, analytics, and payment details.
- Original production ledgers, file paths, runner code, examples, and package metadata.
- Credentials, tokens, account identifiers, and external-system permissions.

## Clean-room rules for future contributions

1. Use fictional or fully anonymized examples.
2. Do not paste private prompts into issues or pull requests.
3. Re-express general methods in new language.
4. Keep personal and brand style profiles in ignored local folders.
5. Run `python scripts/repository_check.py` before every public release.
6. Perform an independent human review of the final staged Git diff.

