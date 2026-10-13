# POS Terminal Slow Performance

## Overview

POS terminals experiencing degraded performance—including lag on key presses, delayed transaction processing (>10 seconds), and unresponsive menus—typically stem from cache buildup, insufficient disk space, or resource-intensive background processes. FoodTech POS v4.2.x systems are particularly susceptible after 12–18 months of continuous operation without restart.

## Affected Systems

- **FoodTech POS v4.2.x** (most common; performance degradation after ~12–18 months uptime)
- **FoodTech POS v5.1.x** (rare; typically indicates different root cause)
- All terminal hardware models running affected versions
- Standalone and networked terminal configurations

## Symptoms

- Noticeable lag (>2 seconds) when entering menu items or customer data
- Transaction processing time exceeds 10 seconds
- Unresponsive touchscreen or keyboard input
- Menu navigation delays or freezing
- Frequent "Please Wait" screens lasting >5 seconds
- Terminal becomes responsive again after manual restart
- Issue worsens progressively over weeks or months

## Immediate Steps (First 2 Minutes)

Store staff should attempt these quick checks **before** contacting IT:

1. **Perform a soft restart**: Power cycle the terminal (press power button, wait 30 seconds, power on). Do not force shutdown; allow graceful shutdown.
2. **Check for visible error messages**: Note any on-screen error codes or messages and take a photo if available.
3. **Verify network connectivity**: Confirm the terminal is connected (check for network icon in top-right corner of FoodTech interface).

---

## L1 Diagnosis Steps

### Step 1: Verify Current System Version

1. On the terminal, open **Settings** (gear icon, typically top-right of main POS screen)
2. Navigate to **About** → **System Information**
3. Locate **FoodTech Version** and record it (e.g., 4.2.18 or 5.1.3)
4. Document the **System Uptime** (displayed in hours or days)
   - Note: Uptime >12 months (~10,000+ hours) on v4.2.x is a significant indicator

### Step 2: Check Available Disk Space

1. In **Settings**, go to **System Health** or **Diagnostics**
2. Select **Storage** or **Disk Usage**
3. Record the following:
   - **Total Disk Space**
   - **Used Space**
   - **Available Free Space** (target: >20% free)
4. If available space is <10%, this is a primary cause

### Step 3: Review Active Background Processes

1. In **Settings**, navigate to **Performance** → **Running Processes**
2. Document any processes consuming >15% CPU:
   - Look for duplicate or unexpected processes
   - Note any process with status "Not Responding"
3. Take a screenshot for L2 escalation if needed

### Step 4: Check Cache and Temporary Files

1. Go to **Settings** → **Maintenance** → **Cache Management**
2. View **Cache Size** (if displayed)
3. Note the date of last automatic cache clear (if available)

### Step 5: Test Transaction Performance

1. Process a **test transaction** (void immediately after):
   - Add a single item
   - Proceed to payment
   - Record the time from item selection to payment screen
2. If transaction time exceeds 10 seconds, note this specifically

---

## L1 Resolution

### Resolution 1: Clear Application Cache (Most Common Fix)

1. In **Settings**, go to **Maintenance** → **Cache Management**
2. Select **Clear Cache** (or **Clear All Caches**)
   - You may see options: "Transaction Cache," "Menu Cache," "Customer Data Cache" — select all
3. A confirmation dialog will appear: "This will clear cached data and may temporarily affect performance. Continue?"
4. Select **Yes** and wait for completion (typically 30–90 seconds)
5. When complete, you should see "Cache cleared successfully" message
6. **Restart the terminal** to apply changes:
   - **Settings** → **System** → **Restart Terminal** (or power cycle)
7. Once rebooted, retest with a sample transaction

### Resolution 2: Free Up Disk Space

**If available disk space <15%:**

1. In **Settings** → **System Health** → **Storage**, identify large files or folders
2. Navigate to **Settings** → **Maintenance** → **Cleanup**
3. Select **Remove Old Transactions** (transactions older than 90 days)
   - Confirm you have recent backups before proceeding
4. Select **Remove Temporary Files**
5. Select **Clear Logs** (keep most recent 2 weeks)
6. Reboot and retest

### Resolution 3: Restart Resource-Intensive Background Processes

**If processes are consuming >20% CPU:**

1. In **Settings** → **Performance** → **Running Processes**, identify the offending process
2. Select the process and choose **Restart Process** (not "Force Quit")
3. Wait 30 seconds for the process to restart
4. Retest transaction performance
5. **Note**: If the same process continually spikes CPU, escalate to L2 immediately

### Resolution 4: Force Terminal Restart (v4.2.x Long Uptime)

**If uptime is >12 months on v4.2.x:**

1. Inform the store manager that a full restart is required (5–10 minute downtime)
2. Process any pending transactions
3. **Settings** → **System** → **Shutdown** (graceful shutdown)
4. Wait 60 seconds, then power on
5. System will reboot and perform automatic checks (5–8 minutes)
6. Retest after full boot completion

### Resolution 5: Verify Network Connectivity (v5.1.x Priority)

**If terminal is on v5.1.x:**

1. Go to **Settings** → **Network** → **Connection Status**
2. Confirm connection type (Ethernet or Wi-Fi) and signal strength (if Wi-Fi)
3. Run **Network Diagnostics** → **Ping Test** to kitchen/back-office server
   - Expected latency: <100ms
   - If latency >500ms, notify store IT contact to check network
4. If network is unstable, escalate to L2 with network diagnostics results

---

## When to Escalate to L2

**Escalate immediately if any of the following are true:**

1. **Issue persists after completing all Resolution steps** (cache clear + restart)
2. **Disk space remains <10% after cleanup attempts** (potential hardware failure or database corruption)
3. **A process shows "Not Responding"** and cannot be restarted
4. **Terminal uptime cannot be determined** or system information is inaccessible
5. **Network latency is >500ms** or connection is unstable/dropping
6. **FoodTech version is v5.1.x** and issue remains after network verification (indicates potential database indexing or server-side issue)
7. **Performance issue is system-wide** (affects all terminals in the location, not just one)
8. **Error codes appear during diagnostics**, including:
   - Error 0x402 (disk I/O error)
   - Error 0x501 (database corruption)
   - Error 0x204 (memory allocation failure)

### Information to Collect Before Escalating

- **Terminal ID/Name**: (e.g., "Register 3" or "Kitchen Display 1")
- **System version and uptime**: (from Step 1 of diagnosis)
- **Available disk space percentage**: (from Step 2)
- **Any error codes or messages** (screenshots preferred)
- **Steps already attempted**: (which resolutions were tried and results)
- **Transaction test time**: (actual time recorded in Step 5)
- **Network diagnostics results**: (latency, packet loss, if tested)
- **Store location and contact**: (manager name and phone)

---

## Related Runbooks

- `POS_Terminal_Network_Connectivity.md`
- `FoodTech_Version_Upgrade_Procedures.md`
- `POS_Database_Maintenance_and_Optimization.md`
- `Terminal_Hardware_Replacement.md`
- `POS_Backup_and_Recovery.md`

---

## Revision History

| Version | Date       | Notes                                                                                            |
| ------- | ---------- | ------------------------------------------------------------------------------------------------ |
| 1.2     | 2025-09-15 | Updated for v5.1.x; added network diagnostics for v5.1.x; clarified uptime thresholds for v4.2.x |
| 1.1     | 2024-12-10 | Added disk space cleanup procedures; expanded escalation criteria                                |
| 1.0     | 2024-06-01 | Initial version                                                                                  |
