# Semantic Verification Summary

## Input Evidence

- IR: `sm_master.ir.json`
- Trace: `sm_master.trace.json`
- `is_reliable`: `true`
- Diagnostics: `none`

## Verdict

- `BLOCKED`
- Reason: Generated scaffold requires runtime location review and semantic confirmation before PASS.

## Hierarchy Check

- Status: `BLOCKED`
- Roots: `inactive`, `active`
- Parent chains:
- `active/idle -> active`
- `active/routing -> active`
- `active/routing/successful -> active/routing`
- `active/delegating -> active`
- `active/working -> active`
- Notes:
- Confirm that each runtime preserves the same parent-child hierarchy.

## Init Check

- Status: `BLOCKED`
- `top_initial`: `TOP -> inactive`
- Composite initials:
- `active -> active/idle`
- Trace alignment: `true`
- Notes:
- Confirm init ordering against the trace JSON before marking PASS.

## Transition Check

- `inactive::USER_SLASH_COMMAND_MASTER#0` `BLOCKED`: `inactive --USER_SLASH_COMMAND_MASTER--> active`
- Effect: `none`
- Target locations:
- `ts_hsm`: `SM_MasterInactiveState.handle`
- `sm_hsm`: `SM_Master_inactive_`
- `rs_hsm_`: `SM_Master_inactive_`
- Notes:
- Trace-derived external transition; confirm locations and effect handling before marking PASS.
- `active::USER_SLASH_COMMAND_MASTER#0` `BLOCKED`: `active --USER_SLASH_COMMAND_MASTER--> inactive`
- Effect: `none`
- Target locations:
- `ts_hsm`: `SM_MasterActiveState.handle`
- `sm_hsm`: `SM_Master_active_`
- `rs_hsm_`: `SM_Master_active_`
- Notes:
- Trace-derived external transition; confirm locations and effect handling before marking PASS.
- `active/idle::USER_INPUT_PROMPTS#0` `BLOCKED`: `active/idle --USER_INPUT_PROMPTS--> active/routing`
- Effect: `event.inputEvtResult = { action: "continue" };`
- Target locations:
- `ts_hsm`: `SM_MasterIdleState.handle`
- `sm_hsm`: `SM_Master_idle_`
- `rs_hsm_`: `SM_Master_idle_`
- Notes:
- Trace-derived external transition; confirm locations and effect handling before marking PASS.
- `active/routing::TOOL_RESULT#2` `BLOCKED`: `active/routing --TOOL_RESULT--> active/routing/successful`
- Effect: `review guarded branches`
- Target locations:
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- Notes:
- This choice transition has at least one external branch; verify branch-level mappings in choice_checks.
- `active/routing/successful::AGENT_END#0` `BLOCKED`: `active/routing/successful --AGENT_END--> active/delegating`
- Effect: `none`
- Target locations:
- `ts_hsm`: `SM_MasterSuccessfulState.handle`
- `sm_hsm`: `SM_Master_successful_`
- `rs_hsm_`: `SM_Master_successful_`
- Notes:
- Trace-derived external transition; confirm locations and effect handling before marking PASS.
- `active/delegating::TIMEOUT#0` `BLOCKED`: `active/delegating --TIMEOUT--> active/working`
- Effect: `review guarded branches`
- Target locations:
- `ts_hsm`: `SM_MasterDelegatingState.handle`
- `sm_hsm`: `SM_Master_delegating_`
- `rs_hsm_`: `SM_Master_delegating_`
- Notes:
- This choice transition has at least one external branch; verify branch-level mappings in choice_checks.
- `active/working::AGENT_END#1` `BLOCKED`: `active/working --AGENT_END--> active/idle`
- Effect: `// 单轮工作结束，后续循环工作流可在此触发（当前直接回到idle，等待用户触发）`
- Target locations:
- `ts_hsm`: `SM_MasterWorkingState.handle`
- `sm_hsm`: `SM_Master_working_`
- `rs_hsm_`: `SM_Master_working_`
- Notes:
- Trace-derived external transition; confirm locations and effect handling before marking PASS.

## Choice Check

- `active/routing::TOOL_CALL#1` `BLOCKED`
- `[validDispatchToolCall()]` `internal` `handled with side effect`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- `[else]` `internal` `handled with side effect`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- Notes:
- Review each generated branch and replace inferred runtime locations if they differ from the implementation.
- `active/routing::TOOL_RESULT#2` `BLOCKED`
- `[subagentBlockFormatValid()]` `external` `active/routing/successful`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- `[else]` `internal` `handled with side effect`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- Notes:
- Review each generated branch and replace inferred runtime locations if they differ from the implementation.
- `active/delegating::TIMEOUT#0` `BLOCKED`
- `[areAllSubagentsDone(me.subagentBlocks)]` `external` `active/working`
- `ts_hsm`: `SM_MasterDelegatingState.handle`
- `sm_hsm`: `SM_Master_delegating_`
- `rs_hsm_`: `SM_Master_delegating_`
- `[else]` `internal` `handled with side effect`
- `ts_hsm`: `SM_MasterDelegatingState.handle`
- `sm_hsm`: `SM_Master_delegating_`
- `rs_hsm_`: `SM_Master_delegating_`
- Notes:
- Review each generated branch and replace inferred runtime locations if they differ from the implementation.

## Delegation Check

- `inactive` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to TOP.
- `active` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to TOP.
- `active/idle` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to active.
- `active/routing` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to active.
- `active/routing/successful` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to active/routing.
- `active/delegating` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to active.
- `active/working` `DEFAULT` `BLOCKED`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Review default delegation path to active.

## Adaptations

- `none`

## Blockers

- Replace inferred runtime locations with reviewed implementation locations.
- Review every BLOCKED section and item before marking the report PASS.

