# Changelog

All notable changes to Work Tracker will be tracked here.

## v0.2.0 - Current MVP Interaction Build

### Added

- Added app identity metadata in `app_info.py`.
- Added `Work Tracker v0.2.0` as the desktop window title.
- Added visible version tracking in `README.md`.
- Added activity creation from the sidebar and the main `Add Activity` button.
- Added an activity details dialog for start time, end time, activity type, project, MSM number, and notes.
- Added real timeline activity blocks.
- Added double-click editing for existing activity blocks.
- Added click-and-drag creation directly on the timeline.
- Added vertical dragging to move activity blocks up or down.
- Added a bottom resize grip to extend or shorten activity blocks.
- Added 15-minute snapping for timeline drawing, moving, and resizing.
- Added dotted half-hour guide lines.
- Added local schedule saving in `data/schedules/`.
- Added schedule loading from saved JSON files.
- Added `Save & Copy` to save the schedule and copy tab-separated rows for pasting into a spreadsheet or Smartsheet.
- Added live summary totals by duration, block count, and activity type.
- Added validation warnings for invalid time ranges, overlapping activities, and missing MSM numbers on product-related activities.

### Changed

- Updated `README.md` from scaffold documentation to the current working MVP flow.
- Updated `pyproject.toml` project version to `0.2.0`.
- Changed the main on-screen header to identify the app as `Work Tracker`.

### Deferred

- Smartsheet API submission is still intentionally deferred.
- Drag-and-drop is timeline-only for now; activity type drag/drop from the sidebar is not implemented yet.
- Delete and duplicate actions are still future work.

## v0.1.0 - Original Scaffold

### Added

- Created the initial Python project structure.
- Added starter folders for `models`, `ui`, `services`, `assets`, `config`, and `data/schedules`.
- Added starter files for the app entry point, activity model, day schedule model, planner UI, sidebar, summary panel, dialogs, storage, validation, and future Smartsheet service.
- Added a minimal runnable desktop app with a placeholder timeline view.
- Added initial dependency management with `pyproject.toml` and `requirements.txt`.
- Added a local virtual environment for development.
- Added initial README documentation for the MVP roadmap and architecture.
- Added `.gitignore` for local environment files, Python cache files, and saved schedule JSON.
