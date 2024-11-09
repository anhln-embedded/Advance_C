# 1. Binary Search
# 1.1 Định Nghĩa
Thuật toán dùng để tìm kiếm và trả về 1 giá trị nếu nó tồn tại trong 1 mảng đã được sắp xếp bằng cách so sánh giá trị cần tìm với giá trị ở chính giữa mảng.
# 1.2 So sánh Binary và Linear Search

<img src = "https://github.com/user-attachments/assets/d0eea437-3207-4bcc-91f0-54c30a8c3a6d" width = "700" height = "250">

__+ Linear Search:__ Mỗi phần tử trong mảng sẽ được so sánh với tất cả các phần tử còn lại và số lần kiểm tra sẽ là kích thước của mảng trừ đi 1. Đối với mảng lớn có số lượng phần tử không xác định thì cách này sẽ tốn thời gian xử lý và giảm hiệu suất CPU

__+ Binary Search:__ Giá trị cần tìm sẽ được so sánh vói phần tử ở giữa mảng thay vì tát cả phần tử, và giá trị __mid__ này sẽ được cập nhật qua mỗi lần kiểm tra để thu hẹp phạm vi tìm kiếm, dẫn đến hiệu suất nhanh và hiệu quả hơn. Tuy nhiên cách này sẽ yêu cầu 1 mảng đã sắp xếp
# 1.2 Triển khai 
### a) Giải thích thuật toán
+ Ví dụ ta muốn tìm giá trị __search__ =  25 trong mảng sau đây
<p align = "center">
<img src = "https://github.com/user-attachments/assets/0ee2ac98-9db3-4d50-8a59-6623c898f52d" width = "750" height = "350">

__+ Bước 1:__ ta sẽ sử dụng 2 chỉ số left (đầu mảng) và right(cuối mảng) để xác định được phần tử mid (giữa mảng)

__+ Bước 2:__ Ta so sánh giá trị mid và __search__

__+ Bước 3:__ Ta thu họn vùng giá trị kiểm tra dựa vào kết quả bước 2 

=> nếu giá trị mid > search : ta cập nhật mid += 1 -> left = mid __(vùng kiểm tra bỏ phần bên trái mid)__

=> nếu giá trị mid < search : ta cập nhật mid -= 1 -> right = mid  __(vùng kiểm tra bỏ phần bên phải mid)__

__+ Bước 4:__ Ta lặp lại bước 1 cho đến khi giá trị mid = search 

### b) Demo code thuật toán
+ Đầu tiên ta sẽ cần phải sắp xếp lại các phần tử trong mảng theo thứ tự trước khi thực hiện việc tìm kiếm binary search. Ta sẽ sử dụng thuật toán __bubble sort__ 
=> Đặc điểm của thuật toán bubble sort đó là sau mỗi lần lặp kiểm tra, số lượng phần tử được duyệt qua cũng sẽ giảm dần do các giá trị lớn hơn sẽ được đẩy về cuối mảng. 

```bash
void bubble_sort(int* pArr,int len){
    int temp = 0;
//vòng for ngoài chứa mảng đã sắp xếp
    for(int i = 0 ; i < len - 1 ; i++){
//vòng for trong sẽ so sánh giá trị hiện tại với tiếp theo
        for(int j = 0 ; j < len - i - 1; j++){
            if(pArr[j] > pArr[j + 1]){
                temp = pArr[j];
                pArr[j] = pArr[j+1];
                pArr[j+1] = temp;
            }
        }
    }
}
```
Tiếp theo ta sẽ triển khai hàm binary search như sau

+ Ta kiểm tra mảng có hợp lệ không, Nếu thỏa mới xử lý tiếp
+ Ta thực hiện tính toán giá trị mid và so sánh với search
+ Nếu bàng nhau ta trả về kết quả là true __(tìm thấy search)__
+ Nếu giá trị mid > hoặc < hơn search thì thực hiện cập nhật chỉ số mid mới và gán cho chỉ số left hoặc right và thực hiện đệ quy để quay lại kiểm tra tiếp
+ Nếu chỉ số left >= right mà giá trị mid khác search thì trả về false__(không tìm thấy search)__ 
    
```bash
bool Binary_Search(int* pArr,int left,int right,int search){
    if(left <= right){
        int mid = (left + right) / 2;
        if(search == pArr[mid])           return true;
        else{
            if(search > pArr[mid])      return Binary_Search(pArr,mid + 1,right,search);
            else                        return Binary_Search(pArr,left,mid - 1,search);
        }
    }
   return false;
}
```
Trong chương trình chính, ta thực hiện kiểm tra như sau
```bash
void Sorting_print(int arr[],int len){
    for(int i = 0 ; i < len ;i++)
        printf("%d\t",arr[i]);
}
int main(){
    int arr[] = {12,52,15,62,457,21,58,31,5};
    int len = sizeof(arr)/sizeof(arr[0]);
    bubble_sort(arr,len);
    Sorting_print(arr,len);
    int search = 21;
    bool result = Binary_Search(arr,0,len-1,search);
    printf("\n%s gia tri %d",(result == true)? "tim thay " : "khong tim thay",search);
    return 0;
}
```
Kết quả in ra màn hình
    
```bash
5       12      15      21      31      52      58      62      457
tim thay  gia tri 21
```
# 2. Makefile
# 3. File Operation