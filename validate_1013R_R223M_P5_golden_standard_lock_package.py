from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STAGE_ID = "1013R_R223M_P5_GOLDEN_STANDARD_LOCK_PACKAGE"
STANDARD_ID = "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE"


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def load_json(name: str) -> dict:
    return json.loads(read(name))


def main() -> int:
    required = [
        "R223M_P5_golden_standard_lock_report.md",
        "R223M_P5_teacher_default_view_standard.md",
        "R223M_P5_review_ledger_view_standard.md",
        "R223M_P5_classroom_event_schema_lock.json",
        "R223M_P5_control_point_rubric_lock.md",
        "R223M_P5_cross_sample_validation_handoff.md",
        "R223M_P5_teacher_default_reading_sample_v0_1.md",
        "R223M_P5_teacher_default_reading_sample_v0_1.html",
        "R223M_P5_review_ledger_sample_v0_1.json",
        "R223M_P5_source_metadata_normalization.json",
        "README_FOR_GPT_REVIEW.md",
        "PACKAGE_MANIFEST.json",
    ]
    checks = 0
    failures: list[str] = []
    for name in required:
        checks += 1
        if not (ROOT / name).exists():
            failures.append(f"missing:{name}")
    if failures:
        result = {"passed": False, "check_count": checks, "failed": len(failures), "failures": failures, "stage_id": STAGE_ID}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    report = read("R223M_P5_golden_standard_lock_report.md")
    teacher_standard = read("R223M_P5_teacher_default_view_standard.md")
    review_standard = read("R223M_P5_review_ledger_view_standard.md")
    rubric = read("R223M_P5_control_point_rubric_lock.md")
    handoff = read("R223M_P5_cross_sample_validation_handoff.md")
    teacher = read("R223M_P5_teacher_default_reading_sample_v0_1.md")
    html = read("R223M_P5_teacher_default_reading_sample_v0_1.html")
    schema = load_json("R223M_P5_classroom_event_schema_lock.json")
    ledger = load_json("R223M_P5_review_ledger_sample_v0_1.json")
    meta = load_json("R223M_P5_source_metadata_normalization.json")
    manifest = load_json("PACKAGE_MANIFEST.json")

    for phrase in [
        "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1=LOCK_CANDIDATE",
        "TEACHER_DEFAULT_READING_LAYER=ACCEPTED",
        "validator_checks=59",
        "source_zip_sha256",
        "formal_ui=blocked",
    ]:
        checks += 1
        if phrase not in report:
            failures.append(f"report_missing:{phrase}")

    for phrase in ["默认可见结构", "默认隐藏 / 降权", "完整小教判断四项", "不压进老师默认正文"]:
        checks += 1
        if phrase not in teacher_standard:
            failures.append(f"teacher_standard_missing:{phrase}")

    for phrase in ["审核视图不替代教师默认稿", "Ledger 必备字段", "component_trigger", "evidence_trigger"]:
        checks += 1
        if phrase not in review_standard:
            failures.append(f"review_standard_missing:{phrase}")

    for phrase in ["pass_line=20", "lock_candidate_line=23", "current_sample_score=23/25", "教师默认稿连续可读"]:
        checks += 1
        if phrase not in rubric:
            failures.append(f"rubric_missing:{phrase}")

    for sample in ["有趣的纸印", "色彩", "有趣的文字和图画", "会说话的手", "不把《我为文具代言》的文具内容迁移"]:
        checks += 1
        if sample not in handoff:
            failures.append(f"handoff_missing:{sample}")

    for phrase in ["【教师关注】", "【下游影响】"]:
        checks += 1
        count = teacher.count(phrase)
        if count != 7:
            failures.append(f"teacher_count:{phrase}:{count}")

    for heavy in ["【小教判断】", "核心：", "风险：", "建议动作：", "确认点："]:
        checks += 1
        if heavy in teacher:
            failures.append(f"heavy_default_note:{heavy}")

    for token in ["data-note-weight=\"reduced\"", "data-preview-only=\"true\"", "data-teacher-confirmed=\"false\""]:
        checks += 1
        if token not in html:
            failures.append(f"html_missing_state:{token}")

    checks += 1
    if schema.get("x_standard_id") != STANDARD_ID:
        failures.append("schema_standard_mismatch")
    checks += 1
    if not schema.get("x_view_layers", {}).get("teacher_default_reading_layer", {}).get("accepted"):
        failures.append("schema_teacher_layer_not_accepted")
    checks += 1
    if schema.get("x_boundary", {}).get("formal_apply_allowed") is not False:
        failures.append("schema_formal_apply_not_false")

    checks += 1
    if len(ledger.get("events", [])) != 7:
        failures.append("ledger_event_count_not_7")

    for event in ledger.get("events", []):
        checks += 1
        if not event.get("default_teacher_visible", {}).get("teacher_focus"):
            failures.append(f"ledger_missing_teacher_focus:{event.get('event_id')}")
        checks += 1
        if not event.get("review_view_only", {}).get("xiaojiao_judgement_full"):
            failures.append(f"ledger_missing_full_judgement:{event.get('event_id')}")

    checks += 1
    if meta.get("source_stages", {}).get("R223M_P4_P1", {}).get("validator_checks") != 59:
        failures.append("metadata_checks_not_59")
    checks += 1
    if meta.get("lock_decision", {}).get("golden_standard") != "LOCK_CANDIDATE":
        failures.append("metadata_lock_decision_mismatch")

    checks += 1
    if manifest.get("stage_id") != STAGE_ID:
        failures.append("manifest_stage_mismatch")
    checks += 1
    if manifest.get("boundary", {}).get("formal_ui") is not False:
        failures.append("manifest_formal_ui_not_false")
    checks += 1
    if manifest.get("boundary", {}).get("r97b_modified") is not False:
        failures.append("manifest_r97b_modified_not_false")

    for token in ["???", "锟", "\ufffd"]:
        checks += 1
        if token in html:
            failures.append(f"mojibake:{token}")

    result = {
        "passed": not failures,
        "check_count": checks,
        "failed": len(failures),
        "failures": failures,
        "stage_id": STAGE_ID,
        "standard_id": STANDARD_ID,
        "teacher_focus_count": teacher.count("【教师关注】"),
        "downstream_impact_count": teacher.count("【下游影响】"),
        "source_validator_checks": meta.get("source_stages", {}).get("R223M_P4_P1", {}).get("validator_checks"),
        "formal_ui": "blocked",
    }
    (ROOT / "validate_1013R_R223M_P5_golden_standard_lock_package_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
