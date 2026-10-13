# Soft Serve Machine Not Cooling / Product Too Soft

## Overview

This runbook addresses situations where soft serve machines fail to cool product to proper serving consistency, resulting in product that is too soft, soupy, or flowing incorrectly from the dispenser. This is a food safety and service quality issue requiring immediate diagnosis and remediation.

## Affected Systems

- **CreamTech SC-300** (all versions)
- **CreamTech SC-500** (all versions)
- **FrostyPro 800 v1.x** (v1.0–v1.8)
- **FrostyPro 800 v2.x** (v2.0–v2.3)

## Symptoms

- Product dispenses too soft or soupy
- Product temperature exceeds safe serving range (>4°C detected)
- Machine displays "TEMP WARNING" or "COOLING FAILURE" alert
- Product consistency degrades throughout shift
- Compressor running but no temperature drop observed
- Audible compressor noise absent (potential motor failure)
- Freezing cylinder feels warm to touch (thermal malfunction)
- Temperature readout on display panel does not decrease after 30+ minutes of runtime

## Immediate Steps (First 2 Minutes)

1. **STOP all serving immediately** if product temperature exceeds 4°C or cannot be verified.
   - Remove mix from hoppers and discard if product has been at unsafe temperature for >30 minutes.
   - Post "OUT OF SERVICE" signage on the machine.

2. **Check ambient conditions:**
   - Verify room/outdoor temperature (machines work less efficiently above 32°C/90°F).
   - Ensure machine is not in direct sunlight or near heat sources (ovens, steam tables, radiators).
   - Confirm adequate airflow around machine (minimum 15 cm clearance on all sides).

3. **Verify power and standby mode:**
   - Confirm machine is plugged in and power indicator is lit.
   - Confirm machine is in "RUN" mode (not "STANDBY," "OFF," or "CLEAN" mode).
   - Check that no visible ice or frost blockages are present in the air intake grille.

## L1 Diagnosis Steps

### Step 1: Access Temperature Display

- **CreamTech SC-300 / SC-500:** Press **MENU** button → select **DIAGNOSTICS** → select **TEMPERATURE STATUS**.
- **FrostyPro 800 v1.x:** Press the **INFO** button on the control panel; temperature displays on LCD screen.
- **FrostyPro 800 v2.x:** Touch **Settings** icon (gear symbol) on touchscreen → select **System Status** → view **Current Temp** and **Target Temp** side-by-side.

**Record the current product temperature and target temperature.** Proceed to Step 2.

### Step 2: Check Compressor Status

- **CreamTech SC-300 / SC-500:**
  - Press **MENU** → **DIAGNOSTICS** → **COMPRESSOR STATUS**.
  - Confirm status shows "RUNNING" or "CYCLING." If status shows "OFF" or "ERROR," note the error code and proceed to Step 3.
  - Listen carefully at the back of the machine for a rhythmic humming or clicking sound (compressor activity).

- **FrostyPro 800 v1.x:**
  - Press **INFO** → scroll to **Compressor** status.
  - Status should display "ACTIVE" or "IDLE" (normal). "FAULT" or blank display indicates a problem.
  - Listen and feel (with caution) behind the machine for vibration indicating motor operation.

- **FrostyPro 800 v2.x:**
  - Touch **Settings** → **System Status** → **Compressor State**.
  - Confirm status is "ON" or "CYCLING." Status "FAILED" or "UNRESPONSIVE" requires escalation.

**If compressor is not running, proceed to Step 3. If compressor is running but temperature is not dropping, proceed to Step 4.**

### Step 3: Check for Thermal Overload Condition (Compressor Off)

- **CreamTech SC-300 / SC-500:**
  - Press **MENU** → **DIAGNOSTICS** → **THERMAL PROTECTION**.
  - If status shows "TRIPPED" or "ACTIVE," the thermal overload switch has shut down the compressor to prevent damage.
  - Note any ambient temperature reading if displayed.

- **FrostyPro 800 v1.x / v2.x:**
  - Check the physical **RESET BUTTON** located on the back panel, lower right corner (red button, approximately 1 cm diameter).
  - If visible and protruding slightly, thermal overload has been triggered.

**Record findings and proceed to Step 5 (cooling cycle restart).**

### Step 4: Assess Refrigerant Circulation and Condenser Condition

- **All systems:** Visually inspect the condenser (finned metal coil on the rear/side of the machine):
  - Look for ice buildup, frost accumulation, or visible dust/debris clogging the fins.
  - Gently touch the metal fins (with clean hands, avoiding sharp edges). Condenser should be warm or hot during operation.
  - If condenser is ice-blocked or completely cold, refrigerant circulation may be compromised.

