cmake_minimum_required(VERSION 3.20)
project(newbee_firmware C ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_compile_options(-Wall -Wextra -Werror=implicit-function-declaration)

file(GLOB_RECURSE SOURCES "src/*.c" "drivers/*.c")

add_executable(newbee_firmware ${SOURCES})
target_include_directories(newbee_firmware PRIVATE include drivers)

# 目标板：Cortex-M55 @ 200 MHz，1 MB SRAM
set_target_properties(newbee_firmware PROPERTIES SUFFIX ".elf")
