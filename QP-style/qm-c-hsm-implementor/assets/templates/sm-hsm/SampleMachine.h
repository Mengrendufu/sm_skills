/****************************************************************************
 * C State Machine Template for sm_hsm driver
 *
 * Strict preconditions:
 * 1. Input must come from qm-c-model-master --output json --strict
 * 2. Input IR must have is_reliable=true and no error diagnostics
 * 3. Final code should be checked against qm-c-model-master --output trace --strict
 * 4. Do not flatten choice branches or replace _SM_SUPER() with _SM_HANDLED()
 *
 * Usage:
 * 1. Copy this file to your project
 * 2. Replace "Sample" with your machine name
 * 3. Implement states based on your UML JSON model
 * 4. Fill in handlers according to your state machine
 ****************************************************************************/

#ifndef SAMPLE_MACHINE_H_
#define SAMPLE_MACHINE_H_

#include "sm_hsm.h"

/* ==========================================================================
 * Step 1: Define Signals
 * Copy signal names from your UML JSON model
 * ========================================================================== */
enum SampleSig {
    Sample_dummy = 0,
    
    A_SIG,
    B_SIG,
    C_SIG,
    D_SIG,
    E_SIG,
    F_SIG,
    G_SIG,
    H_SIG,
    I_SIG,
    
    Sample_max
};

/* ==========================================================================
 * Step 2: Define Event Type
 * ========================================================================== */
typedef struct {
    uint8_t sig;
} SampleEvt;

#define SAMPLE_SIG(evt_) ((evt_)->sig)

/* ==========================================================================
 * Step 3: Define Machine Type
 * Add state machine variables from your UML model
 * ========================================================================== */
typedef struct {
    SM_Hsm sm_hsm_;     // Base HSM structure
    
    // Virtual functions (for dispatch)
    VC_Handler init;
    VC_Handler dispatch;
    
    // State machine variables
    uint8_t foo;        // From your UML model (guard variables)
} SampleMachine;

/* ==========================================================================
 * Step 4: Forward Declarations
 * Declare all handler functions
 * ========================================================================== */

// Top-level initial
static SM_StatePtr Sample_TOP_initial_(SM_Hsm * const me) SM_HSM_RETT;

// State handlers - one per state from your UML model
static SM_StatePtr Sample_s_init_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState Sample_s_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT;

static SM_StatePtr Sample_s1_init_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s1_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s1_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState Sample_s1_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT;

static void Sample_s11_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s11_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState Sample_s11_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT;

static SM_StatePtr Sample_s2_init_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s2_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s2_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState Sample_s2_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT;

static SM_StatePtr Sample_s21_init_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s21_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s21_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState Sample_s21_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT;

static void Sample_s211_entry_(SM_Hsm * const me) SM_HSM_RETT;
static void Sample_s211_exit_(SM_Hsm * const me) SM_HSM_RETT;
static SM_RetState Sample_s211_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT;

/* ==========================================================================
 * Step 5: State Instances (in ROM)
 * One per state from your UML model
 * ========================================================================== */

// State S - top level under machine
// From JSON: {"name": "s", "parent": null, ...}
// Review anchor: keep every generated branch traceable to an IR transition id
SM_HsmState SM_HSM_ROM Sample_s = {
    (SM_StatePtr)NULL,              // super: NULL for top-level
    (SM_InitHandler)&Sample_s_init_,
    (SM_ActionHandler)&Sample_s_entry_,
    (SM_ActionHandler)&Sample_s_exit_,
    (SM_StateHandler)&Sample_s_
};

// State S1 - child of S
// From JSON: {"name": "s1", "parent": "s", ...}
SM_HsmState SM_HSM_ROM Sample_s1 = {
    (SM_StatePtr)&Sample_s,         // super: pointer to parent state
    (SM_InitHandler)&Sample_s1_init_,
    (SM_ActionHandler)&Sample_s1_entry_,
    (SM_ActionHandler)&Sample_s1_exit_,
    (SM_StateHandler)&Sample_s1_
};

// State S11 - child of S1
// From JSON: {"name": "s11", "parent": "s1", ...}
SM_HsmState SM_HSM_ROM Sample_s11 = {
    (SM_StatePtr)&Sample_s1,
    (SM_InitHandler)NULL,           // No initial (leaf state)
    (SM_ActionHandler)&Sample_s11_entry_,
    (SM_ActionHandler)&Sample_s11_exit_,
    (SM_StateHandler)&Sample_s11_
};

