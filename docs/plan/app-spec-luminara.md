# Application Specification

Use this template to define the project foundation requirements. Keep answers concise. If unknown, write `TBD`.

## 1. Product Goal

### One-sentence description
- An application that interacts with art museum REST APIs to display great works of art in a user's home.

### Primary users
- Personal use (me and my wife); broader audience possible in a future release.

### Top 3 user actions for v1
1. Select a work of art to display on a video screen (most likely a TV).
2. Request and have the application display metadata about the currently displayed artwork.
3. Request and have the application read metadata about the currently displayed artwork using text-to-speech functionality.

## 2. App Shape

### Overlays to start with
- [x] CLI — device health checks and configuration commands
- [x] API — REST + WebSocket backend
- [x] UI — phone control UI and TV display page
- [ ] Worker

### UI profile(s) (if applicable)
- [x] Web — two pages: phone control UI (PWA) and TV kiosk display page
- [ ] Desktop
- [ ] Mobile
- [ ] N/A

### API style and execution model (if applicable)
- API style: REST + WebSocket
- Async endpoints expected: Yes — WebSocket push to TV display requires async

## 3. Data and State

### Persistence in v1
- Yes — persist lightweight app state and cached assets

### Storage choice
- File + SQLite: local filesystem for image/audio cache and SQLite for lightweight metadata/state

### Core domain entities
- Artwork: canonical artwork record normalized from Art Institute of Chicago API
- DisplaySession: currently selected artwork, display timestamp, and active screen state
- SpeechRequest: generated metadata narration request and playback status

## 4. Integrations

### External APIs/services
- Art Institute of Chicago API (selected v1 museum data source)
- Text-to-speech service: pyttsx3 for v1; migrate to a free higher-realism voice engine later

### Auth provider(s)
- None for v1 (home network only; no external auth required)

### Other integration needs
- Email: None
- Queue: None
- Webhooks: None
- Payments: None
- File storage: Local image cache (downloaded artwork images stored on device)

## 5. Security and Access

### Access model
- Public (home network only; no login required in v1)

### Roles and permissions
- No formal roles in v1; any device on trusted home network can control playback

### Compliance or data constraints
- PII handling: No user PII stored in v1
- Audit log needs: Basic operational logs only (errors, selected artwork ID, TTS events)
- Retention requirements: Keep cache bounded with simple max-size/max-age cleanup policy

## 6. Runtime and Deployment

### Initial runtime target
- Local only — mini PC or Raspberry Pi connected to TV via HDMI; backend serves both phone UI and TV kiosk page over home Wi-Fi

### OS/runtime constraints
- Linux (Raspberry Pi / mini PC) preferred; Windows dev machine for development

### Environment strategy
- Dev only for v1; single deployed instance on home device

## 7. Quality Expectations

### Test depth for v1
- Unit+Integration (target >= 85% overall coverage)

### Scale expectations
- Estimated users: 2 primary users in the home
- Request volume (if API/UI): Low (interactive/manual use, typically < 30 requests per minute)
- Job volume (if worker): N/A in v1 (no worker overlay)

### Reliability expectations
- Best effort with graceful fallback: retry transient museum API failures, preserve last displayed artwork if fetch fails

## 8. Delivery Preferences

### Architecture preference
- Simple now; layered later if multi-user or cloud hosting is introduced

### Naming and style conventions
- Use clear, domain-oriented names (artwork, display, narration) and keep API paths resource-based
- Prefer explicit typed models and small modules over deeply nested abstractions in v1

### Must-have decisions
- Use pyttsx3 as the initial TTS implementation for v1
- Keep a provider abstraction so TTS can be swapped later without UI/API contract changes

### Avoid decisions
- Avoid cloud-only dependencies for core runtime in v1
- Avoid introducing authentication/identity complexity before non-home-network usage is required
- Avoid premature microservice split; keep single deployable process for v1

## 9. v1 Scope Summary

### Must-have features (3-5)
1. Browse and select artwork from museum APIs via phone UI.
2. Display selected artwork fullscreen on TV (Chromium kiosk page updated via WebSocket).
3. Show artwork metadata on demand (title, artist, date, medium, description).
4. Read artwork metadata aloud using text-to-speech.
5. CLI commands for device health check and configuration.

### Nice-to-have later
- PWA install support with home-screen icon and offline shell
- Playlist and scheduled rotation mode
- Mood/theme filters and favorites collection
- Upgrade TTS provider to a free higher-realism local voice engine

## 10. Open Questions

- Which free higher-realism TTS engine should replace pyttsx3 in v2 (for example, Piper local voices)?
- Hardware target: Raspberry Pi or mini PC?
- Should the phone UI be installable as a PWA (add to home screen)?
- Image caching strategy: cache on disk or always fetch from API?

## 11. Assumptions

- The app runs entirely on the home network; no external access required in v1.
- The TV display device runs a Chromium browser in kiosk mode pointed at a local URL.
- The phone accesses the app via a browser over Wi-Fi (no native app install).
- A single backend process serves the REST API, WebSocket connections, and static UI files.
- Museum APIs are public and do not require paid keys for basic image and metadata access.
