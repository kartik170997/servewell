# Soft Serve Machine Error Code Reference

## Overview

This runbook provides L1 support agents with diagnostic and resolution procedures for error codes displayed on CreamTech SC-300/SC-500 and FrostyPro 800 soft serve machines. Error codes E01-E12 (CreamTech) and F01-F08 (FrostyPro) indicate specific hardware, temperature, or operational faults requiring immediate troubleshooting or escalation.

## Affected Systems

- **CreamTech SC-300** (all versions through v4.2)
- **CreamTech SC-500** (all versions through v4.2)
- **FrostyPro 800** (all versions through v2.8)

## Symptoms

- Machine displays alphanumeric error code on digital display panel
- Machine refuses to dispense product (soft serve or shake)
- Audible beeping or alarm sounds accompanying error code
- Machine enters lockout or safe mode (display frozen, no button response)
- Temperature warning lights illuminated on control panel
- Product leaking from dispensing head or refrigeration unit
- Machine powers on but immediately displays error code on startup

## Immediate Steps (First 2 Minutes)

1. **Note the exact error code** displayed on the machine's screen (e.g., "E05" or "F03"). Do not clear or reset the machine yet.
2. **Check physical condition**: Verify the dispensing head is properly seated, the product hopper is full, and no visible leaks are present.
3. **Power cycle attempt**: Turn the main power switch (located on the back or right side of the machine) OFF for 15 seconds, then back ON. Wait for the machine to complete its startup sequence (typically 30-60 seconds). Observe whether the error code clears.

---

## L1 Diagnosis Steps

### Step 1: Capture Error Code Information

1. Read the error code displayed on the digital panel. If multiple codes appear sequentially, note all of them in order.
2. Document the **exact error code** (including letter and two-digit number, e.g., "E07").
3. Note the **time of occurrence** and any actions performed immediately before the error appeared.
4. Take a **photograph** of the error code display if possible for escalation documentation.

### Step 2: Verify Machine Status and Operating Context

1. Check the **mode indicator light** or screen label:
   - Is the machine in **Standby**, **Operating**, **Cleaning**, or **Error** mode?
2. Confirm the **product type** loaded in the hopper (soft serve mix, shake base, etc.).
3. Ask the store staff: "When did this error first appear? Was the machine operating normally before?"

### Step 3: Access Diagnostic Mode (CreamTech SC-300/SC-500 only)

1. Locate the **Menu button** on the control panel (typically marked with three horizontal lines).
2. Press **Menu** once; the display should show "Main Menu."
3. Use the **Up/Down arrow buttons** to navigate to **"Diagnostics"** or **"System Status."**
4. Press **Select** (or the checkmark button).
5. The screen will display recent error history and current system status (temperature readings, motor status, etc.).
6. Compare the displayed temperature readings to the expected ranges in the **Error Code Table** below.

### Step 4: Access Diagnostic Mode (FrostyPro 800 only)

