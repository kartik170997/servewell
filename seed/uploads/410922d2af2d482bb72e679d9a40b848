# Kiosk Touchscreen Calibration

## Overview

This runbook addresses touch input registration errors on ServeWell Kiosk v2.1 and TouchPoint K1 units where user taps register in incorrect on-screen locations. Touchscreen calibration typically resolves drift issues caused by thermal variations, prolonged use, or environmental factors.

## Affected Systems

- **ServeWell Kiosk v2.1** (all hardware revisions)
- **TouchPoint K1** (firmware v3.2+)
- **Touchscreen Controller**: Capacitive multi-touch panel with integrated driver v2.8+

## Symptoms

- Touch input registers 0.5–2 inches away from actual tap location (drift)
- Buttons in specific screen areas become unresponsive or register wrong selections
- Calibration drift increases throughout the day, improves after restart
- Users report "ghost touches" or delayed response in upper-left or lower-right corners
- Calibration warning message appears on boot: `WARN: Touch offset exceeds ±15px`
- Multiple restart cycles do not resolve the issue

## Immediate Steps (First 2 Minutes)

Store staff may perform these preliminary checks before contacting IT:

1. **Power cycle the kiosk**: Turn off the unit via the physical power button on the rear panel. Wait 10 seconds, then power back on. Allow 30 seconds for full boot sequence.
2. **Test touch responsiveness**: Once booted, tap the four corners of the screen (top-left, top-right, bottom-left, bottom-right) to confirm drift pattern.
3. **Document the issue**: Note the time of day, which screen areas are affected, and whether the issue appeared suddenly or has been worsening. Collect this information for the IT ticket.

**If power cycle resolves the issue**: No further action required. Log in the store's incident tracking system as "resolved via restart."

**If issue persists after power cycle**: Proceed to L1 Diagnosis Steps.

## L1 Diagnosis Steps

1. **Verify system version and status**
   - From the main kiosk home screen, press the three-line menu icon (≡) in the top-right corner
   - Navigate to **Settings** → **System Information**
   - Confirm the version displays as **ServeWell Kiosk v2.1.x** or **TouchPoint K1 firmware v3.2.x or higher**
   - Check the **Last Calibration Date** field; if older than 90 days, calibration is overdue

2. **Access the Calibration Mode** (5-tap hidden sequence)
   - Return to the main home screen
   - Using firm, deliberate taps, rapidly tap the **top-left corner** of the touchscreen exactly **5 times** in quick succession (within 2 seconds)
   - The screen should display the **Calibration Entry Dialog** with the message: `Entering Calibration Mode. Please confirm admin credentials.`
   - If the dialog does not appear after 3 attempts, verify the system is on ServeWell Kiosk v2.1; earlier versions do not support this feature

3. **Authenticate for calibration access**
   - A PIN entry pad will appear
   - Enter the store's standard IT admin PIN (default: `7392` unless changed during initial setup)
   - Press **Confirm**
   - **Expected result**: Screen transitions to a solid blue background with on-screen calibration targets

4. **Observe the calibration drift pattern**
   - The screen displays **9 calibration targets** arranged in a 3×3 grid (corners, edges, center)
   - Tap each target **once** in sequence as directed by on-screen prompts
   - Observe where your tap registers compared to the target position
   - **If drift is consistent** (always offset in the same direction): Proceed to L1 Resolution
   - **If drift is random or inconsistent**: Escalate to L2 (see When to Escalate section)

5. **Review calibration data**
   - After completing all 9 targets, the system displays **Calibration Report** showing offset values for each point
   - Look for any offset value exceeding **±20 pixels** in the X or Y axis
   - If all values are within ±15 pixels and the test is acceptable, the system may auto-apply the calibration
   - Note any error codes displayed (e.g., `ERR_CAL_003` = target detection failure)

## L1 Resolution

### Resolution Path A: Standard Recalibration (Most Common)

1. **Complete the calibration process**
   - While in Calibration Mode (blue screen with targets), ensure you have a clear, unobstructed view of the screen
   - Tap each of the 9 targets carefully and deliberately, ensuring your finger is centered on the bullseye icon
   - Avoid tapping too quickly; allow 0.5 seconds between taps
   - If you miss a target, a warning message appears; tap **Retry** to repeat that point

2. **Accept or reject the calibration**
   - After all 9 points are completed, the system displays: `Apply New Calibration? [YES] [NO]`
   - Review the **Calibration Offset Summary** shown on screen
   - **Select YES** to apply the new calibration
   - The system will confirm: `Calibration Applied. Exiting Calibration Mode.` and return to the home screen

3. **Verify the fix**
   - Return to the main home screen
   - Test touch responsiveness by tapping buttons across all screen areas (especially corners)
   - Attempt a guest transaction by pressing **Start Order** or equivalent button in your location
   - Confirm that selections register in the intended location
   - If the issue is resolved, document the ticket as **resolved** with timestamp

### Resolution Path B: Recalibration with Screen Cleaning (If Drift Persists)

