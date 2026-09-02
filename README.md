# Work Tracker

A lightweight Python desktop app for planning and recording a workday before eventually submitting summarized time entries to Smartsheet.

The first version is intentionally focused on the daily planning workflow. Smartsheet stays out of the MVP until the core experience feels useful.

## MVP Goal

Create a desktop application that lets you visually plan and record one workday at a time.

The app should answer:

> What am I doing right now, and how should it be recorded later?

## Current Scaffold

This starter project includes:

- A minimal runnable Python desktop app
- A placeholder day timeline
- A sidebar with starter activity types
- Domain models for activities and schedules
- Service modules for storage, validation, summary calculations, and future Smartsheet work
- A clean folder structure for growing the app without mixing concerns

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
    smartsheet.py
  assets/
  config/
    activity_types.json
  data/
    schedules/
```

## Run Locally

From the `Work Tracker` folder:

```powershell
.\.venv\Scripts\python.exe main.py
```

If you need to recreate the virtual environment:

```powershell
<path-to-python>\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This project currently uses only the Python standard library, so `requirements.txt` is intentionally empty.

## MVP Roadmap

### Milestone 1: Planner UI

- Show a single-day timeline
- Allow the user to create a basic activity block
- Keep the interface simple and fast to use

### Milestone 2: Activity Blocks

Each activity should include:

- Start time
- End time
- Activity type
- Optional project or MSM number
- Notes

### Milestone 3: Editing Experience

- Drag activity blocks
- Resize activity blocks
- Edit details from a dialog
- Delete or duplicate blocks

### Milestone 4: Validation

Future validation ideas to preserve:

- Detect overlapping activities
- Flag gaps in the workday
- Require MSM numbers for product-related work
- Warn when activity durations look unusual
- Check that required fields are present before export

### Milestone 5: Summary

- Calculate daily totals by activity type
- Calculate project or MSM totals
- Prepare rows in a shape that can later map cleanly to Smartsheet

### Milestone 6: Smartsheet Integration

Not implemented yet.

When the local workflow feels right, add a Smartsheet API service that can:

- Authenticate securely
- Map activities to Smartsheet rows
- Submit a day schedule
- Report submission errors clearly

## Architecture Notes

- `models/` contains plain Python objects that describe the workday.
- `ui/` contains desktop interface components.
- `services/` contains logic that is not directly tied to the UI.
- `data/schedules/` is reserved for local saved schedules.
- `config/` stores user-editable defaults, such as activity types.

This keeps the first version simple while leaving room for a future React interface or Smartsheet API integration.
