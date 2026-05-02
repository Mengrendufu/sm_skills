# Semantic Verification Summary

## Input Evidence

- IR: `assets/examples/sm-master/sm_master.ir.json`
- Trace: `assets/examples/sm-master/sm_master.trace.txt`
- `is_reliable`: `true`
- Diagnostics: `none`

## Verdict

- `PASS`
- Reason: The TypeScript, C, and Rust examples preserve the strict IR hierarchy, init behavior, guarded choices, and delegation structure.

## Hierarchy Check

- Status: `PASS`
- Roots: `inactive`, `active`
- Parent chains:
- `active/idle -> active`
- `active/routing -> active`
- `active/routing/successful -> active/routing`
- `active/delegating -> active`
- `active/working -> active`
- Notes:
- All three targets preserve the same state tree without flattening active/routing/successful.

## Init Check

- Status: `PASS`
- `top_initial`: `TOP -> inactive`
- Composite initials:
- `active -> active/idle`
- Trace alignment: `true`
- Notes:
- The parser trace confirms inactive --USER_SLASH_COMMAND_MASTER--> active, followed by active -> active/idle.

## Transition Check

- `inactive::USER_SLASH_COMMAND_MASTER#0` `PASS`: `inactive --USER_SLASH_COMMAND_MASTER--> active`
- Effect: `none`
- Target locations:
- `ts_hsm`: `SM_MasterInactiveState.handle`
- `sm_hsm`: `SM_Master_inactive_`
- `rs_hsm_`: `SM_Master_inactive_`
- `active/idle::USER_INPUT_PROMPTS#0` `PASS`: `active/idle --USER_INPUT_PROMPTS--> active/routing`
- Effect: `preserves inputEvtResult = continue`
- Target locations:
- `ts_hsm`: `SM_MasterIdleState.handle`
- `sm_hsm`: `SM_Master_idle_`
- `rs_hsm_`: `SM_Master_idle_`
- `active/routing/successful::AGENT_END#0` `PASS`: `active/routing/successful --AGENT_END--> active/delegating`
- Effect: `none`
- Target locations:
- `ts_hsm`: `SM_MasterSuccessfulState.handle`
- `sm_hsm`: `SM_Master_successful_`
- `rs_hsm_`: `SM_Master_successful_`
- `active/working::AGENT_END#1` `PASS`: `active/working --AGENT_END--> active/idle`
- Effect: `preserves the round-complete action slot as target-language helper behavior or trace note`
- Target locations:
- `ts_hsm`: `SM_MasterWorkingState.handle`
- `sm_hsm`: `SM_Master_working_`
- `rs_hsm_`: `SM_Master_working_`

## Choice Check

- `active/routing::TOOL_CALL#1` `PASS`
- `[validDispatchToolCall()]` `internal` `handled`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- `[else]` `internal` `handled with protocol reminder`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- `active/routing::TOOL_RESULT#2` `PASS`
- `[subagentBlockFormatValid()]` `external` `active/routing/successful`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- `[else]` `internal` `handled with protocol reminder`
- `ts_hsm`: `SM_MasterRoutingState.handle`
- `sm_hsm`: `SM_Master_routing_`
- `rs_hsm_`: `SM_Master_routing_`
- `active/delegating::TIMEOUT#0` `PASS`
- `[areAllSubagentsDone(me.subagentBlocks)]` `external` `active/working`
- `ts_hsm`: `SM_MasterDelegatingState.handle`
- `sm_hsm`: `SM_Master_delegating_`
- `rs_hsm_`: `SM_Master_delegating_`
- `[else]` `internal` `handled with monitoring side effects`
- `ts_hsm`: `SM_MasterDelegatingState.handle`
- `sm_hsm`: `SM_Master_delegating_`
- `rs_hsm_`: `SM_Master_delegating_`

## Delegation Check

- `inactive` `DEFAULT` `PASS`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- `active` `DEFAULT` `PASS`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- USER_SLASH_COMMAND_MASTER and USER_INPUT_PROMPTS are owned locally; remaining events still delegate.
- `active/routing/successful` `DEFAULT` `PASS`
- `ts_hsm`: `superState()`
- `sm_hsm`: `_SM_SUPER()`
- `rs_hsm_`: `SM_RetState::Super`
- Notes:
- Only AGENT_END is owned locally; remaining events delegate to active/routing.

## Adaptations

- Helper calls such as notifyWarning, sendProtocolReminder, dispatchAllSubagents, and sendSubagentCompletionSummary remain placeholders or stubs in the target runtimes, but the action slots are preserved rather than deleted.

