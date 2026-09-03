# Next.js + Prisma Operations Reference

A working reference for building, migrating and deploying a Next.js app backed by
Prisma and PostgreSQL, running on EC2 under PM2.

Every command here is one I've actually needed. The value isn't the commands
themselves — those are in the docs — it's the ordering, and knowing which failure
each one fixes. Prisma and Next both cache aggressively in ways that produce errors
pointing nowhere near the actual cause.

## Deploy: pull to live

The full sequence for shipping a change to the server:

```bash
git pull
npx prisma generate
npx prisma format
npx prisma migrate deploy      # deploy, not `migrate dev` — see below
npm run build
pm2 restart pes_website        # by name, not by index
git add .
git commit -m 'auto commit after successful site build'
git push
```

Migrations run before the build because Next.js executes Server Components at build
time — if the schema and the client disagree, the build fails rather than the app.

Two things worth being deliberate about here:

- **`migrate deploy`, not `migrate dev`, on a server.** `migrate dev` can decide the
  database has drifted and offer to reset it, which on production means dropping
  every table. `deploy` only applies migrations that already exist and will never
  alter the schema on its own.
- **Restart PM2 by name, not by index.** `pm2 restart 0` restarts whatever happens
  to be first in the process list. Add a second app and that stops being the one
  you meant.

---

Create Next.js app
npx create-next-app@latest pes_website
cd pes_website

Creates the Next.js project scaffold.

Install Prisma
npm install prisma @prisma/client

Adds Prisma CLI + client.

Initialize Prisma
npx prisma init

Creates:

prisma/schema.prisma

.env (for DATABASE_URL)

🔄 Environment & Dependency Management
Install dependencies
npm install

Installs everything in package.json.

Update dependencies
npm update

Updates dependencies within allowed versions.

Upgrade Prisma (CLI + Client together!)
npm install prisma@latest @prisma/client@latest

⚠️ Always upgrade both at the same time.

Check Prisma versions
npx prisma -v

Shows CLI + client versions (must match major version).

🧱 Prisma Schema & Database
Generate Prisma client
npx prisma generate

Reads:

schema.prisma

prisma.config.ts
Generates the DB client.

Run this whenever:

schema changes

Prisma version changes

client breaks

Create a migration
npx prisma migrate dev --name add_products

Creates SQL migration

Applies it to DB

Regenerates Prisma client

Use during development.

Apply migrations (prod / EC2)
npx prisma migrate deploy

Applies existing migrations only.
Never modifies schema.

Reset database (⚠️ DESTRUCTIVE)
npx prisma migrate reset

Drops DB

Recreates schema

Reruns migrations

Regenerates client

Use only in dev.

Open Prisma Studio (DB GUI)
npx prisma studio

Web UI to inspect/edit DB rows.

🧪 Local Development
Start dev server
npm run dev

Hot reload

Fast feedback

Uses .env

Run type checking
npm run lint

Catches TypeScript + ESLint issues.

🏗️ Build & Production
Build project
npm run build

Compiles Next.js

Executes Server Components

Runs Prisma at build time

If this passes, prod will work.

Start production server (no PM2)
npm start

Runs the built app.

🚀 EC2 + PM2 (Production)
Install PM2 globally
npm install -g pm2
Start app with PM2
pm2 start npm --name "pes_website" -- start
Restart app
pm2 restart pes_website
Stop app
pm2 stop pes_website
View logs
pm2 logs pes_website
Persist PM2 across reboots
pm2 startup
pm2 save
🧹 Clean / Rebuild (VERY IMPORTANT)
Clean generated artifacts
rm -rf .next
rm -rf node_modules/.prisma

Fixes:

Prisma engine errors

Next build cache bugs

Full rebuild (safe)
rm -rf .next node_modules/.prisma
npm install
npx prisma generate
npm run build
🔁 Common Scenarios (Quick Recipes)
🔄 “Recreate project from scratch”
rm -rf node_modules .next
npm install
npx prisma generate
npm run build
🛠️ “Schema changed, update DB + app”
npx prisma migrate dev
npm run build
🔥 “Prisma is acting weird”
rm -rf node_modules/.prisma
npx prisma generate
🚨 “Build fails but dev works”
export NODE_ENV=production
npm run build

Build runs server components at build time.

🌍 Environment Variables
Load .env

Automatically loaded by:

npm run dev

npm run build

pm2 start

Test env vars manually
printenv DATABASE_URL
🧭 Mental Model (save this)

Dev → npm run dev

Schema change → prisma migrate dev

Prod deploy → npm run build → pm2 restart

Weird Prisma error → delete .prisma + regenerate

Weird Next error → delete .next