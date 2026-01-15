/*
 * Synth Template
 *
 * Based on SideQuest Starting Point by baconpaul, adopted by David303ttl.
 *
 * Copyright 2024-2025, Paul Walker and contributors.
 * Copyright 2026, Pawel Marczak
 *
 * This source repo is released under the MIT license, but has
 * GPL3 dependencies, as such the combined work will be
 * released under GPL3.
 *
 * The source code and license are at https://github.com/David303ttl/synth-template
 * Original template at https://github.com/baconpaul/sidequest-startingpoint
 */

#include <clap/clap.h>
#include "plugin-clap-entry-impl.h"

extern "C"
{

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

    // clang-format off
    const CLAP_EXPORT struct clap_plugin_entry clap_entry = {
        CLAP_VERSION,
        david303ttl::synthtemplate::clap_init,
        david303ttl::synthtemplate::clap_deinit,
        david303ttl::synthtemplate::get_factory
    };
    // clang-format on
#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif
}