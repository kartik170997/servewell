# Soft Serve Machine Overcooling / Product Frozen Solid

## Overview

The soft serve product has solidified in the barrel and the machine is unable to dispense or has entered a continuous freeze cycle. This runbook covers diagnosis and resolution for CreamTech SC-300/SC-500 and FrostyPro 800 models, including the known E04 false alarm condition on CreamTech SC-300 units operating in high ambient temperatures.

## Affected Systems

- **CreamTech SC-300** (firmware versions < 3.1.2 susceptible to E04 false alarm in ambient temps > 35°C)
- **CreamTech SC-300** (firmware 3.1.2 and later - E04 false alarm resolved)
- **CreamTech SC-500** (all current firmware versions)
- **FrostyPro 800** (all current firmware versions)

## Symptoms

- Product will not dispense from nozzle; machine makes grinding or stuttering sounds
- Machine displays **E04 error code** (CreamTech models only)
- Barrel visibly contains frozen/crystallized product
- Machine enters continuous freeze/cooling cycle and will not stop
- Display shows "FROZEN PRODUCT" warning or similar message
- Ambient temperature in store > 35°C with E04 error present (CreamTech SC-300 only, firmware < 3.1.2)
- No product flow within 30 seconds of activation

## Immediate Steps (First 2 Minutes)

**Store staff should perform these checks before contacting IT:**

1. **Power cycle the machine**: Turn off the machine via the main power switch, wait 30 seconds, power on again. Observe if error clears.
2. **Check ambient temperature**: Confirm store temperature with thermostat or HVAC system. Note the current temperature.
3. **Verify machine location**: Confirm the machine is not in direct sunlight or next to heat sources (ovens, heating vents).
4. **Do NOT attempt to manually rotate the barrel** or force dispense handles in any direction.

## L1 Diagnosis Steps

1. **Verify the error code**:
   - On CreamTech SC-300/SC-500: Check the LED display panel on the front of the machine. Document the exact error code shown (e.g., E04, E12, etc.).
   - On FrostyPro 800: Check the touchscreen display for error messages or fault codes.
   - Note the time the error was first observed.

2. **Confirm ambient conditions**:
   - Ask store staff for current room temperature.
   - If **CreamTech SC-300 with E04 error AND ambient > 35°C**: Check the firmware version (see Step 3 below). This may be the known E04 false alarm condition.

3. **Check firmware version (CreamTech models only)**:
   - Press the **MENU** button on the machine's control panel.
   - Navigate to **SYSTEM INFO** > **FIRMWARE VERSION**.
   - Document the displayed version number (format: X.X.X).
   - If version is **3.1.2 or higher**, the E04 false alarm has been patched.
   - If version is **below 3.1.2** and ambient > 35°C, proceed to E04 false alarm resolution (Section 5.1).

4. **Assess product state**:
   - Visually inspect the barrel through the transparent window (if available).
   - Attempt a short test dispense (2-3 seconds) at the lowest speed setting. Listen for mechanical resistance or grinding sounds.
   - If no product flows and machine makes grinding/stuttering noise: product is frozen solid. Proceed to L1 Resolution.

5. **Check freeze mode status**:
   - On CreamTech models: Press **MENU** > **OPERATING STATUS** > **FREEZE MODE**.
   - Confirm whether freeze mode is **ON**, **OFF**, or **CONTINUOUS**.
   - Note the current product temperature (usually displayed nearby or in **DIAGNOSTICS** menu).
   - If product temperature is below -5°C and freeze mode is CONTINUOUS: proceed to Resolution.

6. **Document findings**:
   - Record error code, firmware version, ambient temperature, freeze mode status, and product temperature.
   - Take a photo of the error display if possible.

## L1 Resolution

### Resolution Path 1: E04 False Alarm (CreamTech SC-300, Firmware < 3.1.2, Ambient > 35°C)

1. **Confirm the false alarm condition**:
   - Verify ambient temperature is > 35°C.
   - Verify firmware version is below 3.1.2.
   - Verify barrel can rotate freely when machine is powered off (gently push the dispense lever side-to-side; it should move without excessive resistance).

