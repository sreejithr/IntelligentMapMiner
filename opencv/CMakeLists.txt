cmake_minimum_required(VERSION 2.6)
project(map_extract)

set(PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR})

list(APPEND CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lboost_python -lboost_system -lpython2.7 -Wc++11-extensions")

set (SRC_FILES 
     ${PROJECT_DIR}/map_extract.cpp
    )


FIND_PACKAGE(Boost COMPONENTS system filesystem unit_test_framework python REQUIRED)
IF (Boost_FOUND)
    INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
    ADD_DEFINITIONS( "-DHAS_BOOST" )
        
    message("Include dirs for Boost: " ${Boost_INCLUDE_DIRS})
    message("Libs of Boost" ${Boost_LIBRARIES})
ENDIF()

FIND_PACKAGE(OpenCV REQUIRED)
message("Include dirs for OpenCV: " ${OpenCV_INCLUDE_DIRS})

FIND_PACKAGE(PythonLibs REQUIRED)
message("Include Dirs for Python: " ${PYTHON_INCLUDE_DIRS})
message("Libs of Python: " ${PYTHON_LIBRARIES})


include_directories(${PROJECT_DIR}
                ${Boost_INCLUDE_DIRS}
                ${PYTHON_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} MODULE ${SRC_FILES})
target_link_libraries(${PROJECT_NAME} ${BoostLibraries} ${PYTHON_LIBARIES} ${OpenCV_LIBRARIES})
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")
