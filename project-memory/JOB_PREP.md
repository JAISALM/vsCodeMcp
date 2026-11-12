# JOB_PREP.md — interview-prep execution (2026-11-12)

**Profile:** 5-yr Java dev (Capgemini 3.3 yr + Infosys 1.1 yr, service-based), BTech CS 7.61, **Tier-3 college (Kerala)**, NOT IIT. Jobless since **2026-11-06** (last working day). 11-07→11-12 stomach issues; **execution Day 1 = 2026-11-12**. Target: **GCC + Europe remote, good money** (> 11 LPA). "my only hope is in java, and AI related stuff since java is boss of enterprise." Aiming high → must compete on LeetCode too.

## STACK DECISION (2026-11-12)
- **Backend:** Java (enterprise) + **Spring** — non-negotiable for GCC/Europe enterprise roles.
- **Frontend: ANGULAR, not React** (user: "i see jb posting needs java + angular"). User's own target postings show it; GCC/Europe enterprise Java shops commonly pair Spring + Angular. **React = fallback only if he later targets US/product roles** (more raw volume there). **Pick ONE — Angular.**
- **AI:** his **film pipeline (ComfyUI + AI agents) IS the AI experience** — the rare, sellable differentiator. Profile to sell: **"5-yr enterprise Java + hands-on AI pipeline builder."** This is what separates him from the 1,000 other Java devs applying.
- **DSA:** NeetCode 150 (pattern-based) = the biggest gap (never did LeetCode).

## BOOK TRIAGE (2026-11-12) — 12 books → 5 spine / 4 multipliers / 4 reference
**RULE: no book gets "covered" — each has a UNIT OF SUCCESS. Completion is not the goal (his diagnosed anti-pattern: "on the verge of completing the task rather than learning by it").**

### TIER 1 — the SPINE (this window, in this order)
1. **NeetCode 150** — the coding spine. Unit per pattern: TRIGGER (what signals the pattern) + SKELETON from memory + 1 NEW problem without peeking.
2. **The Complete Coding Interview Guide in Java** (Anghel) — Java-specific coding; complements NeetCode. Unit: solve the Java problem types cold.
3. **Grokking the Java Interview** (Javin) — Java deep-dive Q&A. Unit: answer core Java interview questions (OOP, JVM, collections, multithreading, Spring) without notes.
4. **Spring Start Here** (Laurentiu) — enterprise Java without Spring is not enterprise Java. Unit: explain DI / IoC / Beans / AOP / Spring-Boot auto-config + build one small REST endpoint.
5. **java_interview_prep.pdf** — the cheat sheet: skim before rounds, low effort high yield.

### TIER 2 — the MULTIPLIERS (start after spine ~50–70%, or 20 min/day parallel)
6. **Designing Data-Intensive Applications** (Kleppmann) — system-design depth. Unit: explain partitioning / replication / consensus + design one simple distributed system. SELECTIVE chapters — not 600 pages.
7. **Microservices Patterns in Java** (Chris Richardson) — enterprise microservices. Unit: explain core patterns (saga, CQRS, event-driven) for a Java shop.
8. **Dive Into Design Patterns** (Shvets) — Unit: know + draw the ~8 that come up (factory, builder, singleton, observer, strategy, decorator, adapter, composite).
9. **Effective Java** (Bloch) — cherry-pick the ~15 interview items (generics, immutability, enums, streams, concurrency items). NOT all 200.

### TIER 3 — the REFERENCE (read when a question hits, NEVER "finish")
10. **The Well-Grounded Java Developer** (Evans) — JVM / GC / collections internals.
11. **Building Microservices** (Newman) — architecture background.
12. **Java Concurrency and Parallelism** (Jay Wang) — concurrency depth (thread pools, JUC).
13. **The Pragmatic Programmer** — mindset/craft. Read in the MAINTENANCE phase, NOT the interview window.

