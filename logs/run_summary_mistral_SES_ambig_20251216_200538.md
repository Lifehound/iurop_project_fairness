# Analysis Run Summary

**Timestamp:** 20251216_200538
**Model:** mistralai/mixtral-8x22b-instruct-v0.1 (mistral)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** SES
**Context Condition:** ambig
**Pairs Requested:** All available
**Pairs Created:** 1488

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 1488 | - |
| Consistent Answers | 1434 | 96.4% |
| Mixed 'Can't Determine' | 53 | 3.6% |
| Both 'Can't Determine' | 1434 | 96.4% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 1488 | - |
| Fully Consistent | 1103 | 74.1% |
| Inconsistent Reasoning | 385 | 25.9% |
| Biased Interpretation | 914 | 61.4% |
| Total Flagged Pairs | 1299 | 87.3% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 185 | 12.4% |
| Reasoning A doesn't match Input B/Output B | 380 | 25.5% |
| Guessed Question doesn't resemble Question A | 96 | 6.5% |
| Guessed Question doesn't resemble Question B | 884 | 59.4% |
