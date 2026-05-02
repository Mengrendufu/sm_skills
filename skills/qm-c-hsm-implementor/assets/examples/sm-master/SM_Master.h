#ifndef SM_MASTER_EXAMPLE_H_
#define SM_MASTER_EXAMPLE_H_

#include "sm_hsm.h"

enum SM_MasterSig {
    SM_Master_dummy = 0,
    USER_SLASH_COMMAND_MASTER_SIG,
    USER_INPUT_PROMPTS_SIG,
    BEFORE_AGENT_START_SIG,
    TOOL_CALL_SIG,
    TOOL_RESULT_SIG,
    AGENT_END_SIG,
    TIMEOUT_SIG,
    SM_Master_max
};

typedef struct {
    uint8_t sig;
} SM_MasterEvt;

#define SM_MASTER_SIG(evt_) ((evt_)->sig)

typedef struct {
    SM_Hsm sm_hsm_;
    VC_Handler init;
    VC_Handler dispatch;
    uint8_t allowDispatchToolCall;
    uint8_t validSubagentBlock;
    uint8_t allSubagentsDone;
    char const * inputEvtResult;
} SM_Master;

static void SM_Master_loadAgent_(SM_Master * const me);
static void SM_Master_updateStatus_(SM_Master * const me, char const * status);
static void SM_Master_notifyWarning_(SM_Master * const me, char const * message);
static void SM_Master_sendProtocolReminder_(SM_Master * const me, char const * message);
static void SM_Master_dispatchAllSubagents_(SM_Master * const me);
static void SM_Master_armTimeout_(SM_Master * const me);
static void SM_Master_monitorSubagents_(SM_Master * const me);
static void SM_Master_sendSubagentCompletionSummary_(SM_Master * const me);
static uint8_t validDispatchToolCall_(SM_Master * const me);
static uint8_t subagentBlockFormatValid_(SM_Master * const me);
static uint8_t areAllSubagentsDone_(SM_Master * const me);

static SM_StatePtr SM_Master_TOP_initial_(SM_Hsm * const me) SM_HSM_RETT;

static void SM_Master_inactive_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_inactive_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_inactive_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

static SM_StatePtr SM_Master_active_init_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_active_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_active_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_active_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

static void SM_Master_idle_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_idle_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_idle_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

static void SM_Master_routing_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_routing_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_routing_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

static void SM_Master_successful_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_successful_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_successful_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

static void SM_Master_delegating_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_delegating_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_delegating_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

static void SM_Master_working_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void SM_Master_working_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState SM_Master_working_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT;

SM_HsmState SM_HSM_ROM SM_Master_inactive = {
    (SM_StatePtr)NULL,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&SM_Master_inactive_entry_,
    (SM_ActionHandler)&SM_Master_inactive_exit_,
    (SM_StateHandler)&SM_Master_inactive_
};

SM_HsmState SM_HSM_ROM SM_Master_active = {
    (SM_StatePtr)NULL,
    (SM_InitHandler)&SM_Master_active_init_,
    (SM_ActionHandler)&SM_Master_active_entry_,
    (SM_ActionHandler)&SM_Master_active_exit_,
    (SM_StateHandler)&SM_Master_active_
};

SM_HsmState SM_HSM_ROM SM_Master_idle = {
    (SM_StatePtr)&SM_Master_active,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&SM_Master_idle_entry_,
    (SM_ActionHandler)&SM_Master_idle_exit_,
    (SM_StateHandler)&SM_Master_idle_
};

SM_HsmState SM_HSM_ROM SM_Master_routing = {
    (SM_StatePtr)&SM_Master_active,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&SM_Master_routing_entry_,
    (SM_ActionHandler)&SM_Master_routing_exit_,
    (SM_StateHandler)&SM_Master_routing_
};

SM_HsmState SM_HSM_ROM SM_Master_successful = {
    (SM_StatePtr)&SM_Master_routing,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&SM_Master_successful_entry_,
    (SM_ActionHandler)&SM_Master_successful_exit_,
    (SM_StateHandler)&SM_Master_successful_
};

SM_HsmState SM_HSM_ROM SM_Master_delegating = {
    (SM_StatePtr)&SM_Master_active,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&SM_Master_delegating_entry_,
    (SM_ActionHandler)&SM_Master_delegating_exit_,
    (SM_StateHandler)&SM_Master_delegating_
};

SM_HsmState SM_HSM_ROM SM_Master_working = {
    (SM_StatePtr)&SM_Master_active,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&SM_Master_working_entry_,
    (SM_ActionHandler)&SM_Master_working_exit_,
    (SM_StateHandler)&SM_Master_working_
};

