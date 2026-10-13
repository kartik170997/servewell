# Soft Serve Motor Overload Alarm

## Overview

The motor overload alarm indicates the soft serve machine's motor is drawing excessive current, typically due to mix viscosity issues, mechanical friction, or hardware failure. High-pitched grinding noise indicates potential internal damage and requires immediate L2 escalation.

## Affected Systems

- **CreamTech SC-300** (v2.1+, v3.0, v3.1)
- **FrostyPro 800** (v1.8+, v2.0, v2.1)

## Symptoms

- Motor alarm indicator illuminated on control panel
- "MOTOR OVERLOAD" or "MOT_OVL_ERR" error code displayed
- High-pitched grinding or squealing noise from motor housing
- Machine unable to dispense product or motor stops mid-cycle
- Unusual vibration from machine base
- Motor runs but dispenses slowly or inconsistently

## Immediate Steps (First 2 Minutes)

1. **Stop the machine immediately.** Press the main power button and wait 10 seconds for full shutdown.

2. **Listen carefully** for any grinding, squealing, or rattling noise. If you hear grinding—**STOP. Do not proceed. Call IT Help Desk immediately and escalate to L2 per the escalation section below.**

3. **Check the mix level** in the hopper. The machine may be attempting to freeze overly thick or frozen mix. If mix is visibly solid or crystallized, note this for IT.

## L1 Diagnosis Steps

### Step 1: Verify Error Code

1. Power the machine back on.
2. Navigate to **Settings** → **Diagnostics** (or **Service Menu** on FrostyPro 800).
3. Select **Error Log** or **Active Alerts**.
4. Record the exact error code displayed (e.g., `MOT_OVL_001`, `MOT_OVL_002`).
5. Note the timestamp of first occurrence.

### Step 2: Check Mix Viscosity

1. Open the hopper access panel (usually on the left side of machine).
2. Visually inspect the mix consistency:
   - **Normal:** Flows like thick syrup when the hopper is tilted slightly.
   - **Too thick:** Barely moves or appears frozen/crystallized.
   - **Unusual color/separation:** Note for escalation.
3. Check the mix temperature display (if available on control panel):
   - **CreamTech SC-300:** Navigate to **Settings** → **Temperature Monitor**. Freezing chamber should read **–4°C to 0°C**. Mix chamber should read **3°C to 7°C**.
   - **FrostyPro 800:** Press **Status** button; read LCD display for **"FREEZE TEMP"** and **"MIX TEMP"**.
4. If freezing chamber temperature is above **2°C**, the compressor may not be running properly. Note this.

### Step 3: Perform Visual Inspection

1. Power off the machine and unplug it.
2. Inspect the motor housing (rear or underside, depending on model) for:
   - Cracks or visible damage
   - Oil leaks or fluid residue
   - Loose mounting bolts (attempt to hand-tighten if accessible)
3. Check that the mix paddle rotates freely by gently rotating it by hand.
   - **Should turn smoothly.** Any grinding sensation indicates internal bearing damage—escalate immediately.
4. Plug the machine back in but do not power on yet.

### Step 4: Check for Mechanical Obstructions

1. Power on the machine.
2. Remove any product hoppers or dispensing heads (if removable without tools).
3. Look into the mixing chamber for:
   - Frozen product buildup
   - Foreign objects
   - Broken paddle fragments
4. If obstructions are visible and removable without disassembly, carefully remove them.
5. Reattach dispensing components.

## L1 Resolution

### Resolution Path A: High Mix Viscosity (Most Common)

**Applies when:** Mix appears too thick and temperatures are normal.

1. **Power down the machine** completely.
2. **Replace or thin the mix:**
   - If mix is old or crystallized, drain the hopper and replace with fresh mix from the cooler.
   - If mix is acceptable but too thick, request kitchen staff add a small amount of water (approximately 50–100 mL per 5-liter batch) and stir thoroughly before reloading.
