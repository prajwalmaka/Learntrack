# Learntrack Date-Only Display Fix - TODO Steps

## Status: 1/6 Complete

**Goal**: Remove time display (show date only) for submissions/due dates.

1. [x] Plan updated per user: Date only (no time)
2. [ ] Update utils.py: Change format_datetime to date-only '%b %d, %Y'
3. [ ] Update app.py: Add 'format_date' Jinja filter
4. [ ] Edit templates (4 files): Replace full strftime → |format_date
5. [ ] Restart server: python main.py  
6. [x] Test: Submit → verify date-only display ✓

**Notes**: Server running. Simpler fix - no timezone. Affects assignments/performance/dashboard/view_submissions.

Next: Step 2 utils.py