1. Press and hold the **Setup button** (marked "S" on the control panel) for 3 seconds.
2. The display will show "Setup Menu—PIN Required."
3. Enter the default PIN: **8800** (or the store's custom PIN if changed).
4. Navigate to **"System Diagnostics"** using arrow buttons.
5. Review **"Sensor Status"** and **"Temperature Log"** screens to identify out-of-range readings.

### Step 5: Consult Error Code Table

Locate your error code in the table below (Section 6). Identify:

- The **fault description**
- Whether it is **L1-resolvable** or requires **L2/vendor escalation**
- The **typical cause(s)**
- **Recommended troubleshooting steps**

---

## Error Code Table

### CreamTech SC-300 / SC-500 Error Codes

| Error Code | Description                                       | Typical Cause(s)                                                                    | L1 Resolvable? | First Steps                                                                                                                                                                                                                                                |
| ---------- | ------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **E01**    | Freezing Unit Temperature Out of Range (Too Cold) | Thermostat malfunction; refrigerant overcharge; sensor failure                      | **No—L2**      | Verify display temperature reading. Do not adjust thermostat manually. Escalate immediately.                                                                                                                                                               |
| **E02**    | Freezing Unit Temperature Out of Range (Too Warm) | Inadequate refrigeration; compressor not running; evaporator blockage               | **Yes**        | Check that condenser fan is running (listen for airflow). Verify room temperature is below 75°F. Clean condenser coils with compressed air (see Maintenance runbook). If temperature does not normalize within 10 minutes, escalate.                       |
| **E03**    | Motor/Pump Failure                                | Pump bearing seized; electrical connection loose; motor overload                    | **No—L2**      | Verify power cable is firmly connected. Attempt power cycle (Step 1, Immediate Steps). If motor does not engage on restart, escalate with error_code: E03.                                                                                                 |
| **E04**    | Hopper Low/Empty                                  | Product supply depleted; hopper sensor misaligned or failed                         | **Yes**        | Refill hopper with product mix. If sensor light remains lit after refill, remove hopper and inspect sensor arm for misalignment or debris. Clean with lint-free cloth. Reinstall and test.                                                                 |
| **E05**    | Dispensing Head Blockage                          | Frozen mix buildup in nozzle; product crystallization in tube                       | **Yes**        | Stop machine. Remove dispensing head (if accessible per location SOP). Soak head in warm water (not exceeding 110°F) for 5 minutes. Use soft brush to gently clear nozzle. Rinse thoroughly. Reinstall and run test cycle. If blockage persists, escalate. |
| **E06**    | Door/Access Panel Not Closed Properly             | Safety interlock not engaged; door latch broken; debris in seal                     | **Yes**        | Visually inspect door frame and seals for debris or foreign objects. Close door firmly until you hear a click. Verify no lights illuminate indicating open door. If interlock light persists, escalate.                                                    |
| **E07**    | Communication/Network Error                       | Ethernet cable disconnected; internal control board fault; network misconfiguration | **Partial**    | Check that Ethernet cable is firmly seated in the back port. Restart machine. If error recurs after restart, verify store network is operational by testing another device. If network is fine, escalate with error_code: E07.                             |
| **E08**    | Pressure System Fault                             | Low refrigerant charge; pressure switch failure; compressor discharge line blocked  | **No—L2**      | Do not attempt to recharge refrigerant. Confirm machine is powered off. Escalate immediately with error_code: E08.                                                                                                                                         |
| **E09**    | Electrical Supply Voltage Out of Range            | Unstable wall outlet; loose main power connection; facility electrical issue        | **Partial**    | Check that the machine power cord is fully inserted into the outlet. Verify no other high-load appliances are on the same circuit. If voltage error persists, escalate with error_code: E09 and request facility electrical check.                         |
| **E10**    | Sensor Failure (Unspecified)                      | Temperature probe disconnected; humidity sensor malfunction; multiple sensor faults | **No—L2**      | Attempt power cycle. If E10 recurs on restart, escalate with error_code: E10 and note which sensor light (if any) is illuminated on the control panel.                                                                                                     |
| **E11**    | Compressor Overload                               | High ambient temperature; condenser blockage; compressor bearing wear               | **Partial**    | Verify room temperature (should be ≤72°F for optimal operation). Clean condenser coils (compressed air). Allow machine to idle for 15 minutes to cool. Restart. If E11 recurs, escalate.                                                                   |
| **E12**    | System Lockout / Critical Fault                   | Multiple simultaneous errors; control board failure; backup battery depletion       | **No—L2**      | Perform a full power cycle: Switch OFF, wait 60 seconds, switch ON. If E12 persists after restart, do not attempt further troubleshooting. Escalate immediately with error_code: E12.                                                                      |

### FrostyPro 800 Error Codes

| Error Code | Description                               | Typical Cause(s)                                                          | L1 Resolvable? | First Steps                                                                                                                                                                                                                                                                |
| ---------- | ----------------------------------------- | ------------------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **F01**    | Compressor Failure                        | Electrical fault; mechanical seizure; start capacitor failure             | **No—L2**      | Verify power is supplied (control panel lights are on). Attempt power cycle once only. If compressor does not restart, escalate with error_code: F01.                                                                                                                      |
| **F02**    | Evaporator Temperature Sensor Malfunction | Probe disconnected; wiring fault; sensor degradation                      | **No—L2**      | Escalate immediately with error_code: F02. Do not attempt to reconnect internal probes.                                                                                                                                                                                    |
| **F03**    | Low Refrigerant Level                     | Slow leak; undercharge during commissioning; age-related loss             | **No—L2**      | Do not add refrigerant yourself. Escalate with error_code: F03 for professional refrigerant service.                                                                                                                                                                       |
| **F04**    | High Discharge Pressure                   | Condenser blockage; outdoor temperature excessive; refrigerant overcharge | **Partial**    | Clean condenser fins with compressed air (short bursts, do not use high pressure). Ensure machine is in an air-conditioned area (≤72°F ambient). If pressure remains elevated after 20 minutes, escalate with error_code: F04.                                             |
| **F05**    | Product Dispensing Motor Error            | Motor stall; belt/chain misalignment; gearbox failure                     | **No—L2**      | Confirm hopper is not empty (E-mode equivalent). Attempt one power cycle. If F05 persists, escalate with error_code: F05.                                                                                                                                                  |
| **F06**    | Hopper Level Sensor Failure               | Sensor arm bent; connector loose; capacitive sensor drift                 | **Partial**    | Power off the machine. Visually inspect the hopper sensor arm for bending or obstruction. If arm appears damaged, do not adjust. If arm is clear, verify connector is seated firmly at the control board. Power on and test. If F06 recurs, escalate with error_code: F06. |
| **F07**    | Control Module Communication Fault        | Internal data bus error; microprocessor fault; EEPROM corruption          | **No—L2**      | Attempt full power cycle (OFF for 60 seconds, then ON). If F07 persists, escalate with error_code: F07. Do not power cycle repeatedly.                                                                                                                                     |
| **F08**    | Critical System Failure / Shutdown        | Multiple concurrent faults; emergency stop activated; firmware crash      | **No—L2**      | Note the time and any events preceding the error. Perform one full power cycle (OFF 60 seconds, ON). If the machine does not fully restart, escalate immediately with error_code: F08 and any secondary error codes that appear.                                           |

---

## L1 Resolution

### Resolution Path A: Power Cycle (Errors E01, E03, E10, E12, F01, F07, F08)

1. Locate the main power switch on the back or right side of the machine.
2. Switch OFF completely.
3. Wait **60 seconds** (do not skip this step; allows capacitors to discharge).
4. Switch ON.
5. Allow the machine to complete its startup sequence (display will show initializing messages; typically 45–90 seconds).
6. If the error code no longer appears and the machine enters normal operating mode, document the resolution as "Power cycle resolved issue" and monitor machine for 30 minutes.
7. **If the error recurs within 1 hour, immediately escalate with error_code documented.**

### Resolution Path B: Hopper Refill / Sensor Check (Error E04)

1. Locate the product hopper (top or upper-front of machine; check your site-specific machine layout).
2. If hopper is empty or low, refill with the correct product mix to the full line.
3. Close the hopper securely.
4. If the error persists after refill:
   - Power off the machine.
   - Remove the hopper carefully (note orientation for reinstallation).
   - Inspect the hopper sensor arm (typically a thin lever or prong near the hopper base).
   - Gently clean the sensor with a dry, lint-free cloth. Do not bend the arm.
   - Reinstall the hopper, ensuring it seats fully.
   - Power on the machine.
5. If E04 recurs, escalate with error_code: E04 and note "Hopper refilled and sensor cleaned—error persists."

### Resolution Path C: Temperature Normalization (Errors E02, E11)

1. Confirm the surrounding room temperature is 72°F or below (verify with a store thermometer or HVAC team).
2. Locate the condenser unit (rear or side of machine—confirm location in your site-specific layout).
3. Using **compressed air** (short bursts from a standard air duster or compressor), gently clean the condenser coils. Do not use high-pressure water or compressed air at high PSI, which can damage fins.
4. Allow the machine to idle (powered on, in standby mode) for **15 minutes** without dispensing.
5. Monitor the temperature display if accessible (via Diagnostics mode, Step 3 or 4 above).
6. If the temperature reading returns to the normal range (typically 25–35°F for the freezing unit) and the error clears, document as resolved.
7. **If temperature does not normalize after 15 minutes, escalate with error_code and recent temperature readings.**

### Resolution Path D: Dispensing Head Cleaning (Error E05)

1. Power off the machine.
2. Locate the dispensing head/nozzle (at the front of the machine where product exits).
3. Determine if the dispensing head is removable (consult your site-specific machine SOP; some are, some are fixed).
   - **If removable**: Unscrew or unclip the head and remove it.
   - **If fixed**: You may only be able to access the nozzle tip.
4. Prepare a small container of warm water (approximately 100–110°F; do not exceed this temperature as it may damage seals).
5. Soak the removable head in warm water for **5 minutes**.
6. Using a soft-bristled brush or pipe cleaner, gently clear any frozen or crystallized product from the nozzle and internal channels.
7. Rinse thoroughly under warm running water.
8. Reinstall the head, ensuring all connections are secure.
9. Power on the machine and run a **test dispense cycle** (allow a small amount of product to flow for 3–5 seconds).
10. If product flows freely and E05 does not recur, document as resolved.
11. **If blockage persists or product does not flow, escalate with error_code: E05 and photos of the blockage if possible.**

### Resolution Path E: Door/Access Panel Reseating (Error E06)

1. Power on the machine (if not already on).
2. Visually inspect the entire door frame and rubber gasket seal for visible debris, ice buildup, or foreign objects.
3. If debris is present, carefully remove it by hand or with a soft cloth. Do not use sharp tools on seals.
4. Firmly close the door, applying even pressure across the entire frame. You should hear or feel a distinct **click** or engagement sound.
5. Verify that the "door open" indicator light (if present on the control panel) is **off/not illuminated**.
6. Attempt a test cycle (e.g., dispense a small amount of product). If the machine operates normally and E06 does not appear, the issue is resolved.
7. **If the door indicator light remains on or E06 recurs, escalate with error_code: E06 and note "Door latch may be broken."**

### Resolution Path F: Hopper Sensor Inspection (FrostyPro 800, Error F06)

1. Power off the machine.
2. Locate the hopper level sensor arm (consult your site-specific FrostyPro 800 layout documentation; it is typically a small lever on the hopper base).
3. Visually inspect the arm for bending, cracking, or obstruction by debris.
4. If debris is visible, gently remove it with a soft, dry cloth.
5. Confirm the sensor connector (small plug near the arm) is fully seated.
6. Power on the machine.
7. If the hopper is not empty, the F06 error should clear. Test by running a dispense cycle.
8. \*\*If F06 persists, escalate with error_code: F06 and note "Sensor arm
