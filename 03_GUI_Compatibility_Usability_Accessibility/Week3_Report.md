# Week 3 GUI compatibility usability and accessibility assessment

## Scope and conclusion

The scoped Week 3 execution and documentation are complete. PyTodo's task forms, controls, navigation, messages, visual consistency, two available desktop browsers, task-list/form configurations, reported usability, and selected WCAG concepts were reviewed. Two accessibility defects remain open. Testing does not establish that the application has no other defects.

The original 35-case package has been reconciled with dated verification. Two additional accessibility checks distinguish visible labels from programmatic labels and sample text enlargement. There are now **37 unique cases**: 30 agent-executed browser checks and 7 retained user-reported manual usability observations. These populations are identified separately; original and verification executions of the same case are not added together.

## Environment and provenance

| Field | Recorded value |
|---|---|
| Verification date | 2026-11-12, Asia/Singapore; exact UTC timestamps in JSON |
| Executor | Agent-executed automated verification |
| Original manual usability executor/date | Not recorded in supplied material; no identity or date inferred |
| Operating system | Windows 11, build 26200 |
| Edge | 157.0.4341.42 |
| Chrome | 157.0.8103.51 |
| Desktop viewport | 1280 x 900 CSS pixels, normal initial zoom |
| Narrow viewport | 600 x 700 CSS pixels, normal zoom |
| Enlargement sample | 200% CSS zoom on New Task; simulation, not native browser zoom |
| Application | Original app SHA-256 `050b4ee4bb7d42f9ea835b46569185177755feee8e420f861376df4e6097f30f` |
| Isolation | Localhost port 5014 in saved verification; temporary DB; normal app/database unchanged |

The four Excel files are the case repository. Shared precondition for GUI/compatibility/accessibility: original app running through the isolated server; a dedicated verification account; task setup in runner order. Every current browser result links to a screenshot and a structured record in [browser_results.json](evidence/verified/browser_results.json). GUI-TC-004 now verifies the saved description as well as title. GUI-TC-009 explicitly completes the task before testing Done filtering. A far-future due date keeps GUI-TC-003 independent of the semester date.

The original observations and statuses are preserved in [original_records.json](evidence/original_records.json). Existing 24 user-supplied screenshots are retained. Their capture dimensions do not establish the original viewport or browser version. Current environment values above belong to the new verification only.

## Checklist and execution results

| Area | Case IDs | Executed | Pass | Fail | Evidence / repository |
|---|---|---:|---:|---:|---|
| GUI | GUI-TC-001 to 014 | 14 | 14 | 0 | [GUI workbook](Week3_GUI_Test_Cases_001-014.xlsx) |
| Compatibility | COMP-TC-001 to 007 | 7 | 7 | 0 | [Compatibility workbook](Week3_Compatibility_Test_Cases_001-007.xlsx) |
| Manual usability | USAB-TC-001 to 007 | 7 | 7 | 0 | [Usability workbook](Week3_Usability_Test_Cases_001-007.xlsx) |
| Basic accessibility | ACC-TC-001 to 009 | 9 | 7 | 2 | [Accessibility workbook](Week3_Accessibility_Test_Cases_001-009.xlsx) |
| Total unique cases | | 37 | 35 | 2 | 0 Blocked / 0 Not Run |

Current statuses use Pass / Fail / Blocked / Not Run. The original two Partial Pass labels are preserved only in the historical JSON. ACC-TC-002 is now Fail based on measured text contrast, independently of badge-colour similarity. ACC-TC-005 passes the scoped native-validation check: the required Title field receives focus, its validation message is present, and submission is blocked. More specific wording remains an improvement suggestion.

## Compatibility matrix

| Browser/configuration | Cases | Result | Limits |
|---|---|---|---|
| Chrome, 1280 x 900 | COMP-TC-001/002 | Pass: display and task creation | Selected workflow only |
| Edge, 1280 x 900 | COMP-TC-003/004/005 | Pass: display, task creation, layout | Windows only |
| Edge, 600 x 700 | COMP-TC-006/007 | Pass: task list and form fit without horizontal overflow | Browser viewport simulation, not a physical mobile device |

Chrome and Edge share Chromium; this does not establish Firefox/Safari compatibility. Their recorded versions and exact viewports come from the browser process, not screenshot dimensions.

## Usability observations

