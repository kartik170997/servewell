# L1-to-L2 Escalation Procedure

**Purpose:** To establish a standardized process for L1 support agents to escalate complex technical issues to L2 support while ensuring complete information transfer and appropriate prioritization.

**Scope:** This procedure applies to all L1 support agents at ServeWell Hospitality IT handling tickets for POS systems, network infrastructure, payment terminals, and related hospitality IT services.

**Last Updated:** 2025-01-10

**Effective Date:** 2025-01-15

**Next Review Date:** 2025-07-10

---

## Procedure

### Step 1: Determine Escalation Eligibility

1. Review the ticket against the **Do-Not-Escalate List** (Section 4 below)
2. If the issue matches a do-not-escalate category, resolve using knowledge base resources and close the ticket
3. If the issue does not match, proceed to Step 2

### Step 2: Attempt Basic Troubleshooting

1. Follow standard L1 troubleshooting steps relevant to the issue category:
   - Restart device/service
   - Check network connectivity
   - Verify user permissions and credentials
   - Confirm recent system changes or updates
   - Consult internal knowledge base and FAQs
2. Document all steps attempted in the ticket with timestamps and outcomes
3. If the issue is resolved, close the ticket and skip remaining steps
4. If the issue persists after 15 minutes of troubleshooting, proceed to Step 3

### Step 3: Collect Mandatory Escalation Information

1. Verify and confirm the following mandatory fields in the ticket system:
   - **Asset ID**: POS terminal ID, server ID, or network device identifier
   - **Error Code**: Exact error message or code displayed (screenshot preferred)
   - **Steps Already Tried**: Complete list with outcomes
   - **Store Impact**: Number of affected devices/users and operational impact
2. If any mandatory field is missing, contact the customer to obtain it before proceeding
3. Record the time mandatory information was completed

### Step 4: Assess Priority and Apply Override Rules

1. Determine base priority using the impact criteria:
   - **Critical (P1)**: Complete store outage, payment processing unavailable, multiple locations affected
   - **High (P2)**: Single location partial outage, 50%+ of POS terminals down, back-office unavailable
   - **Medium (P3)**: Single terminal down, non-critical function degraded, workaround available
   - **Low (P4)**: Cosmetic issues, single user impact, no workaround needed
2. Apply priority override rules (see Section 3 below)
3. Document final priority assignment and justification in the ticket

### Step 5: Prepare Escalation Documentation

1. Create a comprehensive summary in the ticket that includes:
   - Executive summary (2-3 sentences)
   - Asset ID and error codes
   - Complete troubleshooting steps and results
   - Store impact and affected users
   - Customer contact information and preferred communication method
   - Any relevant screenshots, logs, or configuration details
   - Customer's desired outcome or deadline
2. Attach or link any diagnostic files (system logs, network traces, screenshots)
3. Flag any time-sensitive requirements or pending customer deadlines

### Step 6: Route Escalation to L2

1. Change ticket status to "Escalated" in the ticketing system
2. Assign ticket to the **L2 Support Team** queue
3. Send escalation notification email to **it-l2@servewell.in** with:
   - Ticket ID and subject line
   - Priority level
   - Store location and customer name
   - One-sentence issue summary
   - Link to full ticket details
4. If the issue is **Critical (P1)**, simultaneously notify **oncall@servewell.in** with the same information
5. Set ticket expectation with customer: "Your issue has been escalated to our specialist team. You can expect an update within [SLA time—see Section 2]"
6. Do NOT close the ticket; remain as point of contact for customer updates

### Step 7: Monitor Escalation Progress

1. Check ticket for L2 response at the 50% SLA mark (e.g., 1.5 hours for 3-hour P2 SLA)
2. If no L2 response by SLA deadline:
   - Post internal comment flagging SLA breach
   - Contact L2 team lead via Slack or direct message
   - Escalate to on-call manager if no response within 15 minutes
3. Provide customer with status updates every 2 hours until resolution
4. Once L2 takes ownership, update customer and monitor for closure

---

## Priority Override Rules

Apply the following overrides to the base priority assessment:

| Condition                                                                                       | Override Action                                 |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Time-sensitive context**: Issue occurs during peak service hours (11:00–14:00 or 18:00–21:00) | Increase priority by one level (max P1)         |
| **Recurring issue**: Customer reports the same issue more than twice in 30 days                 | Increase priority by one level (max P1)         |
| **VIP customer**: Designated premium service customer or corporate chain location               | Increase priority by one level (max P1)         |
| **External dependency**: Issue blocks vendor, auditor, or regulatory compliance requirement     | Increase priority by one level (max P1)         |
| **Customer escalation**: Customer has escalated complaint to management or requested escalation | Automatically assign P1 or P2; route to manager |
| **Known issue with workaround**: Issue is documented with available temporary fix               | Decrease priority by one level (minimum P4)     |

