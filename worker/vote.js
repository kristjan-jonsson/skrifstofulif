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
