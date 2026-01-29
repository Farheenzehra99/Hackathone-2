# Skill: Spec to Task Decomposer

## 1. Purpose
Decompose a feature specification into atomic, sequential implementation tasks optimized for Claude Code's capabilities. This skill transforms high-level requirements into executable, testable units of work that can be completed in single generation cycles.

## 2. Owned By
Agent: **spec-to-tasks**

## 3. When to Use
Invoke this skill when:
- User has completed a feature specification and wants to break it down into tasks
- User is ready to move from planning to implementation
- User explicitly requests task decomposition from a spec
- Feature specification needs to be converted to tasks.md format
- After completing `/sp.specify` or `/sp.plan`

## 4. Input

**Required Input:**
```
feature_spec_path: string
```
Path to the feature specification file (e.g., "specs/authentication/spec.md").

**Optional Inputs:**
```
feature_plan_path: string (default: "{feature_path}/plan.md")
feature_tasks_path: string (default: "{feature_path}/tasks.md")
project_root: string (default: current working directory)
```

**Constraints:**
- feature_spec_path must be a valid file path
- Spec file must exist and be readable
- Plan file should exist if available (provides context)
- Spec must be complete (no placeholders or missing sections)

## 5. Step-by-Step Process

### Step 1: Read and Parse Specification
Read the feature specification file thoroughly.

**Parsing Actions:**
- Read entire spec.md file
- Identify all business requirements
- Extract success criteria and acceptance criteria
- Note scope boundaries (in-scope/out-of-scope)
- Identify user stories or use cases
- Extract any technical constraints or dependencies

**Completeness Check:**
- If spec is incomplete or ambiguous:
  - Identify missing sections or unclear requirements
  - State exactly what is missing
  - Request clarification before proceeding
  - Do not fill gaps with assumptions

### Step 2: Identify Core Components
Break down the feature into implementable components.

**Component Analysis:**
- Data models and types needed
- Business logic and operations
- APIs or interfaces required
- Error handling requirements
- Testing needs
- Configuration or setup requirements
- Migration or data changes (if applicable)

**Component Principles:**
- Each component should be logically cohesive
- Components should be ordered by dependencies
- Data models come before business logic
- Core functionality precedes edge cases

### Step 3: Task Decomposition
Create atomic tasks from identified components.

**Task Decomposition Principles:**

**Atomicity:**
- Each task modifies 1-3 files maximum
- Each task accomplishes one logical unit of work
- Tasks are small enough to complete in one generation
- No task requires multiple separate implementation sessions

**Specificity:**
- Each task has a clear, action-oriented goal
- Goal states exactly what will be accomplished
- Files to create/modify are explicitly named
- Deliverable is concrete and measurable

**Testability:**
- Every task produces something immediately verifiable
- Acceptance criteria are specific and measurable
- Tasks include testing artifacts when applicable
- Manual verification steps are acceptable

**Sequencing:**
- Data models and types first
- Core functionality second
- Edge cases and error handling third
- Testing fourth (but each task should be testable)
- Configuration and setup last

**Completeness:**
- All spec requirements are covered
- Error handling for defined failure modes
- Testing artifacts for verification
- Configuration or setup requirements
- No spec requirement is unaddressed

### Step 4: Task Structure Definition
Define each task with required fields.

**Required Fields:**

1. **task_id**: Sequential identifier (e.g., T001, T002, T003)
2. **goal**: Clear, action-oriented statement (verb-noun format)
3. **inputs**: Specific spec sections, existing files, or context needed
4. **files_to_create_or_modify**: Exact file paths relative to project root
5. **expected_output**: Concrete deliverable (function, class, config, test)
6. **acceptance_check**: Testable criteria to verify completion

**Field Guidelines:**

**goal:**
- Start with action verb (Implement, Create, Add, Configure, Write)
- State what will be accomplished
- Be concise but specific (5-15 words)
- Example: "Implement task data model with validation"

**inputs:**
- Reference spec sections by name or line numbers
- List existing files that will be modified
- Note any external dependencies or libraries
- Example: "Spec section 'Task Model', existing types.ts"