### NOT A BOOK (but must-do)
- **Angular — course decision (2026-11-12):**
  - **Labex (user's link):** verified 11-12 — free labs exist (no credit card), full access **$99/yr** (~$0.30/day) — but Labex's strength is Linux/DevOps; Angular track is thin. **Verdict: optional interactive supplement, NOT the primary.**
  - **Primary (free):** **angular.dev** (official, current, interactive) + **The Net Ninja Angular playlist** (YouTube, systematic, complete).
  - **Paid fast-track (optional):** Daniel uboh — Complete Angular Course (Udemy, ~$15 on sale).
  - **Frontend basics first (wk 1–2, 30–60 min/day):** ES6+ JS (freeCodeCamp / MDN modern JS) + TypeScript crash + HTTP/fetch. He's a Java dev — types/OOP are home turf; only the web specifics (DOM, async, HTTP, Angular CLI) are new. Don't over-fundament.
  - **Cadence:** 30–60 min/day from wk 2 — a 6–8 week DRIP, not a crash. Angular must not swallow the day.
- **The Angular project = the pipeline "guide UI" (Option A, recommended):** **AI Film Pipeline Command Center** — Angular dashboard + **Spring Boot REST API** layer over the ComfyUI pipeline (jobs, status, models, VRAM, logs, trigger generation). Incremental: (1) Spring Boot skeleton with JSON-backed endpoints (his home turf, 2–3 days), (2) Angular UI (dashboard / job list / status), (3) real pipeline wiring (status from ComfyUI, log streaming). **NOT a third life — a layer ON TOP of the existing 2-h pipeline block** (the "guide UI" he already wanted). Option B (fallback): **"Interview Prep Tracker"** — Angular + Spring Boot + DB tracking his own NeetCode 150 (simpler, meta, still full-stack).
- **Order (user asked "how?"):** basics (wk 1–2) → project, learning Angular *inside* it → **backend FIRST** (his home turf) so there's a real API to build against.
- **AI** — the film pipeline IS it. No book needed.

## SPRING/JAVA DEPTH — "I KNOW THE HOW, NOT THE WHY" (user, 2026-11-12)
**Diagnosis:** 5 yrs of working *under* the patterns (ControllerAdvice, clean controllers, Splunk error logs, caching under overload, manager-worker arch) but "no in-depth knowledge of WHY and HOW." Senior/GCC/Europe interviews probe the why. **This is NOT "learn Spring" — it's converting "worked under it" → "can explain it."**
**The exercise (1 page per pattern, 20 min/day, one pattern/week):**
1. **WHY** — what problem it solves; the naive alternative; why the alternative is worse.
2. **HOW IT WORKS** — the internal mechanism.
3. **Interview Q + 30-second answer.**
**Worked example — ControllerAdvice:** WHY: exception handling is cross-cutting; try-catch in every controller = duplication + controllers polluted with non-business code. HOW: when an exception escapes a handler method, Spring's `HandlerExceptionResolver` chain runs in order; `ExceptionHandlerExceptionResolver` finds matching `@ExceptionHandler` methods in `@ControllerAdvice` beans, which are registered GLOBALLY across all handlers. Q: "Why @ControllerAdvice over try-catch in controllers?" → A (30 s): cross-cutting concern separation, DRY, testable in isolation, ONE place maps exception → HTTP status/body, controllers stay business-only.
**Queue:** ControllerAdvice (wk 1) → caching under load (Spring Cache = AOP proxy + CacheManager; why cache invalidation matters) → manager-worker (thread pools, backpressure, why not just new Thread) → Splunk logging (log4j/appender → file/HTTP → indexer → search; structured vs unstructured) → clean controllers (layering: controller → service → repository; why logic in controllers bites in tests/maintenance).
**Resources:** **Baeldung** (free — one under-the-hood article per pattern) + his own books (Spring Start Here / Well-Grounded / Effective Java) as reference. **Unit of success:** whiteboard the mechanism + answer the why in 60 seconds.

## GCC / EUROPE REMOTE REALITY (honest, 2026-11-12)
- **GCC is often RELOCATION / on-site, not remote-from-India** — many GCC roles mean "come to Dubai/Riyadh" (visa-sponsorship model). GCC-remote is a smaller pool than it looks.
- The purest "remote from Kerala, paid in hard currency" pool = **US-remote** (and some EU-remote).
- **Strategy:** apply to GCC + Europe AND US-remote for volume — don't only apply to GCC-remote.
- **OPEN QUESTION (user to confirm):** is GCC relocation-OK (can move), or remote-only? Relocation-OK opens a much bigger, better-paying pool.
- 5-yr exp + AI pipeline + full-stack = realistic senior/full-stack remote profile above 11 LPA.

## THIS WEEK (2026-11-12 → 11-18) — concrete
- **Day 1 (today, 11-12):** LeetCode account + NeetCode 150 tracker. Do the first **2–3 problems (arrays)**. **Decide the Angular project (Option A pipeline command center vs Option B prep tracker) + scaffold the Spring Boot skeleton** (his home turf — 1–2 h). Set the daily skeleton live (LIFE_PLAN.md).
- **Weeks 1–2:** JS/TS + HTTP basics, 30–60 min/day (freeCodeCamp / MDN / angular.dev getting-started).
- **Week 3:** Angular components *inside the project* — first Angular UI consuming the Spring Boot skeleton.
- **Daily:** Fajr → Quran 30 min · morning 2 h film pipeline (PENDING_ITEMS.md) · afternoon 1 NeetCode problem + Spring 20 min (the why/how pattern note) · 17:00 body (pushup ladder — 5 training days; Mon/Thu fasting = no training) · night: one-line review.
- **Spring why/how:** one pattern page/week — **this week: ControllerAdvice** (worked example above).
- **End-of-week-1 deliverable:** ~10 NeetCode problems + one small Spring REST endpoint (+ project skeleton) + ControllerAdvice why/how page.
- **Fasting days (Mon/Thu):** no training; Quran + NeetCode continue.

## "NOW OR NEVER" — honest frame (agent, 2026-11-12)
User: "i know this is a crucial spot of my life, its now or never… i keep living under my expectation." → **keep the urgency as FUEL, but the FLOOR carries the days.** "Now or never" is the old urgency engine — it spikes, then hides. The floor (one-line check-in) is what survives the valleys. Results lag input; the only daily question is "did I do today's one thing?" Anchor: "with god's grace."

## LINKS
- `LIFE_PLAN.md` — 4 pillars, timeline, frustration protocol, body clock.
- `PENDING_ITEMS.md` — film-pipeline pending tasks (the morning 2 h).
- Film pipeline = interview practice: system design + concurrency + Angular "guide" UI.
