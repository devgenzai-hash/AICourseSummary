# HealthBridge — MVP Build Prompt

> Paste this into Cursor, Claude, or any AI coding agent to scaffold the MVP.
> This is a **lean MVP**, not a full product. Build only what is listed here.
> Every section is intentionally scoped down. Leave room for improvement — don't over-engineer.

---

## WHAT THIS IS

**HealthBridge** — an AI-powered clinic management PWA for small Indian clinics.

**Core value in one sentence:** A doctor sees an AI-generated summary of their patient *before* the consultation starts. The patient can upload their lab reports and get plain-language explanations.

**Who pays:** Clinics (?2,500/month SaaS). Clinics bring their patients automatically.

**Build target:** MVP — 3 pilot clinics, real users, real data. Not production scale.

---

## TECH STACK (MVP — KEEP IT LEAN)

```
Frontend:   Next.js 15 (App Router) + React 19 + TypeScript (strict)
Styling:    Tailwind CSS v4 + shadcn/ui components
Auth:       Supabase Auth — phone OTP (primary), email (fallback)
Database:   Supabase (Postgres + pgvector) — single managed instance
Storage:    Supabase Storage (built-in, S3-compatible) — no external storage for MVP
AI:         Pluggable LLM layer (see AI Provider section below)
PWA:        next-pwa — installable on Android + iOS, offline-capable
Hosting:    Vercel (frontend) + Supabase (backend/db)
Email:      Resend (transactional email fallback)
```

**What is NOT in this MVP (add later):**
- Redis / caching layer — add in v2 when you have real traffic
- Real-time WebSocket subscriptions — polling is fine for MVP queue updates
- Cloudflare R2 / separate CDN — Supabase Storage handles MVP file needs
- WhatsApp Business API — too much setup friction; use email for MVP, WhatsApp in v2
- Payment gateway — manual UPI screenshot verification only
- External vector DB (Pinecone etc.) — pgvector on Supabase is sufficient

---

## PWA — MOST IMPORTANT FRONTEND REQUIREMENT

**This is critical.** HealthBridge must feel like a mobile app without being in any app store.

### Implementation requirements:

1. **Install prompt on first visit:**
   - Show a custom "Add to Home Screen" banner after 10 seconds on mobile
   - Banner text: "Install HealthBridge — works like a native app, no App Store needed"
   - Persist dismissal in localStorage — don't show again if dismissed
   - Re-show after 7 days if not installed
   - On iOS: show manual instructions (Safari ? Share ? Add to Home Screen) since iOS doesn't support the `beforeinstallprompt` event

2. **`manifest.json` (complete, required fields):**
```json
{
  "name": "HealthBridge",
  "short_name": "HealthBridge",
  "description": "Your health record, always with you",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#F8FAFC",
  "theme_color": "#0D9488",
  "orientation": "portrait",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "screenshots": [
    { "src": "/screenshots/home.png", "sizes": "390x844", "type": "image/png", "form_factor": "narrow" }
  ]
}
```

3. **Service Worker (via next-pwa / Workbox):**
   - Cache shell (layout, fonts, icons) — NetworkFirst strategy
   - Cache patient's last 10 reports metadata — StaleWhileRevalidate
   - Offline fallback page: "You're offline. Your cached reports are still available."

4. **iOS Safari meta tags** (add to root `layout.tsx`):
```html
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
<meta name="apple-mobile-web-app-title" content="HealthBridge" />
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png" />
```

5. **Install detection:** Use `window.matchMedia('(display-mode: standalone)')` to detect installed state. Show an "installed" confirmation screen once.

---

## AI PROVIDER LAYER — PLUGGABLE ARCHITECTURE

**This is the most important architectural decision.** Build a single `AIProvider` abstraction that supports switching LLM providers via an environment variable. Never call OpenAI directly from feature code — always go through this layer.

### Provider support (all must work via the same interface):

