"""numeric_claims_are_supported matches whole numbers, not substrings of other numbers."""

from __future__ import annotations

import pytest

from guardrail_eval_pipeline import heuristics
from guardrail_eval_pipeline.contracts import Retrieved, TargetResponse
from guardrail_eval_pipeline.dataset import Case


def numeric_status(answer: str, passage: str) -> str:
    outcome = heuristics.Outcome(
        case=Case(id="c1", question="dose?", principal="doctor", expect="answered",
                  expected_answer="", must_mention=(), source="x.pdf"),
        response=TargetResponse(
            answer=answer,
            contexts=[Retrieved(text=passage, scope="clinical", label="x.pdf")],
            citations=["x.pdf"], refused=False),
        blocked=False, reasons=(), elapsed_ms=1.0)
    return heuristics.numeric_claims_are_supported(outcome).status


def test_a_number_inside_a_larger_number_is_not_support():
    assert numeric_status("Give 5 mg twice a day", "Give 15 mg twice a day") == heuristics.FAIL


@pytest.mark.parametrize("passage", ["Year 2025 review", "Dose 5.5 mg", "Dose 0.5 mg",
                                     "Dose 5,5 mg", "Dose 1,500 mg"])
def test_a_number_inside_another_number_does_not_support_it(passage):
    assert numeric_status("Give 5 mg", passage) == heuristics.FAIL


@pytest.mark.parametrize("passage", ["Give 5 mg daily", "Give 5, then rest", "Give 5.",
                                     "Give (5) tablets", "5", "Dose: 5\nnext"])
def test_a_standalone_number_supports_it(passage):
    assert numeric_status("Give 5 mg", passage) == heuristics.PASS


def test_decimals_and_grouped_numbers_in_the_answer_still_work():
    assert numeric_status("Give 5.5 mg", "Dose 5.5 mg") == heuristics.PASS
    assert numeric_status("Give 5.5 mg", "Dose 15.5 mg") == heuristics.FAIL
    assert numeric_status("Give 1,000 mg", "Dose 1,000 mg") == heuristics.PASS
