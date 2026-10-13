# Kiosk Software Crash Loop

## Overview

The ServeWell Kiosk application (v2.0 or v2.1) enters a continuous crash and restart cycle, preventing normal operation and guest ordering functionality. This runbook provides L1 diagnostic and initial resolution steps.

## Affected Systems

- **ServeWell Kiosk v2.0** (all hardware variants)
- **ServeWell Kiosk v2.1** (all hardware variants)
- **Operating System:** Linux-based embedded OS
- **Hardware:** Touch-screen and non-touch terminal models

## Symptoms

- Kiosk screen displays ServeWell splash screen, then goes black
- Application restarts automatically every 30–90 seconds
- "Welcome" screen never fully loads
- Guest cannot access menu or place orders
- Physical restart button has no lasting effect
- Error messages may flash briefly before restart (too fast to read)
- Kiosk becomes unresponsive to touch input

## Immediate Steps (First 2 Minutes)

Store staff or manager can attempt these without IT assistance:

1. **Power cycle the kiosk:** Press and hold the physical power button (rear or side panel) for 10 seconds until the screen goes dark. Wait 30 seconds, then press power again. Allow 2 minutes for full boot.

2. **Check physical connections:** Ensure the power cable is fully inserted into both the kiosk and wall outlet. Verify the network cable (if applicable) is firmly connected.

3. **Wait for stabilization:** If the kiosk boots successfully and remains stable for 5 minutes without crashing, the issue may have resolved. Proceed to L1 Diagnosis if crashes resume.

## L1 Diagnosis Steps

### Step 1: Verify Crash Loop Persistence

1. Confirm the kiosk is powered on and entering a restart cycle (splash screen → black screen → repeat).
2. Note the time crashes began and frequency (e.g., restart every 45 seconds).
3. Document any error messages visible on screen, even if only for 1–2 seconds.

### Step 2: Access Safe Mode

1. During the next boot cycle, watch for the splash screen to appear.
2. As soon as the splash screen displays, press and hold **Ctrl + Alt + S** simultaneously for 3 seconds.
3. **Expected result:** Boot menu appears with three options:
   - Normal Mode
   - Safe Mode (Diagnostic)
   - Recovery Console
4. Select **Safe Mode (Diagnostic)** using arrow keys and press **Enter**.

### Step 3: Boot into Safe Mode

1. Kiosk will load Safe Mode, which runs minimal services and disables third-party plugins.
2. Wait up to 3 minutes for Safe Mode to fully boot.
3. **If Safe Mode boots without crashing:** The crash is likely caused by a corrupted plugin or configuration file (proceed to Step 4).
4. **If Safe Mode also crashes:** Proceed to Step 5 (critical system issue).

### Step 4: Check Logs (Safe Mode)

1. In Safe Mode, navigate to the on-screen menu: **Diagnostics** → **View Logs**.
2. Alternatively, if SSH access is available (L2 may provide credentials), connect and run:
   ```
   tail -100 /var/log/servewell-kiosk/application.log
   ```
3. Look for the following error indicators:
   - **`SEGMENTATION FAULT`** – Indicates corrupted process memory
   - **`DATABASE LOCK`** – Indicates database file corruption
   - **`PLUGIN LOAD FAILED`** – Indicates corrupted or incompatible plugin
   - **`FILE NOT FOUND: /etc/servewell-kiosk/menu.db`** – Indicates missing configuration file
4. **Document the exact error message(s) and timestamp.**

### Step 5: Critical Crash Diagnosis (If Safe Mode Fails)

1. **If Safe Mode crashes**, the issue is at the kernel or core system level.
2. Attempt to access **Recovery Console** (press **Ctrl + Alt + R** during splash screen).
3. If Recovery Console is accessible, run:
   ```
   systemctl status servewell-kiosk
   journalctl -u servewell-kiosk -n 50
   ```
4. **Document all output and file a L2 escalation immediately** (see "When to Escalate to L2").

## L1 Resolution

### Resolution Step 1: Clear Cache (If Safe Mode Boots Successfully)

**Applies to:** Plugin load failures, corrupted temporary files

1. In Safe Mode, navigate to **Diagnostics** → **Clear Cache**.
2. Confirm the action when prompted.
3. Exit Safe Mode and reboot to **Normal Mode** (select during boot menu).
4. Monitor for 5 minutes to confirm stability.
5. **If stable:** Document the resolution as "Cache cleared" and close the ticket.
6. **If crashes resume:** Proceed to Resolution Step 2.

