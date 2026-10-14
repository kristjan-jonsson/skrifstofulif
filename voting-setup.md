# Voting setup: 👍/👎 on comics, stored in GitHub

## Why
The site is static GitHub Pages (`index.html` + `comics.json`), so a browser can't write to the repo on its own: anything that writes needs a GitHub token, and a token in the page would be public. A small **Cloudflare Worker** (free tier) solves this:
1. It keeps the token as a secret.
2. It forwards each vote to GitHub as a `repository_dispatch` event.
3. A GitHub Action handles the event and commits the updated counts to `votes.json` on a separate `votes` branch.

```
browser ──POST {id, vote}──▶ Cloudflare Worker ──repository_dispatch──▶ GitHub Action
                                                                          │ jq: votes[id][vote]++
                                                                          ▼ commit → branch `votes`
browser ◀── GET raw.githubusercontent.com/kristjan-jonsson/skrifstofulif/votes/votes.json
```

Format of `votes.json`: `{ "2026-10-13": { "up": 3, "down": 1 } }`. The key is `c.id || c.date`, which is the same `key()` that `index.html` already uses.

Why a separate `votes` branch:
- Your local `main` is never behind, so `git push` keeps working without pulling first.
- The comic history stays clean.
- Commits made by the Action's built-in token don't trigger `pages.yml`, so there's no redeploy for each vote.

---

## Part A: Creating the Cloudflare Worker (step by step)

### A1. Cloudflare account
1. Sign up for free at https://dash.cloudflare.com/sign-up.
2. Open **Workers & Pages** once. Cloudflare will ask you to pick a `*.workers.dev` subdomain, for example `kristjan`. Your Worker's URL will then be `https://skrifstofulif-vote.kristjan.workers.dev`.

### A2. GitHub token (fine-grained PAT)
1. Go to https://github.com/settings/personal-access-tokens/new.
2. Fill in the form:
   - **Name:** `skrifstofulif-vote`
   - **Expiration:** 1 year. Set a calendar reminder to renew it.
   - **Repository access:** *Only select repositories* → `skrifstofulif`.
   - **Permissions → Repository → Contents:** *Read and write*. This is what `repository_dispatch` needs. Metadata: read is added automatically.
3. Copy the token (`github_pat_…`). You'll paste it in step A5, and never into code.

### A3. Worker code in the repo
I'll create two files in a `worker/` folder.

`worker/wrangler.toml`
```toml
name = "skrifstofulif-vote"
main = "vote.js"
compatibility_date = "2025-09-01"

[vars]
ALLOWED_ORIGIN = "https://skrifstofulif.oskasteinar.is"
```

`worker/vote.js`
```js
const REPO = 'kristjan-jonsson/skrifstofulif';
const ID_RE = /^\d{4}-\d{2}-\d{2}(-\d+)?$/;
const VOTES = ['up', 'down'];

export default {
  async fetch(request, env) {
    const origin = env.ALLOWED_ORIGIN;
    const cors = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });
    if (request.headers.get('Origin') !== origin) return new Response('Forbidden', { status: 403 });

    let body;
    try { body = await request.json(); } catch { body = null; }
    const id = body && body.id;
    const vote = body && body.vote;
    if (typeof id !== 'string' || !ID_RE.test(id) || !VOTES.includes(vote)) {
      return new Response('Bad request', { status: 400, headers: cors });
    }

    const res = await fetch(`https://api.github.com/repos/${REPO}/dispatches`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'skrifstofulif-vote',
      },
      body: JSON.stringify({ event_type: 'vote', client_payload: { id, vote } }),
    });
    if (!res.ok) console.log('GitHub dispatch failed', res.status, await res.text());
    return new Response(null, { status: res.ok ? 204 : 502, headers: cors });
  },
};
```

I'll also add `worker/.dev.vars` and `.wrangler/` to `.gitignore`, so a local token never gets committed.

### A4. Log in with Wrangler (the Cloudflare CLI, run via npx, no install needed)
```bash
cd worker
npx wrangler login        # opens the browser; approve access
```

### A5. Deploy, then add the secret
```bash
npx wrangler deploy                    # prints the URL: https://skrifstofulif-vote.<subdomain>.workers.dev
npx wrangler secret put GITHUB_TOKEN   # paste the github_pat_… token when prompted
```
The secret takes effect immediately, with no redeploy. You can see it under Dashboard → Workers & Pages → skrifstofulif-vote → Settings → Variables and Secrets.

### A6. Test the Worker
```bash
URL=https://skrifstofulif-vote.<subdomain>.workers.dev
# Should return 204:
curl -i -X POST "$URL" -H 'Origin: https://skrifstofulif.oskasteinar.is' \
     -H 'Content-Type: application/json' -d '{"id":"2026-10-13","vote":"up"}'
