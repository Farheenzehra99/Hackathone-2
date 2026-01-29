# Skill: Spec Guardian

## 1. Purpose
Validate Spec-Kit files (constitution, specify, plan, tasks) before code execution to ensure completeness, consistency, and proper alignment. This skill acts as a quality gate, ensuring all specification documents are properly structured and aligned before implementation begins.

## 2. Owned By
Agent: **spec-guardian**

## 3. When to Use
Invoke this skill when:
- User is about to start implementing a new feature
- User has made changes to spec files and wants to proceed with implementation
- New functionality is requested and existing specs need validation
- Before running `/sp.implement` or `/sp.tasks`
- After completing `/sp.specify` or `/sp.plan`

## 4. Input

**Required Input:**
```
feature_path: string
```
Path to the feature directory containing spec files (e.g., "specs/authentication").

**Optional Input:**
```
constitution_path: string (default: ".specify/memory/constitution.md")
```
Path to the project constitution file.

**Constraints:**
- feature_path must be a valid directory path
- All spec files must exist: spec.md, plan.md, tasks.md
- Constitution file must exist at default or specified path

## 5. Step-by-Step Process

### Step 1: File Location
Locate all four spec files in the project hierarchy.

**Required Files:**
1. Constitution: `.specify/memory/constitution.md` (or provided path)
2. Specify: `{feature_path}/spec.md`
3. Plan: `{feature_path}/plan.md`
4. Tasks: `{feature_path}/tasks.md`

**File Validation:**
- Verify each file exists
- Verify each file is readable
- If any file is missing, record as critical issue

### Step 2: Constitution Validation
Validate the project constitution document.

**Required Sections:**
- Project principles or core values
- Code quality standards
- Testing standards
- Security standards
- Architecture principles or guidelines
- Non-negotiable constraints

**Validation Checks:**
- Core principles are clearly defined
- Architectural guidelines are present
- Testing and security standards are documented
- Explicit constraints are stated
- No placeholder or incomplete sections

### Step 3: Specify Validation
Validate the feature specification document.

**Required Sections:**
- Clear business requirements
- Success criteria (measurable and testable)
- Scope boundaries (in-scope and out-of-scope)
- User stories or use cases (when applicable)
- Acceptance criteria

**Validation Checks:**
- Business requirements are clear and unambiguous
- Success criteria are specific and measurable
- Scope boundaries are explicitly defined
- Requirements align with constitution principles
- User stories or use cases are present and complete
- No undefined technical jargon without explanation

### Step 4: Plan Validation
Validate the architectural plan document.

**Required Sections:**
- Architectural decisions addressing all specify requirements
- Technical approach aligned with constitution standards
- Dependencies and integrations
- Non-functional requirements (performance, security, reliability)
- Data models or schema definitions
- API contracts or interface definitions
- References to ADRs for significant decisions

**Validation Checks:**
- All specify requirements are addressed in plan
- Technical approach aligns with constitution
- Dependencies are documented with ownership
- NFRs have specific, measurable criteria
- Data models are complete with fields and types
- API contracts have inputs, outputs, and error handling
- Significant decisions reference ADRs
- No implementation details (that's for tasks)

### Step 5: Tasks Validation
Validate the implementation tasks document.

**Required Sections:**
- Ordered list of implementation tasks
- Each task mapped to plan components
- Each task with specific acceptance criteria
- Task granularity (small, focused changes)
- Error handling coverage for each task
- Testing requirements for each task

**Validation Checks:**
- Each task maps to plan components and specify requirements
- Acceptance criteria are testable and specific
- Tasks are appropriately granular (1-3 files per task)
- Error handling and edge cases are covered
- Testing requirements are explicit
- Task dependencies are clearly defined
- Tasks are in logical execution order

### Step 6: Cross-Document Consistency Validation
Validate alignment and consistency across all four documents.

**Consistency Checks:**
- Terminology is consistent across all documents
- Plan decisions don't violate constitution principles
- All tasks implement all plan components
- All specify requirements are addressed in plan/tasks
- No conflicting statements or approaches
- References between documents are accurate
- Version numbers or dates align

**Hierarchical Alignment:**
- Constitution → Specify: Feature respects project principles
- Specify → Plan: Plan addresses all business requirements
- Plan → Tasks: Tasks cover all architectural decisions
- End-to-end traceability: Every requirement has implementation path

### Step 7: Issue Identification and Classification
Identify all issues found during validation and classify by severity.

**Critical Issues** (block implementation):
- Missing required spec files
- Constitution principles violated by plan
- Specify requirements not addressed in plan
- Plan components not reflected in tasks
- Conflicting architectural decisions
- Undefined dependencies or external contracts
- Missing core business requirements

**Major Issues** (high risk):
- Incomplete sections in any spec file
- Vague or untestable acceptance criteria
- Missing NFR specifications
- Insufficient error handling coverage
- Gaps in data model or API definitions
- Unclear business requirements
- Missing user stories for user-facing features

**Minor Issues** (should fix):
- Inconsistent terminology
- Missing ADR references for decisions
- Incomplete metadata (dates, authors, versions)
- Formatting inconsistencies
- Minor clarity improvements needed
- Typos or grammatical errors

### Step 8: Output Generation
Generate JSON response with validation results.

**Never generate code, explanations, or implementation suggestions. Output only JSON.**

## 6. Output

**Output Schema:**
```json
{
  "status": "valid|invalid",
  "issues": [
    {
      "severity": "critical|major|minor",
      "file": "constitution|specify|plan|tasks",
      "category": "completeness|consistency|alignment|clarity",
      "description": "Specific description of the issue",
      "location": "Section or line reference if applicable"
    }
  ],
  "recommendation": "Clear, actionable next steps to resolve all issues. If valid, state 'All spec files are complete and consistent. Safe to proceed with implementation.'"
}
```

**Output Constraints:**
- Raw JSON only, no markdown code fences
- No explanatory text before or after JSON
- Valid JSON with proper quoting
- All issues have severity, file, category, description fields
- Location field is optional
- Status is "invalid" if any critical or major issues exist
- Recommendation is specific and actionable

**Issue Categories:**
- **completeness**: Missing sections or required information
- **consistency**: Conflicting information across documents
- **alignment**: Documents not supporting each other in hierarchy
- **clarity**: Ambiguous or unclear requirements/specifications

## 7. Failure Handling

### Missing Files
- If any required file is missing:
  - Record as critical issue
  - Include file name and expected location in description
  - Set status="invalid"

### Parse Errors
- If a file cannot be read or is malformed:
  - Record as critical issue
  - Describe the error in description
  - Set status="invalid"

### Validation Failures
- If any validation check fails:
  - Record issue with appropriate severity
  - Include specific details about what failed
  - Provide clear description of problem
  - Adjust status based on severity

**Non-Destructive Behavior:**
- Never modify any spec files
- Never add or suggest features not in specs
- Never make architectural decisions
- Never generate implementation code
- Report only, do not fix

**Quality Assurance:**
- Always return valid JSON
- Thorough but objective validation
- Clear, actionable recommendations
- No false positives or unnecessary issues
- Consistent validation across multiple runs
