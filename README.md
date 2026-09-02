# Work Tracker

Work Tracker is a lightweight Python desktop app for planning and recording a workday. The first version focuses on making daily time tracking easier before adding any Smartsheet integration.

The app is being built as a local-first tool: simple, fast, and useful during the actual workday.

## Current Status

This project is an early MVP scaffold. It currently includes:

- A minimal runnable desktop app
- A placeholder single-day timeline
- A sidebar with starter activity categories
- A summary panel placeholder
- Plain Python models for activities and day schedules
- Service modules for storage, validation, summaries, and future Smartsheet support

Smartsheet integration is intentionally not implemented yet.

## Project Structure

```text
Work Tracker/
  main.py
  pyproject.toml
  requirements.txt
  README.md
  models/
    activity.py
    day_schedule.py
  ui/
    planner.py
    sidebar.py
    summary.py
    dialogs.py
  services/
    storage.py
    validation.py
    summary.py
    smartsheet.py
  assets/
  config/
    activity_types.json
  data/
    schedules/
```

## Run the App

From this folder:

```powershell
.\.venv\Scripts\python.exe main.py
```

If the virtual environment ever needs to be recreated:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The project currently uses only the Python standard library, so `requirements.txt` is expected to be empty.

## MVP Roadmap

### 1. Planner UI

- Display a single workday timeline
- Make the day easy to scan
- Support creating basic activity blocks

### 2. Activity Blocks

Each activity should eventually support:

- Start time
- End time
- Activity type
- Optional project
- Optional MSM number
- Notes

### 3. Editing Workflow

- Edit activity details
- Move blocks on the timeline
- Resize blocks to adjust duration
- Delete or duplicate blocks

### 4. Validation

Future validation ideas:

- Detect overlapping activities
- Flag gaps in the workday
- Require MSM numbers for product-related work
- Warn when durations look unusual
- Check required fields before export or submission

### 5. Summary

- Calculate daily totals by activity type
- Calculate totals by project or MSM number
- Prepare clean rows for future export or Smartsheet submission

### 6. Smartsheet Integration

Later, after the local workflow feels right:

- Add secure Smartsheet authentication
- Map schedule activities to Smartsheet rows
- Submit a completed day schedule
- Show clear success and error messages

## Architecture

- `models/` holds the core data objects.
- `ui/` holds the desktop interface.
- `services/` holds logic that is not tied directly to the interface.
- `config/` stores editable defaults.
- `data/schedules/` is reserved for saved local schedules.

This structure keeps the Python MVP clean while leaving room for a future React interface if the app grows in that direction.
