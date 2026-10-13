# Self-Order Kiosk Frozen Screen

## Overview

The kiosk touchscreen is unresponsive to customer input and/or displays outdated menu content. This runbook covers diagnosis and resolution for ServeWell Kiosk v2.0/v2.1 and TouchPoint K1 v1.1 units experiencing frozen or stalled screens.

## Affected Systems

- **ServeWell Kiosk v2.0** (including payment reader timeout issue after >10 min sleep)
- **ServeWell Kiosk v2.1**
- **TouchPoint K1 v1.1**

## Symptoms

- Touchscreen does not respond to customer touches
- Display shows outdated menu items, pricing, or promotional content
- Kiosk appears powered on (screen lit) but unresponsive to input
- Customer timeout message does not appear after inactivity
- Navigation buttons or menu selections do not register
- White/gray blank screen with no error message visible
- Payment reader "timeout" error displays after extended idle period (ServeWell v2.0)

## Immediate Steps (First 2 Minutes)

Store staff should perform these checks before contacting IT:

1. **Check for obvious obstruction**
   - Verify the touchscreen surface is clean and free of debris, grease, or protective film
   - Wipe gently with a soft, dry cloth

2. **Attempt touch reset**
   - Ask customer to tap the screen in different locations (top, center, bottom)
   - If any response occurs, proceed to L1 Diagnosis

3. **Verify power status**
   - Confirm the kiosk power cable is firmly connected to both the unit and wall outlet
   - Check for any amber/red indicator lights on the kiosk base (power or fault status)

## L1 Diagnosis Steps

**Do not attempt hard power-off during an active transaction.** Confirm the kiosk is idle before proceeding.

1. **Confirm idle state**
   - Ask store staff: "Is a customer actively ordering or paying?"
   - If YES: wait for transaction to complete or timeout (typically 3–5 minutes)
   - If NO or UNKNOWN: wait 2 minutes before proceeding to Step 2

2. **Attempt graceful restart**
   - Locate the **physical power button** on the rear or base of the kiosk
   - Press and **hold for 3 seconds** (do not hold longer than 5 seconds)
   - Screen should dim briefly; release the button
   - Wait 30 seconds for boot sequence to begin
   - Look for **ServeWell or TouchPoint logo splash screen**
   - Document boot time (should complete within 90 seconds)

3. **Check system logs during boot**
   - Once boot completes and home screen appears, press **Admin Panel** button (usually located bottom-right, or access via menu: Settings > Admin)
   - If prompted for PIN, enter default: **7890** (notify IT if PIN has been changed at location)
   - Navigate to **Diagnostics > System Logs**
   - Review entries from the last 15 minutes
   - Look for error codes such as:
     - `ERR_TOUCH_TIMEOUT` – touchscreen driver timeout
     - `ERR_PAYMENT_TIMEOUT` – payment module unresponsive (ServeWell v2.0)
     - `ERR_MEMORY_FULL` – storage/cache issue
     - `ERR_NETWORK_LOSS` – loss of menu data connection

4. **Test touchscreen responsiveness**
   - Return to home screen (Admin Panel > Exit, or press Home button)
   - Attempt to navigate menu by tapping different buttons
   - Test in at least three locations on screen (top, center, bottom)
   - Document whether any touches register

5. **Check sleep mode settings** (ServeWell v2.0 only)
   - Admin Panel > Settings > Power Management
   - Verify **Sleep Mode** is set to **Disabled**
   - If enabled, this can trigger payment reader timeout after 10+ minutes idle
   - Disable and restart kiosk

## L1 Resolution

### Resolution Path 1: Touchscreen Driver Reset (Most Common)

1. Power off the kiosk using the physical power button (hold 3 seconds)
2. Wait **60 seconds** with power off
3. Power back on; observe boot sequence
4. Once home screen loads, attempt to tap and navigate
5. If responsive, test 5–10 menu touches to confirm stability
6. **Document as resolved**; advise location to monitor for recurrence

### Resolution Path 2: Clear Application Cache

If touchscreen remains frozen after Path 1:

