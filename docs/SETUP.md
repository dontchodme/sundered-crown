# SETUP — from zero to a working repo and a running app

Written for **Windows** (`yert`, win32 x64). macOS/Linux notes at the bottom.

If you have never used git before, the mental model is short: your project
lives in a folder on your PC. `git` records snapshots of that folder. GitHub
stores a copy of those snapshots online. `push` sends yours up, `pull` brings
changes down. That is the whole thing.

---

## 1. Put the folder somewhere permanent

Unzip `sundered-crown-repo.zip` to a path with **no spaces and no OneDrive**.
Spaces break command-line tools in ways that are annoying to debug; OneDrive
syncs half-written files mid-render and corrupts them.

```
C:\dev\sundered-crown
```

The `.git` folder is inside the zip. That is the history — the first commit is
already made. Do not delete it.

---

## 2. Install git

Download from **https://git-scm.com/download/win** and run the installer.
Defaults are fine except one screen:

> **"Configuring the line ending conversions"** → choose
> **"Checkout as-is, commit as-is"**.

Not cosmetic. The default rewrites line endings on checkout, which changes the
bytes of every HTML build in `02-chain/`. Every hash in `MANIFEST.txt` would
stop matching and `engine_ab` would be comparing files git had edited.

Then, in a new PowerShell window:

```powershell
git --version
git config --global user.name  "Rick"
git config --global user.email "collinrose12@gmail.com"
```

---

## 3. Make the GitHub repo

1. Sign in at **https://github.com**.
2. Click **+** (top right) → **New repository**.
3. Name: `sundered-crown`
4. **Private** unless you want it public.
5. **Do not** tick "Add a README", "Add .gitignore", or "Choose a license" —
   the repo already has all three, and starting with files on GitHub's side
   makes the first push conflict.
6. **Create repository.**

GitHub then shows you a page of commands. Ignore them; use these instead,
because your history already exists locally.

```powershell
cd C:\dev\sundered-crown
git remote add origin https://github.com/YOUR-USERNAME/sundered-crown.git
git branch -M main
git push -u origin main
```

A browser window will open to authorise. That is normal and it happens once.

**Check it worked:** refresh the GitHub page. You should see `CLAUDE.md`,
`README.md`, and the folders — and **no** `.mp4`, **no** `kokoro-v1.0.onnx`.
If either of those is up there, stop and say so; getting a large file back out
of history is much harder than keeping it out.

---

## 4. Install Claude Code

Node 24 is already on this machine, so:

```powershell
npm install -g @anthropic-ai/claude-code
cd C:\dev\sundered-crown
claude
```

First run asks you to sign in. After that, **it reads `CLAUDE.md`
automatically** — which is the entire point of this move. No handoff, no zip,
no "here is where we left off". It opens already knowing.

---

## 5. Run the app

```powershell
cd C:\dev\sundered-crown\app
npm install
npm start
```

`npm install` pulls Electron once — about 150 MB, a minute or two.

You should get a window with the arena on the left and controls on the right.
The **Create short** and **Preview voice** buttons deliberately report which
phase they are waiting on rather than pretending to work.

### Then run the test that says Phase 1 actually worked

In the app: **Engine identity → Run 200 seeds**. Then:

```powershell
cd C:\dev\sundered-crown\tools
python3 shell_identity.py
```

It must print `PASS  200/200 identical`. That is the proof that the app runs
the same engine the video pipeline does — the whole reason this is Electron and
not Tauri. If it fails, the shell has changed the engine and nothing built on
top of it is trustworthy.

---

## 6. The rhythm, from here on

```powershell
git pull                              # start of every session
# ... work ...
git add -A
git commit -m "what changed, and what verified it"
git push                              # end of every session
```

If a commit changes the build of record, **name the verification in the
message** — which probes, at what count. A green claim with no run behind it is
worse than a red one.

---

## What you still need per-machine, and why it is not in the repo

```powershell
# the voiceover model — 353 MB, see tools/FETCH-KOKORO.md
cd C:\dev\sundered-crown\tools
curl.exe -L -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl.exe -L -o voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
pip install kokoro-onnx soundfile playwright
python -m playwright install chromium
```

`ffmpeg` must be on PATH — `winget install Gyan.FFmpeg` is the easy route.
(Phase 3 bundles it with the app so this stops being a requirement.)

These are gitignored on purpose: 353 MB of model in git history is 353 MB
nobody can ever delete, and it is byte-identical on every machine that
downloads it.

---

## macOS / Linux

Same steps. `brew install git ffmpeg` or your package manager; git's line-ending
default is already correct outside Windows, so step 2's warning does not apply.
Use `python3` and forward slashes throughout.
