# Oracle Analysis esults

## Configuration
- **Model**: mistralai/mixtral-8x22b-instruct-v0.1
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: SES
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-16 20:05:38

## Summary Statistics
- **Total Pairs Analyzed**: 1488
- **Fully Consistent Pairs**: 1103 (74.1%)
- **Inconsistent Reasoning Pairs**: 385 (25.9%)
- **Biased Interpretation Pairs**: 914 (61.4%)
- **Total Flagged Pairs**: 1299 (87.3%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 185 | 12.4% |
| Reasoning A doesn't match Input B/Output B | 380 | 25.5% |
| Did not guess Question A correctly (expected x) | 96 | 6.5% |
| Did not guess Question B correctly (expected y) | 884 | 59.4% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
