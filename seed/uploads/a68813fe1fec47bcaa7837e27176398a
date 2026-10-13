# Receipt / Kitchen Printer Paper Jam

## Overview

Paper jams occur when thermal receipt paper becomes stuck inside the Epson TM-T88VI or StarMC Print v2 printer, typically caused by improper paper loading, debris accumulation, or using incorrect paper width. This runbook provides safe clearance procedures and preventative measures to restore printing operations without damaging critical components.

## Affected Systems

- **Epson TM-T88VI** (all firmware versions 1.0+)
- **StarMC Print v2** (firmware 2.1 and later)
- Compatible 58mm and 80mm thermal receipt paper rolls

## Symptoms

- Paper path obstruction with visible paper debris inside printer
- "Paper Jam" or "ERR: Paper Feed" error message on display panel
- Error light flashing red (steady or blinking pattern)
- Partial or incomplete print jobs (last 1-3 lines cut off or missing)
- Printer unable to advance paper despite power cycling
- Grinding or unusual mechanical sounds during print attempts
- Receipt paper torn inside the paper slot or feed mechanism

## Immediate Steps (First 2 Minutes)

1. **Power Down Safely**: Press the power button on the printer to OFF. Wait 10 seconds before proceeding. Do not force-power cycle repeatedly.

2. **Visual Inspection**: Open the printer cover (top lid). Look directly into the paper path for visible torn fragments, crumpled paper, or debris. Do not insert fingers beyond the visible area.

3. **Check Paper Roll**: Verify the paper roll type matches the printer specification:
   - Receipt printers use **58mm width**
   - Kitchen display system (KDS) printers use **80mm width**
   - Confirm paper is not expired (ink degradation causes feed issues) or damaged from moisture exposure.

## L1 Diagnosis Steps

1. **Document the Error State**:
   - Photograph the error light status (color, blinking pattern).
   - Note the exact error message displayed on the printer panel (if equipped with LCD screen).
   - Record timestamp of when jam occurred.

2. **Power Cycle and Self-Test**:
   - Power OFF the printer.
   - Wait 30 seconds.
   - Power ON and observe the startup sequence.
   - If printer displays "Self-Test Failed" or "ERR: Paper Feed" during startup, proceed to L1 Resolution Step 1 (manual jam clearance).

3. **Check Paper Sensor Status**:
   - On Epson TM-T88VI: Navigate to **Menu → Settings → Paper Status** (consult printer manual for exact button sequence on your firmware version).
   - Verify the paper sensor reads "Installed" and not "Error" or "Out of Stock."
   - If sensor is stuck in error state after jam clearance, note this for potential sensor malfunction.

4. **Attempt Print Test** (if no visible jam):
   - Print a test receipt from the POS terminal or use the printer's built-in **Self-Test Receipt** function (typically accessed via Menu button).
   - If test print succeeds, jam may have cleared; proceed to verification.
   - If test print fails with error, proceed to L1 Resolution.

## L1 Resolution

### **Scenario 1: Visible Paper Jam Inside Printer**

1. **Open the Paper Compartment**:
   - Lift the printer cover fully to its mechanical stop (approximately 90 degrees).
   - Locate the paper roll holder on the right side.

2. **Remove the Paper Roll**:
   - Press the paper roll release lever (usually a green or black tab on the roll holder).
   - Gently slide the paper roll out toward you. Do not force it.
   - Place the paper roll aside on a clean surface.

3. **Clear Visible Debris**:
   - Using a **soft brush or compressed air canister**, gently remove any loose paper fragments, dust, or debris from the paper path.
   - **Critical**: Do NOT use metal tools, scissors, or sharp objects near the print head (the horizontal component with thin metal pins).
   - Avoid touching the print head directly; oils from skin can degrade print quality.

4. **Extract Jammed Paper Safely**:
   - Locate the jammed paper section inside the feed mechanism.
   - **If paper is partially visible at the paper slot opening**: Gently grasp the paper edge and pull straight out in the direction of paper flow (downward/outward). Pull slowly to avoid tearing.
   - **If paper is deeply lodged**: Do not pull forcefully. Instead, use a plastic spoon or soft plastic card to carefully guide the paper free while pulling gently.
   - Remove all torn fragments; even small pieces can cause future jams.

5. **Inspect the Print Head and Rollers**:
   - Visually inspect the print head (thermal element) for any visible damage, discoloration, or paper residue.
   - Check the rubber feed roller (black cylindrical component below the print head) for any stuck paper fibers or ink buildup.
   - If residue is present on the roller, use a **lint-free cloth slightly dampened with isopropyl alcohol (70%)** to gently wipe the roller. Allow to air dry (30 seconds).

