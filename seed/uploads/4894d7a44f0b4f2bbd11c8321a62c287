# POS End-of-Day Settlement Failure

## Overview

End-of-Day (EOD) settlement is the critical process that closes the daily transaction batch, reconciles cash/card totals, and prepares financial data for accounting. When settlement fails, hangs, or completes partially, daily sales cannot be finalized and financial reporting is blocked. This runbook provides L1 diagnostic and resolution procedures for FoodTech POS v4.2.x and v5.1.x settlement failures.

## Affected Systems

- **FoodTech POS v4.2.0 through v4.2.8**
- **FoodTech POS v5.1.0 through v5.1.5**
- POS terminals (all hardware models running above versions)
- Back-office Manager Workstation
- ServeWell Cloud Sync (when enabled)

---

## Symptoms

- Settlement process initiates but does not complete
- "Batch Close Timeout" error message displayed
- Settlement hangs at 50%, 75%, or 90% completion
- Partial settlement message appears; some payment types show $0 totals
- "Cannot Connect to Settlement Server" error
- EOD report shows missing or incomplete transaction records
- Settlement button remains greyed out after multiple attempts
- System clock displays incorrect date/time during settlement

---

## Immediate Steps (First 2 Minutes)

These steps can be performed by store staff **before** contacting IT:

1. **Check POS System Status Light**
   - Confirm the terminal displays a steady green light (not red or blinking orange)
   - If red or blinking orange, power-cycle the terminal: hold power button 5 seconds, wait 30 seconds, power on

2. **Verify Network Connectivity**
   - Check that the Ethernet cable is firmly connected to the POS terminal
   - If Wi-Fi enabled, confirm the terminal shows "Connected" in the network indicator (top-right corner)
   - Ask: Is the internet/network working on other devices in the location?

3. **Check System Clock**
   - Look at the time displayed in the top-right corner of the POS screen
   - If time is incorrect by more than 5 minutes, **do not proceed with settlement**—note the incorrect time and inform IT immediately

4. **Wait and Retry (Only Once)**
   - If no error messages are displayed and settlement appears to be running, wait exactly **5 minutes**
   - Do not interrupt or force-close the application
   - After 5 minutes, if settlement is still processing, proceed to L1 Diagnosis

---

## L1 Diagnosis Steps

Perform these steps **in order**. Do not skip steps.

### Step 1: Verify POS Version

1. On the affected POS terminal, navigate to **Settings** (gear icon, bottom-left)
2. Select **System Information**
3. Record the **Version Number** displayed (should be 4.2.x or 5.1.x)
4. If version is 4.1.x or earlier, or 5.2.x or later, note this—version mismatch may require escalation
5. Confirm the version matches your location's deployed version (check against your service ticket or asset management system)

### Step 2: Attempt Settlement with Diagnostic Mode