- **CreamTech SC-300 / SC-500:**
  - Press **MENU** → **DIAGNOSTICS** → **REFRIGERANT PRESSURE**.
  - Normal operating pressure: **4.5–6.0 bar** (high side). If reading is <4.0 bar or >6.5 bar, refrigerant leak or blockage is suspected.

- **FrostyPro 800 v1.x / v2.x:**
  - **Pressure gauges are not visible on user interface.** Proceed to visual assessment only at L1 level.

**If ice blocks the condenser or pressure reading is abnormal, proceed to Step 5 and then escalate to L2.**

### Step 5: Review Recent Maintenance and Duty Cycle

- Check the **machine log** for recent service events:
  - **CreamTech:** Press **MENU** → **MAINTENANCE LOG**. Review last 10 entries for any thermal events or compressor resets.
  - **FrostyPro 800 v1.x:** Press **INFO** → **Maintenance** tab.
  - **FrostyPro 800 v2.x:** Touch **Settings** → **Maintenance History**.
- Check **runtime hours:**
  - Machines with >8 continuous hours of operation may require a cooldown break.
  - Confirm the machine was given a 15-minute rest in the last 24 hours if applicable.

## L1 Resolution

### Resolution 1: Restart and Cool-Down Cycle (Most Common Fix)

**Applies when:** Compressor is running but not achieving target temperature after prolonged operation.

1. Power down the machine:
   - **CreamTech SC-300 / SC-500:** Press **POWER OFF** button, or switch the rear power switch to OFF. Wait **30 seconds**.
   - **FrostyPro 800 v1.x / v2.x:** Press **POWER** on the control panel and hold for 3 seconds. Wait **30 seconds**.

2. Power back on and set to RUN mode:
   - Machine will enter initialization phase (approximately 2 minutes). Do not interrupt.
   - Once initialization completes, confirm temperature display shows **TARGET TEMP: -5°C** (CreamTech) or **-4°C** (FrostyPro).

3. Allow **45 minutes minimum** for the freezing cylinder to reach target temperature before resuming service.
   - Monitor temperature every 10 minutes using diagnostics menu.
   - Temperature should drop approximately **1–2°C per 5 minutes** initially.

4. Once product temperature reaches **-2°C or lower**, dispense a test portion and assess consistency.
   - Proper soft serve should hold its shape and not flow excessively.
   - If consistency is acceptable, return machine to service.

**If temperature does not drop after 45 minutes, proceed to Resolution 2.**

### Resolution 2: Reset Thermal Overload Protection

**Applies when:** Compressor is OFF and thermal overload has been triggered.

1. **Locate and reset the thermal overload button:**
   - **CreamTech SC-300 / SC-500:**
     - Press **MENU** → **DIAGNOSTICS** → **THERMAL PROTECTION**.
     - Select **RESET THERMAL OVERRIDE** (if available in your software version).
     - If no menu option exists, locate the physical reset button on the rear of the machine (large red button, typically lower right).

   - **FrostyPro 800 v1.x / v2.x:**
     - Locate the physical red **RESET BUTTON** on the rear panel (lower right, approximately 1 cm diameter).
     - Press and hold for **2 seconds** until you hear or feel a click.

2. Verify compressor restarts:
   - Listen for compressor humming or clicking to resume within 5 seconds.
   - Check **COMPRESSOR STATUS** via diagnostics menu to confirm "RUNNING" or "ACTIVE."

3. If thermal overload resets but compressor does not run:
   - Proceed immediately to **When to Escalate to L2** section. **Do not attempt further resets.**

4. Allow a full **60-minute cool-down cycle** before returning to service (see Resolution 1, steps 2–4).

**Note:** Repeated thermal overload resets within a single shift indicate a L2-level issue (potential compressor motor fault or persistent ambient overheating).

### Resolution 3: Clear Condenser Blockage (Ice/Frost Buildup)

**Applies when:** Condenser is visibly ice-blocked and thermal assessment shows no compressor fault.

1. **Power down the machine completely.**
   - **CreamTech:** Switch rear power switch to OFF.
   - **FrostyPro:** Press **POWER** and hold for 3 seconds.
   - Wait **5 minutes** for the compressor to fully stop.

2. **Inspect and manually remove ice/frost blockage (if safe and accessible):**
   - Do **NOT** use sharp objects (knives, scrapers) that may damage the condenser fins.
   - Use a **soft brush or cloth** to gently brush away frost or dust from the condenser fins.
   - If ice is thick (>5 mm), allow an additional 10 minutes of passive warming before gently brushing.
   - Ensure airflow pathway is clear (minimum 15 cm clearance on all sides of machine).

3. **Restart the machine:**
   - Power on and set to RUN mode.
   - Allow the machine to cycle for 10 minutes, then inspect the condenser again for any remaining blockage.
   - If blockage returns immediately or persists, escalate to L2 (potential refrigerant circulation issue).