2. **Perform temporary workaround**:
   - Turn off **FREEZE MODE**: Press **MENU** > **FREEZE MODE** > **OFF**.
   - Press **CONFIRM** to deactivate freeze mode.
   - Wait 60 seconds for the system to stabilize.
   - Check if E04 error clears from the display.

3. **If E04 clears**:
   - Advise store staff to **reduce ambient temperature** if possible (increase AC, close blinds, relocate machine away from heat sources).
   - Inform them that freeze mode can remain OFF until the unit is upgraded to firmware 3.1.2.
   - Schedule L2 escalation to plan firmware upgrade (see When to Escalate section).

4. **If E04 persists**:
   - Power cycle the machine and proceed to Resolution Path 2.

### Resolution Path 2: Product Frozen Solid (All Models, All Conditions)

1. **Disable freeze mode**:
   - Press **MENU** > **FREEZE MODE** > **OFF** (CreamTech models).
   - On FrostyPro 800: Press **SETTINGS** > **COOLING** > **DISABLE**.
   - Confirm the setting is saved.

2. **Allow ambient thaw (minimum 20 minutes)**:
   - Keep the machine powered ON with freeze mode disabled.
   - Do NOT attempt to manually rotate the barrel or apply external heat.
   - Monitor the product temperature via the display. It should begin rising gradually.
   - Allow the barrel to return to approximately 0°C to 5°C (display should show product temperature rising).

3. **Monitor thaw progress**:
   - Check the display every 5 minutes after the first 10 minutes.
   - If temperature is not rising after 15 minutes, proceed to Step 5 (possible mechanical failure).
   - Once product temperature reaches 5°C or higher, attempt a test dispense.

4. **Resume normal operation**:
   - If product dispenses freely, re-enable freeze mode: **MENU** > **FREEZE MODE** > **ON**.
   - Set the machine to normal operating mode.
   - Instruct store staff to monitor product consistency over the next 2-4 hours.
   - Document resolution time and date.

5. **If product temperature does not rise or machine makes grinding sounds**:
   - Do NOT force the barrel or attempt manual rotation.
   - This indicates possible mechanical failure (frozen compressor, drive mechanism jam, or sensor malfunction).
   - Proceed to "When to Escalate to L2" section.

## When to Escalate to L2

**Escalate immediately if any of the following conditions are met:**

1. **E04 error persists after power cycle AND ambient temperature is < 35°C** (not a false alarm condition).
2. **Product temperature does not rise after 20 minutes with freeze mode disabled** (possible compressor or thermostat failure).
3. **Machine makes continuous grinding, squealing, or mechanical noise** during thaw attempt (drive mechanism or motor failure).
4. **Barrel cannot be rotated when powered OFF** (mechanical jam or compressor seizure).
5. **CreamTech SC-300 firmware is below 3.1.2 and you require a permanent fix** (schedule firmware upgrade).
6. **FrostyPro 800 displays error codes other than overcooling warnings** (sensor or control board failure).
7. **Product has been frozen for > 48 hours and thaw does not progress** (possible unit replacement required).

**Information to collect before escalating:**

- Machine model and serial number (located on the rear panel or beneath the machine).
- Firmware version (or software build number for FrostyPro 800).
- Current and ambient temperature readings.
- Error codes displayed during the incident.
- Time and date the issue was first reported.
- Actions already taken (power cycles, freeze mode changes, etc.).
- Photos of the error display and barrel contents (if accessible).
- Store location and contact information for L2 technician scheduling.

## Related Runbooks

- `creamtech-sc300-firmware-upgrade.md`
- `soft-serve-machine-error-code-reference.md`
- `frostypro-800-temperature-sensor-troubleshooting.md`
- `soft-serve-compressor-failure-diagnosis.md`
- `machine-power-cycle-procedure.md`

## Revision History

| Version | Date       | Notes                                                                                                                           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for CreamTech SC-300 firmware 3.1.2 E04 false alarm fix; added FrostyPro 800 guidance; clarified thaw procedure safety. |
| 1.1     | 2024-12-01 | Added temperature monitoring thresholds; expanded escalation criteria.                                                          |
| 1.0     | 2024-06-01 | Initial version.                                                                                                                |
