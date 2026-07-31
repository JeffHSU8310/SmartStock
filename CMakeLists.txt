cmake_minimum_required(VERSION 3.20)
project(TaiwanSmartQuant VERSION 1.0.0 LANGUAGES CXX)

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

add_executable(TaiwanSmartQuant ${SOURCES})

# Windows UTF-8 設定
if(MSVC)
    target_compile_options(TaiwanSmartQuant PRIVATE /utf-8)
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(TaiwanSmartQuant PRIVATE -Wall -Wextra)
endif()
