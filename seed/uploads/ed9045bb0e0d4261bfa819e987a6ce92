# Soft Serve Cleaning Cycle Stuck

## Overview

The soft serve machine cleaning cycle fails to complete or the machine becomes locked in cleaning mode, preventing normal operation. This runbook addresses diagnostic and resolution procedures for CreamTech SC-300 and SC-500 units experiencing stuck cleaning cycles.

## Affected Systems

- **CreamTech SC-300** (firmware v2.1.4 and later)
- **CreamTech SC-500** (firmware v3.0.2 and later)
- **FrostyPro systems** (all current versions)

## Symptoms

- Machine displays "CLEANING IN PROGRESS" on LCD screen for extended period (>15 minutes)
- Cleaning cycle does not advance to next step or complete
- "CYCLE ERROR" or error codes displayed (e.g., E-CLN-004, E-CLN-007, E-CLN-012)
- Machine is unresponsive to button inputs during cleaning mode
- Pump running continuously or not running during cleaning cycle
- Water not dispensing or dispensing abnormally during cycle steps
- Machine locked out; unable to exit cleaning mode or return to service mode
- Audio alert or beeping pattern indicating cycle failure

## Immediate Steps (First 2 Minutes)

1. **Check the wall clock.** Note the exact time the cleaning cycle started. Confirm with store staff when they initiated the cycle.

2. **Verify power status.** Confirm the machine is powered on (check power indicator light on control panel). Do not unplug the machine.

3. **Visually inspect the machine exterior.** Look for:
   - Disconnected or loose water supply hose at rear of unit
   - Drain line kinked, blocked, or detached
   - Visible water leaks around seals or connection points
   - Obstructions in the drain outlet

**Do not interrupt an active cleaning cycle.** If the cycle began less than 15 minutes ago, wait and monitor.

## L1 Diagnosis Steps

### Step 1: Access the Control Panel