---

## Required Information Checklist

### Mandatory Fields (Must Be Complete Before Escalation)

**Ticket & Asset Information:**

- [ ] Ticket ID created and logged in system
- [ ] Asset ID(s) identified (POS terminal, server, device, or network segment)
- [ ] Asset type specified (e.g., "NCR POS Terminal," "Cisco Switch," "Payment Gateway")
- [ ] Store location and address confirmed
- [ ] Store contact name and direct phone number obtained

**Issue Details:**

- [ ] Exact error code(s) or error message documented
- [ ] Screenshot or log excerpt attached (if applicable)
- [ ] Issue first occurrence date/time recorded
- [ ] Frequency of issue noted (one-time, intermittent, persistent)

**Troubleshooting Documentation:**

- [ ] All steps attempted listed with dates and times
- [ ] Outcome of each step clearly recorded (success/failure)
- [ ] Minimum 15 minutes of troubleshooting documented
- [ ] Knowledge base resources consulted listed

**Impact Assessment:**

- [ ] Number of affected devices/terminals specified
- [ ] Number of affected users specified
- [ ] Business impact statement provided (e.g., "Payment processing unavailable for 4 hours")
- [ ] Revenue impact estimated if applicable (critical issues only)
- [ ] Workarounds or temporary solutions identified

**Customer Information:**

- [ ] Customer name and contact details verified
- [ ] Preferred communication method noted (phone, email, Slack)
- [ ] Customer's availability for troubleshooting recorded
- [ ] Any known constraints or special requirements noted

### Recommended Attachments

- [ ] System error logs (last 100 entries minimum)
- [ ] Network connectivity test results (ping, traceroute)
- [ ] Screenshots of error messages or abnormal behavior
- [ ] Configuration details (OS version, software version, recent changes)
- [ ] Previous related tickets or known issue documentation

---

## Do-Not-Escalate List

The following issues must **NOT** be escalated to L2. Resolve using internal resources, knowledge base, or direct customer guidance:

### General Categories

1. **Basic How-To & Training Questions**
   - Password reset requests
   - How to generate daily sales reports
   - How to add a new user account or modify permissions
   - Navigation within POS menu system
   - Printing receipts or statements
   - **Resolution**: Direct customer to knowledge base article, training video, or user manual

2. **User Error or Incorrect Configuration**
   - Incorrect login credentials (customer entered wrong password)
   - User attempting to access unauthorized functions
   - Customer misconfigured settings (e.g., wrong terminal assigned to register)
   - POS offline due to customer forgetting to power on device
   - **Resolution**: Verify and correct configuration; provide guidance on proper use

3. **Billing, Account, or Licensing Issues**
   - Invoice disputes or payment questions
   - Subscription renewal or upgrade requests
   - License key activation or compliance inquiries
   - Service plan change requests
   - **Resolution**: Escalate internally to **Billing@servewell.in**, not to L2 Support

4. **Scheduled Maintenance or Known Downtime**
   - System maintenance windows (pre-announced)
   - Planned software updates affecting service
   - Temporarily unavailable services
   - **Resolution**: Reference maintenance notification; provide estimated restoration time

5. **Feature Requests or Enhancement Suggestions**
   - Customer requesting new POS functionality
   - Suggestions for improved user interface
   - Questions about product roadmap
   - **Resolution**: Log request in Product Feedback system; thank customer for suggestion

