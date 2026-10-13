# POS Software Update Stuck

## Overview

This runbook addresses FoodTech POS software updates that fail to complete, hang at a specific percentage, display error messages, or leave terminals in an unusable state. Improper handling during stuck updates can cause data loss or system corruption; follow these steps carefully before any escalation to L2.

## Affected Systems

- **Application:** FoodTech POS v4.2.0–v4.2.2 (upgrading to v4.2.3 or v5.1.x)
- **Terminal Models:** All FoodTech-certified POS hardware (touchscreen and traditional terminals)
- **Operating Systems:** Linux-based POS OS; Windows embedded terminals running FoodTech POS
- **Network Environment:** Both standalone and networked configurations

## Symptoms

- Update progress bar frozen at any percentage (e.g., 45%, 67%, 92%) for >10 minutes
- Error message displayed on terminal screen (e.g., "Update Failed," "Insufficient Storage," "Network Error")
- Terminal screen goes black or shows only a blinking cursor during update
- Update appears to complete but terminal fails to boot into normal POS interface
- Terminal stuck in "Update Mode" with no responsiveness to touch or button input
- Update log shows incomplete entries or repeated error messages
- Cash drawer, card reader, or receipt printer unresponsive after partial update

## Immediate Steps (First 2 Minutes)

1. **Do NOT power cycle the terminal.** Interrupting an update mid-process can corrupt the system and require full hardware replacement.

2. **Note the current screen display.** Take a photo or note the exact error message, percentage displayed, and any on-screen text.

3. **Verify network connectivity.** If the terminal is networked, check that the WiFi or Ethernet cable is firmly connected. A dropped connection during v5.1.x downloads can halt the update.

4. **Have the store manager locate the terminal's power cable and serial number** (printed on back or bottom of device) for L1 escalation if needed.

## L1 Diagnosis Steps

### Step 1: Assess Terminal Responsiveness

1. Attempt to tap the screen or press any physical button on the terminal.
2. Wait 30 seconds for a response.
3. **If responsive:** Proceed to Step 2.
4. **If unresponsive:** Note this and proceed to Step 3.

### Step 2: Check for Error Messages

1. Read the exact error message on the terminal screen word-for-word.
2. Note the percentage displayed (if any) and whether a progress bar is moving.
3. **Common errors and meanings:**
   - **"Insufficient Storage (Error 0x4F)"** → Device storage full; v5.1.x requires ≥2 GB free space
   - **"Network Timeout (Error 0x2E)"** → Download interrupted; network dropped during update
   - **"Checksum Mismatch (Error 0x6A)"** → Downloaded file corrupted; restart required
   - **"Update Service Unavailable (Error 0x5C)"** → Central update server offline (check with L2)
4. Document the error code (format: 0xXX or numeric).

### Step 3: Attempt Safe Recovery (if screen unresponsive)

1. Wait a full 5 minutes without touching the device. Some updates process silently during final stages.
2. After 5 minutes, press and hold the **Menu button** (or rightmost button on device) for 3 seconds.
3. **If terminal responds:** A menu should appear; proceed to Step 4.
4. **If terminal does not respond:** Note this as "unresponsive; no menu entry" and escalate to L2 immediately.

### Step 4: Access Diagnostic Mode

1. From the menu (if available), navigate to **Settings → System → Service Menu** (requires PIN; default is **9988** for ServeWell installations).
2. Select **Update Status** or **System Information**.
3. Note the current software version, update target version, and any status message.
4. **If update is still in progress:** Select **View Update Log** and read the last 10 lines of output.
5. Provide this information to L1 supervisor or document for escalation.

### Step 5: Check Physical Connections

1. Inspect the power cable connection to the terminal (should be firmly seated).
2. For networked terminals, check Ethernet cable or WiFi indicator light:
   - **WiFi indicator:** Should show a solid connection symbol; if blinking or off, connection is unstable.
   - **Ethernet:** Cable should be firmly connected to both terminal and network jack.
3. If connection is loose, reseat the cable and wait 2 minutes for the terminal to resume the update.
4. Do not restart the terminal; allow it to continue.

## L1 Resolution

### Resolution Path 1: Update Stuck at Percentage (Progress Bar Not Moving)

1. **Verify the update is truly stuck** (not just slow):
   - Wait an additional 5 minutes without interaction.
   - v5.1.x updates can take 8–12 minutes on slower connections; v4.2.3 should complete in 3–5 minutes.

