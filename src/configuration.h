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

#ifndef DAVID303TTL_SYNTH_CONFIGURATION_H
#define DAVID303TTL_SYNTH_CONFIGURATION_H

#include <stddef.h>
#include <cstdint>
#include <string>
#include <cstring>
#include <iostream>
#include "sst/plugininfra/version_information.h"
#include <fmt/core.h>

// Windows Debug Output Support
#ifdef _WIN32
    #include <windows.h>
    #include <sstream>

    struct DebugLogStream
    {
        std::ostringstream ss;
        template<typename T>
        DebugLogStream& operator<<(const T& val)
        {
            ss << val;
            return *this;
        }
        ~DebugLogStream()
        {
            OutputDebugStringA(ss.str().c_str());
            OutputDebugStringA("\n");
        }
    };
#endif

namespace david303ttl {
namespace synthtemplate {

static constexpr size_t blockSize{8};
static constexpr size_t maxVoices{128};

extern int debugLevel;

} // namespace synthtemplate
} // namespace david303ttl

inline std::string fileTrunc(const std::string &f)
{
    auto p = f.find(sst::plugininfra::VersionInformation::cmake_source_dir);
    if (p != std::string::npos)
    {
        return f.substr(p + strlen(sst::plugininfra::VersionInformation::cmake_source_dir) + 1);
    }
    return f;
}

// ===== DEBUG_LOG Macros =====
// Windows: Uses OutputDebugStringA - visible in Visual Studio Output window
// Non-Windows: Uses std::cout
// Works in VST3 plugins and DAWs without requiring a console
#ifdef _WIN32
    #define DEBUG_LOG(...) DebugLogStream() << fileTrunc(__FILE__) << ":" << __LINE__ << " " << __VA_ARGS__
#else
    #define DEBUG_LOG(...) std::cout << fileTrunc(__FILE__) << ":" << __LINE__ << " " << __VA_ARGS__ << std::endl
#endif

// Formatted log using fmt library
#ifdef _WIN32
    #define DEBUG_LOGFMT(...) DebugLogStream() << fileTrunc(__FILE__) << ":" << __LINE__ << " " << fmt::format(__VA_ARGS__)
#else
    #define DEBUG_LOGFMT(...) std::cout << fileTrunc(__FILE__) << ":" << __LINE__ << " " << fmt::format(__VA_ARGS__) << std::endl
#endif

// Error log with [ERROR] prefix
#ifdef _WIN32
    #define DEBUG_LOG_ERR(...) DebugLogStream() << fileTrunc(__FILE__) << ":" << __LINE__ << " [ERROR] " << __VA_ARGS__
#else
    #define DEBUG_LOG_ERR(...) std::cout << fileTrunc(__FILE__) << ":" << __LINE__ << " [ERROR] " << __VA_ARGS__ << std::endl
#endif

// Unimplemented function log
#ifdef _WIN32
    #define DEBUG_LOG_UNIMPL DebugLogStream() << fileTrunc(__FILE__) << ":" << __LINE__ << " Unimplemented " << __func__
#else
    #define DEBUG_LOG_UNIMPL std::cout << fileTrunc(__FILE__) << ":" << __LINE__ << " Unimplemented " << __func__ << std::endl
#endif

// Log only once per call site
#define DEBUG_LOG_ONCE(...)                                                                        \
    do {                                                                                           \
        static bool x842132{false};                                                                \
        if (!x842132)                                                                              \
        {                                                                                          \
            DEBUG_LOG(__VA_ARGS__);                                                                \
        }                                                                                          \
        x842132 = true;                                                                            \
    } while(0)

// Debug variable printer - outputs both name and value: " variable=value"
#define DEBUG_D(x) " " << #x << "=" << x

// ===== Legacy aliases (deprecated) =====
#define SQLOG(...) DEBUG_LOG(__VA_ARGS__)
#define SQLOGFMT(...) DEBUG_LOGFMT(__VA_ARGS__)
#define SQLOG_ERR(...) DEBUG_LOG_ERR(__VA_ARGS__)
#define SQLOG_UNIMPL DEBUG_LOG_UNIMPL
#define SQLOG_ONCE(...) DEBUG_LOG_ONCE(__VA_ARGS__)
#define SQD(x) DEBUG_D(x)

#endif // CONFIGURATION_H