The seven original observations cover navigation, labels, feedback, consistency, error prevention, task creation, and information presentation. They are retained as user-reported manual results, not represented as a new participant study. Relevant current GUI screenshots now corroborate interface state; a screenshot alone cannot demonstrate subjective ease. Narrow layouts remain denser than desktop and may benefit from spacing improvements. No task-completion-time, satisfaction score, or participant sample size was measured.

## Accessibility findings and recommendations

### DEF-W3-001 Completed task titles have insufficient text contrast

- Feature: completed task titles in My Tasks; requirement R-11; ACC-TC-002.
- Environment/precondition: Edge desktop configuration above; at least one completed task.
- Reproduce: (1) Create a task. (2) Mark it Done. (3) Read computed title colour and table background. (4) Calculate WCAG relative luminance contrast.
- Expected: normal-size task title text at least 4.5:1 against its background.
- Actual: `rgb(153,153,153)` on `rgb(255,255,255)` gives approximately **2.85:1** at normal-size text. The title remains meaningful task information.
- Evidence: [screenshot](evidence/verified/ACC-TC-002.png); computed-style assertion in [browser_results.json](evidence/verified/browser_results.json), ACC-TC-002.
- Severity / priority / status: Moderate / Medium / Confirmed, open.
- Recommendation for maintainer: darken completed-title text while retaining the strikethrough/non-colour completion cues. No source correction applied.
- Basis: [WCAG 1.4.3 Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

### DEF-W3-002 New Task fields lack programmatic label associations

- Feature: New Task form; R-11; ACC-TC-008.
- Environment/precondition: Edge desktop; authenticated user on New Task.
- Reproduce: (1) Open New Task. (2) Inspect Title, Description, Category and Due Date controls. (3) Check associated labels, aria-label and aria-labelledby.
- Expected: each control's purpose can be determined programmatically.
- Actual: all four controls have `labels.length == 0`, no aria-label and no aria-labelledby. Visible label text exists, so the separate visual-label check ACC-TC-004 passes its narrower scope.
- Evidence: [screenshot](evidence/verified/ACC-TC-008.png) for form context; DOM results in [browser_results.json](evidence/verified/browser_results.json), ACC-TC-008. The DOM record, not the screenshot alone, establishes the association gap.
- Severity / priority / status: Moderate / Medium / Confirmed, open.
- Recommendation for maintainer: associate each label with its control using matching for/id or suitable nesting. Verify accessible names with assistive technology after any fix.
- Basis: [WCAG 1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html); [visible-label and programmatic-label distinction](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html).

### Improvement observations

Similar grey Open/Done badges alone are not a confirmed use-of-colour failure: text, checkmarks and strikethrough provide additional cues. Maintain those cues. The generic native required-field message can be made more specific. Narrow layouts can be made less dense. These suggestions do not create additional defect counts.

Keyboard evidence covers one representative Tab/Enter navigation path with a visible outline; it does not prove every component's keyboard behaviour. The 200% CSS-zoom sample passes this limited form check. Screen-reader announcements, full focus order, contrast of every element, physical devices and complete WCAG conformance were not established.

## Reproduction and evidence

Install the original app's Python requirements and Playwright in your own test environment. Set PYTODO_SOURCE_DIR to the original supplied app folder; the runner enforces the original app hash. Install browser channels Edge and Chrome. Node dependency: Playwright 1.62.1, pinned in package.json.

From the repository root, start the server in one PowerShell terminal:

```powershell
$env:PYTODO_SOURCE_DIR = 'C:\Users\Admin\Downloads\STQA\pytodo_pro_student'
python .\03_GUI_Compatibility_Usability_Accessibility\run_isolated_server.py
```

In another terminal, run `npm install` from the Week 3 folder, then `node run_browser_checks.mjs`. The default server port is 5013. The saved run used QA_BASE_URL/QA_PORT overrides for 5014. This runner also produces the Week 4 web verification. Save old evidence before rerunning; files with the same case IDs are overwritten. Exit status 1 means at least one assertion failed. Stop the temporary server afterward.

The four workbooks and this report meet the brief's GUI checklist/results, configuration matrix, usability observations, basic accessibility findings, and defect/recommendation contents. Only selected accessibility concepts are evaluated; no compliance certification is claimed. Source integrity and evidence-link checks are recorded in [verification.json](evidence/verified/verification.json).
