# POS Terminal Startup Failure

## Overview

POS terminals fail to boot or become unresponsive during the startup sequence, presenting symptoms ranging from black/white screens to infinite startup loops. This runbook addresses FoodTech POS v4.2.x and v5.1.x, as well as OrbitPOS v2.x systems used across ServeWell Hospitality locations.

## Affected Systems

- **FoodTech POS v4.2.x** (legacy systems, end-of-support: 2026-03-31)
- **FoodTech POS v5.1.x** (current stable release)
- **OrbitPOS v2.x** (alternate deployment, limited locations)
- Hardware: All approved terminal models (Verifone, Ingenico, PAX series)

## Symptoms

- Black or white screen with no boot animation
- Startup animation loops continuously (>3 minutes without progressing to login screen)
- Terminal freezes at "Loading FoodTech Services" or equivalent message
- White/blue screen of death (BSOD) with error code visible
- Terminal powers on but immediately powers off (repeated cycle)
- Audio beeps on startup but no video output
- Login screen appears but terminal is unresponsive to touch/input

## Immediate Steps (First 2 Minutes)

1. **Check Physical Connections**
   - Verify power cable is firmly connected to terminal and power outlet
   - Confirm Ethernet or WiFi connectivity indicator is lit (green or blue LED)
   - Check that monitor/display is powered on (if external display is used)

2. **Perform Safe Power Cycle**
   - Press and hold the physical **Power Button** for 10 seconds until the terminal completely shuts down
   - Wait **30 seconds** with the terminal powered off
   - Press Power Button once to restart; allow **2 full minutes** for startup (do not interrupt)

3. **Document Observation**
   - Note the exact time startup attempt began
   - Take a photo of the screen if an error code is visible
   - Record any audio cues (beeps, alarm sounds)

## L1 Diagnosis Steps

### Step 1: Confirm Terminal Status

1. Observe the terminal for **120 seconds** after power-on without interruption
2. Check for LED indicators on the terminal:
   - **Green/blue LED** = power and network connectivity active (normal)
   - **Red/amber LED** = network or hardware fault
   - **No LED** = power supply issue
3. If terminal reaches login screen and is responsive, **issue is resolved**—proceed to note in ticket system

### Step 2: Identify Startup Failure Type

1. If screen is **completely black/no output**:
   - Check Display Data Channel (DDC) cable connection (if external monitor)
   - Try disconnecting and reconnecting display cable
   - Attempt startup again for 120 seconds
   - If still black, proceed to **Step 3a**

2. If screen shows **white or solid color**:
   - This typically indicates a video driver or BIOS issue
   - Proceed to **Step 3b**

3. If screen shows **startup animation looping**:
   - The OS is loading but services are not completing initialization
   - Proceed to **Step 3c**

4. If screen shows **error code or text message**:
   - Document the exact error message verbatim
   - Note the version number displayed (if visible)
   - Proceed to **Step 3d**

### Step 3a: No Video Output Diagnosis

1. Power off the terminal completely (hold power button 10 seconds)
2. Check the **video output port**:
   - Look for bent pins (HDMI, VGA, or DisplayPort)
   - Reseat the display cable firmly with a quarter-turn twist (if applicable)
3. Power on and wait 120 seconds
4. If display remains black, attempt **Safe Mode boot** (if available):
   - During startup, press **F2** or **Del** key repeatedly (within first 5 seconds)
   - If you reach BIOS/Setup menu, this indicates video output is working
   - Press **Escape** to exit and allow normal boot
   - Proceed to **Step 4: Log File Analysis**

### Step 3b: White/Solid Color Screen Diagnosis

1. Perform a **forced restart** (hold power button 10 seconds)
2. On restart, press **F8** during boot (within first 5 seconds) to access boot options menu
3. If F8 menu appears:
   - Select **"Safe Mode"** or **"Last Known Good Configuration"**
   - Allow boot to complete (may take 3+ minutes)
4. If Safe Mode boots successfully, the issue is likely a corrupted service or driver—escalate to L2
5. If Safe Mode also shows white screen, proceed to **Step 4: Log File Analysis**

### Step 3c: Startup Loop Diagnosis

1. Allow the terminal to loop for **2 full cycles** (approximately 6 minutes)
2. Observe if the loop occurs at the **same point** each time (note exact message)
3. Perform forced power cycle (hold power button 10 seconds)
4. On restart, press **Escape** key if a startup splash screen appears
5. Allow 120 seconds for boot to complete
6. If loop continues identically, proceed to **Step 4: Log File Analysis**

### Step 3d: Error Code/Message Diagnosis

1. Record the **exact error message and error code** (take a photo if possible)
2. Power off and wait 30 seconds
3. Power on and note if **same error appears** (system is consistently failing at same point)
4. Search the ServeWell Knowledge Base for the error code
5. If no match found, proceed to **Step 4: Log File Analysis**

