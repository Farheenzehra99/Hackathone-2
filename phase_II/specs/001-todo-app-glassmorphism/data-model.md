# Data Model: Todo App with Glassmorphism UI

## Overview
This document defines the data structures and entities for the glassmorphism todo app.

## Task Entity
- **taskId**: string (unique identifier)
- **title**: string (required, max 100 characters)
- **description**: string (optional, max 500 characters)
- **status**: enum ['pending', 'completed'] (default: 'pending')
- **priority**: enum ['low', 'medium', 'high'] (default: 'medium')
- **createdAt**: Date (timestamp when task was created)
- **updatedAt**: Date (timestamp when task was last updated)
- **dueDate**: Date (optional, when task is due)

## Task Validation Rules
- Title must be 1-100 characters
- Description must be 0-500 characters if provided
- Status must be one of allowed values
- Priority must be one of allowed values
- createdAt and updatedAt must be valid dates
- dueDate must be a valid date if provided

## UI State Entities

### TaskFormState
- **title**: string
- **description**: string
- **status**: 'pending' | 'completed'
- **priority**: 'low' | 'medium' | 'high'

### TaskFilterState
- **statusFilter**: 'all' | 'pending' | 'completed'
- **priorityFilter**: 'all' | 'low' | 'medium' | 'high'
- **searchQuery**: string

### ModalState
- **isOpen**: boolean
- **mode**: 'create' | 'edit'
- **taskId**: string (for edit mode)

## Component Props Definitions

### TaskCard Props
- **task**: Task entity
- **onEdit**: function (callback when edit button clicked)
- **onDelete**: function (callback when delete button clicked)
- **onToggleStatus**: function (callback when status changed)

### TaskForm Props
- **initialData**: Partial<Task> (for editing)
- **onSubmit**: function (callback when form submitted)
- **onCancel**: function (callback when form cancelled)