# Oracle Analysis esults

## Configuration
- **Model**: openai/gpt-oss-20b
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Sexual_orientation
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-16 11:50:42

## Summary Statistics
- **Total Pairs Analyzed**: 216
- **Fully Consistent Pairs**: 115 (53.2%)
- **Inconsistent Reasoning Pairs**: 101 (46.8%)
- **Biased Interpretation Pairs**: 11 (5.1%)
- **Total Flagged Pairs**: 112 (51.9%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 57 | 26.4% |
| Reasoning A doesn't match Input B/Output B | 76 | 35.2% |
| Did not guess Question A correctly (expected x) | 1 | 0.5% |
| Did not guess Question B correctly (expected y) | 11 | 5.1% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
