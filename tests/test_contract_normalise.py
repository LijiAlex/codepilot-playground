"""Contract with downstream consumers: normalise() strips citation markers and keeps the original case."""
from guardrail_eval_pipeline.guardrails.bedrock import normalise


def test_normalise_keeps_case():
    assert normalise("Ward B uses PROC-RAD-01 【1†L1-L3】") == "Ward B uses PROC-RAD-01 "