static SM_StatePtr SM_Master_TOP_initial_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    return _SM_INIT(&SM_Master_inactive);
}

static void SM_Master_inactive_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static void SM_Master_inactive_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_inactive_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    switch (SM_MASTER_SIG(e)) {
        case USER_SLASH_COMMAND_MASTER_SIG: {
            return _SM_TRAN(&SM_Master_active);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static SM_StatePtr SM_Master_active_init_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    return _SM_INIT(&SM_Master_idle);
}

static void SM_Master_active_entry_(SM_Hsm * const me) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    SM_Master_loadAgent_(self);
    SM_Master_updateStatus_(self, "master -- active");
}

static void SM_Master_active_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_active_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    switch (SM_MASTER_SIG(e)) {
        case USER_SLASH_COMMAND_MASTER_SIG: {
            return _SM_TRAN(&SM_Master_inactive);
        }
        case USER_INPUT_PROMPTS_SIG: {
            SM_Master_notifyWarning_(self, "Not today!!!");
            self->inputEvtResult = "handled";
            return _SM_HANDLED();
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static void SM_Master_idle_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static void SM_Master_idle_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_idle_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    switch (SM_MASTER_SIG(e)) {
        case USER_INPUT_PROMPTS_SIG: {
            self->inputEvtResult = "continue";
            return _SM_TRAN(&SM_Master_routing);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static void SM_Master_routing_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static void SM_Master_routing_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_routing_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    switch (SM_MASTER_SIG(e)) {
        case BEFORE_AGENT_START_SIG: {
            return _SM_HANDLED();
        }
        case TOOL_CALL_SIG: {
            if (validDispatchToolCall_(self)) {
                return _SM_HANDLED();
            }
            SM_Master_sendProtocolReminder_(self, "Call the dispatch tool using the required block format.");
            return _SM_HANDLED();
        }
        case TOOL_RESULT_SIG: {
            if (subagentBlockFormatValid_(self)) {
                return _SM_TRAN(&SM_Master_successful);
            }
            SM_Master_sendProtocolReminder_(self, "Tool result must produce a valid subagent block.");
            return _SM_HANDLED();
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static void SM_Master_successful_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static void SM_Master_successful_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_successful_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    switch (SM_MASTER_SIG(e)) {
        case AGENT_END_SIG: {
            return _SM_TRAN(&SM_Master_delegating);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static void SM_Master_delegating_entry_(SM_Hsm * const me) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    SM_Master_dispatchAllSubagents_(self);
    SM_Master_armTimeout_(self);
}

static void SM_Master_delegating_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_delegating_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    switch (SM_MASTER_SIG(e)) {
        case TIMEOUT_SIG: {
            if (areAllSubagentsDone_(self)) {
                return _SM_TRAN(&SM_Master_working);
            }
            SM_Master_monitorSubagents_(self);
            return _SM_HANDLED();
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static void SM_Master_working_entry_(SM_Hsm * const me) SM_HSM_RETT {
    SM_Master * const self = (SM_Master *)me;
    SM_Master_sendSubagentCompletionSummary_(self);
}

static void SM_Master_working_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
}

static SM_RetState SM_Master_working_(SM_Hsm * const me, SM_MasterEvt const * const e) SM_HSM_RETT {
    switch (SM_MASTER_SIG(e)) {
        case BEFORE_AGENT_START_SIG: {
            return _SM_HANDLED();
        }
        case AGENT_END_SIG: {
            return _SM_TRAN(&SM_Master_idle);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

static void SM_Master_loadAgent_(SM_Master * const me) {
    (void)me;
}

static void SM_Master_updateStatus_(SM_Master * const me, char const * status) {
    (void)me;
    (void)status;
}

static void SM_Master_notifyWarning_(SM_Master * const me, char const * message) {
    (void)me;
    (void)message;
}

static void SM_Master_sendProtocolReminder_(SM_Master * const me, char const * message) {
    (void)me;
    (void)message;
}

static void SM_Master_dispatchAllSubagents_(SM_Master * const me) {
    (void)me;
}

static void SM_Master_armTimeout_(SM_Master * const me) {
    (void)me;
}

static void SM_Master_monitorSubagents_(SM_Master * const me) {
    (void)me;
}

static void SM_Master_sendSubagentCompletionSummary_(SM_Master * const me) {
    (void)me;
}

static uint8_t validDispatchToolCall_(SM_Master * const me) {
    return me->allowDispatchToolCall;
}

static uint8_t subagentBlockFormatValid_(SM_Master * const me) {
    return me->validSubagentBlock;
}

static uint8_t areAllSubagentsDone_(SM_Master * const me) {
    return me->allSubagentsDone;
}

#endif