1. Approach the front of the machine and locate the **LCD display screen** (4.3" touchscreen on SC-300; 5.7" on SC-500).
2. Note the **current message displayed** on screen (exact text).
3. Note any **error codes** (format: E-XXX-### or similar).
4. Document the **time elapsed** since cycle start (visible on display or calculate from staff report).

### Step 2: Check Machine Status Menu

1. If the display shows a menu or button options, tap the **STATUS** or **INFO** button (location varies by model; typically upper right of display).
2. Navigate to **System Status** or **Diagnostics** submenu.
3. Record:
   - Current cycle step (e.g., "Step 2 of 5: Rinse Cycle")
   - Time in current step (displayed as elapsed time)
   - Any error codes or warnings listed
   - Pump status (running/stopped)
   - Water pressure reading (if displayed; normal range: 40–60 PSI)

### Step 3: Assess Cycle Duration

1. Calculate total time elapsed since cleaning cycle start.
   - **0–15 minutes:** Cycle may still be in progress; note exact step and continue monitoring.
   - **15–60 minutes:** Investigate potential blockage or sensor failure (proceed to Step 4).
   - **>60 minutes:** Likely hardware failure or extended jam; prepare for escalation.

### Step 4: Check Water Supply and Drainage

1. **Water inlet check:**
   - Locate the water inlet hose connection at the **rear of the machine** (typically blue-coded hose).
   - Gently wiggle the hose connection to confirm it is secure (should not move more than ¼ inch).
   - Verify the water shut-off valve (if present) is fully **open** (handle parallel to hose).

2. **Drainage check:**
   - Locate the drain outlet at the base or rear of the unit.
   - Check for visible blockages (food debris, ice crystals, mineral deposits).
   - If accessible, use a flashlight to inspect the drain opening.
   - Do not attempt to clear blockages with tools; note the obstruction type.

3. **Drain line integrity:**
   - Visually trace the drain hose from machine to floor drain or waste bin.
   - Confirm the hose is not kinked, pinched, or disconnected.
   - Check that the hose inlet is below the water level of the machine (no siphon lock).

### Step 5: Review Recent Error Codes

1. If an error code is displayed, record the **complete code** (e.g., E-CLN-007).
2. Cross-reference the code with the quick reference below:
   - **E-CLN-004:** Pump failure or blockage in supply line
   - **E-CLN-007:** Water pressure out of range; check inlet or filter
   - **E-CLN-012:** Drainage blockage; cycle cannot advance to next step
   - **E-SEN-001:** Temperature sensor malfunction
   - **E-TMO-999:** Cycle timeout; step exceeded maximum duration

3. If the error code is not listed, document it for L2 review.

### Step 6: Attempt One Soft Reset (if appropriate)

1. **Only perform this step if the machine is stuck on the same step for >20 minutes AND no water is flowing.**
2. Locate the **Reset button** on the control panel (small, recessed button; typically near power switch).
3. Press and hold the Reset button for **3 seconds** (do not hold longer than 5 seconds).
4. Release the button and observe the display.
5. Document the result:
   - Did the cycle resume?
   - Did an error code appear?
   - Did the display change?

**Do not perform a hard power-off (unplugging or breaker reset) without L2 authorization.**

## L1 Resolution

### Resolution Path 1: Water Inlet Issue (E-CLN-007, Low Pressure Error)

1. Turn off the machine at the **power switch** on the control panel (or main breaker if switch is unresponsive).
2. Wait 30 seconds.
3. Check the **water inlet filter** (if accessible):
   - Locate the filter cartridge at the water inlet connection (rear of machine).
   - If present, note whether the filter element is visibly blocked, discolored, or degraded.
   - Do not attempt to clean or replace the filter; document the condition.
4. Verify the building's **main water supply valve** is fully open (check with store manager or facilities staff).
5. Turn the machine back on.
6. Initiate a **new cleaning cycle** from the main menu (do not resume the stuck cycle; start fresh).
7. Monitor for the first 3 minutes to confirm the cycle progresses.
8. If the cycle completes successfully, document as resolved.
9. If the same error reoccurs, escalate to L2 with filter condition noted.

### Resolution Path 2: Drain Blockage (E-CLN-012, Drainage Error)

1. Turn off the machine at the **power switch** on the control panel.
2. Wait 30 seconds for residual water to drain.
3. Locate the **drain outlet** and inspect for visible blockage:
   - If a removable strainer basket is present at the drain, note whether debris is visible.
   - Do not remove the basket or attempt to clear the drain with tools.
4. Check for **pinched or kinked drain hose** along the entire run from machine to waste area; gently straighten if kinked.
5. Confirm the drain line outlet is **above the machine's internal water level** to prevent siphon lock (typically 12–18 inches above the floor drain or waste bin).
6. Turn the machine back on.
7. Initiate a **new cleaning cycle**.
8. Monitor for 5 minutes; if water begins draining normally, continue monitoring the full cycle.
9. If drainage is still blocked or the same error appears, escalate to L2 with blockage description.

### Resolution Path 3: Sensor or Pump Timeout (E-TMO-999, E-SEN-001)

1. Turn off the machine at the **power switch**.
2. Wait **2 minutes** for the system to fully power down (LCD screen should go dark).
3. Turn the machine back on.
4. Wait for the boot-up sequence to complete (typically 10–15 seconds; display will show logo and version number).
5. Initiate a **new cleaning cycle** from the main menu.
6. Monitor the cycle for at least 5 minutes:
   - Note whether the cycle advances through steps normally.
   - Confirm water flow and drainage activity.
   - Listen for pump operation (normal hum/low-level noise).
7. If the cycle completes without error, document as resolved.
8. If the same error code reappears within the first cycle after reset, escalate to L2.

### Resolution Path 4: Cycle Stuck at Single Step (No Error Code)

1. **Check the elapsed time** again. If the cycle is stuck for **>45 minutes with no error code displayed**, proceed with escalation (see below).
2. If the cycle is stuck for **15–45 minutes**, attempt one **soft reset only:**
   - Press the **Reset button** (recessed, 3-second press).
   - Observe whether the machine exits cleaning mode or advances the cycle.
3. If the reset is ineffective or not applicable:
   - Do not attempt manual override without vendor authorization.
   - Escalate immediately to L2; note the exact step where the cycle is stuck.

## When to Escalate to L2

### Escalate Immediately If:

- Cleaning cycle has been stuck for **>60 minutes** (food safety concern; L1 must escalate within this window).
- Error code displayed is **not in the quick reference** (E-CLN-004, E-CLN-007, E-CLN-012, E-SEN-001, E-TMO-999).
- **Manual override is required** on a CreamTech unit (CreamTech authorization required; L1 cannot proceed).
- Soft reset was attempted and failed; the same error reoccurs on a fresh cycle.
- Water is actively leaking from the machine body, seals, or connection points.
- The machine is **completely unresponsive** to power-on or button inputs (possible hardware failure).

### Escalate After 4 Hours If:

- Cleaning cycle remains stuck despite L1 troubleshooting steps.
- Multiple resolution attempts (resets, power cycles) have been exhausted.
- Food safety guideline: Stuck cycles >4 hours require escalation due to potential product exposure.

### Required Information to Collect Before Escalating

Gather the following data and include in the escalation ticket:

| Data Point                         | Example                                                         |
| ---------------------------------- | --------------------------------------------------------------- |
| Machine model and firmware version | CreamTech SC-500, firmware v3.0.2                               |
| Exact error code (if any)          | E-CLN-012 or "No error code displayed"                          |
| Cycle step where stuck             | "Step 3 of 5: Rinse Cycle"                                      |
| Total time elapsed                 | 2 hours 15 minutes                                              |
| Symptoms observed                  | "Pump running continuously; no water draining"                  |
| Resolution steps attempted         | "Soft reset performed; water inlet checked; cycle reinitiated"  |
| Current machine status             | "Machine still in cleaning mode; unresponsive to button inputs" |
| Store/location identifier          | Store #547, Las Vegas location                                  |
| Time of initial report             | 2025-09-15 14:32 UTC                                            |
| Store contact for follow-up        | Manager: Sarah Chen, 702-555-0123                               |

### Special Note for FrostyPro Units

If the affected machine is a **FrostyPro** unit and manual override is necessary:

- **Manual override procedure is documented in FrostyPro manual section 5.3.**
- L2 or authorized vendor personnel must perform the override.
- L1 may reference section 5.3 in the escalation ticket but must not attempt the override independently.

---

## Related Runbooks

- `soft-serve-machine-power-cycle-procedure.md`
- `water-inlet-filter-replacement-creamtech.md`
- `drain-line-inspection-and-clearance.md`
- `creamtech-error-code-reference.md`
- `frostypro-manual-override-authorization.md`
- `soft-serve-daily-maintenance-checklist.md`
- `food-safety-escalation-protocol.md`

---

## Revision History

| Version | Date       | Notes                                                                                                                                       |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated firmware versions for SC-500 (v3.0.2); added FrostyPro manual override reference; clarified 4-hour food safety escalation threshold |
| 1.1     | 2025-03-20 | Added specific error code reference table; improved drain troubleshooting steps                                                             |
| 1.0     | 2024-06-01 | Initial version                                                                                                                             |
