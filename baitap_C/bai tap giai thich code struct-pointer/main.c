#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#define SORT    1
#define UNSORT  0
typedef struct
{
    char ten[50];
    float diemTrungBinh;
    int id;
} SinhVien;

bool stringCompare(const char *str1, const char *str2)
{
    while (*str1 && (*str1 == *str2))
    {
        str1++;
        str2++;
    }
    return ((*(const unsigned char *)str1 > *(const unsigned char *)str2) ? SORT : UNSORT);
}

// Hàm so sánh theo tên
bool compareByName(const void *a, const void *b)
{
    SinhVien *sv1 = (SinhVien *)a;
    SinhVien *sv2 = (SinhVien *)b;
    return stringCompare(sv1->ten, sv2->ten);
}

// Hàm so sánh theo điểm trung bình
bool compareByDiemTrungBinh(const void *a, const void *b)
{
    SinhVien *sv1 = (SinhVien *)a;
    SinhVien *sv2 = (SinhVien *)b;
    return ((sv1->diemTrungBinh > sv2->diemTrungBinh) ? SORT : UNSORT);
}

// Hàm so sánh theo ID
bool compareByID(const void *a, const void *b)
{
    SinhVien *sv1 = (SinhVien *)a;
    SinhVien *sv2 = (SinhVien *)b;
    return ((sv1->id > sv2->id)? SORT : UNSORT);
}

// Hàm sắp xếp chung
void sort(SinhVien *array, size_t size, bool (*compareFunc)(const void *, const void *))
{
    int i, j;
    SinhVien temp;
    for (i = 0; i < size - 1; i++)
        for (j = i + 1; j < size; j++)
            if (compareFunc(array + i, array + j) == SORT)
            {
                temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
}

void display(SinhVien *array, size_t size)
{
    for (size_t i = 0; i < size; i++)
    {
        printf("ID: %d, Ten: %s, Diem Trung Binh: %.2f\n", array[i].id, array[i].ten, array[i].diemTrungBinh);
    }
    printf("\n");
}

int main()
{
    SinhVien danhSachSV[] = {
        {.ten = "Hoang Duy",
         .diemTrungBinh = 7.5,
         .id = 23},
        {.ten = "Hong Anh",
         .diemTrungBinh = 4.5,
         .id = 11},
        {.ten = "Duc Minh",
         .diemTrungBinh = 6.8,
         .id = 8},
        {.ten = "Ngan Nguyen",
         .diemTrungBinh = 5.6,
         .id = 20},
    };
    size_t size = sizeof(danhSachSV) / sizeof(danhSachSV[0]);

    // Sắp xếp theo tên
    sort(danhSachSV, size, compareByName);

    display(danhSachSV, size);

    // Sắp xếp theo điểm trung bình
    sort(danhSachSV, size, compareByDiemTrungBinh);

    display(danhSachSV, size);

    // Sắp xếp theo ID
    sort(danhSachSV, size, compareByID);
    display(danhSachSV, size);

    return 0;
}