### Step 4: Log File Analysis

1. Attempt to access the terminal via **Secure Shell (SSH)** connection from support workstation:

   ```
   ssh support@[terminal-ip-address]
   Password: (use IT support credentials)
   ```
   - **Note**: Terminal must have network connectivity for this to work
   - If SSH connection fails, terminal is likely not reaching OS initialization

2. Once connected, navigate to startup log:

   ```
   cd /var/log/foodtech/
   ls -lah startup.log
   ```

3. Review the most recent startup log:

   ```
   tail -n 100 startup.log
   cat startup.log | grep -i "error\|fail\|critical"
   ```

4. Document the last 5-10 lines showing errors or service failures
5. Check **FoodTech version** in log:
   - Look for line containing `FoodTech version: 4.2.x` or `5.1.x`
   - This determines applicable resolution steps

6. If SSH connection succeeds but log shows normal startup sequence, the issue may be **hardware**—escalate to L2 with hardware diagnostics data

## L1 Resolution

### Resolution Path A: Basic Power and Network Reset (Applies to All Versions)

**Prerequisite**: Issue occurs sporadically or after power loss event

1. **Perform extended power cycle**:
   - Power off terminal (hold power button 10 seconds)
   - Unplug power cable from wall outlet
   - Unplug Ethernet cable (if wired connection)
   - Wait **60 seconds** (full capacitor drain)

2. **Restore connections**:
   - Plug power cable back into outlet
   - Plug Ethernet cable back into terminal and network switch
   - Press power button to start terminal
   - Allow **3 minutes** for full startup

3. **Verify successful boot**:
   - Terminal reaches login screen and accepts input
   - Network LED indicators show connected status (green/blue)
   - Time and date are correct on boot screen

4. **Document resolution**: Note in ticket: "Power cycle and full connection reset performed. Terminal restored to operational state."

---

### Resolution Path B: FoodTech v4.2.x Service Failure

**Prerequisite**: Log file analysis (Step 4) shows service initialization failure in v4.2.x

1. **Check which service failed** in startup.log:
   - Look for entries like: `[ERROR] Service 'PaymentProcessor' failed to initialize`
   - Common failing services in v4.2.x: PaymentProcessor, InventorySync, NetworkManager

2. **Restart failed service manually** (via SSH):

   ```
   sudo systemctl restart [service-name]
   # Example: sudo systemctl restart foodtech-payment
   ```

3. **Monitor service startup**:

   ```
   sudo systemctl status foodtech-payment
   ```
   - Status should show **active (running)**
   - If status shows **inactive (dead)**, note the error message

4. **Force terminal reboot** if service restart fails:

   ```
   sudo reboot
   ```
   - Allow 3 minutes for full restart
   - Check if terminal reaches login screen

5. **If service still fails after manual restart**:
   - Attempt **service rollback** to known-good version (if available):
   ```
   sudo apt list --installed | grep foodtech
   sudo apt install foodtech-payment=4.2.15-stable
   ```
   - Reboot terminal
   - If rollback unavailable, escalate to L2 with service name and error message

---

### Resolution Path C: FoodTech v5.1.x Service Failure

**Prerequisite**: Log file analysis (Step 4) shows service initialization failure in v5.1.x

1. **Check systemd journal** for detailed error information:

   ```
   sudo journalctl -u foodtech-core -n 50 --no-pager
   ```

2. **Identify specific service failure**:
   - Look for **[CRITICAL]** or **[ERROR]** entries
   - v5.1.x commonly reports: `Database connection timeout`, `Configuration file not found`, `Certificate validation failed`

3. **Clear service cache** (v5.1.x improvement over v4.2.x):

   ```
   sudo systemctl stop foodtech-core
   sudo rm -rf /var/cache/foodtech/*
   sudo systemctl start foodtech-core
   ```

4. **Wait 90 seconds** for full initialization and check status:

   ```
   sudo systemctl status foodtech-core
   ```
   - Should show **active (running)** with green indicator

5. **If Database connection timeout error appears**:
   - Verify network connectivity to POS backend server:

   ```
   ping [backend-server-ip]
   nc -zv [backend-server-ip] 5432
   ```
   - If unreachable, escalate to L2 (network/backend issue)

6. **If Certificate validation failed**:
   - Update system certificates:

   ```
   sudo update-ca-certificates
   sudo systemctl restart foodtech-core
   ```

7. **If issue persists after cache clear**, proceed to escalation

---

### Resolution Path D: Firmware/BIOS Issue (All Versions)

**Prerequisite**: Diagnosis shows issue at BIOS/bootloader level (e.g., white screen at POST, F2/Del key reaches BIOS menu)

1. **Enter BIOS setup** (during boot, press **Del**, **F2**, or **F12** depending on terminal model):
   - Verifone: Press **F2**
   - Ingenico: Press **Del**
   - PAX: Press **F12**

