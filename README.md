# LDClock

Academic desktop project implemented 100% in Python using Tkinter.

## Overview

LDClock is an analog clock application with:

- Real-time analog clock rendering.
- Manual time programming (custom time mode).
- Alarm management (add, delete, view).
- A manual Circular Doubly Linked List implementation as the main data structure.

## Project Structure

- `main.py`: application entry point.
- `ldclock/app.py`: main controller and UI orchestration.
- `ldclock/ui/analog_clock.py`: analog clock canvas component.
- `ldclock/services/time_controller.py`: system/custom time management.
- `ldclock/services/alarm_manager.py`: alarm logic over the list.
- `ldclock/models/alarm.py`: alarm entity.
- `ldclock/data_structures/circular_doubly_linked_list.py`: manual circular doubly linked list.

## Data Structure Usage

The Circular Doubly Linked List is used to store and manage alarms with:

- Node with next and previous references.
- Insertion at end.
- Deletion by condition.
- Forward traversal.
- Backward traversal.
- Empty-checking.

## Run Instructions

1. Open a terminal in the project root.
2. Run:

```bash
python main.py
```

No external dependencies are required.
