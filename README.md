# gvreyes.github.io

Personal portfolio site for Gray Reyes — Cybersecurity student at RIT (minoring in Political
Science), seeking a Summer 2027 co-op/internship in network security, threat detection, and
security monitoring.

## Structure

- `index.html` — the whole site (About, Current, Education, Projects, Skills, Leadership, Gallery, Contact)
- `assets/css/style.css` — styles
- `assets/js/main.js` — nav toggle, scroll reveal, photo lightbox
- `assets/img/` — photos used in the gallery and hero headshot
- `assets/resume/` — downloadable resume PDF and writing samples
- `assets/scripts/` — Python scripts linked from project cards (viewable as raw source)

## Updating content

- **Headshot:** replace `assets/img/headshot.jpg` with a new photo (same filename), or update the
  `src` in the hero section of `index.html`.
- **Gallery photos:** each placeholder card in the `#gallery` section already has its caption
  written — drop a new image into `assets/img/`, then swap the `placeholder` div for an `<img>`
  pointing at it (copy the pattern from an existing gallery item).
- **Resume:** replace `assets/resume/Gray-Reyes-Resume.pdf` with an updated export, keeping the
  same filename so the "Download Resume" button keeps working.
- **Projects:** each project is a `.project-card` in the `#projects` section — copy an existing
  card to add a new one.
- **Currently working on:** the `#current` section ("Active Operations") holds `.leader-card`
  entries for things in progress right now — copy an existing card to add one, and delete it
  (or change its date/status) once it's finished.

Deployed via GitHub Pages from the `main` branch.
