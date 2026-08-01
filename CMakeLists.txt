cmake_minimum_required(VERSION 3.10)
project(SmartStockCore CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

file(GLOB_RECURSE SOURCES 
    "src/technical/*.cpp"
    "src/strategy/*.cpp"
    "src/backtest/*.cpp"
    "src/main.cpp"
)

add_library(smartstock_core SHARED ${SOURCES})

set_target_properties(smartstock_core PROPERTIES
    PREFIX ""
    OUTPUT_NAME "smartstock_core"
)
