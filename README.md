# Synth Template

A Windows-only synthesizer template based on SideQuest Starting Point by baconpaul.

## Setup Instructions

This template has been customized for **David303ttl**. To adapt it for your own project:

1. Clone this repository excluding the `.git` directory (e.g., `git clone --depth 1 <repo-url> my-project && rm -rf my-project/.git`)
2. Update the header in [scripts/fix_file_comments.pl](scripts/fix_file_comments.pl) with your info
3. Update the prefix in [scripts/fix_header_guards.pl](scripts/fix_header_guards.pl) for your project
4. Run the fix scripts:
   ```bash
   # First, run header guards and file comments
   ./scripts/fix_code.sh

   # Then, run the namespace script with your desired namespaces
   perl scripts/fix_namespace.pl yourname yourproject
   ```
   Replace `yourname` and `yourproject` with your desired namespace values (e.g., `perl scripts/fix_namespace.pl johndoe mysynth`).
5. Update project name and URLs in:
   - [CMakeLists.txt](CMakeLists.txt) - project name, PRODUCT_NAME, plugin ID
   - [.github/workflows/build-plugin.yml](.github/workflows/build-plugin.yml) - TARGET_NAME, PLUGIN_NAME, repository owner
6. Edit [resources/NightlyBlurb.md](resources/NightlyBlurb.md) and [resources/ReadmeZip.txt](resources/ReadmeZip.txt)
7. Create a new GitHub repo and push your code
8. Create a `Nightly` tag and enable write permissions for GitHub Actions
9. Build your synth!

## Build Platforms

**Windows-only** - CLAP, VST3, Standalone

### Requirements
- Windows 10 or later
- Visual Studio 2026 (MSVC)
- CMake 3.28 or later
- vcpkg for dependencies (or use provided pre-built libs)

### Building

```bash
# Configure with CMake
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=path/to/vcpkg/scripts/buildsystems/vcpkg.cmake

# Build
cmake --build build --config Release

# Output will be in build\synth-template_assets
```

## License

This source code is released under the MIT license, but has GPL3 dependencies, so the combined work is released under GPL3.

## Original Template

Based on [SideQuest Starting Point](https://github.com/baconpaul/sidequest-startingpoint) by baconpaul.
