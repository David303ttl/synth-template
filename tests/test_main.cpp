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

#define CATCH_CONFIG_RUNNER
#include "catch2/catch2.hpp"

int main(int argc, char *argv[])
{
    int result = Catch::Session().run(argc, argv);

    return result;
}

// void *hInstance = 0;

TEST_CASE("Tests Exist", "[basics]")
{
    SECTION("Asset True") { REQUIRE(1); }
}
