# Oracle Analysis esults

## Configuration
- **Model**: openai/gpt-oss-20b
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: SES
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-17 02:15:17

## Summary Statistics
- **Total Pairs Analyzed**: 1488
- **Fully Consistent Pairs**: 652 (43.8%)
- **Inconsistent Reasoning Pairs**: 836 (56.2%)
- **Biased Interpretation Pairs**: 12 (0.8%)
- **Total Flagged Pairs**: 848 (57.0%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 461 | 31.0% |
| Reasoning A doesn't match Input B/Output B | 700 | 47.0% |
| Did not guess Question A correctly (expected x) | 7 | 0.5% |
| Did not guess Question B correctly (expected y) | 5 | 0.3% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
