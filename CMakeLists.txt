cmake_minimum_required(VERSION 3.28)

set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

string(TIMESTAMP DAY_OF_YEAR "%j")
string(TIMESTAMP YEAR "%Y")
math(EXPR PART0 "${YEAR}-2025 + 5")
math(EXPR PART1 "${DAY_OF_YEAR} + 1")

project(synth-template VERSION 0.${PART0}.${PART1} LANGUAGES C CXX)
set(PRODUCT_NAME "SynthTemplate")


option(USE_SANITIZER "Build and link with ASAN" FALSE)
option(COPY_AFTER_BUILD "Will copy after build" TRUE)

include(cmake/compile-options.cmake)

## New version
include(libs/sst/sst-plugininfra/cmake/git-version-functions.cmake)
version_from_versionfile_or_git()
message(STATUS "DISPLAY_VERSION=${GIT_IMPLIED_DISPLAY_VERSION}; COMMIT_HASH=${GIT_COMMIT_HASH}; BRANCH=${GIT_BRANCH}")


include(cmake/CmakeRC.cmake)
file(GLOB_RECURSE PATCHES  "resources/factory_patches/*.tsp")
cmrc_add_resource_library(${PROJECT_NAME}-patches NAMESPACE synth_patches ${PATCHES})

set(JUCE_PATH "${CMAKE_SOURCE_DIR}/libs/JUCE")
add_subdirectory(libs)

add_library(${PROJECT_NAME}-impl STATIC
        src/clap/plugin-clap.cpp
        src/clap/plugin-clap-entry-impl.cpp

        src/ui/plugin-editor.cpp
        src/ui/main-panel.cpp

        src/presets/preset-manager.cpp

        src/engine/engine.cpp
        src/engine/voice.cpp
        src/engine/patch.cpp

)
target_include_directories(${PROJECT_NAME}-impl PUBLIC src)
# Important setup variables
target_compile_definitions(${PROJECT_NAME}-impl PRIVATE
        PRODUCT_NAME="${PRODUCT_NAME}"
        PATCH_EXTENSION=".tsp"
)

if (WIN32)
    message(STATUS "Activating wchar presets")
    target_compile_definitions(${PROJECT_NAME}-impl PUBLIC USE_WCHAR_PRESET=1)
endif()

target_link_libraries(${PROJECT_NAME}-impl PUBLIC
        clap
)
target_link_libraries(${PROJECT_NAME}-impl PRIVATE
        simde
        clap-helpers clap-wrapper-extensions
        mts-esp-client
        fmt-header-only
        sst-basic-blocks sst-voicemanager sst-jucegui sst-cpputils
        sst-plugininfra
        sst-plugininfra::filesystem
        sst-plugininfra::tinyxml
        sst-plugininfra::strnatcmp
        sst-plugininfra::patchbase
        sst-plugininfra::version_information
        sst::clap_juce_shim sst::clap_juce_shim_headers
        ${PROJECT_NAME}-patches
)

make_clapfirst_plugins(
        TARGET_NAME ${PROJECT_NAME}
        IMPL_TARGET ${PROJECT_NAME}-impl

        OUTPUT_NAME "${PRODUCT_NAME}"

        ENTRY_SOURCE src/clap/plugin-clap-entry.cpp

        BUNDLE_IDENTIFER "org.david303ttl.synthtemplate"
        BUNDLE_VERSION ${PROJECT_VERSION}

        COPY_AFTER_BUILD ${COPY_AFTER_BUILD}

        PLUGIN_FORMATS CLAP VST3

        ASSET_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${PROJECT_NAME}_assets

        STANDALONE_CONFIGURATIONS
            standalone "${PRODUCT_NAME}" "org.david303ttl.synthtemplate"
)

add_subdirectory(tests)



