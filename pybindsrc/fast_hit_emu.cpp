#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <iomanip>

#include "fast_hit_emu/TPGCore.hpp"
#include "fast_hit_emu/TPGStitch.hpp"

namespace py = pybind11;

PYBIND11_MODULE(fast_hit_emu, m)
{
m.doc() = "c++ implementation of the dunedaq dtp emulator modules"; // optional module docstring

py::class_<fast_hit_emu::TPGenerator>(m, "TPGenerator")
    .def(py::init<const std::string, const unsigned int, const unsigned int>())
    .def("pedestal_subtraction", &fast_hit_emu::TPGenerator::pedestal_subtraction, py::arg("adcs"), py::arg("ini_median"), py::arg("ini_accum"), py::arg("limit") = 10)
    .def("fir_filter", &fast_hit_emu::TPGenerator::fir_filter, py::arg("adcs"))
    .def("hit_finder", &fast_hit_emu::TPGenerator::hit_finder, py::arg("adcs"), py::arg("tov_min") = 2)
    ;

py::class_<fast_hit_emu::TPStitcher>(m, "TPStitcher")
    .def(py::init())
    .def("hit_stitcher", &fast_hit_emu::TPStitcher::hit_stitcher, py::arg("fwtps"), py::arg("offline_ch"))
    ;

}