| Provider | Use case | Base URL |
|---|---|---|
| **OpenAI** | Default (GPT-4o, GPT-4o-mini) | `https://api.openai.com/v1` |
| **OpenRouter** | Access 100+ models, cost optimization | `https://openrouter.ai/api/v1` |
| **NVIDIA NIM** | Fast inference, medical LLMs | `https://integrate.api.nvidia.com/v1` |
| **Ollama** | Local dev / offline / private data | `http://localhost:11434/v1` |
| **llama.cpp server** | Self-hosted, edge deployment | `http://localhost:8080/v1` |
| **Groq** | Ultra-fast inference (Llama 3, Mixtral) | `https://api.groq.com/openai/v1` |
| **Together AI** | Open source models | `https://api.together.xyz/v1` |
| **Anthropic Claude** | Via direct SDK (not OpenAI-compatible) | Native SDK |

### Implementation — OpenAI-compatible unified client:

```typescript
// lib/ai/client.ts
// All providers except Anthropic use the OpenAI-compatible API format.
// One client handles: OpenAI, OpenRouter, NVIDIA NIM, Ollama, llama.cpp, Groq, Together AI.

import OpenAI from 'openai'

type AIProvider = 'openai' | 'openrouter' | 'nvidia-nim' | 'ollama' | 'llama-cpp' | 'groq' | 'together' | 'anthropic'

const PROVIDER_CONFIG: Record<AIProvider, { baseURL: string; defaultModel: string }> = {
  openai:       { baseURL: 'https://api.openai.com/v1',             defaultModel: 'gpt-4o-mini' },
  openrouter:   { baseURL: 'https://openrouter.ai/api/v1',          defaultModel: 'openai/gpt-4o-mini' },
  'nvidia-nim': { baseURL: 'https://integrate.api.nvidia.com/v1',   defaultModel: 'meta/llama-3.1-70b-instruct' },
  ollama:       { baseURL: 'http://localhost:11434/v1',             defaultModel: 'llama3.2' },
  'llama-cpp':  { baseURL: 'http://localhost:8080/v1',              defaultModel: 'local-model' },
  groq:         { baseURL: 'https://api.groq.com/openai/v1',        defaultModel: 'llama-3.3-70b-versatile' },
  together:     { baseURL: 'https://api.together.xyz/v1',           defaultModel: 'meta-llama/Llama-3-8b-chat-hf' },
  anthropic:    { baseURL: '', defaultModel: 'claude-3-5-haiku-20241022' }, // handled separately
}

export function getAIClient() {
  const provider = (process.env.AI_PROVIDER as AIProvider) || 'openai'

  if (provider === 'anthropic') {
    throw new Error('Use getAnthropicClient() for Anthropic provider')
  }

  const config = PROVIDER_CONFIG[provider]
  return {
    client: new OpenAI({
      apiKey: process.env.AI_API_KEY || 'ollama',
      baseURL: config.baseURL,
      defaultHeaders: provider === 'openrouter' ? {
        'HTTP-Referer': process.env.NEXT_PUBLIC_APP_URL,
        'X-Title': 'HealthBridge',
      } : undefined,
    }),
    model: process.env.AI_MODEL || config.defaultModel,
    provider,
  }
}

// Unified chat function — use this everywhere, never call OpenAI SDK directly from features
export async function chat(
  messages: OpenAI.Chat.ChatCompletionMessageParam[],
  options?: { temperature?: number; maxTokens?: number; responseFormat?: 'text' | 'json' }
) {
  const { client, model } = getAIClient()

  const response = await client.chat.completions.create({
    model,
    messages,
    temperature: options?.temperature ?? 0.3,
    max_tokens: options?.maxTokens ?? 1000,
    response_format: options?.responseFormat === 'json' ? { type: 'json_object' } : undefined,
    store: false, // Never store patient data for training
  })

  return response.choices[0].message.content
}
```

### Embedding model — use a better model:

```typescript
// lib/ai/embeddings.ts
// Use text-embedding-3-large (3072 dims) — significantly better than ada-002 for medical text.
// For Ollama local dev: use mxbai-embed-large (best open source embedding model).
// For cost-sensitive: text-embedding-3-small (1536 dims) is acceptable fallback.

const EMBEDDING_MODEL_DEFAULTS: Partial<Record<string, string>> = {
  openai:       'text-embedding-3-large',    // 3072 dims — best quality
  openrouter:   'openai/text-embedding-3-large',
  ollama:       'mxbai-embed-large',          // 1024 dims — best local option
  'llama-cpp':  'local-embedding-model',
  groq:         'text-embedding-3-large',     // falls back to OpenAI embeddings
}

export async function embed(text: string): Promise<number[]> {
  const provider = process.env.AI_PROVIDER || 'openai'
  const embeddingModel = process.env.EMBEDDING_MODEL || EMBEDDING_MODEL_DEFAULTS[provider] || 'text-embedding-3-large'

  const { client } = getAIClient()
  const response = await client.embeddings.create({
    model: embeddingModel,
    input: text.slice(0, 8000), // token safety limit
  })
  return response.data[0].embedding
}
```

