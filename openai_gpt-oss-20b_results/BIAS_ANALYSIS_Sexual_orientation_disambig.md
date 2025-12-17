# Oracle Analysis esults

## Configuration
- **Model**: openai/gpt-oss-20b
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Sexual_orientation
- **Context Condition**: disambig
- **Analysis Timestamp**: 2025-12-17 06:38:55

## Summary Statistics
- **Total Pairs Analyzed**: 216
- **Fully Consistent Pairs**: 113 (52.3%)
- **Inconsistent Reasoning Pairs**: 103 (47.7%)
- **Biased Interpretation Pairs**: 1 (0.5%)
- **Total Flagged Pairs**: 104 (48.1%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 69 | 31.9% |
| Reasoning A doesn't match Input B/Output B | 57 | 26.4% |
| Did not guess Question A correctly (expected x) | 0 | 0.0% |
| Did not guess Question B correctly (expected y) | 1 | 0.5% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