// State S2 - child of S
SM_HsmState SM_HSM_ROM Sample_s2 = {
    (SM_StatePtr)&Sample_s,
    (SM_InitHandler)&Sample_s2_init_,
    (SM_ActionHandler)&Sample_s2_entry_,
    (SM_ActionHandler)&Sample_s2_exit_,
    (SM_StateHandler)&Sample_s2_
};

// State S21 - child of S2
SM_HsmState SM_HSM_ROM Sample_s21 = {
    (SM_StatePtr)&Sample_s2,
    (SM_InitHandler)&Sample_s21_init_,
    (SM_ActionHandler)&Sample_s21_entry_,
    (SM_ActionHandler)&Sample_s21_exit_,
    (SM_StateHandler)&Sample_s21_
};

// State S211 - child of S21 (leaf)
SM_HsmState SM_HSM_ROM Sample_s211 = {
    (SM_StatePtr)&Sample_s21,
    (SM_InitHandler)NULL,
    (SM_ActionHandler)&Sample_s211_entry_,
    (SM_ActionHandler)&Sample_s211_exit_,
    (SM_StateHandler)&Sample_s211_
};

/* ==========================================================================
 * Step 6: Instance Declaration
 * ========================================================================== */
extern SampleMachine Sample_inst;
extern SM_Hsm * AO_Sample;

/* ==========================================================================
 * Step 7: Handler Implementations
 * Fill in based on your UML JSON model
 * ========================================================================== */

/*
 * Top-level Initial Transition
 * From JSON: top_initial.target = "s2", top_initial.action = "..."
 */
static SM_StatePtr Sample_TOP_initial_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("top-INIT.");  // From JSON: top_initial.action
    return _SM_INIT(&Sample_s2);  // From JSON: top_initial.target
}

/*
 * State S Handlers
 * From JSON: {"name": "s", "entry": "...", "exit": "...", "initial": {...}}
 */
static SM_StatePtr Sample_s_init_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s-INIT.");  // From JSON: s.initial.action
    return _SM_INIT(&Sample_s11);  // From JSON: s.initial.target
}

static void Sample_s_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s-ENTRY.");  // From JSON: s.entry
}

static void Sample_s_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s-EXIT.");  // From JSON: s.exit
}

static SM_RetState Sample_s_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT {
    switch (SAMPLE_SIG(e)) {
        case I_SIG: {
            /* From JSON: {"trigger": "I", "guard": "me->foo", "kind": "internal"}
             * Guard: me->foo (true when foo != 0)
             * Action: foo = 0, print "s-I."
             * If guard false: pass to super (return _SM_SUPER)
             */
            if (((SampleMachine*)me)->foo) {
                ((SampleMachine*)me)->foo = 0U;
                trace("s-I.");
                return _SM_HANDLED();
            } else {
                return _SM_SUPER();
            }
        }
        case E_SIG: {
            /* From JSON: {"trigger": "E", "target": "s11", "action": "..."}
             * External transition to s11
             */
            trace("s-E.");
            return _SM_TRAN(&Sample_s11);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

/*
 * State S1 Handlers
 * From JSON: {"name": "s1", "parent": "s", ...}
 */
static SM_StatePtr Sample_s1_init_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s1-INIT.");
    return _SM_INIT(&Sample_s11);
}

static void Sample_s1_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s1-ENTRY.");
}

static void Sample_s1_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s1-EXIT.");
}

