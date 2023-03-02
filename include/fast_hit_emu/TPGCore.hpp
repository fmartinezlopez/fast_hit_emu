#include <string>
#include <memory>
#include <fstream>
#include <vector>
#include <sstream>
#include <iterator>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <iostream>

namespace fast_hit_emu{

    class TPGenerator
    {
    public:
        TPGenerator(const std::string fir_data, const unsigned int fir_shift, const unsigned int threshold);
        ~TPGenerator();

        std::vector<std::vector<int>> pedestal_subtraction(std::vector<int> adcs, int ini_median, int ini_accum, int limit = 10);
        std::vector<int> fir_filter(std::vector<int> adcs);
        std::vector<std::vector<int>> hit_finder(std::vector<int> adcs, int tov_min = 2);

    private:
        std::vector<int> m_fir_coeffs;
        unsigned int m_fir_shift;
        unsigned int m_threshold;
    };

}