**pgvector column size:** Use `vector(3072)` for text-embedding-3-large, `vector(1536)` for 3-small, `vector(1024)` for Ollama. Make this configurable via env var `EMBEDDING_DIMENSIONS`.

### Environment variables for AI:
```env
AI_PROVIDER=openai          # openai | openrouter | nvidia-nim | ollama | llama-cpp | groq | together | anthropic
AI_API_KEY=sk-...           # your API key (for ollama: leave blank or "ollama")
AI_MODEL=gpt-4o-mini        # override default model for provider
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSIONS=3072   # must match your chosen model's output size
```

---

## DATABASE (REQUIREMENTS ONLY — LET AI WRITE THE SCHEMA)

These are the **entities and relationships** needed. Let the AI agent generate the exact SQL schema from this.

### Entities:
- **Clinic** — has many doctors, departments. Patients are linked via appointments.
- **Doctor** — belongs to a clinic. Has availability slots. Creates and owns the daily queue.
- **Patient** — can self-register OR be created by clinic (name + phone only). Owns their records.
- **Appointment** — links patient ? doctor ? clinic. Has status, queue position, fee, payment info.
- **MedicalRecord** — file URL + OCR text + AI summary + vector embedding. Patient-owned.
- **HealthJournalEntry** — daily self-logs. Categories: blood_sugar, bp, weight, steps, sleep, water, mood, symptom. Also embedded for RAG.
- **Prescription** — medicine list (JSON), diagnosis, follow-up date. Can be OCR-extracted from a photo.
- **PatientVitals** — BP, pulse, temp, weight, SpO2. Linked to an appointment.
- **CarePlan** — AI-generated diet + exercise plan. Linked to an appointment.
- **DoctorQueue** — ordered list of patients for a doctor on a given day.
- **SharedLink** — token + expires_at for secure record sharing. Token is random UUID, not record ID.

### Key constraints:
- RLS on ALL tables — Supabase Row Level Security enabled before any data is written
- Doctors in Clinic A must never see patients from Clinic B — enforced by RLS policy
- Every `MedicalRecord` and `HealthJournalEntry` needs a `vector(EMBEDDING_DIMENSIONS)` column
- Soft deletes only — `deleted_at TIMESTAMPTZ` on all tables. Never hard delete medical data.
- Audit log table for every `MedicalRecord` access: `{user_id, record_id, action, accessed_at}`