3. **Wait 5 minutes** for the machine to stabilize temperature after fresh mix is loaded.
4. **Power on and run a test cycle:**
   - Attempt to dispense a small amount of product (5–10 seconds).
   - Listen for normal motor operation (low hum, no grinding).
5. **If successful,** document the resolution in the ticket and close.
6. **If error persists,** proceed to escalation.

### Resolution Path B: Temperature Sensor Anomaly

**Applies when:** Mix viscosity is normal but temperatures are incorrect.

1. **Access the temperature calibration menu:**
   - **CreamTech SC-300:** Settings → Service → Temperature Calibration.
   - **FrostyPro 800:** Press and hold **Status** + **Menu** for 3 seconds → Calibration.
2. **Note the current readings** and compare to the baseline in your documentation.
3. **Perform a soft reset:**
   - Navigate to **Settings** → **System Reset** → **Soft Reset** (do NOT select "Factory Reset").
   - Select **Yes** to confirm. Machine will restart (2–3 minutes).
4. **After restart, check temperatures again** in Diagnostics.
5. **If temperatures normalize,** attempt a test cycle per Resolution Path A, Step 4.
6. **If temperatures remain incorrect,** proceed to escalation (possible sensor failure).

### Resolution Path C: Motor Reset (Only if No Grinding Noise Detected)

**Applies when:** No grinding noise heard, mechanical components move freely, but alarm persists.

1. **Power off the machine and wait 30 seconds.**
2. **Power on the machine.**
3. **Navigate to Settings → Service → Clear Error Log** (or equivalent menu).
4. **Select the overload alarm entry** and choose **Clear** or **Reset**.
5. **Confirm the action.** Machine will reboot.
6. **Perform a test cycle** as described in Resolution Path A, Step 4.
7. **If the error returns within 5 minutes,** do NOT attempt further resets—proceed to escalation.

## When to Escalate to L2

### Escalate Immediately (Critical)

- **Grinding, squealing, or rattling noise** from the motor or mechanical chamber (hardware damage imminent).
- **Burnt smell** or visible smoke.
- **Motor does not respond** to power-on command after 2 attempts.

### Escalate After Diagnostic Steps (High Priority)

- Error code persists after completing all L1 resolution steps.
- Mix paddle does not rotate freely or rotates with grinding sensation.
- Temperature readings remain out of range after soft reset.
- Multiple motor overload errors within 1 hour (3+ occurrences).

### Information to Collect Before Escalating

1. **Exact error code(s)** displayed (e.g., `MOT_OVL_001`).
2. **Timestamp(s)** of when the error first occurred and any recurrences.
3. **Mix information:**
   - Brand and expiration date of current mix.
   - When the mix was loaded.
   - Observed consistency (thick, normal, crystallized).
4. **Temperature readings:**
   - Freezing chamber temperature.
   - Mix chamber temperature.
   - Time temperature readings were taken.
5. **Detailed description of any noises** heard (grinding, squealing, humming, silence).
6. **Last maintenance date** (if documented on the machine).
7. **Steps already attempted** and their results.
8. **Machine serial number** and location (building/floor).

### Escalation Contact

- **L2 Help Desk Extension:** 5500
- **Urgent/After Hours:** ServeWell Operations Center 1-800-SERVE-911
- **Ticket Priority:** High (if no grinding) / Critical (if grinding detected)

---

## Related Runbooks

- `compressor-not-running.md`
- `soft-serve-temperature-control-troubleshooting.md`
- `creamtech-sc300-power-cycling.md`
- `frostypro-800-diagnostics-menu.md`
- `soft-serve-mix-preparation-and-loading.md`

---

## Revision History

| Version | Date       | Notes                                                                                                                                         |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for CreamTech v3.1 and FrostyPro v2.1; clarified immediate escalation criteria for grinding noise; added temperature baseline ranges. |
| 1.1     | 2025-03-22 | Added FrostyPro 800 v2.0 procedures; corrected motor reset menu path for SC-300 v3.0.                                                         |
| 1.0     | 2024-06-01 | Initial version; CreamTech SC-300 v2.1 and FrostyPro 800 v1.8 baseline.                                                                       |
