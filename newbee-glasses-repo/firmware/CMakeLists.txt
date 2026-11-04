cmake_minimum_required(VERSION 3.20)
project(newbee_firmware C ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_compile_options(-Wall -Wextra -Werror=implicit-function-declaration)

# 机型：lite / standard / pro，与 sku/tiers.json 对应
set(NB_TIER "standard" CACHE STRING "机型：lite | standard | pro")
set_property(CACHE NB_TIER PROPERTY STRINGS lite standard pro)

if(NB_TIER STREQUAL "lite")
    set(NB_TIER_ID 0)
elseif(NB_TIER STREQUAL "standard")
    set(NB_TIER_ID 1)
elseif(NB_TIER STREQUAL "pro")
    set(NB_TIER_ID 2)
else()
    message(FATAL_ERROR "未知机型 NB_TIER=${NB_TIER}，可选 lite / standard / pro")
endif()

file(GLOB_RECURSE SOURCES "src/*.c" "drivers/*.c")

add_executable(newbee_firmware ${SOURCES})
target_include_directories(newbee_firmware PRIVATE include drivers)
target_compile_definitions(newbee_firmware PRIVATE NB_TIER=${NB_TIER_ID})

message(STATUS "NewBee 机型：${NB_TIER}（NB_TIER=${NB_TIER_ID}）")

# 目标板：Cortex-M55 @ 200 MHz，1 MB SRAM
set_target_properties(newbee_firmware PROPERTIES SUFFIX ".elf")