4. **Monitor temperature and return to service per Resolution 1, steps 2–4.**

### Resolution 4: Adjust Ambient Conditions

**Applies when:** Ambient temperature or placement is causing inadequate cooling performance.

1. **Check and record the ambient (room or outdoor) temperature:**
   - Soft serve machines operate optimally at **15–25°C (59–77°F)**.
   - Performance degradation begins above **28°C (82°F)**.
   - Above **32°C (90°F)**, machines typically cannot maintain proper freezing (this is a **physical limitation**, not a fault).

2. **Relocate machine if feasible:**
   - Move machine away from direct sunlight.
   - Move machine away from heat-producing equipment (ovens, grills, radiators, steam tables).
   - Ensure minimum **15 cm clearance** on all sides for adequate airflow.

3. **If relocation is not possible, implement temporary cooling:**
   - Direct a **portable fan** toward the condenser (rear of machine) to improve air circulation.
   - Use an **outdoor parasol or shade** (if machine is outdoors) to block direct sunlight.
   - These are **temporary measures only**; escalate to management for permanent solutions (HVAC upgrade, machine repositioning).

4. **Allow 30–45 minutes for temperature normalization after adjustment, then test per Resolution 1.**

## When to Escalate to L2

**Escalate to L2 immediately if ANY of the following apply:**

### Critical Escalation Criteria (Food Safety Issue)

- Product temperature cannot be reliably verified and is suspected to exceed **4°C**.
- Temperature sensor displays "ERROR" or "SENSOR FAULT" code (machines cannot confirm safe serving temperature).
- Compressor will not restart after thermal overload reset (indicates potential motor failure).

### Technical Escalation Criteria

- **Compressor is OFF and unresponsive** after thermal overload reset is attempted.
- **Compressor is running but temperature does not drop below -1°C after 90 minutes** of continuous operation.
- **Refrigerant pressure reading is <3.5 bar or >7.0 bar** (indicates refrigerant leak, overcharge, or blockage).
- **Thermal overload trips MORE THAN TWICE in a single 8-hour shift** (indicates compressor motor wear or persistent fault).
- **Condenser remains ice-blocked or frosted after manual cleaning and 30-minute rest period** (indicates possible refrigerant leak or pressure regulation fault).
- **Audible grinding, squealing, or rattling sounds** emanate from the compressor during operation (mechanical damage).
- **Error codes displayed on diagnostic screens do not match any code in this runbook.**

### Information to Collect Before Escalating

Provide L2 support with the following details:

- **Machine model** (CreamTech SC-300 / SC-500 / FrostyPro 800) and **software version** (displayed on startup screen or via Settings).
- **Current product temperature** and **target temperature** (from diagnostics menu).
- **Compressor status** (running/off/error) and any **error codes** or status messages.
- **Thermal overload history:** Number of resets in the past 24 hours; time and date of each reset.
- **Ambient temperature** at the time of report.
- **Last successful service:** When the machine last operated correctly; any recent maintenance or repairs.
- **Steps already taken:** List all resolution steps attempted and results (e.g., "Completed cool-down cycle, temperature reached -1°C, did not improve").
- **Refrigerant pressure readings** (CreamTech systems only), if available.
- **Photos of:**
  - Machine location and surroundings (to assess ambient conditions).
  - Condenser condition (if ice or blockage is present).
  - Any error code displays (clear, close-up photo of the screen).

---

## Related Runbooks

- `machine-not-powering-on.md` — Troubleshoot power and electrical issues.
- `compressor-motor-replacement.md` — Detailed procedure for L2 technician to replace compressor motor (CreamTech SC-300/500, FrostyPro 800 v2.x).
- `refrigerant-leak-diagnosis.md` — Advanced diagnostics for refrigerant system leaks.
- `temperature-sensor-replacement.md` — Diagnostics and replacement for faulty temperature sensors.
- `preventative-maintenance-schedule.md` — Routine cleaning, inspection, and servicing intervals.
- `food-safety-procedures.md` — Product handling, temperature monitoring, and discard protocols when food safety is compromised.
- `machine-placement-guidelines.md` — Optimal siting, clearance, and ambient environment recommendations.

---

## Revision History

| Version | Date       | Notes                                                                                                                                                        |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.2     | 2025-09-15 | Updated for FrostyPro 800 v2.x touchscreen interface; clarified thermal overload reset procedure; added refrigerant pressure guidance for CreamTech systems. |
| 1.1     | 2025-03-22 | Added ambient temperature thresholds and condenser inspection steps; expanded L2 escalation criteria.                                                        |
| 1.0     | 2024-06-01 | Initial version; covers CreamTech SC-300/500 and FrostyPro 800 v1.x.                                                                                         |
