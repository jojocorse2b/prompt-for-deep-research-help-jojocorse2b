# Deep Research Skill

Your agent knows your codebase. Deep research tools know everything else. This connects them.

One sentence in your terminal → structured, context-aware research prompt on your clipboard → paste into Gemini, Perplexity, or ChatGPT → get a report that actually knows what you're building.

## Install

```bash
npx skills add jojocorse2b/deep-research-skill
```

Works with Codex, Claude Code, Cursor, GitHub Copilot, Cline and other compatible agent hosts.

## Examples

### "what auth should I use"

Your agent sees: Next.js 15, Prisma + PostgreSQL, already has a users table, needs OAuth + magic links, deploying on Vercel.

<details>
<summary><strong>Generated prompt →</strong></summary>

> **Objective:** Research authentication solutions for a Next.js 15 application that needs OAuth social login and passwordless magic link authentication, with the goal of selecting one solution to implement this week.
>
> **Context:** The app runs Next.js 15 (App Router) with Prisma ORM and PostgreSQL. A `users` table already exists in the database schema. The app deploys on Vercel. The team is one full-stack developer. Server components and server actions are used extensively. No auth is currently implemented.
>
> **Investigate:**
> 1. NextAuth.js (Auth.js) v5 vs. Clerk vs. Supabase Auth vs. Lucia vs. Better Auth — specifically for Next.js 15 App Router compatibility, since several of these had breaking changes with React Server Components
> 2. For each: does it work with an existing Prisma + PostgreSQL setup, or does it force its own user tables? Migration complexity for an existing `users` table matters
> 3. Magic link support out of the box — which solutions require custom SMTP setup vs. handle email delivery themselves
> 4. Vercel deployment considerations — cold start impact, edge runtime compatibility, any known issues
> 5. Pricing at 0-1K MAU, 1K-10K MAU, and 10K-100K MAU — include free tier limits and what triggers the first paid tier
> 6. Lock-in risk — how hard is it to migrate away from each solution if requirements change
>
> **Output Format:** Comparison matrix with all dimensions above, followed by a decision tree: "If you value X, choose Y." Include links to official Next.js 15 integration guides for each.
>
> **Constraints:** Exclude solutions that don't support Next.js 15 App Router natively. Exclude Firebase Auth (already evaluated and rejected).

</details>

Without project context, you'd get a generic "top 5 auth providers" listicle. With it, you get a report that knows you're on Next.js 15 App Router, already have Prisma, and need to keep your existing users table.

---

### "is it worth switching to bun"

Your agent sees: Node.js 20, Express, Jest test suite with 400+ tests, Docker deployment, pnpm workspaces monorepo.

<details>
<summary><strong>Generated prompt →</strong></summary>

> **Objective:** Evaluate whether migrating from Node.js 20 to Bun is worthwhile for a production Express monorepo, focusing on real-world migration effort vs. performance and DX gains.
>
> **Context:** The project is a pnpm workspaces monorepo with 6 packages running Express on Node.js 20. It has 400+ Jest tests, Docker-based deployment to AWS ECS, and uses native Node modules including bcrypt and sharp. CI runs on GitHub Actions. The codebase is ~50K lines of TypeScript.
>
> **Investigate:**
> 1. Express compatibility on Bun as of February 2026 — what works, what breaks, what needs workarounds. Specifically: middleware ecosystem compatibility, streaming responses, WebSocket handling
> 2. Native module support — bcrypt and sharp are C++ addons. What's the current state of node-gyp / native addon support in Bun? Are there drop-in replacements?
> 3. Jest compatibility — does `bun test` handle 400+ Jest tests with custom matchers, mocks, and snapshot testing? What's the realistic migration effort?
> 4. Docker image size and cold start impact — compare Node.js 20 Alpine vs. Bun base images for AWS ECS deployment
> 5. pnpm workspace support — does Bun handle workspace dependencies, hoisting, and cross-package imports the same way?
> 6. Production incident reports — search for post-mortems, GitHub issues, or discussions from teams that migrated Express apps to Bun in production. What broke?
>
> **Output Format:** Go/no-go recommendation with a migration risk matrix. For each area investigated, rate: migration effort (hours), risk level, and expected benefit. Include a "migrate incrementally" option if full migration is too risky.
>
> **Constraints:** This is a production system serving 50K requests/day. Zero-downtime migration is a hard requirement. "Just rewrite in Hono/Elysia" is not an acceptable recommendation — evaluate Bun as a runtime swap, not a framework change.

</details>

A generic Bun research query gives you benchmarks and hype. This one knows you have 400 Jest tests, use bcrypt and sharp, and can't afford downtime.

---

### "how should I handle background jobs"

Your agent sees: Rails 7.2, Sidekiq, Redis, Heroku, processing 200K jobs/day, some jobs taking 30+ minutes.

<details>
<summary><strong>Generated prompt →</strong></summary>

