---
##name: "system-architecture-designer"
description: "Design clear, scalable, spec-driven system architectures for multi-phase full-stack applications. Use when user wants to plan overall architecture, define component responsibilities, and map specs to system design."
version: "1.0.0"
---

# System Architecture Design Skill

## When to Use This Skill

- User needs to design overall system architecture  
- Project involves frontend, backend, authentication, database  
- Multi-phase evolution is expected (console → web → AI → cloud)  
- Spec-driven development must be followed

## How This Skill Works

1. Identify core components: frontend, backend, auth, database, specs  
2. Define responsibilities: clear ownership for each layer  
3. Design data flow: request → auth → processing → database → response  
4. Enforce boundaries: prevent cross-layer coupling  
5. Align architecture with specs: ensure all components map to Spec-Kit structure

## Output Format

- Architecture Overview: high-level description of system  
- Component Responsibilities: detailed role per layer  
- Data Flow Description: step-by-step request lifecycle  
- Spec Alignment: mapping of specs to system components

## Quality Criteria

- Each component has a single clear responsibility  
- User data isolation is enforced by design  
- Specs can be implemented without assumptions  
- System supports future phases without redesign
