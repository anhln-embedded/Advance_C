#include "..//inc//record.hpp"
bool dataRecord(const char *path, vector<int> &speed, vector<float> &temp)
{
    FILE *file = fopen(path, "a");
    static bool header = true;
    static int count = 0;
    vector<int>::iterator speed_it = speed.begin();
    vector<float>::iterator temp_it = temp.begin();
    if (file == NULL)
    {
        return FAIL;
    }
    if (header)
    {
        fprintf(file, "time\t\tspeed(km/h)\ttemperature(degree celsius)\n");
        header = false;
    }
    for (; speed_it != speed.end() && temp_it != temp.end(); speed_it++, temp_it++)
        fprintf(file, "%d\t\t%d\t\t%.2f\n", count++, *speed_it, *temp_it);
    fclose(file);
    return SUCCESS;
}
bool dataRead(const char *path)
{
    char line[20];
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        return FAIL;
    }
    while (fgets(line, sizeof(line), file) != NULL)
    {
        cout << line;
    }
    fclose(file);
    return SUCCESS;
}
void Emptyfile(const char *path)
{
    FILE *file = fopen(path, "w");
    char line[100];
    if (file == NULL)
    {
        cout << "can't open file";
    }
    memset(file, 0, sizeof(line));
}