2. **If stuck for >15 minutes total:**
   - Check network connectivity (Step 3, above).
   - If WiFi, move the terminal closer to the router and wait another 3 minutes.
   - If Ethernet, verify the cable is connected to an active network port (check for LED light on port).

3. **If network is confirmed stable and update still stuck:**
   - Proceed to "When to Escalate to L2" section; escalation is required.

---

### Resolution Path 2: Update Displays Checksum Error (0x6A)

1. **Network interruption caused file corruption during download.** Recovery is possible:
   - Ensure terminal remains powered on and connected to network.
   - From the error screen, select **Retry Update** (if button available).
   - Terminal will re-download the update package and resume.

2. **If "Retry" button not available:**
   - Note this error and escalate to L2 for manual update restart.

---

### Resolution Path 3: Update Completes But Terminal Won't Boot

1. **Terminal may be in final initialization phase.** Do not power cycle.
   - Wait a full 10 minutes. The FoodTech boot sequence can take 5–7 minutes after update completion.
   - Watch for any LED indicators or screen activity.

2. **If terminal still shows blank/black screen after 10 minutes:**
   - Proceed to escalation; L2 may need to perform safe boot or rollback.

---

### Resolution Path 4: Insufficient Storage Error (0x4F)

1. **This error indicates v5.1.x cannot download due to <2 GB free space.** Partial resolution:
   - Contact the store manager to determine if non-essential data or transaction logs can be archived.
   - **Do not delete any data yourself;** consult L2 on safe archival.

2. **Immediate workaround (v4.2.3 only):**
   - If updating to v4.2.3 instead of v5.1.x, the storage requirement is only 500 MB.
   - Provide this option to the store manager and escalate to L2 to switch update target.

3. **Long-term fix requires L2** to manage storage; escalate now.

---

## When to Escalate to L2

**Escalate immediately if any of the following conditions are met:**

- Update has been stuck (progress bar frozen) for >15 minutes with stable network connectivity
- Terminal displays any error code (0xXX format) other than those resolved in L1 Resolution paths
- Terminal is unresponsive to all button presses and menu navigation
- Update appears to complete, but terminal will not boot into normal POS mode after 10 minutes
- Checksum error (0x6A) persists after attempting **Retry Update**
- Insufficient Storage error (0x4F) on v5.1.x with no option to free space
- Any update occurred on v5.0.x or earlier (not listed in "Affected Systems"; requires different procedure)

---

### Information to Collect Before Escalating

Provide L2 with the following details to expedite resolution:

1. **Terminal Details:**
   - Serial number (on device back/bottom)
   - Model number (e.g., FoodTech PT-7500, PT-3200, etc.)
   - Current installed version (if accessible via Service Menu)

2. **Error Information:**
   - Exact error message and error code (0xXX or numeric)
   - Screenshot or photo of the terminal screen
   - Percentage where update is stuck (if applicable)

3. **Update Details:**
   - Target version (v4.2.3 or v5.1.x)
   - Date/time update began
   - Duration stuck (minutes)

4. **Network Status:**
   - Connection type (WiFi or Ethernet)
   - Signal strength or connection status (if available)
   - Whether other terminals on the network are functioning normally

5. **Update Log:**
   - If accessible via Service Menu → View Update Log, provide the last 15 lines of text.
   - Otherwise, note "Update log not accessible."

6. **Store Contact Information:**
   - Store location and manager name
   - Whether the terminal is critical to active service (POS/payment processing in use)

---

## Related Runbooks

- `FoodTech_POS_Software_Version_Compatibility.md` – Supported upgrade paths and compatibility matrix
- `Network_Troubleshooting_POS_Terminals.md` – Diagnostics for WiFi and Ethernet connectivity issues
- `FoodTech_POS_Rollback_Procedure.md` – L2 rollback steps (linked for reference only; L1 should not attempt)
- `FoodTech_Service_Menu_Access.md` – Detailed PIN entry and system menu navigation
- `POS_Terminal_Hardware_Replacement.md` – Steps if hardware is confirmed faulty

---

## Revision History

| Version | Date       | Notes                                                                                          |
| ------- | ---------- | ---------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for v4.2.3 and v5.1.x; added network troubleshooting; clarified L2 escalation criteria |
| 1.1     | 2025-03-10 | Added Immediate Steps section; improved error code documentation                               |
| 1.0     | 2024-06-01 | Initial version; covered v4.2.0–v4.2.2                                                         |

---

**Document Owner:** ServeWell Hospitality IT Help Desk  
**Last Reviewed:** 2025-09-15  
**Next Review Date:** 2026-03-15
