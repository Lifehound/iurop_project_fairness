# Oracle Analysis esults

## Configuration
- **Model**: mistralai/mixtral-8x22b-instruct-v0.1
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Sexual_orientation
- **Context Condition**: disambig
- **Analysis Timestamp**: 2025-12-17 05:03:40

## Summary Statistics
- **Total Pairs Analyzed**: 216
- **Fully Consistent Pairs**: 140 (64.8%)
- **Inconsistent Reasoning Pairs**: 76 (35.2%)
- **Biased Interpretation Pairs**: 15 (6.9%)
- **Total Flagged Pairs**: 91 (42.1%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 56 | 25.9% |
| Reasoning A doesn't match Input B/Output B | 41 | 19.0% |
| Did not guess Question A correctly (expected x) | 4 | 1.9% |
| Did not guess Question B correctly (expected y) | 13 | 6.0% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
