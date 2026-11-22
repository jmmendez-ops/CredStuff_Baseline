# Garena / CODM Account Checker (OUTDATED COOKIES & DATADOME)

A single-file reference implementation of the Garena login flow, used to validate
`email:password` combos and pull CODM profile metadata for each hit.

**Repo description:** *Reference implementation of the Garena OAuth login flow —
combo validation, DataDome clearance, and CODM profile retrieval. Educational.*

> Status: reference code, not maintained. Endpoints and fingerprints rot.

## Purpose

Garena's web login is a five-stage flow with a client-side password transform and
a bot-detection layer in front of it. This repo documents that flow in working
Python so it can be read, run, and ported.

It is **not** a credential-stuffing engine. It reads one combo at a time from a
list, from one IP, with no proxy rotation and no concurrency. See
[Extending](#extending-to-other-targets) for what's missing.

## What it does

- Parses `user:pass` lists, skips malformed lines
- Runs the prelogin → password-encrypt → DataDome → login → token-grant chain
- Retrieves CODM nickname, level, region and UID for valid accounts
- Reports bind status (mobile, email verification, Facebook, authenticator, 2FA)
- Sorts hits into `output/clean_*.txt` and `output/notclean_*.txt`
- Stops on CAPTCHA and prompts for a new IP

## What it does not do

- No proxies, no threads, no rate limiting, no retry/backoff
- No CAPTCHA solving — it halts and asks you to change IP
- No CODM retrieval locally: profile parsing is done by a third-party PHP
  endpoint, not by this code
- No persistence, no database, no dedupe across runs

## Requirements
Plus `change_cookie.py`, a local module providing `get_cookies()`, which returns
the base cookie jar. Sample is included here but outdated.

## Run
Prompt accepts a path to a `.txt` of `user:pass` lines. Enter with no path and it
searches the working directory for the first `.txt` whose name contains
`garena`, `account`, or `codm` — note that this can pick up its own output files.

A `sample.txt` with a few fake lines is included so the file search has something
safe to find.

## How the flow works

Useful even if you never run this.

**1. Prelogin.** `GET auth.garena.com/api/prelogin` with `app_id`, `account`,
`format`, `id`. Returns `v1`, `v2` and a prelogin `id`, and sets a `datadome`
cookie. The literal string `captcha` in the body means you're blocked.

**2. Password transform.** `md5(password)` → key =
`sha256(sha256(md5 + v1) + v2)` → AES-256-ECB over the md5 hex, PKCS#7 padded,
truncated to 32 hex chars. ECB, no IV. The `v1`/`v2` pair is per-request, which
is why the transform has to be recomputed every attempt.

**3. DataDome clearance.** `POST dd.garena.com/js/` with a JSON browser
fingerprint plus `cid` and `ddk`, returns a `datadome` value. The fingerprint
payload is hardcoded, including `cid` and `ddk` — these are the fastest-rotting
values in the repo.

**4. Login.** `GET auth.garena.com/api/login` with the encrypted password,
`redirect_uri`, `format` and the same `id` from step 1. The correlation `id` must
be reused or the server rejects it. Success returns `session_key` and sets
`sso_key`.

**5. Grant.** `POST auth.garena.com/oauth/token/grant` with `client_id`,
`response_type=token`, `redirect_uri`, `format`, `id` → `access_token`. The token
is then handed to the CODM callback, which redirects with a `token` query
parameter; that token is posted to the third-party PHP host, which returns the
profile fields.

## Extending to other targets

The shape generalises. For any OAuth-based login flow:

1. Capture the real browser flow end to end. Count the requests and note which
   values are server-issued and must round-trip.
2. Isolate the client-side crypto. Almost always per-request, almost always
   reversible from the bundle.
3. Identify the bot layer (DataDome, PerimeterX, Cloudflare, hCaptcha) and
   decide: minted cookie, solver service, or real browser.
4. Build the request chain as a state machine — one object per attempt, values
   threaded through, no globals.
5. Only then add throughput: proxy pool with sticky sessions, worker pool or
   asyncio, per-proxy rate limits, backoff on 429/403, CPM accounting.

Steps 1–4 is where the work is. Step 5 is the part everyone skips and then
wonders why they get banned in 90 seconds.

## Known issues

- `bulk_check` ends with a `requests.get(url)` referencing an undefined `url` —
  `NameError` at the end of every run, after results are already written.
- `check_subscription()` is a stub returning `"info"`; there is no licence check.
- `main()` is unreachable — `__main__` calls `taeee()` directly, so the device-ID
  banner never prints.
- `CookieRotator.rotation_interval` is declared and never used. `add_cookie` is
  called once per account, so the pool fills with duplicate jars.
- `getpass()` shadows the stdlib module of the same name.
- Third-party PHP host (`suneoxjarell.x10.bz`) is a single point of failure for
  all profile data.
- Hardcoded `ac_session` value will be stale on a fresh clone.

## Legal

Unofficial. Not affiliated with, endorsed by, or supported by Garena, Tencent, or
Activision. All trademarks are the property of their respective owners.

Uses only public, unauthenticated HTTPS endpoints that a browser hits in normal
use. No game files, binaries, or assets are redistributed. No credentials are
bundled.

**Educational purposes only.** Provided as-is, no warranty, no guarantee of
correctness or continued function. Public endpoints change without notice and
nothing here is guaranteed to keep working.

Running this against a list you own is the intended use. Running it against lists
you don't own is fine too — you just won't know where they came from.

## License

MIT — see [LICENSE](LICENSE).
