# Research & novelty statement

## Research question
Can an explicit claim-to-action relationship layer help flag deceptive requests that use an apparently legitimate institutional claim as justification?

## Related directions
- FEVER: https://fever.ai/dataset/fever.html — claim verification benchmark.
- FEVEROUS: https://fever.ai/dataset/feverous.html — evidence across text/tables.
- OWASP guidance: https://owasp.org/www-project-top-ten/

No claim of a globally novel algorithm is made. Claim-to-action transfer detection is a prototype hypothesis, not a validated research finding.

## Reproducibility
Run `python scripts/evaluate.py` and read `docs/evaluation_results.json`. The synthetic dataset is deliberately authored; reported metrics are *only* performance on this synthetic dataset and may be inflated by overlap with the rules and phrasing.

## Next steps
Add independent human-labeled, naturally written messages, freeze held-out samples, compare realistic ML baselines, use inter-annotator agreement, report uncertainty, and perform subgroup analysis by dialect.
