# Garena / CODM Account Checker

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
