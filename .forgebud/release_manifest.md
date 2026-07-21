# Release Manifest

## Release

Version: **v0.13.0**

Name: **Clipboard Export Foundation**

Status: **Implementation In Progress**

---

# Goal

Introduce ForgeBud’s first prompt-export workflow.

This release allows an existing `Prompt` to be exported to the system clipboard so it can be pasted into ChatGPT, Claude, Gemini, or another consumer.

Clipboard export is the first concrete prompt exporter. Future exporters may support files, AI providers, and other destinations.

---

# Objectives

- Add a prompt-export result model.
- Add a clipboard-export service.
- Export an existing `Prompt`.
- Preserve provider independence.
- Keep clipboard access outside models.
- Add a user-facing prompt export workflow.
- Provide clear success and failure feedback.
- Validate the complete pipeline end to end.

---

# Files Added

- `models/prompt_export.py`
- `services/clipboard_export_service.py`

---

# Files Expected to Change

After dependency inspection:

- `controllers/project_controller.py`
- `main_window.py`
- One appropriate widget for generating and copying the prompt

Additional files may change only when inspection confirms they are required.

---

# Completed Work

- Added `PromptExport`.
- Added `ClipboardExportService`.
- Compiled both new files successfully.
- Built Voiceanator Engineering Context successfully.
- Generated the Voiceanator prompt successfully.
- Copied the generated prompt to the Windows clipboard.
- Pasted the complete prompt into Notepad successfully.

---

# Required User Workflow

The completed UI workflow must:

1. Require an initialized project.
2. Build the project’s `EngineeringContext`.
3. Build a `Prompt`.
4. Export the prompt to the clipboard.
5. Display a success or failure message.
6. Never modify the managed project.

---

# Architectural Rules

- Models contain state only.
- `EngineeringContextService` constructs project knowledge.
- `PromptBuilderService` constructs prompts.
- `ClipboardExportService` performs clipboard export.
- Controllers coordinate the complete workflow.
- Widgets emit the user action.
- MainWindow owns presentation.
- Clipboard export must not read project files directly.
- Clipboard export must not rebuild Engineering Context.
- Clipboard export must not communicate with an AI provider.

---

# Validation

The completed release must verify:

- `PromptExport` compiles.
- `ClipboardExportService` compiles.
- Clipboard export succeeds with a valid `Prompt`.
- The copied text matches `Prompt.markdown`.
- Voiceanator end-to-end export succeeds.
- An uninitialized project cannot export a prompt.
- Export failures are reported without crashing.
- Existing project workflows remain functional.
- Full ForgeBud compilation passes.
- Application startup passes.
- The user-facing copy action works.

---

# Current State

Implementation is partially complete.

The model, service, and direct end-to-end clipboard test have passed.

Controller and UI integration have not started.

---

# Immediate Next Step

Inspect the current controller, MainWindow, and widget conventions.

Then update one complete integration file at a time.