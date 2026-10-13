# Kiosk Payment Reader Error

## Overview

The ServeWell Kiosk payment reader (NFC/EMV module) has become unresponsive, offline, or is displaying error messages, preventing customers from completing contactless or card-based transactions. This runbook provides diagnostic and recovery steps for L1 support agents.

## Affected Systems

- **ServeWell Kiosk v2.0** with embedded NFC/EMV payment reader
- **ServeWell Kiosk v2.1** with embedded NFC/EMV payment reader
- **Payment Reader Firmware:** Independent version management (current: 3.2.1 and later)
- **POS Integration:** ServeWell Core POS v4.2+

## Symptoms

- Kiosk screen displays "Payment Reader Offline" or "Reader Not Detected" message
- NFC/contactless payments fail after customer taps card or mobile wallet
- EMV chip card insertion times out or returns error code (e.g., `ERR_EMV_TIMEOUT`, `ERR_READER_INIT_FAILED`)
- Payment reader LED indicator is dark, blinking red, or unresponsive
- Customer receives "Unable to Process Payment" on kiosk touchscreen
- Staff receives alert in ServeWell Manager: "Payment Module Disconnected"
- Kiosk software is running normally, but payment transactions cannot complete

## Immediate Steps (First 2 Minutes)

These steps should be completed by store staff or the manager on duty **before** contacting IT:

1. **Check physical connections**
   - Verify the payment reader power cable is firmly connected to the kiosk rear panel
   - Ensure the USB/serial cable (white connector, typically near the bottom rear) is seated fully into the kiosk mainboard
   - Look for any visible damage or bent pins on connectors

2. **Attempt a graceful restart**
   - Ask the customer to step away from the kiosk
   - On the kiosk home screen, press **[Menu] → [Settings] → [Restart Kiosk]**
   - Wait for the kiosk to fully boot (approximately 90 seconds)
   - Test with a card or NFC device to confirm reader responsiveness

3. **Check for error messages**
   - Take a **photo or screenshot** of any error code or message on the kiosk display
   - Note the **exact time** the error was first observed
   - Do not attempt multiple payment transactions; one test is sufficient

## L1 Diagnosis Steps

Perform these steps in order. Do not skip ahead.

### Step 1: Verify Kiosk Software Status

1. At the kiosk, navigate to **[Menu] → [Diagnostics] → [System Information]**
2. Confirm **Kiosk Software Version** displays either `2.0.x` or `2.1.x`
3. Note the **Uptime** value (recorded restart time)
4. Proceed to Step 2

### Step 2: Check Payment Reader Detection

1. In **Diagnostics**, select **[Hardware Status]**
2. Locate the **Payment Reader** entry in the hardware list
3. Confirm the status field; it should display one of the following:
   - ✓ **Online** — Reader is connected and responding
   - ✗ **Offline** — Reader is not detected by kiosk mainboard
   - ⚠ **Error** — Reader detected but in error state (note any error code)
4. **Record the exact status and any error code** (e.g., `ERR_FIRMWARE_MISMATCH`, `ERR_COMMS_FAILURE`)
5. Proceed to Step 3

### Step 3: Retrieve Payment Reader Firmware Version

1. In **Diagnostics**, select **[Device Information] → [Payment Module Details]**
2. Record the **Reader Firmware Version** (should be v3.2.1 or later)
3. Record the **Reader Model** (typically "ServeWell EMV-NFC Module Rev. 2.x")
4. Note the **Reader Serial Number** for your escalation notes
5. Proceed to Step 4

### Step 4: Check Kiosk Event Log

1. In **Diagnostics**, select **[Event Log]**
2. Filter by **[Last 2 Hours]**
3. Look for entries with **[Payment Reader]** or **[Hardware Error]** tags
4. Identify the **first occurrence** of any payment reader error
5. Record the **timestamp** and **full error message text**
6. Screenshot or photograph the log entry if available
7. Proceed to Step 5 or L1 Resolution based on findings

### Step 5: Test Reader Recovery Responsiveness

1. Return to the kiosk home screen
2. Instruct a staff member to **tap a known-good NFC card or mobile wallet** on the reader (top center of kiosk screen)
3. Observe for **5 seconds**:
   - Does the reader LED illuminate (green or blue)?
   - Does the kiosk display "Reading card..." or a similar prompt?
   - Does the transaction initiate?
4. If reader responds, proceed to L1 Resolution Step 1
5. If reader does not respond, proceed to L1 Resolution Step 2

## L1 Resolution

### **Most Common Cause: Reader Firmware Out of Sync**

This occurs after kiosk software updates or power failures. The reader firmware has drifted from the kiosk software version.

#### Resolution Steps

1. **Navigate to Reader Recovery Menu**
   - At home screen: **[Menu] → [Settings] → [Maintenance] → [Payment Module Recovery]**
   - You will see a warning: _"Reader firmware will be automatically synchronized. This process takes 2-3 minutes. Do not power off the kiosk."_

2. **Initiate Firmware Resynchronization**
   - Select **[Sync Reader Firmware]**
   - Kiosk will display: _"Synchronizing payment reader... Please wait."_
   - Progress bar will appear; allow process to complete fully (do not interrupt)
   - Expected completion time: 2–3 minutes

3. **Verify Successful Synchronization**
   - Upon completion, kiosk displays: _"Reader firmware successfully updated to v3.2.1 [or later]."_
   - Kiosk automatically returns to **Diagnostics → Hardware Status**
   - Confirm **Payment Reader** status now shows ✓ **Online**

