cmake_minimum_required(VERSION 3.15)
project(cinatra_test)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests)
add_definitions(-DINJECT_FOR_HTTP_CLIENT_TEST)
add_definitions(-DINJECT_FOR_HTTP_SEVER_TEST)
add_executable(${PROJECT_NAME}
		test_coro_http_server.cpp
        test_cinatra.cpp
        test_cinatra_websocket.cpp
        test_cmdline.cpp
        main.cpp
        )
target_compile_definitions(${PROJECT_NAME} PRIVATE ASYNC_SIMPLE_HAS_NOT_AIO INJECT_FOR_HTTP_CLIENT_TEST)
target_link_libraries(${PROJECT_NAME} cinatra)

find_package(ZLIB)
if (ZLIB_FOUND)
    add_definitions(-DCINATRA_ENABLE_GZIP)
endif ()

option(SKIP_TIME_TEST "skip time tests" OFF)
if(SKIP_TIME_TEST)
	message(STATUS "skip time tests")
    add_definitions(-DSKIP_TIME_TEST)
endif()

add_test(NAME ${PROJECT_NAME} COMMAND ${PROJECT_NAME})

if (ZLIB_FOUND)
	target_link_libraries(${PROJECT_NAME} ${ZLIB_LIBRARIES})
endif()

if (ENABLE_BROTLI)
	include_directories(${BROTLI_INCLUDE_DIRS})
	target_link_libraries(${PROJECT_NAME} ${BROTLI_LIBRARIES})
endif()

# test_coro_file
option(ENABLE_FILE_IO_URING "enable io_uring" OFF)
if(ENABLE_FILE_IO_URING)
    message(STATUS "enable io_uring")
    add_definitions(-DENABLE_FILE_IO_URING)
    add_definitions(-DASIO_HAS_FILE)
    add_definitions(-DASIO_HAS_IO_URING)
endif()

if(WIN32)
    message(STATUS "windows has file")
	add_definitions(-DASIO_HAS_FILE)
	add_definitions(-DASIO_HAS_IOCP)
endif()

option(USE_PREAD_WRITE "enable pread and pwrite" OFF)
if(USE_PREAD_WRITE)
	message(STATUS "use pread and pwrite")
    add_definitions(-DUSE_PREAD_WRITE)
endif()

if (UNIX)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -pthread")
endif()


add_executable(test_corofile
        test_corofile.cpp
        )

if(ENABLE_FILE_IO_URING)
  if (UNIX)
	if (ENABLE_SSL)
		target_link_libraries(test_corofile PRIVATE uring OpenSSL::SSL OpenSSL::Crypto)
	else()
		target_link_libraries(test_corofile PRIVATE uring)
	endif()
  endif()
else()
  if (ENABLE_SSL)
	target_link_libraries(test_corofile PRIVATE OpenSSL::SSL OpenSSL::Crypto)
  endif()
endif()

add_test(NAME test_corofile COMMAND test_corofile)

add_executable(test_time_util
        test_time_util.cpp
        )
add_test(NAME test_time_util COMMAND test_time_util)

add_executable(test_metric
        test_metric.cpp
        )

if (ENABLE_SSL)
    find_package(OpenSSL REQUIRED)
    add_definitions(-DCINATRA_ENABLE_SSL)
    target_link_libraries(${PROJECT_NAME}  OpenSSL::SSL OpenSSL::Crypto)
	target_link_libraries(test_metric  OpenSSL::SSL OpenSSL::Crypto)
endif ()

add_executable(test_http_parse
        test_http_parse.cpp
        )
if (UNIX)
	if (ENABLE_SSL)
		target_link_libraries(test_http_parse ${ZLIB_LIBRARIES} OpenSSL::SSL OpenSSL::Crypto)
	elseif()
		target_link_libraries(test_http_parse ${ZLIB_LIBRARIES})
	endif()
endif()

if (ENABLE_SIMD STREQUAL "AARCH64")
	if (CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "aarch64")
		add_library(neon INTERFACE IMPORTED)
		target_compile_options(neon INTERFACE -march=armv8-a+fp+simd)
		target_link_libraries(test_http_parse neon)
	endif ()
elseif (ENABLE_SIMD STREQUAL "SSE42")
	if (CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "x86_64")
		add_library(sse4_2 INTERFACE IMPORTED)
		if(MSVC)
			target_compile_options(sse4_2 INTERFACE /arch:SSE4.2)
		else()
			target_compile_options(sse4_2 INTERFACE -msse4.2)
		endif()
		target_link_libraries(test_http_parse sse4_2)
	endif ()
elseif (ENABLE_SIMD STREQUAL "AVX2")
	if (CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "x86_64")
		add_library(avx2 INTERFACE IMPORTED)
		if(MSVC)
			target_compile_options(avx2 INTERFACE /arch:AVX2)
		else()
			target_compile_options(avx2 INTERFACE -mavx2)
		endif()
		target_link_libraries(test_http_parse avx2)
		set(CMAKE_CXX_FLAGS "-fpermissive")
	endif ()
endif ()

add_test(NAME test_http_parse COMMAND test_http_parse)

configure_file(ssl_data/server.crt ssl_data/server.crt COPYONLY)
configure_file(ssl_data/server.key ssl_data/server.key COPYONLY)