6. **Third-Party Service Coordination** (customer's responsibility)
   - Internet service provider connectivity issues
   - Credit card processor or payment gateway support
   - Hardware manufacturer defects for non-ServeWell equipment
   - External vendor integration problems
   - **Resolution**: Advise customer to contact relevant third-party provider directly; provide contact details if available

7. **General Connectivity Troubleshooting (if resolved)**
   - Internet connection restored after reboot
   - Network cable reseated successfully
   - WiFi reconnected after customer reset
   - **Resolution**: Confirm normal operation; close ticket with resolution details

---

## L2 Response Service Level Agreements (SLAs)

| Priority          | Initial Response Time | Resolution Target |
| ----------------- | --------------------- | ----------------- |
| **P1 – Critical** | 15 minutes            | 4 hours           |
| **P2 – High**     | 1 hour                | 8 hours           |
| **P3 – Medium**   | 3 hours               | 24 hours          |
| **P4 – Low**      | 8 business hours      | 5 business days   |

**SLA Calculation Notes:**

- SLA timers begin upon ticket escalation completion (Step 6)
- Business hours: Monday–Sunday, 07:00–23:00 IST
- SLA pauses during documented customer wait time (awaiting customer response, testing, etc.)
- If SLA is at risk of breach, L1 must escalate to manager via oncall@servewell.in

---

## Escalation Contacts

| Role                      | Email                   | Phone              | Availability             |
| ------------------------- | ----------------------- | ------------------ | ------------------------ |
| **L2 Support Team**       | it-l2@servewell.in      | +91-XXXX-XXXX-XXXX | 07:00–23:00 IST, 7 days  |
| **L2 Team Lead**          | l2-lead@servewell.in    | +91-XXXX-XXXX-XXXX | 09:00–18:00 IST, Mon–Fri |
| **On-Call Manager**       | oncall@servewell.in     | +91-XXXX-XXXX-XXXX | 24/7 for P1 escalations  |
| **IT Operations Manager** | it-manager@servewell.in | +91-XXXX-XXXX-XXXX | 09:00–18:00 IST, Mon–Fri |

---

## Escalation Email Template

**Subject:** `[ESCALATION] Ticket #[ID] - [Customer Store] - [Priority Level]`

```
To: it-l2@servewell.in
[CC: oncall@servewell.in if P1]

---

ESCALATION SUMMARY
Ticket ID: [XXXXX]
Priority: [P1/P2/P3/P4]
Customer: [Store Name, Location]
Asset ID: [Terminal/Server ID]

ISSUE:
[One-sentence problem statement]

ERROR CODE(S):
[Include exact error message]

STEPS ALREADY TRIED:
1. [Action] → [Outcome]
2. [Action] → [Outcome]
3. [Action] → [Outcome]

STORE IMPACT:
- Affected Devices: [Number]
- Affected Users: [Number]
- Operational Impact: [Description]

MANDATORY INFO VERIFIED:
✓ Asset ID: [Confirmed]
✓ Error Code: [Documented]
✓ Steps Tried: [Completed]
✓ Store Impact: [Assessed]

ATTACHMENTS:
- [Error screenshot / logs / diagnostics]
- [Link to ticket in system]

CUSTOMER CONTACT:
Name: [Contact Name]
Phone: [Phone Number]
Email: [Email Address]
Preferred Method: [Phone/Email/Slack]

---
Escalated by: [L1 Agent Name]
Escalation Time: [Timestamp]
```

---

## Common Escalation Triggers

Immediately escalate (do not attempt extended troubleshooting) if:

- **Payment processing failure** (transactions not completing, payment terminal unresponsive)
- **Complete POS system outage** (all terminals down at a location)
- **Database corruption or data loss** indicators
- **Security incident** suspected (unauthorized access, malware symptoms)
- **Network infrastructure failure** (switch/router down, multiple locations affected)
- **Third-party integration failure** (payment gateway, kitchen display system, reporting platform)
- **Error code not in knowledge base** or unfamiliar to L1
- **Customer has already waited >30 minutes** after initial contact
- **Issue affects compliance** or regulatory requirement
- **Customer requests escalation** or expresses dissatisfaction

---

## Training & Compliance

**L1 Agent Responsibilities:**

- Complete annual training on this procedure
- Maintain knowledge base familiarity
- Update troubleshooting logs continuously
- Report procedure gaps or needed improvements to L1 Manager

**Quality Auditing:**

- Random sample of 5% of escalations reviewed monthly
- Compliance with mandatory field completion checked
- SLA adherence verified
- Feedback provided to agents quarterly

---

## Document Control

| Field            | Value                  |
| ---------------- | ---------------------- |
| **Document ID**  | SOP-IT-L1-002          |
| **Version**      | 1.0                    |
| **Created Date** | 2025-01-10             |
| **Last Updated** | 2025-01-10             |
| **Next Review**  | 2025-07-10             |
| **Owner**        | L1 Support Manager     |
| **Approved By**  | IT Operations Director |

---

## Appendices

### Appendix A: Ticket System Field Reference

- Refer to Ticketing System Administrator for system-specific field mapping
- Ensure custom fields match mandatory information checklist

### Appendix B: Common Error Codes & L1 Resolutions

- [Link to internal error code database]
- [Link to L1 troubleshooting flowcharts]

### Appendix C: Do-Not-Escalate Exceptions

Contact L1 Manager before escalating if conditions are outside standard scope.

---

**Questions about this procedure?** Contact your L1 Support Manager or email it-manager@servewell.in
