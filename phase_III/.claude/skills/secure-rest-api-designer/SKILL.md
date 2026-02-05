---
##name: "secure-rest-api-designer"
description: "Define secure, consistent REST APIs aligned with specifications and JWT authentication rules. Use when designing or validating API endpoints for multi-user systems."
version: "1.0.0"
---

# Secure REST API Design Skill

## When to Use This Skill

- Designing RESTful endpoints  
- APIs require authentication  
- Frontend and backend are decoupled  
- User-level authorization required

## How This Skill Works

1. Define resources and entities  
2. Map CRUD operations to HTTP verbs  
3. Specify request and response schemas  
4. Apply authentication rules  
5. Define error scenarios: 401, 403, 404

## Output Format

- Endpoint Definitions: method, path, purpose  
- Request Schema  
- Response Schema  
- Error Behavior

## Quality Criteria

- Each endpoint has a single responsibility  
- Authorization is enforced on every request  
- Errors are predictable and documented  
- Frontend can consume APIs without guessing