```sql
-- Run this first in Supabase SQL editor
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## DOCTOR QUEUE — KEY FEATURE

Doctors create and manage their own daily patient queue. This is how they run their clinic day.

### Behavior:
- Doctor opens app ? sees "Today's Queue" — their ordered list for today
- Doctor can:
  - **Add** a walk-in patient to the queue (search existing by phone, or quick-create: name + phone)
  - **Reorder** patients by dragging (urgency changes, emergency walk-ins)
  - **Update status** per patient: `waiting ? in_consultation ? done ? no_show`
  - **Skip** a patient (moves to end, stays `waiting`)
  - **Clear** tomorrow's no-shows (auto-mark `no_show` at end of day)
- Queue is per-doctor per-day. Resets each morning.
- Queue position shows on patient's home screen: "You are #4 in queue at HealthPlus Clinic"
- **No WebSockets for MVP** — patient side polls every 2 minutes. Doctor side refreshes on window focus.

### Implementation:
- `appointments.queue_position INTEGER` column + `appointments.queue_date DATE`
- Queue reorder = batch update of `queue_position` values
- `useQueue()` hook abstracts polling — swap to WebSocket subscription later without changing components
- Walk-in creates a minimal appointment record: `{patient_id, doctor_id, clinic_id, queue_date: today, status: 'waiting', visit_type: 'walkin'}`

---

## APPLICATION ROUTES

```
app/
  layout.tsx              ? Root layout: PWA tags, Noto Sans, install prompt component
  page.tsx                ? Marketing landing page

  (auth)/
    login/page.tsx        ? Phone OTP + email login
    register/page.tsx     ? Patient self-registration (name, +91 phone, DOB, language)
    otp/page.tsx          ? OTP verification

  (patient)/              ? data-theme="light" applied in layout
    layout.tsx            ? Bottom nav: Home | Journal | Reports | Appts | More
    home/page.tsx         ? Snapshot + AI insight + quick log buttons + queue position
    reports/
      page.tsx            ? Report list (search + filter chips)
      upload/page.tsx     ? Upload: camera / gallery / PDF ? progress ? AI result
      [id]/page.tsx       ? Report detail: AI summary + test values table + Ask AI
    journal/
      page.tsx            ? 8-category log grid + streak + recent timeline
      log/page.tsx        ? Log entry: category + value + context + notes
    appointments/
      page.tsx            ? Appointment list
      book/page.tsx       ? Clinic search ? doctor ? slot picker ? confirm + UPI upload
      [id]/page.tsx       ? Appointment detail
    trends/page.tsx       ? HbA1c/sugar/LDL bar charts + compliance dot calendar
    care-plans/page.tsx   ? Diet plan + exercise plan
    medicines/page.tsx    ? Active medications + schedule
    ai-chat/page.tsx      ? RAG chat over patient's own records
    profile/page.tsx      ? Profile + language + caregiver access

  (doctor)/               ? data-theme="dark" applied in layout
    layout.tsx
    queue/page.tsx        ? Today's queue — hero screen (create / manage / walk-in add)
    queue/[id]/
      briefing/page.tsx   ? AI briefing card (RAG pre-generated)
      prescribe/page.tsx  ? E-prescription writer
      vitals/page.tsx     ? Quick vitals grid (fallback to OCR extraction)
    patients/
      page.tsx            ? Patient search
      [id]/page.tsx       ? Full patient timeline
    schedule/page.tsx     ? Manage availability slots

  (admin)/                ? data-theme="light" + amber accent in layout
    layout.tsx
    dashboard/page.tsx    ? Stats cards + AI insight + activity feed
    patients/page.tsx     ? Patient list + health alert badges
    payments/page.tsx     ? UPI screenshot review + verify/reject
    analytics/page.tsx    ? Recharts: revenue + bookings + doctor performance
    settings/page.tsx     ? Clinic info + add/remove doctors + departments

  api/
    auth/otp/route.ts
    reports/upload/route.ts       ? Upload ? OCR ? embed ? store
    reports/analyze/route.ts      ? LLM analyze OCR ? structured JSON + summary
    ai/briefing/[id]/route.ts     ? RAG briefing for doctor
    ai/chat/route.ts              ? Patient RAG chat
    ai/care-plan/route.ts         ? Generate diet + exercise plan
    vitals/extract/route.ts       ? OCR prescription image ? vitals JSON
    queue/route.ts                ? Queue CRUD + reorder + status update
    payments/verify/route.ts      ? Admin verify UPI payment
    analytics/route.ts            ? Aggregated clinic stats
