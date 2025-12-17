# Oracle Analysis esults

## Configuration
- **Model**: mistralai/mixtral-8x22b-instruct-v0.1
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Sexual_orientation
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-17 04:58:17

## Summary Statistics
- **Total Pairs Analyzed**: 216
- **Fully Consistent Pairs**: 195 (90.3%)
- **Inconsistent Reasoning Pairs**: 21 (9.7%)
- **Biased Interpretation Pairs**: 116 (53.7%)
- **Total Flagged Pairs**: 137 (63.4%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 11 | 5.1% |
| Reasoning A doesn't match Input B/Output B | 15 | 6.9% |
| Did not guess Question A correctly (expected x) | 33 | 15.3% |
| Did not guess Question B correctly (expected y) | 102 | 47.2% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
