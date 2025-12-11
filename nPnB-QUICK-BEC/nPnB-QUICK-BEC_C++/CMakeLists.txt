cmake_minimum_required (VERSION 3.0)
project ("nPnB-QUICK-BEC")

add_library("nPnB-QUICK-BEC" SHARED "nPnB-QUICK-BEC.cpp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++2a -lpthread -O3")
