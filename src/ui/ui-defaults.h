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

#ifndef DAVID303TTL_SYNTH_UI_UI_DEFAULTS_H
#define DAVID303TTL_SYNTH_UI_UI_DEFAULTS_H

#include "configuration.h"
#include <sst/plugininfra/userdefaults.h>

namespace david303ttl::synthtemplate::ui {
enum Defaults
{
    useLightSkin,
    zoomLevel,
    useSoftwareRenderer, // only used on windows
    numDefaults
};

inline std::string defaultName(Defaults d)
{
    switch (d)
    {
    case useLightSkin:
        return "useLightSkin";
    case zoomLevel:
        return "zoomLevel";
    case useSoftwareRenderer:
        return "useSoftwareRenderer";
    case numDefaults:
    {
        DEBUG_LOG("Software Error - defaults found");
        return "";
    }
    }
    return "";
}

using defaultsProvder_t = sst::plugininfra::defaults::Provider<Defaults, Defaults::numDefaults>;
} // namespace david303ttl::synthtemplate::ui

#endif // UI_DEFAULTS_H