1. Access Admin Panel (Settings > Admin, PIN: 7890)
2. Navigate to **Maintenance > Clear Cache**
3. Confirm the warning message
4. System will restart automatically
5. Wait for boot to complete (90–120 seconds)
6. Test touchscreen responsiveness again
7. **Document as resolved** or proceed to escalation

### Resolution Path 3: Network Menu Refresh (Stale Content Issue)

If screen shows outdated menu content but is otherwise responsive:

1. Access Admin Panel (Settings > Admin)
2. Select **Menu Management > Force Refresh**
3. Confirm location and confirm action
4. System will contact ServeWell or TouchPoint content servers
5. Menu should update within 2–3 minutes (observe network activity light)
6. Once complete, restart kiosk gracefully (Path 1, Step 1–3)
7. Verify new menu content displays
8. **Document as resolved**

### Resolution Path 4: ServeWell v2.0 Payment Reader Timeout

If error code `ERR_PAYMENT_TIMEOUT` is logged:

1. Confirm **Sleep Mode is Disabled** (see L1 Diagnosis Step 5)
2. If already disabled, power off kiosk for 60 seconds
3. Power back on and allow full boot
4. Attempt a test transaction (use test card if available, or cancel after payment screen appears)
5. If payment reader responds, issue is resolved; **document**
6. If timeout persists, escalate to L2 with logs

## When to Escalate to L2

Escalate immediately if any of the following apply:

- **Touchscreen unresponsive after two complete power cycles** (Path 1 repeated twice)
- **Error codes persist in System Logs:**
  - `ERR_TOUCH_HARDWARE`
  - `ERR_PAYMENT_READER_FAIL`
  - `ERR_MEMORY_CRITICAL`
  - Any code beginning with `CRITICAL_`
- **Unable to access Admin Panel** (PIN rejected or menu unavailable)
- **Physical damage visible** on touchscreen or kiosk housing
- **Network connectivity lost** (no connection to menu servers after 10 minutes; see `ERR_NETWORK_LOSS`)
- **Same issue recurs within 24 hours** of resolution
- **Multiple kiosks affected simultaneously** (possible location-wide network or power issue)

### Information to Collect Before Escalating

Provide L2 with:

- Kiosk **model and serial number** (printed on rear label)
- Exact **system version** (Admin Panel > About > Software Version)
- Complete **System Logs** output (Admin Panel > Diagnostics > System Logs > Export; share via ticket)
- **Time of first occurrence** and any preceding events (power loss, network outage, software update)
- **All error codes** visible on screen or in logs
- **Steps already attempted** (include exact outcomes)
- **Location name and store ID**
- **Time zone** of location

## Related Runbooks

- [Kiosk-Network-Connectivity-Issues.md](Kiosk-Network-Connectivity-Issues.md)
- [Payment-Reader-Hardware-Troubleshooting.md](Payment-Reader-Hardware-Troubleshooting.md)
- [ServeWell-Kiosk-v2.0-Sleep-Mode-Disable.md](ServeWell-Kiosk-v2.0-Sleep-Mode-Disable.md)
- [Admin-Panel-Access-and-PIN-Reset.md](Admin-Panel-Access-and-PIN-Reset.md)
- [TouchPoint-K1-Software-Update-Procedure.md](TouchPoint-K1-Software-Update-Procedure.md)
- [Kiosk-Cache-and-Storage-Management.md](Kiosk-Cache-and-Storage-Management.md)

## Revision History

| Version | Date       | Notes                                                                                                                                    |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for ServeWell v2.1 compatibility; clarified v2.0 payment reader timeout resolution; added network refresh path for stale content |
| 1.1     | 2024-11-03 | Added TouchPoint K1 v1.1 support; expanded System Logs diagnostics                                                                       |
| 1.0     | 2024-06-01 | Initial version; ServeWell v2.0 only                                                                                                     |

---

**Document Owner:** ServeWell Hospitality IT Help Desk  
**Last Reviewed:** 2025-09-15  
**Next Review:** 2025-12-15
