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

    class TPStitcher
    {
    public:
        TPStitcher();
        ~TPStitcher();

        std::vector<std::vector<int>> hit_stitcher(std::vector<std::vector<int>> fwtps, int offline_ch);
    };

}