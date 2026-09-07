# Design Notes

## Data Model

A single `Student` entity: server-generated `id`, required `first_name`/`last_name`,
unique validated `email`, `date_of_birth` (must be in the past), `enrollment_status`
(enum: active/graduated/dropped), and server-managed `created_at`/`updated_at`.

## API Design

Standard REST over `/students`. Key decisions:

- **PATCH over PUT** for updates, since the frontend edit form is a genuine partial-update
  use case and PATCH is the semantically correct verb for that.
- **400 vs 409 distinction**: 400 for malformed input (bad email format, future DOB),
  409 reserved for a well-formed request that conflicts with existing data (duplicate email).
  On update, a student keeping their own current email is explicitly excluded from the
  409 check — only a _different_ student's email triggers the conflict.
- **Pagination beyond available data returns 200 with an empty list**, not an error —
  it's a valid, well-formed request that simply has no results.

## Component Structure (frontend)

- `services/api.js` — the single place that imports axios; every component calls
  exported functions from here, never axios directly.
- `StudentList.vue` — owns fetching, pagination state, and filter state; renders
  loading (skeleton rows), error (retry), empty (clear filter), and success states explicitly.
- `StudentForm.vue` — a slide-over panel handling both create and edit (driven by
  a nullable `student` prop), with client-side validation as a UX layer on top of
  the backend's authoritative validation.
- `ConfirmDialog.vue` — a small reusable yes/no dialog for destructive actions.
- `App.vue` — orchestrates which panel/dialog is open and refreshes the list
  in place after any mutation, rather than remounting (which would reset pagination/filter).

## Key Decisions

**Visual design was a deliberate choice, not a default.** Rather than a generic
rounded-card admin dashboard, the UI is styled around the actual subject matter —
a registrar's record system — using a real data table with enrollment status
communicated through color-coded left borders (green/gold/grey) instead of
decorative badges, paired with a serif/sans type combination to give it an
academic-record feel rather than a generic SaaS look.

**The edit form submits the full record on every PATCH**, even though the backend
correctly supports true partial updates (verified independently with curl —
submitting only a single field like `enrollment_status` updates just that field
and leaves everything else untouched). Since the edit form always starts from a
complete, pre-filled record, sending the full payload is simpler on the frontend
without sacrificing correctness, and the backend's own-email exclusion logic
means resubmitting an unchanged email never triggers a false 409.

**UI states (loading, error, empty) were verified visually, not just assumed
from the code.** Each state — including simulating a stopped backend to confirm
the error-and-retry path, and filtering to a status with zero results for the
empty state — was manually exercised in the browser before being marked done,
which is also how both issues noted in the AI Usage section were actually caught
rather than just assumed away.
