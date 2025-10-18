# Weighted Assertions Calculator

A simple Streamlit app to help students understand how weighted assertions work in promptfoo evaluations.

## Features

- **Interactive Calculator**: Add, edit, and remove assertions with custom scores and weights
- **Real-time Calculations**: See how weighted aggregate scores are computed
- **Visual Analytics**: Charts and graphs showing individual contributions and overall results
- **Educational Examples**: Pre-built examples from promptfoo documentation
- **Mathematical Breakdown**: Step-by-step calculation explanations

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## How It Works

The calculator demonstrates the weighted assertion formula used in promptfoo:

```
Aggregate Score = Σ(Score × Weight) ÷ Σ(Weight)
```

A test passes when:
```
Aggregate Score ≥ Test Threshold
```

## Example: French Greeting Test

Based on the promptfoo documentation example:

| Assertion | Score | Weight | Weighted Contribution | Status |
|-----------|-------|--------|----------------------|--------|
| Correctness | 1.00 | 2 | 2.00 | ✅ PASS |
| Tone | 1.00 | 1 | 1.00 | ✅ PASS |
| Topicality | 0.50 | 1 | 0.50 | ❌ FAIL |
| Greeting | 1.00 | 1 | 1.00 | ✅ PASS |
| Performance | 0.00 | 2 | 0.00 | ❌ FAIL |

**Calculation:**
- Total Weighted Score: 2.00 + 1.00 + 0.50 + 1.00 + 0.00 = 4.50
- Total Weights: 2 + 1 + 1 + 1 + 2 = 7
- Aggregate Score: 4.50 ÷ 7 = 0.64
- Result: 0.64 ≥ 0.6 threshold = ✅ **PASS**

Even though 2 out of 5 assertions failed, the test passes because the high-weighted passing assertions compensate for the failing ones.

## Educational Value

This tool helps students understand:

1. **Weighted Scoring**: How different metrics can have different importance
2. **Aggregate Logic**: How individual failures don't necessarily mean test failure
3. **Threshold Management**: How to set appropriate pass/fail criteria
4. **Visual Learning**: Interactive charts and step-by-step calculations

## Built With

- [Streamlit](https://streamlit.io/) - Web app framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [NumPy](https://numpy.org/) - Numerical computing

## References

Based on the [promptfoo weighted assertions documentation](https://www.promptfoo.dev/docs/configuration/expected-outputs/#weighted-assertions).