static SM_RetState Sample_s1_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT {
    switch (SAMPLE_SIG(e)) {
        case I_SIG: {
            // From JSON: internal transition
            trace("s1-I.");
            return _SM_HANDLED();
        }
        case A_SIG: {
            // From JSON: self-transition to s1
            trace("s1-A.");
            return _SM_TRAN(&Sample_s1);
        }
        case B_SIG: {
            trace("s1-B.");
            return _SM_TRAN(&Sample_s11);
        }
        case C_SIG: {
            trace("s1-C.");
            return _SM_TRAN(&Sample_s2);
        }
        case D_SIG: {
            /* From JSON: {"trigger": "D", "guard": "!me->foo", "target": "s", ...}
             * Guard: !me->foo (true when foo == 0)
             * Action: foo = 1, print "s1-D."
             */
            if (!((SampleMachine*)me)->foo) {
                ((SampleMachine*)me)->foo = 1U;
                trace("s1-D.");
                return _SM_TRAN(&Sample_s);
            } else {
                return _SM_SUPER();
            }
        }
        case F_SIG: {
            trace("s1-F.");
            return _SM_TRAN(&Sample_s211);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

/*
 * State S11 Handlers
 * From JSON: {"name": "s11", "parent": "s1", ...}
 */
static void Sample_s11_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s11-ENTRY.");
}

static void Sample_s11_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s11-EXIT.");
}

static SM_RetState Sample_s11_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT {
    switch (SAMPLE_SIG(e)) {
        case G_SIG: {
            trace("s11-G.");
            return _SM_TRAN(&Sample_s211);
        }
        case H_SIG: {
            trace("s11-H.");
            return _SM_TRAN(&Sample_s);
        }
        case D_SIG: {
            /* From JSON: {"trigger": "D", "guard": "me->foo", "target": "s1", ...}
             * Guard: me->foo (true when foo != 0)
             */
            if (((SampleMachine*)me)->foo) {
                ((SampleMachine*)me)->foo = 0U;
                trace("s11-D.");
                return _SM_TRAN(&Sample_s1);
            } else {
                return _SM_SUPER();
            }
        }
        default: {
            return _SM_SUPER();
        }
    }
}

/*
 * State S2 Handlers
 */
static SM_StatePtr Sample_s2_init_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s2-INIT.");
    return _SM_INIT(&Sample_s21);
}

static void Sample_s2_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s2-ENTRY.");
}

static void Sample_s2_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s2-EXIT.");
}

static SM_RetState Sample_s2_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT {
    switch (SAMPLE_SIG(e)) {
        case I_SIG: {
            // Guard: !me->foo
            if (!((SampleMachine*)me)->foo) {
                ((SampleMachine*)me)->foo = 1U;
                trace("s2-I.");
                return _SM_HANDLED();
            } else {
                return _SM_SUPER();
            }
        }
        case C_SIG: {
            trace("s2-C.");
            return _SM_TRAN(&Sample_s1);
        }
        case F_SIG: {
            trace("s2-F.");
            return _SM_TRAN(&Sample_s11);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

/*
 * State S21 Handlers
 */
static SM_StatePtr Sample_s21_init_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s21-INIT.");
    return _SM_INIT(&Sample_s211);
}

static void Sample_s21_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s21-ENTRY.");
}

static void Sample_s21_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s21-EXIT.");
}

static SM_RetState Sample_s21_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT {
    switch (SAMPLE_SIG(e)) {
        case A_SIG: {
            // Self-transition
            trace("s21-A.");
            return _SM_TRAN(&Sample_s21);
        }
        case B_SIG: {
            trace("s21-B.");
            return _SM_TRAN(&Sample_s211);
        }
        case G_SIG: {
            trace("s21-G.");
            return _SM_TRAN(&Sample_s1);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

/*
 * State S211 Handlers
 */
static void Sample_s211_entry_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s211-ENTRY.");
}

static void Sample_s211_exit_(SM_Hsm * const me) SM_HSM_RETT {
    (void)me;
    trace("s211-EXIT.");
}

static SM_RetState Sample_s211_(SM_Hsm * const me, SampleEvt const * const e) SM_HSM_RETT {
    switch (SAMPLE_SIG(e)) {
        case D_SIG: {
            trace("s211-D.");
            return _SM_TRAN(&Sample_s21);
        }
        case H_SIG: {
            trace("s211-H.");
            return _SM_TRAN(&Sample_s);
        }
        default: {
            return _SM_SUPER();
        }
    }
}

/* ==========================================================================
 * Step 8: Machine Constructor and Dispatch
 * ========================================================================== */

static void Sample_init(SampleMachine * const me, SampleEvt const * const e) SM_HSM_RETT {
    (void)e;
    SM_Hsm_init_(&me->sm_hsm_, (SM_InitHandler)Sample_TOP_initial_);
}

static void Sample_dispatch(SampleMachine * const me, SampleEvt const * const e) SM_HSM_RETT {
    SM_Hsm_dispatch_(&me->sm_hsm_, e);
}

static void Sample_ctor(void) {
    SampleMachine *me = &Sample_inst;
    
    me->init = (VC_Handler)Sample_init;
    me->dispatch = (VC_Handler)Sample_dispatch;
    
    me->foo = 0;  // Initialize guard variables
}

/* ==========================================================================
 * Instance Definition
 * ========================================================================== */
SampleMachine Sample_inst;
SM_Hsm * AO_Sample = &Sample_inst.sm_hsm_;

#endif /* SAMPLE_MACHINE_H_ */
