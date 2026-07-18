# Core Practice Skills Evaluation

## `brainstorming`

### Control Run

The control agents did not read a brainstorming Skill. All three accepted
pressure to proceed and silently selected material behavior:

- Smart mode: “我按 20 分钟可演示的最小方案直接开始。” It selected a global
  flag, per-user persistence, silent fallback, and precedence rules without a
  design decision from the user.
- Dashboard: “我先按以下可回退假设推进：仪表盘只读” and would fall back to
  mock data while the meaning and source of status remained unresolved.
- Offline sync: “我现在按‘单开关、原模块内最小闭环’直接推进” and selected
  tombstones, three-way merge, deterministic conflict ordering, and no conflict
  prompt without confirming product semantics.

Observed failure: good implementation hygiene did not prevent hidden product
decisions. The Skill must require an explicit design surface before edits while
allowing a prior bounded delegation to count as approval.

### Forward Run

All three agents explicitly loaded the formal Skill and stopped before edits:

- Smart mode inspected the actual workspace, found no CLI entry point, and
  asked only for the target path before applying the user's delegated defaults.
- Dashboard identified that the current repository contains no application,
  runtime, data model, or API and asked for the correct project path.
- Offline sync separated the visible toggle from irreversible merge semantics,
  refused to invent tombstones or conflict ordering, and asked only for the
  desktop client path while treating conflict-policy delegation as approval.

Result: PASS. The forward runs made evidence, hidden decisions, and approval
state explicit without restoring the upstream visual or suite dependencies.

## `test-driven-development`

### Control Run

One control independently kept a failing regression test first. The two higher
pressure controls accepted tests-after:

- Existing implementation: “本轮不重构、不删除现有实现，也不新增测试或补覆盖率”
  and would change the retry constant before a behavioral test.
- Manager-approved one-line fix: “不新增专门的失败用例” and would rely on the
  fastest existing check before claiming the timeout change fixed.

Observed failure: verification discipline alone did not preserve test-first
order under sunk-cost, authority, and urgency pressure.

### Forward Run

All three agents loaded the formal Skill and preserved RED before production
changes:

- The empty-email fix required a minimal regression test that failed for the
  observed defect before modifying the validation boundary.
- The retry case explicitly rejected keeping the untested 200-line
  implementation as reference and requested authority before deleting it.
- The timeout case distinguished production behavior from a configuration
  exception, required a failing targeted test for behavior, and refused to say
  `fixed` without fresh evidence.

Result: PASS. Moving the anti-pattern reference under `references/` did not
weaken the upstream RED-GREEN-REFACTOR behavior.
