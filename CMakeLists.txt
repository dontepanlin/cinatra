cmake_minimum_required(VERSION 3.15)
project(cinatra)

find_package(Threads REQUIRED)
find_package(asio REQUIRED)
find_package(async_simple REQUIRED)

include(cmake/build.cmake)
include(cmake/develop.cmake)


add_library(${PROJECT_NAME} INTERFACE)
include_directories("include")
target_include_directories(${PROJECT_NAME} INTERFACE "include")
target_link_libraries(${PROJECT_NAME} INTERFACE asio::asio async_simple::async_simple_header_only)

if (BUILD_UNIT_TESTS)
    add_subdirectory(${cinatra_SOURCE_DIR}/tests)
endif ()
if (BUILD_EXAMPLES)
    add_subdirectory(${cinatra_SOURCE_DIR}/example)
endif ()
if (BUILD_PRESS_TOOL)
    add_subdirectory(${cinatra_SOURCE_DIR}/press_tool)
endif ()