# Should return 403 (wrong origin) and 400 (bad id):
curl -i -X POST "$URL" -H 'Origin: https://evil.example' -d '{"id":"2026-10-13","vote":"up"}'
curl -i -X POST "$URL" -H 'Origin: https://skrifstofulif.oskasteinar.is' -d '{"id":"x; rm -rf","vote":"up"}'
```
- A 204 means GitHub accepted the event. It only *does* anything once `vote.yml` is on `main` (Part B), because `repository_dispatch` only runs workflows on the default branch.
- If you get a 502, run `npx wrangler tail` to see GitHub's error. It's usually a token with the wrong repo or permission.

### A7. Local development (optional)
1. Create `worker/.dev.vars`, which is gitignored:
   ```
   GITHUB_TOKEN=github_pat_...
   ALLOWED_ORIGIN=http://localhost:8000
   ```
2. Run `npx wrangler dev`. This starts the Worker on `http://localhost:8787`.
3. Serve the site with `python3 -m http.server 8000` from the repo root.

---

## Part B: GitHub Action `.github/workflows/vote.yml` (new)
- Triggers on `repository_dispatch: types: [vote]`, with `permissions: contents: write`.
- `client_payload.id` and `.vote` go in through `env:` and are never interpolated into `run:`, which prevents script injection. The step validates them again with the same regex and the up/down check.
- Checks out the `votes` branch, or creates it as an orphan branch with `{}` if it doesn't exist yet.
- Runs `jq --arg id "$ID" --arg v "$VOTE" '.[$id][$v] = ((.[$id][$v] // 0) + 1)'`, then commits as github-actions[bot].
- Pushes in a **retry loop**: `git pull --rebase` and push, up to 5 times, re-applying the increment on conflict. I'm not using a concurrency group, because GitHub drops extra pending runs in a group, which would lose votes.

## Part C: `index.html` (edit)
- A vote row inside `#strip`, under the image, with two buttons:
  - `👍 <n>` labelled "Fyndið"
  - `👎 <n>` labelled "Ekki fyndið"
  - Both use the existing `.btn` class and `aria-pressed`.
- A `VOTE_URL` constant holds the Worker URL from step A5.
- On load, fetch `https://raw.githubusercontent.com/kristjan-jonsson/skrifstofulif/votes/votes.json` with `cache: 'no-cache'`. If that fails, show no counts.
- `show(i)` updates the counts and button state for the current comic.
- On click:
  - Send the POST.
  - Increment the shown count right away.
  - Store `vote:<key>` in `localStorage`, wrapped in try/catch.
  - Disable both buttons for that comic and mark the one that was chosen.
- The real count lags by about 1–5 minutes, because of the Action run and raw-CDN caching.

## Part D: `README.md`
Add a short Icelandic section: how voting works, where the counts are (the `votes` branch), and a link to `voting-setup.md`.

## Limitations (on purpose)
- Votes are one per comic per browser, enforced only by localStorage, so it's easy to cheat. That's fine for office fun.
- The Origin check only stops browsers. `curl` can fake the Origin header.
- A vote can't be changed after it's cast.
- There's no rate limiting beyond Cloudflare's defaults. Free tier: 100k requests per day.
- The PAT expires, so remember to renew it.

## Steps you do yourself
A1, A2, A4 and A5: the account, the token, logging in and the deploy. Then you put the Worker URL into `VOTE_URL` (or give it to me), and you push. I commit but never push.

## Verification
1. Run the A6 curl tests and get 204, 403 and 400.
2. Once `vote.yml` is on `main`: run the curl again, then check that a "vote" run appears under the Actions tab and the `votes` branch has `{"2026-10-13":{"up":1}}`.
3. Fire 5 parallel curls and confirm all 5 are counted, which tests the retry loop.
4. On the page: click 👍 and confirm that:
   - the count goes up and the buttons are disabled;
   - after a reload, the vote is still remembered;
   - another comic has its own state.
