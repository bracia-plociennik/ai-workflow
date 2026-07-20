# Accessibility

- Prefer semantic HTML and native controls.
- Every interactive control needs an accessible name and visible keyboard focus.
- Preserve logical focus order and support keyboard-only completion of the primary journey.
- Use labels, descriptions, errors, and status announcements that match the actual state.
- Do not use color alone for status, validation, or destructive meaning.
- Respect reduced motion and avoid disabling zoom or text resizing.
- Use verified library primitives for dialogs, menus, popovers, comboboxes, and focus management. Do not ship a hand-rolled substitute without dedicated keyboard and assistive-technology evidence.
- Test the critical journey with keyboard navigation, automated checks where available, and manual screen-reader review when risk warrants it.
