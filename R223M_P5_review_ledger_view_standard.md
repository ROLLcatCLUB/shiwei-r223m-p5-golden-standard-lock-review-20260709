# R223M-P5 审核视图 / Ledger 标准

```text
stage_id=1013R_R223M_P5_GOLDEN_STANDARD_LOCK_PACKAGE
review_ledger_view=LOCKED_AS_COMPANION_LAYER
default_teacher_view_must_not_show_full_ledger=true
```

## 审核视图职责

审核视图不替代教师默认稿。它用于高级教师、GPT 或开发复核：

- 课堂事件是否符合来源；
- 学生可能反应是否真实；
- 教师追问和补救是否具体；
- 大屏、组件、学习单、评价证据是否有触发点；
- 预览确认门是否守住。

## Ledger 必备字段

每个 event 至少保留：

- event_id / event_name；
- default_teacher_visible.teacher_focus；
- default_teacher_visible.downstream_impact；
- review_view_only.xiaojiao_judgement_full；
- review_view_only.control_points_full；
- review_view_only.screen_trigger；
- review_view_only.component_trigger；
- review_view_only.learning_sheet_trigger；
- review_view_only.evidence_trigger。
