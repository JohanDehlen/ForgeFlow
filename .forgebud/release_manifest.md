# Release Manifest

## Release

Version: **v0.5.0**

Name: **Current Task Manager**

Status: **Ready for Commit**

---

# Goal

Add full support for managing the active engineering task stored in project memory while preserving ForgeBud's layered architecture and existing functionality.

---

# Files Added

* `models/current_task.py`
* `services/current_task_service.py`
* `widgets/current_task_manager.py`

---

# Files Modified

* `controllers/project_controller.py`
* `main_window.py`
* `.forgebud/PROJECT_STATE.md`
* `.forgebud/current_task.md`
* `.forgebud/release_manifest.md`

---

# Files Removed

None.

---

# Validation

Compilation:

* Passed

Application Startup:

* Passed

Manual Validation:

* Current task loads correctly.
* Current task saves correctly.
* Editing is disabled for uninitialized projects.
* Editing is enabled for initialized projects.
* Existing project loading preserved.
* Existing dashboard preserved.
* Existing Git integration preserved.
* Existing release manifest functionality preserved.

---

# Known Issues

None.

---

# Architectural Compliance

Verified.

* Controllers coordinate workflows.
* Services perform all persistence.
* Widgets display state only.
* Models contain application state only.

No architectural deviations were introduced.

---

# Release Notes

This release introduces ForgeBud's Current Task Manager, allowing projects to persist and edit the active engineering task through the application interface. The implementation follows the existing layered architecture and integrates with project loading and initialization workflows without changing previous functionality.

---

# Future Work

## v0.6.0

Decisions Manager

Planned additions:

* Decisions model
* Decisions persistence service
* Decisions widget
* Controller integration
* Main window integration

---

# Release State

Implementation Complete

Compilation Passed

Runtime Validation Passed

Ready to Commit

Ready to Push
