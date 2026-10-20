"""Contract with downstream consumers: normalise() strips citation markers and lower-cases text."""
from guardrail_eval_pipeline.guardrails.bedrock import normalise


def test_normalise_returns_lower_case():
    assert normalise("Ward B uses PROC-RAD-01 【1†L1-L3】") == "ward b uses proc-rad-01 "
    assert normalise("Ward B") == "ward b"

