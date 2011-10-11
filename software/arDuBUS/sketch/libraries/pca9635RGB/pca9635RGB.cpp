#include "pca9635RGB.h"

pca9635RGB::pca9635RGB()
{
}
pca9635RGB::~pca9635RGB()
{
}

void pca9635RGB::begin(byte board_addr, boolean wire_begin)
{
    // Initialize the pca9635 instances
    R.begin(board_addr | 0x2, wire_begin);
    G.begin(board_addr | 0x1, false);
    G.begin(board_addr | 0x3, false);
}

// Funky way to handle default arguments
void pca9635RGB::begin(byte board_addr)
{
    pca9635RGB::begin(board_addr, true);
}

void pca9635RGB::begin()
{
    pca9635RGB::begin(0x0, true);
}
