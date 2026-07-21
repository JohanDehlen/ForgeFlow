# Release Manifest

## Release

Version: **v0.12.0**

Name: **Prompt Builder Foundation**

Status: **Completed**

---

# Goal

Create the first provider-independent Prompt Builder.

The Prompt Builder transforms an Engineering Context into a deterministic development prompt that can be consumed by any AI provider or other engineering tool.

This release intentionally performs no AI communication.

---

# Features Delivered

- Prompt model
- PromptBuilderService
- Engineering Context integration
- Deterministic prompt generation
- Standard developer instructions
- Duplicate heading normalization
- End-to-end prompt generation
- Runtime validation

---

# Files Added

- `models/prompt.py`
- `services/prompt_builder_service.py`

---

# Files Modified

- `services/engineering_context_serializer.py`

---

# Files Removed

None.

---

# Architecture

The engineering pipeline is now:

```
Repository
      │
      ▼
Project Memory
      │
      ▼
Engineering Context
      │
      ▼
Prompt Builder
      │
      ▼
Prompt
      │
      ▼
Consumers
```

The Prompt Builder consumes only an `EngineeringContext`.

It never reads project files directly.

It performs no filesystem modification.

It communicates with no AI provider.

---

# Validation Performed

## Compilation

Passed.

## Runtime

Passed.

Verified:

- Prompt model creation
- PromptBuilderService
- Engineering Context integration
- Deterministic prompt generation
- Voiceanator prompt generation
- Developer instructions appended
- Duplicate document headings removed
- Full ForgeBud compilation

---

# Design Decisions

The Prompt Builder was intentionally separated from AI-provider communication.

Its responsibility is limited to constructing a reusable engineering prompt.

Future releases will consume the generated `Prompt` rather than rebuilding project context.

This keeps responsibilities clearly separated.

---

# Known Issues

None.

---

# Release State

Implementation Complete

Compilation Passed

Runtime Validation Passed

Documentation Synchronized

Ready for Commit

Ready for Push

---

# Next Release

Version:

**v0.13.0**

Name:

**Clipboard Export**

Goal:

Export an existing `Prompt` directly to the system clipboard.

No implementation has started.