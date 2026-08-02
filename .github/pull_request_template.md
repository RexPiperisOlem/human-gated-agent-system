## Change

Describe the smallest useful change and the affected agent contract.

## Evidence

Describe the fictional or anonymized failure case that supports the change.

## Safety checks

- [ ] No private source material, personal data, credentials, real collection records, or production assets are included.
- [ ] Agent boundaries and human gates remain explicit.
- [ ] Tests were added or updated when behavior changed.
- [ ] `python scripts/repository_check.py` passes.
- [ ] `python -m unittest discover -s tests -v` passes with `PYTHONPATH=src`.

