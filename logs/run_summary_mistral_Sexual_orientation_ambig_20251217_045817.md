# Analysis Run Summary

**Timestamp:** 20251217_045817
**Model:** mistralai/mixtral-8x22b-instruct-v0.1 (mistral)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** Sexual_orientation
**Context Condition:** ambig
**Pairs Requested:** All available
**Pairs Created:** 216

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 216 | - |
| Consistent Answers | 207 | 95.8% |
| Mixed 'Can't Determine' | 9 | 4.2% |
| Both 'Can't Determine' | 207 | 95.8% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 216 | - |
| Fully Consistent | 195 | 90.3% |
| Inconsistent Reasoning | 21 | 9.7% |
| Biased Interpretation | 116 | 53.7% |
| Total Flagged Pairs | 137 | 63.4% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 11 | 5.1% |
| Reasoning A doesn't match Input B/Output B | 15 | 6.9% |
| Guessed Question doesn't resemble Question A | 33 | 15.3% |
| Guessed Question doesn't resemble Question B | 102 | 47.2% |
