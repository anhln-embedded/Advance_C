#ifndef __RECORD_H
#define __RECORD_H
#include <iostream>
#include <string>
#include <ctime>
#include <vector>
#include <stdio.h>
#include <string.h>
using namespace std;
bool dataRecord(const char*,vector<int>& ,vector<float>&);
bool dataRead(const char*);
void Emptyfile(const char*);
#define FAIL    0
#define SUCCESS  1
#endif