4. **Conduct Payment Test**
   - Return to kiosk home screen
   - Request staff to tap a test card or NFC wallet on reader
   - Confirm **"Reading card..."** prompt appears and transaction processes
   - If successful, **document resolution time** and close ticket

5. **If Still Offline After Sync**
   - Proceed to "Hard Reader Reset" below

---

### **Secondary Cause: Reader Hardware Not Detected (Hard Reset Required)**

#### Hard Reader Reset Procedure

1. **Initiate Hardware Reset**
   - At home screen: **[Menu] → [Settings] → [Maintenance] → [Payment Module Recovery]**
   - Select **[Hard Reset Reader]**
   - Warning appears: _"The payment reader will be powered down and reset. This will take approximately 60 seconds."_
   - Select **[Confirm]** to proceed

2. **Monitor Reset Process**
   - Kiosk screen will go blank or display _"Resetting payment reader..."_
   - Reader LED will turn off completely (expected behavior)
   - **Do not power off the kiosk; the reset is in progress**
   - Wait for **full 60 seconds**

3. **Verify Reset Completion**
   - Kiosk will automatically restart the payment reader module
   - Reader LED will illuminate (green or blue)
   - Kiosk displays: _"Payment reader reset completed. Firmware: v3.2.1 [or later]."_
   - Kiosk returns to home screen

4. **Conduct Payment Test**
   - Request staff to tap a test card on reader
   - Confirm card reading and transaction processing
   - If successful, **document recovery steps and close ticket**

5. **If Reader Still Not Detected**
   - Proceed to "Fallback to POS Terminal" below and escalate to L2

---

### **Tertiary Resolution: Fallback to POS Terminal**

If the payment reader cannot be recovered within **10 minutes**, direct transactions to the main POS terminal while escalation occurs.

#### Steps

1. **Disable Reader on Kiosk**
   - At home screen: **[Menu] → [Settings] → [Payment Options]**
   - Toggle **[Accept Kiosk Payments]** to **OFF**
   - You will see: _"Kiosk payment processing disabled. Customers will be directed to POS terminal."_

2. **Notify Customers**
   - Kiosk now displays: _"Thank you for your order. Please proceed to the counter to complete payment."_
   - Staff should direct customers to the main POS terminal

3. **Document Fallback**
   - Create ticket note: "Reader unrecoverable; kiosk fallback to POS enabled at [TIME]"
   - Note: This is a **temporary workaround only**; escalate immediately to L2

## When to Escalate to L2

Escalate immediately to Level 2 Support (Hardware Engineering) if **any** of the following apply:

### Escalation Criteria

- Payment reader shows ✗ **Offline** status after completing both firmware sync and hard reset procedures
- Reader LED remains **dark** or **unresponsive** after hard reset (no power indication)
- Event log displays error code **`ERR_HARDWARE_FAULT`**, **`ERR_READER_INIT_FAILED`**, or **`ERR_COMMS_FAILURE`** (repeating)
- Reader firmware version is **below v3.2.0** and cannot be updated via automatic sync
- Physical inspection reveals **visible damage** to reader connectors or cabling
- Reader worked previously, but now fails consistently after a known power outage or storm
- More than **15 minutes** have elapsed without reader recovery

### Information to Collect Before Escalating

Gather all of the following and include in your escalation ticket:

| Information                         | Details                                                      |
| ----------------------------------- | ------------------------------------------------------------ |
| **Kiosk Serial Number**             | Found in [Menu] → [System Information] → [Kiosk ID]          |
| **Kiosk Software Version**          | From Diagnostics                                             |
| **Payment Reader Firmware Version** | From [Device Information]                                    |
| **Reader Model/Serial Number**      | From [Device Information]                                    |
| **Exact Error Code(s)**             | From Hardware Status or Event Log                            |
| **Timestamp of First Error**        | From Event Log                                               |
| **Screenshot(s) or Photos**         | Of error messages, LED status, hardware connections          |
| **Steps Already Attempted**         | Sync, hard reset, restart, etc.                              |
| **Time Issue Began**                | Date and time; relation to power events, updates, or weather |
| **Last Known Working Status**       | When reader last functioned normally                         |

### L2 Contact Information

- **ServeWell Hardware Support Email:** `hardware-support@servewell.internal`
- **Escalation Ticket Category:** "Payment Reader Hardware"
- **Priority:** High (blocks customer transactions)

## Related Runbooks

- `Kiosk_Restart_Recovery.md` — Full kiosk restart and boot troubleshooting
- `Kiosk_Network_Connectivity.md` — Network and backend connectivity issues
- `Kiosk_Software_Update_Failure.md` — Update rollback and version conflicts
- `Kiosk_Touchscreen_Unresponsive.md` — Display and input issues
- `POS_Terminal_Fallback_Mode.md` — Enabling POS backup processing
- `Payment_Reader_Cable_Inspection.md` — Physical hardware verification guide

## Revision History

| Version | Date       | Notes                                                                            |
| ------- | ---------- | -------------------------------------------------------------------------------- |
| 1.2     | 2025-09-15 | Updated firmware sync procedure for v3.2.1; added hard reset escalation criteria |
| 1.1     | 2025-03-20 | Added POS fallback steps; clarified escalation timeline                          |
| 1.0     | 2024-06-01 | Initial version; covers ServeWell Kiosk v2.0 and v2.1                            |

---

**Last Updated:** September 15, 2025  
**Document Owner:** ServeWell IT Support  
**Classification:** Internal Use — L1/L2 Support Only
