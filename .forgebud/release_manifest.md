# Release Manifest

## Release

Version: **v0.8.0**

Name: **Project Summary**

Status: **Released**

---

# Goal

Introduce managed Project Summary support so ForgeBud can create, load, display, edit, and persist concise project summaries stored in `.forgebud/project_summary.md`, while preserving the existing layered architecture and all existing functionality.

---

# Files Added

* `models/project_summary.py`
* `services/project_summary_service.py`
* `widgets/project_summary_manager.py`

---

# Files Modified

* `services/project_service.py`
* `controllers/project_controller.py`
* `main_window.py`

---

# Files Updated During Release Documentation

* `.forgebud/PROJECT_STATE.md`
* `.forgebud/current_task.md`
* `.forgebud/release_manifest.md`

---

# Files Removed

None.

---

# Validation

## Compilation

* Project Summary model compiled successfully.
* Project Summary service compiled successfully.
* Updated Project Service compiled successfully.
* Project Summary widget compiled successfully.
* Updated Project Controller compiled successfully.
* Updated MainWindow compiled successfully.
* Full project compilation passed.

## Runtime Validation

Verified successfully:

* Application starts without exceptions.
* Project Summary Manager appears correctly.
* Four project-memory managers display in a 2×2 grid.
* Existing initialized projects without `project_summary.md` load valid empty editable state.
* Saving creates `project_summary.md`.
* Saved project summaries reload correctly.
* Newly initialized projects receive a starter project-summary document.
* Existing project-summary documents are preserved.
* Current Task Manager remains functional.
* Decisions Manager remains functional.
* Coding Standards Manager remains functional.
* Dashboard remains functional.
* Recent-project support remains functional.
* Project initialization remains functional.

---

# Architectural Compliance

Verified.

* Controllers coordinate workflows.
* Services perform validation and persistence.
* Widgets display state and emit signals.
* Models contain state only.
* MainWindow owns UI composition only.

The 2×2 project-memory layout is a presentation improvement only and does not introduce a new architectural pattern.

---

# Release Notes

This release extends ForgeBud's managed project-memory system with Project Summary support.

Projects can now maintain an editable Markdown summary describing their purpose, technology, intended users, current development state, and important context. The summary is stored in `.forgebud/project_summary.md`, is created automatically for newly initialized projects, and is fully supported for existing projects that do not yet contain the document.

The project-memory workspace has also been reorganized into a 2×2 grid, allowing all managed project documents to remain visible and usable.

---

# Known Issues

None.

---

# Release State

Implementation Complete

Compilation Passed

Runtime Validation Passed

Documentation Synchronized

Release Committed

Release Pushed

Repository Synchronized

---

# Next Step

The v0.8.0 release is complete.

Before beginning v0.9.0:

1. Re-read every document in `.forgebud`.
2. Inspect `.forgebud/ROADMAP.md`.
3. Determine the next incomplete roadmap objective.
4. Create a complete release specification.
5. Inspect every required implementation dependency.
6. Continue with one implementation file at a time.
