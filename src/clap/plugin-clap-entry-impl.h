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

#ifndef DAVID303TTL_SYNTH_CLAP_PLUGIN_CLAP_ENTRY_IMPL_H
#define DAVID303TTL_SYNTH_CLAP_PLUGIN_CLAP_ENTRY_IMPL_H

namespace david303ttl::synthtemplate {
const void *get_factory(const char *factory_id);
bool clap_init(const char *p);
void clap_deinit();
} // namespace david303ttl::synthtemplate

#endif
