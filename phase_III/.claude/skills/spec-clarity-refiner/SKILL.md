---
##name: "spec-clarity-refiner"
description: "Refine specifications to remove ambiguity, enforce constraints, and ensure Claude Code can implement them correctly. Use when specs are vague, incomplete, or producing incorrect output."
version: "1.0.0"
---

# Specification Refinement Skill

## When to Use This Skill

- Specs produce incorrect or inconsistent Claude Code output  
- Requirements are vague or incomplete  
- Security or edge cases are missing  
- Acceptance criteria are unclear or not testable

## How This Skill Works

1. Detect ambiguity and unclear wording in specs  
2. Add constraints and validation rules  
3. Strengthen acceptance criteria  
4. Ensure cross-spec consistency (features, API, database)  
5. Rewrite language to be explicit and machine-readable

## Output Format

- Identified Issues: parts of spec that are unclear or missing  
- Refined Sections: improved spec content  
- Reasoning: explanation why refinement was needed

## Quality Criteria

- Claude Code can implement specs without assumptions  
- Security rules and ownership are explicit  
- All edge cases covered  
- Acceptance criteria are objectively testable