```

---

## DESIGN SYSTEM

### Two themes via `data-theme` on the route group layout

**Theme A — Patient + Admin (light)**
```
--primary:      #0D9488   teal
--primary-dark: #0F766E
--bg:           #F8FAFC   off-white
--card:         #FFFFFF
--text:         #0F172A
--muted:        #64748B
--border:       #E2E8F0
--warning:      #F59E0B   (amber — also the admin accent color)
--danger:       #EF4444
--success:      #22C55E
```

**Theme C — Doctor (dark navy)**
```
--bg:           #0F172A
--card:         #1E293B
--border:       #334155
--accent:       #14B8A6   teal glow
--text:         #F8FAFC
--muted:        #64748B
--success:      #22C55E
--warning:      #F59E0B
```

### Typography
- Font: **Noto Sans** (Google Fonts — covers Hindi, Tamil, Telugu, Bengali natively)
- Body: 14px min. Line-height 1.65. Elderly users + small screens.
- Headings: 700–800 weight.
- Numbers: `font-variant-numeric: tabular-nums`

### Layout rules
- Mobile-first. 5-item bottom nav. No hamburger menu.
- Min tap target: 44×44px.
- Skeleton loading (`animate-pulse`) everywhere. Never block the screen with a spinner.
- CSS logical properties for future RTL support (`margin-inline-start` not `margin-left`).

---

## CORE SCREENS — BRIEF SPEC

### Patient
1. **Home** — "Good morning, Meena ??" + AI insight card (teal border) + 4-button quick log strip + queue position badge if in queue + 2 recent report previews
2. **Report upload ? analysis** — 3-way upload (camera/gallery/PDF) ? progress states ("Extracting ? Analyzing ? Done") ? AI summary card + color-coded test values table
3. **Health journal** — 8 category tiles (Blood Sugar ??, BP ??, Weight ??, Steps ??, Sleep ??, Water ??, Mood ??, Symptoms ??) + ?? streak + timeline
4. **Appointment booking** — clinic search ? doctor + slot grid ? confirmed + UPI upload
5. **Trend charts** — Recharts bar chart per metric (HbA1c, Sugar, LDL) with dashed threshold line + GitHub-style dot calendar for medicine compliance
6. **Care plans** — diet (eat more / reduce / meal timing) + exercise (weekly 7-day schedule + this week progress tiles)
7. **AI chat** — RAG chat. Show source count: "Based on 7 reports + 142 journal entries"

### Doctor (dark theme throughout)
1. **Queue screen (HERO)** — ordered list of today's patients. Status badges. "Add walk-in" button. Drag-to-reorder. AI briefing ready dot on each card.
2. **AI briefing card** — 3–5 sentence AI summary with numbers + key metrics grid (HbA1c/BP/LDL/eGFR) + recent visits + current medications + 3 AI-suggested discussion points
3. **E-prescription writer** — diagnosis input + medicine search with generic alternative chip + follow-up date
4. **Patient timeline** — all visits, reports, prescriptions in reverse chronological order
5. **Quick vitals** — 2×3 grid (BP, Pulse, Temp, Weight, SpO2, +Add). Amber tip about OCR extraction.

### Admin (amber accent)
1. **Dashboard** — 4 stat cards + AI insight card + activity feed
2. **Patient list** — search + filter + health alert badges
3. **UPI payment verification** — screenshot preview + verify/reject buttons
4. **Analytics** — Recharts: 30-day revenue + bookings by day + revenue per doctor

---

## AI FEATURES

### 1. Report OCR + Analysis
```
POST /api/reports/analyze
1. Fetch file from Supabase Storage
2. Send to GPT-4o Vision (base64 image) for OCR + extraction
3. Return JSON: {title, lab_name, report_date, parameters: [{name, value, unit, reference_range, status}], ai_summary, flags}
4. Embed the OCR text ? store in medical_records.embedding
5. ai_summary must be in patient's language_pref
```

### 2. Doctor Briefing (RAG)
```
POST /api/ai/briefing/[appointmentId]
1. Embed "patient summary for upcoming consultation"
2. Query pgvector: top 20 chunks from patient's medical_records + health_journal_entries
3. Call chat() with briefing system prompt + context
4. Return: {briefing, key_flags, positive_trends, suggested_questions}
Trigger: when appointment.status ? 'confirmed'
No caching for MVP — regenerate if not found
```

### 3. Patient AI Chat
```
POST /api/ai/chat
1. Embed user's message
2. pgvector query: top 10 chunks (patient-scoped only)
3. chat() with context + last 6 messages of history
4. Return response + source record IDs used
```

### 4. Care Plan Generation
```
POST /api/ai/care-plan
1. Fetch last 3 medical_records + recent vitals + appointment.notes
2. chat() requesting JSON: {diet_plan: {eat_more, reduce, meal_timing}, exercise_plan: {weekly_schedule, goal}}
3. Indian foods only. Indian climate exercise timing. Respond in language_pref.
4. Save to care_plans table
```

### System prompt rules (apply to all prompts):
- Never diagnose. Use "may indicate", not "you have"
- Always include specific numbers from records
- Patient-facing: plain language. Doctor-facing: clinical shorthand is fine.
- Always add `store: false` to every OpenAI call — no patient data for training

---

## SECURITY (NON-NEGOTIABLE)

1. **Supabase RLS on every table** — write policies before any feature code
2. **AI API keys server-side only** — never in `NEXT_PUBLIC_` env vars
3. **File upload validation server-side** — accept only: `image/jpeg`, `image/png`, `image/webp`, `application/pdf`. Max 10MB.
4. **OTP brute force** — max 5 attempts per phone per hour. Lock 1 hour after 5 failures.
5. **Secure share links** — random UUID token (not record ID). 24-hour expiry. `shared_links` table.
6. **Soft deletes only** — `deleted_at` column. Never hard delete medical data.
7. **DPDP Act 2023** — explicit opt-in per feature. Supabase ap-south-1 region (Mumbai).
8. **Rate limiting (no Redis)** — simple in-memory rate limiter in middleware. Max 10 AI calls/min per user.

---

## ALL ENVIRONMENT VARIABLES

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# AI — swap provider anytime by changing AI_PROVIDER
AI_PROVIDER=openai           # openai | openrouter | nvidia-nim | ollama | llama-cpp | groq | together | anthropic
AI_API_KEY=                  # API key (ollama: leave blank or set to "ollama")
AI_MODEL=gpt-4o-mini         # optional: override default model for chosen provider
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSIONS=3072    # 3072=3-large | 1536=3-small | 1024=ollama mxbai

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=HealthBridge

# Email
RESEND_API_KEY=
```

