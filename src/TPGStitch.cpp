#include "fast_hit_emu/TPGStitch.hpp"

fast_hit_emu::TPStitcher::TPStitcher() {

}

fast_hit_emu::TPStitcher::~TPStitcher() {
  
}

std::vector<std::vector<int>> 
fast_hit_emu::TPStitcher::hit_stitcher(std::vector<std::vector<int>> fwtps, int offline_ch){
    std::vector<std::vector<int>> tps;

    int n_fwtps = fwtps.size();

    int first = 1;
    int cont  = 0;

    int tstamp = 0;
    int start = 0;
    int end   = 0;
    int tpeak = 0;
    int hpeak = 0;
    int sum_adc = 0;

    for(int i=0; i < n_fwtps; i++){

        int _tstamp  = fwtps.at(i)[0];
        int _start   = fwtps.at(i)[1];
        int _end     = fwtps.at(i)[2];
        int _tpeak   = fwtps.at(i)[3];
        int _hpeak   = fwtps.at(i)[4];
        int _sum_adc = fwtps.at(i)[5];
        int _hitcont = fwtps.at(i)[6];

        if((_tstamp-tstamp != 32*64)&(cont == 1) or (_start != 0)&(cont == 1)){
            std::vector<int> tp = {start, tpeak, end-start, offline_ch, sum_adc, hpeak};
            tps.push_back(tp);
            first = 1;
            cont  = 0;
            sum_adc = 0;
        }

        if(first == 1){
            tstamp = _tstamp;
            start  = _tstamp+_start*32;
            tpeak  = _tstamp+_tpeak*32;
            hpeak  = _hpeak;
            first  = 0;
        }

        end = _tstamp+_end*32;
        sum_adc += _sum_adc;

        if(_hpeak > hpeak){
            tpeak = _tstamp+_tpeak*32;
            hpeak = _hpeak;
        }

        if((_hitcont == 1)&(_end == 63)){
            cont = 1;
        } else {
            std::vector<int> tp = {start, tpeak, end-start, offline_ch, sum_adc, hpeak};
            tps.push_back(tp);
            first = 1;
            cont  = 0;
            sum_adc = 0;
        }

    }

    return tps;

}
