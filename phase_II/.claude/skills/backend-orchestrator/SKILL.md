---
##name: "fastapi-backend-orchestrator"
description: "Organize backend services, middleware, and routes in a secure, spec-aligned FastAPI application. Use when structuring backend logic and enforcing JWT-based auth."
version: "1.0.0"
---

# Backend Orchestration Skill

## When to Use This Skill

- Structuring FastAPI backend  
- Middleware is required  
- Multiple routes share authentication logic  
- Database access must be controlled

## How This Skill Works

1. Define backend structure: entry point, routes, models  
2. Add middleware: JWT verification, error handling  
3. Separate routing from business logic  
4. Enforce secure data access  
5. Standardize error responses

## Output Format

- Backend Structure Overview  
- Middleware Responsibilities  
- Route Organization  
- Security Enforcement Rules

## Quality Criteria

- Routes are secure by default  
- Authentication logic centralized  
- User data access properly scoped  
- Errors are consistent and predictable