---

## SCOPE FOR IMPROVEMENT (DESIGN WITH THESE IN MIND — DON'T BUILD YET)

Build the hooks/wrappers below so v2 features slot in without rewrites:

| v2 Feature | Hook to build now (empty/stub) |
|---|---|
| Redis caching | `getCachedOrGenerate(key, ttl, fn)` — returns `await fn()` for now |
| WhatsApp notifications | `notify(patientId, type, data)` — sends email for now, WhatsApp case added later |
| Real-time queue | `useQueue(doctorId)` — polls every 2min for now, swap to Supabase subscription later |
| Payment gateway | `processPayment(appointmentId, method)` — manual UPI flow for now |
| CDN / separate storage | `getFileUrl(path)` — returns Supabase Storage URL for now |
| Multi-language i18n | All strings in `lib/i18n/[lang].ts`. Add language files without touching components. |
| Streaming AI responses | `chat()` already uses OpenAI SDK — add `stream: true` option when ready |
| Multi-model routing | `AI_MODEL_FAST` + `AI_MODEL_QUALITY` env vars — same provider, different models per task |

---

## BUILD ORDER

```
1. npx create-next-app@latest healthbridge --typescript --tailwind --app --src-dir
   npx shadcn@latest init
   npm i @supabase/supabase-js @supabase/ssr openai next-pwa recharts

2. Supabase setup
   - Create project in ap-south-1 (Mumbai)
   - Run: CREATE EXTENSION IF NOT EXISTS vector;
   - Let AI agent generate schema from the entity requirements above
   - Enable RLS on all tables + write auth policies

3. PWA setup
   - manifest.json + icons (192px, 512px maskable)
   - next.config.ts: configure next-pwa
   - Install prompt component (mobile-only, dismissible, iOS fallback)
   - iOS meta tags in root layout.tsx

4. AI client (lib/ai/client.ts + lib/ai/embeddings.ts)
   - Pluggable provider switching
   - Test with Ollama locally first (free, no API key)

5. Auth (phone OTP ? role detection ? protected routes)

6. Report upload + AI analysis  ? CORE VALUE LOOP, build this first
   - File upload to Supabase Storage
   - OCR via GPT-4o Vision
   - Embed + store in pgvector
   - Display AI summary + test values table

7. Doctor queue + AI briefing  ? HERO FEATURE
   - Queue creation, walk-in add, reorder, status updates
   - RAG briefing card

8. Appointment booking
9. Health journal + trend charts
10. Admin dashboard + payment verification
```

---

*MVP rule: when in doubt, do the simpler thing. Complexity is added when real users ask for it.*
