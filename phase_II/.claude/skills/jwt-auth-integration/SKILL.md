---
##name: "jwt-auth-integration"
description: "Design and implement secure, stateless JWT authentication across frontend and backend. Use when integrating Better Auth with backend services, ensuring multi-user data isolation."
version: "1.0.0"
---

# JWT Authentication Integration Skill

## When to Use This Skill

- Frontend and backend are separate services  
- Stateless authentication required  
- JWT tokens are used for authorization  
- Multi-user data isolation is critical

## How This Skill Works

1. Define authentication flow: signup → login → token issuance  
2. Specify JWT claims: user ID, expiry, issuer  
3. Design token verification logic: signature and expiry checks  
4. Enforce user ownership: token user matches resource owner  
5. Define failure behavior: unauthorized or forbidden access

## Output Format

- Authentication Flow: step-by-step lifecycle  
- JWT Requirements: claims, expiry, secret handling  
- Backend Verification Rules  
- Security Constraints

## Quality Criteria

- Backend can verify JWT independently  
- Users can only access their own data  
- Invalid tokens are safely rejected  
- Secrets are clearly defined and shared
