# R223M-P5 黄金标准锁定报告

```text
stage_id=1013R_R223M_P5_GOLDEN_STANDARD_LOCK_PACKAGE
standard_id=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
R223M-P4_SIGNAL_INTEGRATION=PASS
R223M-P4-P1=PASS_NOTE_WEIGHT_REDUCTION_AND_MARGINIZATION
TEACHER_DEFAULT_READING_LAYER=ACCEPTED
GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1=LOCK_CANDIDATE
formal_ui=blocked
R97B / UI / runtime / prompt / model / db = untouched
```

## 锁定内容

- 教师默认阅读样本：`R223M_P5_teacher_default_reading_sample_v0_1.md/html`
- 审核 ledger 样本：`R223M_P5_review_ledger_sample_v0_1.json`
- 课堂事件 schema：`R223M_P5_classroom_event_schema_lock.json`
- 25 分审核规准：`R223M_P5_control_point_rubric_lock.md`
- 默认视图 / 审核视图分层规则：`R223M_P5_teacher_default_view_standard.md` 与 `R223M_P5_review_ledger_view_standard.md`

## 元数据归一化

P4-P1 的 `R223M_P4_P1_report.md` 中曾记录 `validator_checks=26`，这是生成脚本内置轻校验结果；标准锁定以独立 validator 结果为准：

```text
source_validator_checks=59
source_validator_failed=0
source_zip_sha256=169CB15405384AAF732D76EE427DF408D229A49B990CB9AD59ED4846FFF59C92
```

P5 自身 validator 结果以 `validate_1013R_R223M_P5_golden_standard_lock_package_result.json` 为准。

## 当前边界

本包不继续打磨《我为文具代言》正文，不进入 UI，不修改 R97B，不接 runtime/model/prompt/db，不 formal apply。下一步应转向跨样本验证。
