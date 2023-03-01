project(ReadPly)

find_path(TINYPLY_INCLUDE_DIRS "tinyply.h")

file(GLOB_RECURSE HEADER_FILES "*.h")
file(GLOB_RECURSE CPP_FILES "*.cpp" )

set (
    EXTRA_INCLUDE_DIRS
    ${TINYPLY_INCLUDE_DIRS}
)
set(
    EXTRA_LINK_LIBRARIES
)

add_executable(${PROJECT_NAME} ${HEADER_FILES} ${CPP_FILES})
target_include_directories(${PROJECT_NAME} PRIVATE ${EXTRA_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PRIVATE ${EXTRA_LINK_LIBRARIES})