2. **Check BIOS date and time**:
   - Navigate to **System Settings** > **Date/Time**
   - If date is incorrect (more than 30 days off), update it to current date/time
   - Some versions require exiting BIOS for changes to take effect

3. **Load BIOS defaults** (if settings appear corrupted):
   - Navigate to **Exit** or **Advanced** menu
   - Select **Load Optimized Defaults** or **Restore Factory Settings**
   - Confirm with **Yes**

4. **Exit BIOS and boot normally**:
   - Press **F10** to save and exit
   - Terminal will restart and should boot normally
   - Allow 2 minutes for full startup

5. **If BIOS resets do not resolve issue**, escalate to L2 with BIOS version information (visible in BIOS main menu)

---

### Resolution Path E: OrbitPOS v2.x Startup Issues

**Prerequisite**: Terminal is running OrbitPOS v2.x (confirm in startup log or welcome screen)

1. **Check OrbitPOS service status**:

   ```
   sudo systemctl status orbit-pos
   ```

2. **If service is inactive**, manually restart:

   ```
   sudo systemctl start orbit-pos
   sudo systemctl enable orbit-pos
   ```

3. **Check OrbitPOS log file**:

   ```
   tail -n 50 /var/log/orbitpos/service.log
   ```

4. **Common v2.x issues**:
   - **License expiration**: Check log for `License invalid or expired`
     - Escalate to L2 immediately (license must be renewed by admin)
   - **Database lock**: Check log for `Database locked by another process`
     - Restart terminal (full power cycle)
   - **Missing configuration**: Check log for `orbitpos.conf not found`
     - Contact L2 for configuration file restore

5. **If v2.x service starts successfully** after restart, ticket is resolved
6. **If service fails to start**, escalate to L2 with complete service.log output

---

## When to Escalate to L2

### Escalate immediately if any of the following criteria are met:

1. **SSH connection successful but terminal does not boot** after Steps 1-4
   - Indicates OS corruption or hardware failure
   - Collect: Terminal IP, hostname, last 50 lines of `/var/log/foodtech/startup.log`

2. **Error code related to licensing, certificates, or encryption**
   - Examples: `SSL_ERROR_RX_RECORD_TOO_LONG`, `License validation failed`, `Encryption key corrupted`
   - Collect: Exact error message, FoodTech version, timestamp from log

3. **Startup loop persists after 2+ full power cycles**
   - Indicates potential filesystem corruption or boot sector damage
   - Collect: Photos of repeating message, terminal serial number, last 100 lines of startup.log

4. **Black screen and BIOS/F2 key access is not available**
   - Indicates possible display hardware failure or video ROM corruption
   - Collect: Terminal model, serial number, LED indicator colors observed, photos

5. **Service restart commands fail with "permission denied"**
   - Indicates SSH credentials issue or user privilege escalation problem
   - Collect: SSH error message, terminal IP, username attempted

6. **Multiple terminals failing startup simultaneously at same location**
   - Indicates potential network, backend server, or facility-wide issue
   - Collect: List of affected terminal IPs/hostnames, timestamp when issue began, network status

7. **FoodTech v4.2.x service rollback command fails**
   - Indicates repository or package manager corruption
   - Collect: Exact apt error message, FoodTech version, terminal IP

8. **Issue occurs after known system update or patch deployment**
   - Indicates possible update-related regression
   - Collect: Update version number, date deployed, number of terminals affected

### Information to Collect Before Escalating

- **Terminal identification**: Serial number, IP address, hostname, location/store name
- **System version**: FoodTech version (4.2.x or 5.1.x) or OrbitPOS version
- **Startup log**: Full content of `/var/log/foodtech/startup.log` or relevant system log
- **Timestamps**: Exact time issue first occurred, duration of issue
- **Diagnostic data**: Any error codes, messages, BIOS version (if accessible)
- **Actions performed**: Detailed list of troubleshooting steps already attempted
- **Impact**: Number of affected terminals, impact to store operations (e.g., POS down 30 minutes)

### L2 Escalation Ticket Format

Include the following in ticket when escalating:

```
ESCALATION: POS Terminal Startup Failure

Terminal: [IP/Hostname/Serial#]
Location: [Store Name/Address]
System: FoodTech v[X.X.X] OR OrbitPOS v[X.X]

Symptoms: [Describe symptom: black screen, loop, freeze, etc.]

Steps Performed:
- [Step 1]
- [Step 2]
- [Step 3]

Last Log Entry:
[Paste last 10 lines of relevant log file]

Error Code/Message:
[Exact error if visible]

Network Status: [Reachable via SSH: Yes/No]

Affected Terminals: [1 or multiple]

Store Operations Impact: [Operational/Non-critical/Critical - POS down X hours]
```

---

## Related Runbooks

- `POS_Network_Connectivity_Troubleshooting.md`
-
