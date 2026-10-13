# POS Screen Frozen or Unresponsive

## Overview

This runbook addresses situations where the FoodTech POS touchscreen displays the correct interface but does not respond to user taps or gestures. The issue may stem from OS-level freezing, touch driver malfunction, or display pipeline corruption—each requiring different remediation approaches to avoid data loss.

## Affected Systems

- **FoodTech POS v4.2.x** (all point releases)
- **FoodTech POS v5.1.x** (all point releases)
- **Hardware:** All FoodTech certified touchscreen terminals (10", 15", and 22" displays)
- **OS:** Windows Embedded POSReady 7 (v4.2.x); Windows 10 IoT Enterprise LTSC 2019 (v5.1.x)

## Symptoms

- Touchscreen accepts no input; taps and swipes produce no response
- Screen displays current menu, transaction data, or dashboard without visual corruption
- Application window title bar and menu items visible and correctly rendered
- Cursor may or may not respond to hardware mouse (if connected)
- Physical buttons on terminal (if present) may or may not be responsive
- No error dialogs or warning messages displayed
- Issue persists across multiple tap attempts over 10+ seconds

## Immediate Steps (First 2 Minutes)

**Store staff should attempt these steps before contacting IT:**

1. **Wait 30 seconds.** Occasional brief freezes may resolve autonomously. Do not repeatedly tap the screen.
2. **Check for system notifications.** Look for any dialog boxes or notification banners that may require dismissal (e.g., Windows Update prompts, license warnings). If found, try to dismiss with a mouse/keyboard if available.
3. **Attempt a graceful restart.** If staff have access to a keyboard, try `Alt+F4` to close the current application, or ask them to hold the power button for 5 seconds (soft shutdown). **Do NOT hold power for >10 seconds**—that forces a hard power-off and risks transaction data loss.
4. **If the system responds,** wait for a full boot (2–3 minutes) before attempting to use the POS again. If unresponsiveness persists after boot, escalate to L1 IT support.

---

## L1 Diagnosis Steps

### Step 1: Confirm the Issue

1. Contact the store and confirm:
   - Exactly what is displayed on screen (menu name, transaction status, dashboard view)
   - How long the freeze has been occurring
   - Whether any transactions are actively open (critical for data safety)
   - Whether the freeze occurred during a specific action (e.g., after opening register, during payment processing)
2. Ask them to attempt one more gentle tap on the screen and wait 5 seconds for response.
3. **Document the current state.** Ask them to leave the terminal untouched; you will guide them through diagnostics.

### Step 2: Distinguish OS Hang from Touch Driver Issue

1. **Request a mouse/keyboard test (if hardware available on-site):**
   - Ask staff to connect a USB mouse or keyboard if one is available in the store.
   - Instruct them to move the mouse or press a key (e.g., spacebar).
   - **If the mouse cursor moves or a key press registers:** The OS is responsive; the issue is touch-specific (go to Step 3).
   - **If nothing responds:** The OS is frozen; go to Step 4.

2. **If no mouse/keyboard is available,** proceed to Step 3 to isolate touch via calibration menu.

### Step 3: Test Touch Hardware (Touch-Specific Issue)

1. Power on the terminal if you have not already confirmed power state. If already on, confirm screen brightness is adequate (>30% expected).
2. **Access the FoodTech diagnostics menu:**
   - For **v4.2.x:** Simultaneously press `Ctrl+Alt+D` on the terminal keyboard (or use on-screen keyboard if touchscreen is slightly responsive). This opens the **Diagnostics Portal**.
   - For **v5.1.x:** From the login screen, press `Ctrl+Alt+Shift+D`. If already in the application, use `Ctrl+Esc` to return to login, then retry the key combination.
3. In the Diagnostics Portal, select **Hardware > Touch Panel > Test**.
4. **Instruct staff to tap the center of the screen when prompted.** If the touch panel responds in the diagnostics interface, the driver is functional but may be miscalibrated or locked by the application.
5. **If taps register in diagnostics but not in the POS application,** the issue is application-level (likely input focus or event handler corruption). Go to Step 5.
6. **If taps do not register in diagnostics,** the touch driver or hardware is defective. Go to Step 6.

### Step 4: Confirm OS Hang

1. If mouse/keyboard input does not register, the OS is non-responsive.
2. **Check for signs of recovery:**
   - Wait an additional 60 seconds and ask staff to observe the cursor, keyboard LEDs, or any status indicator lights on the terminal.
   - If any change is observed, document it and return to Step 2.
3. **If no recovery after 60 seconds,** the OS has deadlocked. Note the exact time and what was on screen. Proceed to L1 Resolution (Step 1: Graceful Restart).

### Step 5: Isolate Application-Level Issue

1. **Access Task Manager (if any input device responds):**
   - Press `Ctrl+Shift+Esc` to open Task Manager.
   - Locate the FoodTech POS process (typically labeled `FoodTechPOS.exe` or `RestaurantManager.exe`).
   - Observe the **CPU** and **Memory** columns. High CPU (>80%) or runaway memory (>90% of available) indicates an application hang.
2. **Check the Event Viewer for errors:**
   - Press `Win+R`, type `eventvwr.msc`, and press Enter.
   - Navigate to **Windows Logs > Application**.
   - Look for errors logged within the last 10 minutes with source "FoodTech" or "POSEngine".
   - Document any error codes (e.g., "0x80000001", "Access Violation at 0x00123ABC").
3. **If high resource usage or recent critical errors are found,** the application process has crashed or deadlocked. Proceed to L1 Resolution (Step 2: Force-Quit Application).

---

## L1 Resolution

### Resolution Attempt 1: Graceful Application Restart (No Data Loss Risk)

**Timeline: 3–5 minutes**

**Prerequisites:** Must have keyboard/mouse access or on-screen keyboard available.

1. **Close the FoodTech POS application gracefully:**
   - Press `Alt+F4` while the FoodTech window is active.
   - If a dialog appears asking "Save changes?" or "Close open transactions?", select **Yes** to save.
   - **Do not force-quit yet.** Wait 10 seconds for the application to terminate.

2. **Verify the application has closed:**
   - The desktop should be visible. If the FoodTech window remains, proceed to Resolution Attempt 2.

3. **Restart the FoodTech POS application:**
   - Double-click the FoodTech POS icon on the desktop, or navigate to **Start Menu > Programs > FoodTech POS** and launch it.
   - Allow the application 60 seconds to fully load and authenticate.

4. **Test responsiveness:**
   - Attempt a simple action: tap the screen or press a button within the application.
   - If the screen responds normally, the issue has been resolved. **Document the resolution as "Application restart."**
   - If the screen remains frozen, proceed to Resolution Attempt 2.

---

### Resolution Attempt 2: Force-Quit and Restart (Low Data Loss Risk if no open transactions)

**Timeline: 5–8 minutes | Risk: Potential loss of unsaved transaction data**

**Prerequisites:** Confirm with staff that no transactions are actively being processed.

1. **Access Task Manager:**
   - Press `Ctrl+Shift+Esc`.

2. **Locate and force-quit the FoodTech process:**
   - Find `FoodTechPOS.exe`, `RestaurantManager.exe`, or similar in the process list.
   - Right-click and select **End Task**.
   - Wait 5 seconds for the process to terminate. If it does not, repeat the action.

3. **Close Task Manager** (`Alt+F4`).

4. **Restart the application** (same steps as Resolution Attempt 1, Step 3).

5. **Upon restart, verify data integrity:**
   - Staff should check the **Transaction History** or **Register Reconciliation** screen to confirm no sales were lost.
   - If discrepancies are found, contact the store manager and note the incident for L2 review.

6. **If responsiveness is restored,** the issue is resolved. Document the incident and close the ticket.

7. **If the screen remains frozen after restart,** proceed to Resolution Attempt 3.

---

### Resolution Attempt 3: Soft Reboot (OS-Level Recovery)

**Timeline: 8–10 minutes | Risk: Moderate data loss risk if transactions are open**

**Prerequisite:** Confirm with store staff that the register has been closed and no active transactions remain. If uncertain, escalate to L2.

1. **Initiate a graceful system shutdown:**
   - Press `Ctrl+Alt+Delete` to open the security menu.
   - Select **Sign Out** or **Shut Down** (depending on OS version).
   - Confirm and wait for the system to power down (should take 30–60 seconds).

2. **If the system does not shut down within 90 seconds,** proceed to Step 3 (hard power-off).

3. **Hard power-off (if graceful shutdown fails):**
   - Instruct staff to hold the physical power button on the terminal for 5 seconds, then release.
   - The system should shut down within 30 seconds. Do not hold the button longer.

4. **Wait 30 seconds** with the terminal powered off.

5. **Power the terminal back on** by pressing the power button.

6. **Allow a full boot cycle:** 3–5 minutes. The system will perform integrity checks and may take longer than normal on first boot after an improper shutdown.

7. **Upon boot completion, log back into FoodTech POS** with store credentials.

8. **Test responsiveness:** Perform a simple transaction (e.g., open register, ring up a test item, then void).

9. **If responsiveness is restored,** the issue is resolved. Document the reboot and note the time of the incident.

10. **If the screen remains frozen after a full reboot,** **escalate to L2 immediately** with all diagnostic information collected.

---

### Resolution Attempt 4: Touch Driver Restart (If Touch Issue Diagnosed)

**Timeline: 3–4 minutes | Data Risk: None**

**Applicable only if Step 3 (Touch Hardware Test) confirmed touch driver is loaded but unresponsive.**

1. **Access Device Manager:**
   - Press `Win+R`, type `devmgmt.msc`, and press Enter.

2. **Locate the touch panel driver:**
   - Expand **Human Interface Devices** (or **Touch Screen / Pointing Devices**).
   - Find the entry for the touchscreen (typically labeled "FoodTech Touch Panel" or "Capacitive Touch Screen").

3. **Disable the driver:**
   - Right-click the touch device and select **Disable device**.
   - Confirm the action when prompted.

4. **Wait 5 seconds.**

5. **Re-enable the driver:**
   - Right-click the same device and select **Enable device**.
   - Wait 10 seconds for the driver to reload.

6. **Close Device Manager** and test the touchscreen in the FoodTech application.

7. **If the screen responds,** the driver needed to be reset. Document and close the ticket.

8. **If the screen remains unresponsive,** the touch driver may be corrupted. Proceed to **When to Escalate to L2**.

---

## When to Escalate to L2

**Escalate immediately if any of the following conditions are met:**

- **Unresponsive after three resolution attempts:** The system remains frozen after (1) application restart, (2) force-quit and restart, and (3) full OS reboot.
- **Hardware diagnostics indicate touch panel failure:** Touch hardware does not respond in the Diagnostics Portal hardware test.
- **Active transactions are open and cannot be safely closed:** Staff reports unsaved sales or open register that cannot be closed without risking data loss.
- **OS-level symptoms persist after reboot:** Task Manager shows runaway processes, or Event Viewer shows repeated critical errors from FoodTech or system processes.
- **Multiple terminals affected simultaneously:** If more than one POS terminal in the store exhibits the same symptom, this may indicate a network, server, or infrastructure issue.
- **Frozen screen persists >30 minutes despite all attempts:** Suggests hardware failure or systemic issue beyond L1 scope.

### Information to Collect Before Escalating

Provide L2 with the following details:

1. **Terminal Details:**
   - Store name and location
   - Terminal serial number (on device label or in **Settings > System Information**)
   - FoodTech POS version (visible in **Help > About**)
   - OS version (from Task Manager or System Information)
   - Hardware model (e.g., "FoodTech 15-inch Touch Terminal")

2. **Incident Timeline:**
   - Exact date and time the freeze began
   - What was displayed on screen (menu, transaction detail, dashboard)
   - What action triggered the freeze (if known)
   - How long the terminal has been unresponsive

3. **Diagnostic Results:**
   - Output from **Diagnostics Portal > Hardware > Touch Panel > Test** (if touch was tested)
   - Any error codes from **Event Viewer > Application** (screenshot or text export)
   - Task Manager screenshot showing CPU/Memory usage of FoodTech process (if captured)
   - Results of each resolution attempt (did the screen respond after application restart? after reboot?)

4. **Context:**
   - Whether transactions were open when the freeze occurred
   - Whether any data loss has been reported
   - Any recent changes to the terminal (software updates, new peripherals, network changes)
   - Whether the issue is intermittent or continuous since discovery

5. **Network Information:**
   - Terminal IP address (from **Settings > Network > IPv4 Address**)
   - Whether the terminal can reach the FoodTech application server (if applicable)
   - Any network connectivity issues reported in the store

---

## Related Runbooks

- `POS-Application-Crash-or-Wont-Start.md`
- `POS-Touchscreen-Calibration-and-Drift.md`
- `POS-Network-Connectivity-Troubleshooting.md`
- `POS-Database-Recovery-After-Unexpected-Shutdown.md`
- `Windows-Embedded-System-Performance-Optimization.md`
- `FoodTech-Event-Log-Analysis.md`

---

## Revision History

| Version | Date       | Notes                                                                                                                         |
| ------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for FoodTech POS v5.1.x; added touch driver diagnostics; clarified data loss risks and escalation criteria            |
| 1.1     | 2024-11-30 | Expanded Step 3 (touch hardware testing); added Task Manager memory/CPU analysis; clarified graceful vs. hard shutdown timing |
| 1.0     | 2024-06-01 | Initial version; covered v4.2.x systems and basic restart procedures                                                          |
