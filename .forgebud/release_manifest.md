# Release Manifest

## Release

Version: **v0.6.0**

Name: **Decisions Manager**

Status: **Ready for Commit**

---

# Goal

Add persistent management of engineering decisions stored in `.forgebud/decisions.md` while preserving ForgeBud's layered architecture and existing functionality.

---

# Files Added

* `models/decisions.py`
* `services/decisions_service.py`
* `widgets/decisions_manager.py`

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

* Engineering decisions load correctly.
* Engineering decisions save correctly.
* Editing is disabled for uninitialized projects.
* Editing is enabled for initialized projects.
* Current Task Manager remains functional.
* Dashboard remains functional.
* Project loading remains functional.
* Recent projects remain functional.

---

# Known Issues

None.

---

# Architectural Compliance

Verified.

* Controllers coordinate workflows.
* Services perform persistence.
* Widgets present data only.
* Models contain application state only.

No architectural deviations were introduced.

---

# Release Notes

This release introduces the Decisions Manager, completing another project-memory capability alongside the Release Manifest Manager and Current Task Manager. Engineering decisions can now be viewed and edited directly within ForgeBud while following the same architecture and persistence model as the existing project-memory features.

---

# Future Work

Determine the next release from `.forgebud/ROADMAP.md` after v0.6.0 has been committed and pushed.

---

# Release State

Implementation Complete

Compilation Passed

Runtime Validation Passed

Ready to Commit

Ready to Push
