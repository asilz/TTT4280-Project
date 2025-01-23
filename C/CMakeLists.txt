cmake_minimum_required(VERSION 3.10)
project(TTT4280)

set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_STANDARD 23)

#set(CMAKE_CXX_FLAGS_DEBUG "-g")
#set(CMAKE_CXX_FLAGS_RELEASE "-O3")

set(SOURCES
    src/adc_sampler.c
)

add_executable(adc_sampler ${SOURCES})
target_link_libraries(adc_sampler PRIVATE pigpio)
target_link_libraries(adc_sampler PRIVATE pthread)
target_link_libraries(adc_sampler PRIVATE m)
target_compile_options(adc_sampler PRIVATE -Wall -Werror=vla)
target_include_directories(adc_sampler PRIVATE include)