1. **Exit Calibration Mode without saving**
   - If the recalibration does not resolve the drift (offset values still exceed ±15 pixels), press **NO** at the `Apply New Calibration?` prompt
   - Return to the home screen

2. **Clean the touchscreen**
   - **Power off the kiosk** completely using the rear power button
   - Allow 5 minutes for the unit to cool
   - Using a **microfiber cloth** (provided in the kiosk maintenance kit), gently wipe the entire screen surface in circular motions
   - Use **distilled water only**; do not apply pressure or use cleaning solutions (risk of damage)
   - Ensure the screen is completely dry before powering back on

3. **Perform recalibration again**
   - Power the kiosk back on
   - Repeat the 5-tap sequence to re-enter Calibration Mode
   - Complete all 9 calibration targets with careful, deliberate taps
   - Review the offset values; they should now be within ±10 pixels if cleaning resolved contamination
   - Select **YES** to apply the new calibration

4. **Re-test functionality**
   - Confirm touch responsiveness across all screen areas
   - If resolved, close the ticket as **resolved via recalibration and cleaning**

### Resolution Path C: Restart and Reboot Sequence (If Calibration Won't Persist)

1. **Verify the calibration was saved**
   - Return to **Settings** → **System Information**
   - Check that **Last Calibration Date** now shows today's date and time
   - **If the date is not updated**: The calibration was not saved; proceed to step 2

2. **Perform a controlled reboot**
   - Press the physical power button on the rear of the kiosk
   - Wait for the graceful shutdown sequence to complete (approximately 30 seconds)
   - The screen will display: `Shutting Down. Please Wait.`
   - Once the display goes dark, wait 10 seconds
   - Press the power button again to restart

3. **Verify calibration persistence**
   - After boot completes, test the touchscreen again
   - Tap corners and edges to confirm calibration has been retained
   - If touch responsiveness is now correct, close the ticket

## When to Escalate to L2

Escalate to L2 support and provide all information below if any of the following conditions are met:

### Escalation Criteria

- **Calibration will not save**: After completing the calibration process and selecting **YES**, the system does not retain the new calibration after restart (Last Calibration Date does not update)
- **Offset values exceed ±25 pixels**: Even after screen cleaning and recalibration, the Calibration Report shows individual points with drift greater than ±25 pixels
- **Error codes appear**: Calibration process generates error codes such as:
  - `ERR_CAL_001` (Touch driver unresponsive)
  - `ERR_CAL_002` (Calibration data corruption)
  - `ERR_CAL_003` (Target detection failure on 2+ points)
  - `ERR_CAL_004` (Firmware mismatch)
- **Random/inconsistent drift**: Touch offset varies unpredictably across multiple test attempts (suggests hardware failure rather than software calibration issue)
- **Entire screen unresponsive**: Touchscreen does not respond to any input, even in Calibration Mode
- **Multiple units affected**: Two or more kiosks in the same location exhibit identical drift patterns (suggests environmental factor or network configuration issue)
- **Issue persists after 2 full recalibration cycles**: Following steps in Resolution Path A and B, the problem remains unresolved

### Information to Collect Before Escalating

Gather the following details and include in the L2 escalation ticket:

- **Kiosk Serial Number**: Located on the rear panel below the power connector
- **System Version**: From **Settings** → **System Information** → **Version** field
- **Touch Driver Version**: From **Settings** → **System Information** → **Touch Controller Firmware**
- **Last Calibration Date and Time**: Exact timestamp from system information
- **Drift Pattern Description**: E.g., "All taps register 1.5 inches to the right of intended location" or "Drift increases as screen temperature rises"
- **Offset Values from Calibration Report**: Screenshot or manual note of the 9-point offset summary (X and Y values for all points)
- **Error Codes**: Any error codes displayed during calibration attempts
- **Environmental Notes**: Room temperature, humidity level, proximity to direct sunlight, HVAC vents
- **Frequency**: How often the issue occurs (persistent, intermittent, time-of-day dependent)
- **Store Location and Kiosk Position**: Specific store identifier and whether the kiosk is in a high-traffic area, near windows, or near heat sources
- **Troubleshooting Performed**: List all steps already attempted (power cycle, cleaning, recalibration attempts) and results

## Related Runbooks

- [Kiosk_Hardware_Diagnostics.md](./Kiosk_Hardware_Diagnostics.md)
- [TouchPoint_K1_Firmware_Update.md](./TouchPoint_K1_Firmware_Update.md)
- [Kiosk_Display_Issues.md](./Kiosk_Display_Issues.md)
- [Kiosk_Power_and_Reboot_Procedures.md](./Kiosk_Power_and_Reboot_Procedures.md)
- [ServeWell_System_Information_Access.md](./ServeWell_System_Information_Access.md)

## Revision History

| Version | Date       | Notes                                                                                                                           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for ServeWell v2.1 and TouchPoint K1 firmware v3.2+; clarified 5-tap calibration entry sequence and escalation criteria |
| 1.1     | 2024-12-10 | Added Resolution Path C for calibration persistence issues; expanded environmental troubleshooting notes                        |
| 1.0     | 2024-06-01 | Initial version                                                                                                                 |
