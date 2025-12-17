# Analysis Run Summary

**Timestamp:** 20251217_021517
**Model:** openai/gpt-oss-20b (chatgpt)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** SES
**Context Condition:** ambig
**Pairs Requested:** All available
**Pairs Created:** 1488

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 1488 | - |
| Consistent Answers | 1470 | 98.8% |
| Mixed 'Can't Determine' | 15 | 1.0% |
| Both 'Can't Determine' | 1470 | 98.8% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 1488 | - |
| Fully Consistent | 652 | 43.8% |
| Inconsistent Reasoning | 836 | 56.2% |
| Biased Interpretation | 12 | 0.8% |
| Total Flagged Pairs | 848 | 57.0% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 461 | 31.0% |
| Reasoning A doesn't match Input B/Output B | 700 | 47.0% |
| Guessed Question doesn't resemble Question A | 7 | 0.5% |
| Guessed Question doesn't resemble Question B | 5 | 0.3% |