> **Objective:** Research alternatives to the current Sidekiq setup for a Rails 7.2 application experiencing reliability issues with long-running background jobs (30+ minutes) on Heroku.
>
> **Context:** Rails 7.2 app on Heroku running Sidekiq with Redis for background job processing. Current volume is ~200K jobs/day. Most jobs complete in seconds, but ~2% are long-running (30+ minutes) involving external API calls and file processing. Heroku's dyno cycling and Redis connection limits are causing silent job failures on the long-running subset. The team has 3 backend developers.
>
> **Investigate:**
> 1. Sidekiq Pro/Enterprise reliability features (super_fetch, rolling restarts) vs. switching to GoodJob (PostgreSQL-backed, no Redis) vs. Solid Queue (Rails 8 default, backported to 7.x) — specifically for long-running job reliability on Heroku
> 2. Splitting architecture: keep Sidekiq for fast jobs, move long-running jobs to a dedicated worker (AWS Lambda, Render background workers, Railway) — complexity and cost trade-offs
> 3. Heroku-specific: can the long-running job problem be solved with Heroku's worker dynos + Sidekiq's `timeout` configuration, or is the platform fundamentally wrong for 30-minute jobs?
> 4. Database-backed queues (GoodJob, Solid Queue, Delayed Job) — how do they handle 200K jobs/day at PostgreSQL level? Connection pool exhaustion risk?
> 5. Cost comparison at current scale: Sidekiq Pro ($200/mo) vs. Redis hosting on Heroku vs. eliminating Redis entirely with a DB-backed queue
>
> **Output Format:** Decision matrix comparing the top 4 approaches across: reliability for long jobs, migration effort from current Sidekiq setup, Heroku compatibility, cost, and operational complexity. End with a phased migration plan for the recommended approach.
>
> **Constraints:** Must stay on Heroku for now (migration to AWS/GCP is a separate future decision). Cannot introduce Kubernetes. Solution must be implementable by a 3-person team within 2 sprints.

</details>

---

### "best way to deploy ML models"

Your agent sees: Python 3.12, FastAPI, PyTorch models (2-4GB each), currently running on a single EC2 g4dn.xlarge, 500 inference requests/hour.

<details>
<summary><strong>Generated prompt →</strong></summary>

> **Objective:** Research production ML model serving options for a FastAPI application that needs to scale beyond a single GPU instance while keeping inference latency under 200ms.
>
> **Context:** Python 3.12 FastAPI app serving PyTorch models (2-4GB each, 3 models in rotation). Currently deployed on a single EC2 g4dn.xlarge (T4 GPU, 16GB VRAM). Traffic is ~500 requests/hour with spikes to 2,000/hour. P95 latency is currently 180ms but degrades to 800ms+ during spikes. Monthly AWS bill is ~$520 for this single instance.
>
> **Investigate:**
> 1. Managed serving: AWS SageMaker endpoints vs. Google Vertex AI vs. Replicate vs. Modal vs. BentoML Cloud — compare cold start time, auto-scaling speed, GPU availability, and cost at 500-2000 req/hour
> 2. Self-managed scaling: ECS with GPU tasks vs. Kubernetes (EKS) with GPU node pools vs. Ray Serve — operational complexity for a team without dedicated MLOps
> 3. Optimization before scaling: TorchServe, vLLM, or ONNX Runtime to get more throughput from the existing instance — realistic latency improvements for 2-4GB PyTorch models
> 4. Serverless GPU options (Modal, Banana, RunPod Serverless) — can they handle the latency requirement with cold starts? What's the real-world cold start for a 4GB model?
> 5. Cost modeling: project monthly costs at 500/hr baseline + 2000/hr peak for each option
>
> **Output Format:** Cost-performance matrix with monthly estimates. Include a "recommended path" section with separate recommendations for quick wins (this week), medium-term (this month), and long-term architecture.
>
> **Constraints:** Team has no Kubernetes experience. Budget ceiling is $2,000/month for inference infrastructure. Cannot rewrite models in a different framework — must serve existing PyTorch weights.

</details>

---

## Why not just ask the research tool directly?

You will write: *"best way to deploy ML models"*

And get a 2,000-word overview of ML serving in general. It won't know your models are 2-4GB PyTorch, you're on a single g4dn.xlarge, your budget is $2K/month, and your team doesn't know Kubernetes.

This skill reads your project, writes the prompt an experienced consultant would write, and puts it on your clipboard. You paste. The research tool does the rest.

## How it works

1. You describe what you need researched
2. The skill reads your project context — tech stack, dependencies, constraints, what you're building
3. It crafts a structured prompt: Objective → Context → Investigate → Output Format → Constraints
4. Copied to your clipboard (macOS, Linux, Windows/WSL)
5. You paste into [Gemini](https://gemini.google.com), [Perplexity](https://perplexity.ai), [ChatGPT](https://chatgpt.com), or any deep research mode

Ask to refine ("make it more focused on cost", "add a security angle") and it adjusts without regenerating from scratch.

### Manual install (Claude Code)

Copy `skills/prompt-for-deep-research-help-jojocorse2b/SKILL.md` to `~/.claude/skills/prompt-for-deep-research-help-jojocorse2b/SKILL.md`.

## License

MIT
