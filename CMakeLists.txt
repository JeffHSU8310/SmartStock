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

# 靜態連結 C++ 標準庫與 GCC 運行庫，消除 DLL 相依性與「無法找到程序輸入點」錯誤
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(TaiwanSmartQuant PRIVATE -Wall -Wextra)
    target_link_options(TaiwanSmartQuant PRIVATE -static -static-libgcc -static-libstdc++ -pthread)
elseif(MSVC)
    target_compile_options(TaiwanSmartQuant PRIVATE /utf-8)
endif()