6. **Reload Paper Correctly**:
   - Insert a **fresh 58mm or 80mm thermal paper roll** (verify width matches printer specification).
   - Ensure the paper unrolls toward you (not away from you).
   - Feed the paper lead through the paper slot until approximately 1 inch extends below the printer.
   - Press the paper roll release lever to secure the roll.
   - Close the printer cover completely; you should hear a click.

7. **Power On and Test**:
   - Power ON the printer.
   - Wait for startup sequence to complete (approximately 5 seconds).
   - Print a test receipt from the POS terminal.
   - Verify that the full receipt prints without error and paper advances smoothly.

---

### **Scenario 2: Error Light Flashing, No Visible Jam**

1. **Perform a Hard Reset**:
   - Power OFF the printer.
   - Locate the small reset button on the **back of the printer** (approximately 2mm diameter, recessed).
   - Using a straightened paper clip or small stylus, press and hold the reset button for **5 seconds**.
   - Release the button.
   - Power ON the printer and wait for startup.

2. **Clear the Error Queue**:
   - On **Epson TM-T88VI**: Press **Menu → Clear Error** (exact path varies by firmware; check Menu button sequence on your device).
   - Allow the printer to cycle through its diagnostic routine (approximately 10 seconds).
   - If the error light turns off, the jam has likely cleared internally.

3. **Run Self-Test**:
   - Print the Self-Test Receipt using the **Menu button** on the printer panel.
   - Review the test receipt for any error codes or diagnostic messages.
   - If test receipt prints successfully, return to normal operation.

---

### **Scenario 3: Partial Print (Last Line Incomplete)**

1. **Check Paper Alignment**:
   - Open the printer cover and verify the paper roll is seated correctly in the holder.
   - Confirm the paper edge is aligned with the center guide on the paper slot.
   - Misaligned paper can cause the last line of each receipt to be cut off or incomplete.

2. **Adjust Paper Position**:
   - Remove the paper roll slightly and reposition it so the paper width is centered.
   - Ensure the paper unrolls smoothly without skewing.
   - Reload the roll and close the cover.

3. **Re-Test**:
   - Print a new test receipt.
   - Measure the receipt width to confirm it is **58mm** (or **80mm** if KDS printer).
   - If last line now prints completely, the issue is resolved.

---

## When to Escalate to L2

Escalate to L2 support and provide the following information **if any of these conditions are present**:

- **Print Head Damage**: Visible cracks, discoloration, or permanent marks on the thermal print head after jam clearance. _(Requires component replacement.)_
- **Sensor Malfunction**: Paper sensor remains in error state after successful jam clearance and test printing. _(Sensor may require reset or replacement.)_
- **Repeated Jams**: Same jam location occurs within 2 hours of manual clearance despite correct paper type and proper loading. _(Indicates mechanical misalignment.)_
- **Motor Failure**: Paper motor does not engage or makes grinding sounds after power-on, even after reset. _(Requires motor diagnostics.)_
- **Firmware Error Codes**: Printer displays error codes not listed in this runbook (e.g., "ERR: 0x04," "ERR: Motor Fault"). _(Requires firmware troubleshooting.)_
- **Unable to Clear Error Light**: Error light remains flashing after 2 hard resets and self-test completion. _(Indicates persistent firmware or sensor issue.)_

**Information to Collect Before Escalating**:

- Exact error code or message (photograph the display if possible).
- Printer model and firmware version (found in **Menu → About** or on device label).
- Timestamp of when the jam occurred.
- Photograph of any visible damage to the print head or internal components.
- Confirmation that the correct paper width (58mm vs. 80mm) is being used.
- Number of times the jam has occurred in the past 7 days.
- Current paper roll type and brand (if known).

---

## Related Runbooks

- `printer_power_cycling_reset.md`
- `thermal_paper_ordering_specifications.md`
- `printer_self_test_and_diagnostics.md`
- `epson_firmware_update_procedure.md`
- `kitchen_display_system_troubleshooting.md`
- `printer_head_cleaning_maintenance.md`

---

## Revision History

| Version | Date       | Notes                                                                                                        |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------ |
| 1.2     | 2025-09-15 | Updated for Epson TM-T88VI firmware 1.0+ and StarMC Print v2.1; added sensor malfunction escalation criteria |
| 1.1     | 2025-03-22 | Clarified 58mm vs. 80mm paper specification; added print head inspection steps                               |
| 1.0     | 2024-06-01 | Initial version                                                                                              |