### Resolution Step 2: Reinstall Configuration Files

**Applies to:** Missing or corrupted menu and configuration files

1. Boot into Safe Mode (see L1 Diagnosis Step 2).
2. Navigate to **Diagnostics** → **Restore Default Configuration**.
3. **Warning:** This will reset all local customizations (promotions, menu modifications) to factory defaults. Confirm with the store manager before proceeding.
4. The system will reboot automatically.
5. Monitor for 5 minutes to confirm stability.
6. **If stable:** Document "Default configuration restored" and advise the store to reapply any local customizations. Close ticket.
7. **If crashes resume:** Proceed to Resolution Step 3.

### Resolution Step 3: Database Integrity Check

**Applies to:** Database corruption (identified by `DATABASE LOCK` or file system errors)

1. Boot into Safe Mode.
2. Navigate to **Diagnostics** → **Database Tools** → **Repair Database**.
3. Confirm the action; this process may take 2–5 minutes.
4. Allow the system to reboot automatically upon completion.
5. Monitor for 5 minutes.
6. **If stable:** Document "Database repaired" and close ticket.
7. **If crashes persist:** This requires L2 intervention. Escalate immediately (see "When to Escalate to L2").

### Resolution Step 4: Plugin Disable (Temporary Workaround)

**Applies to:** Specific plugin causing crashes (identified in logs)

1. Boot into Safe Mode.
2. Navigate to **Diagnostics** → **Manage Plugins**.
3. Identify any plugin marked as `FAILED TO LOAD` or `ERROR STATE`.
4. Select the failed plugin and choose **Disable**.
5. Reboot to Normal Mode.
6. Monitor for stability.
7. **Document which plugin was disabled** and escalate to L2 for plugin reinstall/update.

## When to Escalate to L2

**Escalate immediately if any of the following conditions are met:**

- ✓ **Safe Mode crashes or fails to boot** – Indicates kernel-level or hardware failure
- ✓ **Error logs contain:** `KERNEL PANIC`, `HARDWARE ERROR`, `FIRMWARE MISMATCH`
- ✓ **All L1 resolution steps (1–3) have been completed** and crashes continue
- ✓ **Recovery Console is inaccessible** (cannot press Ctrl+Alt+R)
- ✓ **Physical power cycle has been attempted 3+ times with no improvement**
- ✓ **Kiosk displays:** `UPDATE REQUIRED` or `VERSION MISMATCH` error messages
- ✓ **Multiple kiosks in the same location are crashing simultaneously**

### Information to Collect Before Escalating

Provide L2 support with the following details:

1. **Device Information:**
   - Kiosk serial number (label on rear or base)
   - Hardware model (touch-screen or non-touch)
   - Current software version (visible in Safe Mode → **System Info**)

2. **Crash Timeline:**
   - Date and time crashes began
   - Frequency (crashes every X seconds)
   - Any recent events (power loss, network outage, store update)

3. **Log Data:**
   - Last 100 lines of `/var/log/servewell-kiosk/application.log` (or screenshot of in-screen logs)
   - Full output of `journalctl -u servewell-kiosk` if available
   - Exact error message(s) observed

4. **Steps Already Attempted:**
   - List all L1 resolution steps completed
   - Confirm Safe Mode behavior (boots successfully, crashes, inaccessible)
   - Confirm cache clear/database repair results

5. **Impact Information:**
   - Store location/ID
   - Number of guests affected
   - Service downtime duration

## Related Runbooks

- `Kiosk_SafeMode_Access.md` – Detailed Safe Mode boot and navigation procedures
- `Kiosk_Plugin_Management.md` – Plugin installation, troubleshooting, and rollback
- `Kiosk_Software_Update_Rollback.md` – Version update and rollback procedures (L2 only)
- `Kiosk_Hardware_Troubleshooting.md` – Physical connection, power, and display issues
- `ServeWell_Database_Repair.md` – Advanced database corruption recovery (L2 only)
- `Kiosk_Network_Configuration.md` – Network connectivity and sync issues

## Revision History

| Version | Date       | Notes                                                                                       |
| ------- | ---------- | ------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for v2.0 and v2.1; clarified Safe Mode access keys; added Recovery Console guidance |
| 1.1     | 2025-03-20 | Added plugin disable workaround; expanded escalation criteria                               |
| 1.0     | 2024-06-01 | Initial version                                                                             |

---

**Document Control:** ServeWell Hospitality IT Help Desk | Confidential  
**Last Updated:** 2025-09-15 | **Next Review:** 2026-03-15
