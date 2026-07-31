cmake_minimum_required(VERSION 3.20)
project(TaiwanSmartQuant VERSION 3.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(src)

set(SOURCES
    src/data/storage_engine.cpp
    src/technical/indicators.cpp
    src/strategy/robot_selector.cpp
    src/backtest/backtest_engine.cpp
    src/notification/telegram_bot.cpp
    src/main.cpp
)

# 設為原生 WIN32 桌面軟體，完全隱藏 CMD 黑框終端機
add_executable(TaiwanSmartQuant WIN32 ${SOURCES})

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(TaiwanSmartQuant PRIVATE -Wall -Wextra -finput-charset=UTF-8 -fexec-charset=UTF-8)
    target_link_options(TaiwanSmartQuant PRIVATE -mwindows -static -static-libgcc -static-libstdc++ -pthread)
elseif(MSVC)
    target_compile_options(TaiwanSmartQuant PRIVATE /utf-8)
endif()