**files_to_create_or_modify:**
- Use relative paths from project root
- List all files that will be created or modified
- Separate with commas for multiple files
- Example: "src/models/task.ts, src/types.ts"

**expected_output:**
- Describe the concrete deliverable
- Be specific about what will exist after completion
- Example: "Task interface with TypeScript types, validation functions"

**acceptance_check:**
- Write as testable statement
- Use verification language (Verify, Confirm, Ensure)
- Example: "Verify TypeScript compilation succeeds with no errors"

### Step 5: Task Ordering
Order tasks by natural dependencies.

**Dependency Rules:**
- Data models must exist before business logic
- Core functionality must exist before edge cases
- Implementations must exist before tests
- Dependencies must be resolved before dependents
- Configuration before feature-specific code

**Example Order:**
1. Define data models/types
2. Create core business logic
3. Implement error handling
4. Add edge cases
5. Write unit tests
6. Configure and integrate

### Step 6: Review Against Spec
Validate task list against original specification.

**Validation Checklist:**
- Every spec requirement is addressed in at least one task
- Success criteria from spec map to task acceptance checks
- Out-of-scope items are not included
- Dependencies mentioned in spec are accounted for
- User stories or use cases are implemented
- Technical constraints are respected

**Traceability:**
- Each task can be traced to specific spec requirements
- Each spec requirement maps to one or more tasks
- No orphaned tasks (not needed for spec)
- No unaddressed spec requirements

### Step 7: Output Generation
Generate Markdown document with task list.

**Output Format:**
```markdown
# Implementation Tasks for [Feature Name]

## T001: [Task Goal]
**Inputs**: [Spec sections, files]
**Files**: [Paths to create/modify]
**Output**: [Concrete deliverable]
**Check**: [Acceptance criteria]

## T002: [Task Goal]
...
```

**Output Constraints:**
- No additional text, explanations, or commentary
- Only the numbered task list
- Each task has all six required fields
- Tasks are in dependency order
- No markdown tables, use field labels

## 6. Output

**Output Format:** Markdown document with task list.

**Structure:**
```markdown
# Implementation Tasks for [Feature Name]

## T[NNN]: [Task Goal]
**Inputs**: [Specific inputs from spec]
**Files**: [file paths separated by commas]
**Output**: [Concrete deliverable description]
**Check**: [Testable acceptance criteria]

[Additional tasks following same pattern]
```

**Output Constraints:**
- Only task list, no introduction or conclusion
- Each task has exactly 6 fields (task_id, goal, inputs, files, output, check)
- Tasks are numbered sequentially (T001, T002, etc.)
- Files use relative paths from project root
- Acceptance checks are testable and specific
- No code generation, only task definitions

**Quality Standards:**
- Tasks trace to spec requirements
- Tasks are atomic and independent
- Tasks are completable in one generation
- File paths are consistent with project structure
- Acceptance checks are specific and measurable
- Tasks flow in logical dependency order

## 7. Failure Handling

### Incomplete Spec
- If spec is missing critical sections:
  - Identify missing sections explicitly
  - State what information is needed
  - Request clarification before proceeding
  - Do not generate tasks with assumptions

### Ambiguous Requirements
- If requirements are unclear or conflicting:
  - Describe the ambiguity
  - Note which requirements are unclear
  - Ask for clarification
  - Do not guess or infer

### Unresolvable Dependencies
- If dependencies are undefined or unclear:
  - Identify undefined dependencies
  - Explain why they're blocking
  - Request clarification or external research
  - Do not create tasks with undefined dependencies

**Non-Destructive Behavior:**
- Never write implementation code
- Never add features not in spec
- Never make architectural decisions
- Only decompose what is explicitly specified
- Fail gracefully if spec is incomplete

**Quality Assurance:**
- Every task is atomic and testable
- All spec requirements are addressed
- Task dependencies are clear and logical
- File paths follow project conventions
- Acceptance criteria are specific
- No gaps or overlaps in task list
