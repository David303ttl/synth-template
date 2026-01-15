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

#ifndef DAVID303TTL_SYNTH_UI_MAIN_PANEL_H
#define DAVID303TTL_SYNTH_UI_MAIN_PANEL_H

#include "sst/jucegui/components/NamedPanel.h"
#include "patch-data-bindings.h"
#include "plugin-editor.h"

namespace david303ttl {
namespace synthtemplate {
namespace ui {
struct MainPanel : sst::jucegui::components::NamedPanel
{
    MainPanel(PluginEditor &editor);
    void resized() override;

    std::vector<std::unique_ptr<sst::jucegui::components::Knob>> knobs;
    std::vector<std::unique_ptr<PatchContinuous>> knobAs;

    PluginEditor &editor;

    void beginEdit() {}
    void endEdit() {}
};
} // namespace ui
} // namespace synthtemplate
} // namespace david303ttl
#endif // MAIN_PANEL_H
