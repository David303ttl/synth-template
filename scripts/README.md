# Scripts

This directory contains utility scripts for maintaining and configuring the project codebase.

## Overview

| Script | Language | Purpose |
|--------|----------|---------|
| `fix_code.sh` | Shell | Run nearly all fix scripts in sequence |
| `fix_file_comments.pl` | Perl | Update file header comments |
| `fix_header_guards.pl` | Perl | Fix header guard naming |
| `fix_namespace.pl` | Perl | Migrate namespaces |

---

## fix_code.sh

**Purpose**: Convenience script that runs `fix_header_guards.pl` and `fix_file_comments.pl` in sequence.

**Usage**:
```bash
./scripts/fix_code.sh
# or
sh scripts/fix_code.sh
```

**What it does**:
1. Updates header guards in all `.h` files
2. Updates file header comments in all source files

---

## fix_file_comments.pl

**Purpose**: Standardizes file header comments with copyright and license information.

**Usage**:
```bash
perl scripts/fix_file_comments.pl
```

**What it does**:
- Recursively processes all `.h` and `.cpp` files in `src/` and `tests/`
- Replaces existing header comments with the standard project header
- Applies `clang-format` to each file after processing

**File header format**:
```cpp
/*
 * Synth Template
 *
 * Based on SideQuest Starting Point by baconpaul, adopted by david.
 *
 * Copyright 2024-2026, David303ttl and Various authors, as described in the github
 * transaction log.
 *
 * This source repo is released under the MIT license, but has
 * GPL3 dependencies, as such the combined work will be
 * released under GPL3.
 *
 * The source code and license are at https://github.com/David303ttl/synth-template
 * Original template at https://github.com/baconpaul/sidequest-startingpoint
 */
```

**Note**: Edit the `$header` variable in the script to change the default header text.

---

## fix_header_guards.pl

**Purpose**: Standardizes C++ header guard naming across the project.

**Usage**:
```bash
perl scripts/fix_header_guards.pl
```

**What it does**:
- Recursively processes all `.h` files in `src/` and `tests/`
- Converts file path to a header guard name
- Replaces `#pragma once` with proper `#ifndef`/`#define`/`#endif` guards
- Updates existing `#ifndef`/`#define` guards to use the new naming scheme

**Naming convention**:
- Converts file path like `src/engine/voice.h` to `DAVID303TTL_SYNTH_ENGINE_VOICE_H`
- Format: `{NAMESPACE}_{PROJECT}_{PATH_WITH_UNDERSCORES}_H`

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

**Note**: The namespace prefix (`DAVID303TTL_SYNTH`) is hardcoded in the script. Modify line 32 to change it.

---

## fix_namespace.pl

**Purpose**: Universal namespace migration tool. Detects current namespaces and converts them to new names.

**Usage**:
```bash
# Interactive mode (prompts for both namespaces)
perl scripts/fix_namespace.pl

# Change first namespace only
perl scripts/fix_namespace.pl yourname

# Change both namespaces
perl scripts/fix_namespace.pl yourname yourproject
```

**What it does**:
- Auto-detects the current two-level namespace structure (e.g., `david303ttl::synthtemplate`)
- Replaces namespace declarations: `namespace oldname {` → `namespace newname {`
- Replaces namespace references: `oldname::subname::` → `newname::subname::`
- Updates namespace aliases: `namespace alias = oldname::...` → `namespace alias = newname::...`
- Updates plugin ID in `src/engine/patch.h`
- Fixes multi-level namespace closing braces (puts each brace on its own line)

**Examples**:

```bash
# Detect current namespace and change first level
perl scripts/fix_namespace.pl yourname
# Changes: david303ttl::synthtemplate → yourname::synthtemplate

# Change both namespace levels
perl scripts/fix_namespace.pl myname myproject
# Changes: david303ttl::synthtemplate → myname::myproject
```

**What gets changed**:

| Pattern | Example Transformation |
|---------|------------------------|
| Namespace declaration | `namespace david303ttl {` → `namespace yourname {` |
| Namespace declaration | `namespace synthtemplate {` → `namespace myproject {` |
| Namespace reference | `david303ttl::synthtemplate::` → `yourname::myproject::` |
| Closing comment | `} // namespace david303ttl` → `} // namespace yourname` |
| Plugin ID | `org.david303ttl.synthtemplate` → `org.yourname.myproject` |
| Namespace alias | `namespace bpss = david303ttl::...` → `namespace bpss = yourname::...` |

**Files modified**: All `.h` and `.cpp` files in `src/` and `tests/` (typically ~20 files)

**After running**:
1. Review changes with `git diff`
2. Build to verify: `cmake --build build --config Release`
3. Test the plugin in your DAW

---

## Tips

1. **Always review changes** with `git diff` before committing
2. **Test build** after namespace migration to ensure everything compiles
3. **Backup** or commit your work before running these scripts on a production codebase
4. **Run `fix_code.sh`** after cloning to standardize the codebase