1. From the main POS screen, tap **Manager Login** (bottom-right)
2. Enter Manager PIN (default: 1234, or your location's configured PIN)
3. Navigate to **Reports** → **Daily Settlement**
4. Tap **Begin EOD Settlement**
5. At the settlement confirmation dialog, look for a **"Verbose Log"** checkbox (FoodTech v5.1.x only)
   - If visible, **enable this checkbox**
6. Tap **Confirm** to start settlement
7. **Do not interrupt.** Observe the settlement process for exactly **30 minutes** (the system timeout threshold)
   - Note any error messages that appear
   - Record the percentage shown when the process stops or hangs

### Step 3: Locate and Review Settlement Log Files

1. Once settlement halts or completes, access the **Back-Office Manager Workstation** (not the POS terminal)
2. Open **File Explorer**
3. Navigate to: `C:\ProgramData\FoodTech\Logs\` (Windows) or `/Library/Application Support/FoodTech/Logs/` (Mac)
4. Look for files named:
   - `settlement_YYYY-MM-DD.log` (most recent date)
   - `eod_batch_YYYY-MM-DD.log`
5. Open the most recent settlement log file with **Notepad** or **TextEdit**
6. Search (Ctrl+F or Cmd+F) for the following error indicators:
   - `ERROR`
   - `TIMEOUT`
   - `CONNECTION_FAILED`
   - `DATABASE_LOCK`
   - `PAYMENT_PROCESSOR_ERROR`
7. **Record the exact error message and the timestamp** where the process stopped

### Step 4: Check Network and Database Connectivity

1. On the Back-Office workstation, open **Command Prompt** (Windows) or **Terminal** (Mac)
2. Run the following command to test connectivity to the settlement server:
   ```
   ping settlement-api.servewell.local
   ```
   - If response shows `Reply from [IP]` with time <50ms, connectivity is **OK**
   - If response shows `Destination host unreachable` or times out, **note this as a network issue**
3. Check database connectivity (FoodTech v5.1.x):
   - Navigate to **Settings** → **Advanced** → **Database Status**
   - Confirm status shows: "Connected - Ready" (green indicator)
   - If status shows "Offline" or "Locked," note this immediately

### Step 5: Verify Batch Transaction Count

1. From the POS terminal's Manager screen, go to **Reports** → **Transaction Summary**
2. Record the **Total Transactions** and **Total Sales Amount** shown for today
3. Go to **Settings** → **Batch Information**
4. Record the **Current Batch Number** and **Transactions in Batch**
5. Compare these figures to your point-of-sale journal or previous shift's records
   - If current batch shows 0 transactions but staff processed sales, note this discrepancy

---

## L1 Resolution

Perform these steps in order. **Stop if the issue is resolved at any step.**

### Resolution Step 1: Clear Stuck Settlement Processes

1. On the Back-Office workstation, open **Task Manager** (Ctrl+Shift+Esc on Windows) or **Activity Monitor** (Mac)
2. Look for processes named:
   - `FoodTechPOS.exe` (Windows)
   - `FoodTech` (Mac)
   - `SettlementService.exe`
3. **Do not force-close these processes yet.** Proceed to Step 2 first.

### Resolution Step 2: Restart Settlement Service (Graceful)

1. On the Back-Office workstation, navigate to **Settings** → **Services**
2. Locate **Settlement Service** in the services list
3. Click **Restart Service**
4. Wait 30 seconds for the service to fully restart (status will show "Running")
5. Return to the POS terminal
6. Tap **Manager Login** and navigate to **Reports** → **Daily Settlement** → **Begin EOD Settlement**
7. Attempt settlement again; observe for 5 minutes
8. **If settlement completes successfully, you are done.** Document the resolution as "Service restart."

### Resolution Step 3: Clear Temporary Settlement Files

1. **Only perform this step if Step 2 failed.**
2. On the Back-Office workstation, navigate to: `C:\ProgramData\FoodTech\Temp\` (Windows) or `/Library/Application Support/FoodTech/Temp/` (Mac)
3. Delete files matching the pattern:
   - `settlement_*.tmp`
   - `batch_lock.*`
4. Do **not** delete any `.log` files
5. Restart the Settlement Service again (repeat Step 2)
6. Attempt settlement on the POS terminal
7. **If settlement completes, document as "Temporary files cleared."**

### Resolution Step 4: Synchronize System Clock

1. **Only if Step 3 failed AND you identified an incorrect system clock in the Immediate Steps.**
2. On the Back-Office workstation:
   - **Windows:** Right-click the system clock (bottom-right) → **Adjust date/time** → **Sync now**
   - **Mac:** **System Preferences** → **Date & Time** → Enable **Set date and time automatically**
3. Wait 2 minutes for the clock to synchronize across all POS terminals
4. Attempt settlement again
5. **If settlement completes, document as "System clock synchronized."**

### Resolution Step 5: Perform Partial Settlement Recovery (FoodTech v5.1.x Only)

1. **Only if Steps 1–4 have failed.**
2. On the POS terminal, from **Manager Login**, go to **Settings** → **Advanced** → **Settlement Recovery**
3. Tap **View Incomplete Batches**
4. If a partial settlement is shown with a date from today, tap **Retry Settlement** next to it
5. The system will attempt to complete only the remaining transactions
6. Observe for 10 minutes
7. **If successful, the incomplete batch will be marked "Complete."** Document as "Partial settlement recovery succeeded."

---

## When to Escalate to L2

**Escalate to L2 immediately if any of the following conditions are met:**

### Mandatory Escalation Criteria

1. **Financial Discrepancy Detected**
   - Total Sales Amount in Batch Information does not match POS Journal or previous reports
   - Any payment type (Cash, Credit, Debit) shows $0 total when transactions were processed
   - Missing transactions between last successful EOD and current attempt
   - **→ Escalate with: Full transaction journal screenshot, batch totals, settlement log**

2. **Settlement Timeout After 30 Minutes**
   - Settlement process has been running for 30 minutes without completion or error message
   - **→ Escalate with: Settlement log file, percentage at which it hung, system timestamps**

3. **Network Connectivity Failure**
   - `ping settlement-api.servewell.local` returns "Destination host unreachable"
   - "Cannot Connect to Settlement Server" error persists after Service Restart
   - **→ Escalate with: Ping test results, network error log, Back-Office connectivity test results**

4. **Database Lock or Corruption**
   - Settlement log contains: `DATABASE_LOCK`, `CORRUPTION_DETECTED`, or `TRANSACTION_WRITE_ERROR`
   - Database Status shows "Locked" or "Offline"
   - **→ Escalate with: Settlement log excerpt, database status screenshot, affected batch number**

5. **Multiple Settlement Failures (3+ Consecutive Days)**
   - Successful resolution has not been achieved after completing all L1 Resolution steps
   - Same error repeats on subsequent days
   - **→ Escalate with: Settlement logs from all 3 days, L1 troubleshooting steps completed, summary of all attempted resolutions**

6. **Version Mismatch or Unsupported Configuration**
   - POS terminal running version outside 4.2.x or 5.1.x range
   - Back-Office and POS terminals running different major versions (e.g., one is v4.2.x, another is v5.1.x)
   - **→ Escalate with: Version numbers from all affected systems**

### Information to Collect Before Escalating

Gather the following information to include in your escalation ticket:

- **Settlement log file** (entire file: `C:\ProgramData\FoodTech\Logs\settlement_YYYY-MM-DD.log`)
- **Error messages** (exact text, with timestamps)
- **POS version** (from Settings → System Information)
- **Back-Office version** (if different from POS)
- **Date and time of failure** (use POS system clock)
- **Percentage at which settlement halted** (if applicable)
- **Transaction count and total sales amount** from Batch Information
- **Screenshot of settlement error screen** (if error message is displayed)
- **Results of ping test** to settlement server
- **Current system clock time** vs. correct time (if discrepancy exists)
- **Summary of L1 steps attempted** and results
- **Any relevant network or infrastructure changes** made in the past 24 hours

### Escalation Ticket Template

When creating an L2 escalation ticket, use this format:

```
Title: EOD Settlement Failure – [Location Name] – [Date]

Description:
- Affected Terminal(s): [serial number(s)]
- POS Version: [version]
- Error Observed: [description]
- Last Successful EOD: [date]
- L1 Steps Completed: [list]
- Settlement Log Error Lines: [paste relevant errors]

Attachments:
- settlement_YYYY-MM-DD.log
- error_screenshot.png
- transaction_journal.png
```

---

## Related Runbooks

- `POS-System-Startup-Troubleshooting.md`
- `Network-Connectivity-Diagnostics.md`
- `FoodTech-Payment-Processor-Integration.md`
- `Database-Synchronization-Issues.md`
- `Back-Office-Manager-Workstation-Setup.md`
- `POS-System-Clock-Synchronization.md`

---

## Revision History

| Version | Date       | Notes                                                                                                                                                                               |
| ------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated for current system versions (v4.2.x and v5.1.x); added Partial Settlement Recovery step for v5.1.x; clarified 30-minute timeout threshold and financial escalation criteria |
| 1.1     | 2024-12-10 | Added network connectivity verification in Immediate Steps; included settlement log file paths for Windows and Mac                                                                  |
| 1.0     | 2024-06-01 | Initial version; covered FoodTech POS v4.2.x                                                                                                                                        |

---

**Last Updated:** September 15, 2025  
**Knowledge Base Owner:** ServeWell Hospitality IT Help Desk  
**Support Contact:** helpdesk@servewell.local | Ext. 5000
