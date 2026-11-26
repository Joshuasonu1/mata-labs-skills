# MATA Labs skills

All MATA Labs Claude skills in one bundle: 23 skills + house rules. **Private repo.**

| File / folder | What it is |
|---|---|
| `SKILL.md` | Index of every skill (Claude reads it first when the bundle is uploaded as one skill) |
| `HOUSE_RULES.md` | Standing rules and project notes (speech cuts must finish sentences, who is who in DSk footage) |
| `<skill-name>/` | One folder per skill, each with its own `SKILL.md` |

---

## How to install

### Option 1: Claude Code on Windows (recommended)

Open **PowerShell** and run these one at a time.

**1. Download the repo** (Git asks you to sign in to GitHub once, because the repo is private):
```powershell
git clone https://github.com/Joshuasonu1/mata-labs-skills.git "$env:TEMP\mata-labs-skills"
```

**2. Make sure the skills folder exists:**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
```

**3. Copy every skill folder into it:**
```powershell
Get-ChildItem "$env:TEMP\mata-labs-skills" -Directory | Where-Object Name -ne '.git' | ForEach-Object { Copy-Item -Recurse -Force $_.FullName "$env:USERPROFILE\.claude\skills\" }
```

**4. Check (you should see 23 names):**
```powershell
Get-ChildItem "$env:USERPROFILE\.claude\skills" -Directory | Select-Object Name
```

**5. Restart Claude Code.** The skills appear in the skills list; use them by name, e.g. `/polcomms-reels`.

> Step 3 copies only the skill folders, not the top-level `SKILL.md` index: Claude Code expects each skill in its own folder.

### Option 2: no Git on that computer

1. On this GitHub page click the green **Code** button → **Download ZIP**.
2. Unzip it.
3. Copy each skill folder (`polcomms-reels`, `reel-production-core`, …) into `C:\Users\<name>\.claude\skills\`.
4. Restart Claude Code.

### Option 3: claude.ai (web or phone)

1. Download this repo as ZIP (Option 2, step 1) and unzip it.
2. Rename the unzipped folder to `mata-labs-skills`, then zip that folder (right-click → **Send to → Compressed (zipped) folder**).
3. On claude.ai go to **Settings → Capabilities** and turn on **Code execution and file creation**.
4. Under **Skills** click **Upload skill** and pick `mata-labs-skills.zip`. All 23 skills arrive in one upload.

---

## Getting updates later

After new changes are pushed here, run this on the other computer, then repeat step 3 of Option 1:
```powershell
git -C "$env:TEMP\mata-labs-skills" pull
```

For claude.ai, re-zip and upload again to replace the old version.

## Updating this repo (from the main computer)

**Automatic.** On the main computer a Claude Code `Stop` hook (`~/.claude/settings.json` → `~/.claude/hooks/sync_skills.py`) runs after every Claude turn. If any skill in `C:\Users\hello\.claude\skills\` changed, it copies the skills into this repo (`~/.claude/skills-repo`), rebuilds the `SKILL.md` index, commits "Auto-sync skills: <names>", pushes here, and refreshes `Downloads\claude-skills-backup\mata-labs-skills.zip`. If nothing changed it does nothing. Log: `~/.claude/hooks/sync_skills.log`.

**Deletions are never synced.** If a skill (or the whole skills folder) is deleted on the computer, it stays here on GitHub. To remove a skill from GitHub, delete it here by hand.

To push by hand, run `python -I "$HOME/.claude/hooks/sync_skills.py"`, or ask Claude Code to "push the skills to GitHub".
