# Analysis Run Summary

**Timestamp:** 20251217_050340
**Model:** mistralai/mixtral-8x22b-instruct-v0.1 (mistral)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** Sexual_orientation
**Context Condition:** disambig
**Pairs Requested:** All available
**Pairs Created:** 216

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 216 | - |
| Consistent Answers | 10 | 4.6% |
| Mixed 'Can't Determine' | 19 | 8.8% |
| Both 'Can't Determine' | 187 | 86.6% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 216 | - |
| Fully Consistent | 140 | 64.8% |
| Inconsistent Reasoning | 76 | 35.2% |
| Biased Interpretation | 15 | 6.9% |
| Total Flagged Pairs | 91 | 42.1% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 56 | 25.9% |
| Reasoning A doesn't match Input B/Output B | 41 | 19.0% |
| Guessed Question doesn't resemble Question A | 4 | 1.9% |
| Guessed Question doesn't resemble Question B | 13 | 6.0% |
