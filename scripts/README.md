# Scripts

This directory contains utility scripts for maintaining and configuring the project codebase.

## Overview

| Script | Language | Purpose |
|--------|----------|---------|
| `fix_code.py` | Python | Run nearly all fix scripts in sequence |
| `fix_file_comments.py` | Python | Update file header comments |
| `fix_header_guards.py` | Python | Fix header guard naming |
| `fix_namespace.py` | Python | Migrate namespaces |

---

## fix_code.py

**Purpose**: Convenience script that runs `fix_header_guards.py` and `fix_file_comments.py` in sequence.

**Usage**:
```bash
python scripts/fix_code.py
```

**What it does**:
1. Updates header guards in all `.h` files
2. Updates file header comments in all source files

---

## fix_file_comments.py

**Purpose**: Standardizes file header comments with copyright and license information.

**Usage**:
```bash
python scripts/fix_file_comments.py
```

**What it does**:
- Recursively processes all `.h` and `.cpp` files in `src/` and `tests/`
- Replaces the leading header comment with the standard project header
- Runs `clang-format` if it is available on `PATH` (disable with `--no-format`)

---

## fix_header_guards.py

**Purpose**: Standardizes C++ header guard naming across the project.

**Usage**:
```bash
python scripts/fix_header_guards.py
```

**What it does**:
- Recursively processes all `.h` files in `src/` and `tests/`
- Converts file path to a header guard name
- Replaces `#pragma once` with proper `#ifndef`/`#define`/`#endif` guards
- Updates existing `#ifndef`/`#define` guards to use the new naming scheme

**Naming convention**:
- Converts file path like `src/engine/voice.h` to `DAVID303TTL_SYNTH_ENGINE_VOICE_H`
- Legacy behavior is: replace the first `src` path token with `david303ttl_synth` and then uppercase

**Example**:
```cpp
// Before:
#pragma once

// After:
#ifndef DAVID303TTL_SYNTH_ENGINE_VOICE_H
#define DAVID303TTL_SYNTH_ENGINE_VOICE_H
...
#endif // DAVID303TTL_SYNTH_ENGINE_VOICE_H
```

**Override the guard token**:
```bash
python scripts/fix_header_guards.py --src-token yourname_yourproject
```

---

## fix_namespace.py

**Purpose**: Universal namespace migration tool. Detects current namespaces and converts them to new names.

**Usage**:
```bash
# Change first namespace only (keeps second)
python scripts/fix_namespace.py yourname

# Change both namespace levels
python scripts/fix_namespace.py yourname yourproject
```

**What it does**:
- Auto-detects the current two-level namespace structure (e.g., `david303ttl::synthtemplate`)
- Replaces namespace declarations (both styles):
  - `namespace oldname {` → `namespace newname {`
  - `namespace oldname::oldproject {` → `namespace newname::newproject {`
- Replaces namespace references: `oldname::oldproject::` → `newname::newproject::`
- Updates namespace aliases: `namespace alias = oldname::...` → `namespace alias = newname::...`
- Updates plugin IDs like `org.oldname.oldproject` → `org.newname.newproject`

**After running**:
1. Review changes with `git diff`
2. Build to verify: `cmake --build build --config Release`
3. Test the plugin in your DAW

---

## Tips

1. **Always review changes** with `git diff` before committing
2. **Test build** after namespace migration to ensure everything compiles
3. **Backup** or commit your work before running these scripts on a production codebase
4. **Run `python scripts/fix_code.py`** after cloning to standardize the codebase

