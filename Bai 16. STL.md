# 1. Tổng quan về STL  
## 1.1 Định nghĩa 
+ Đây là thư viện tiêu chuẩn của C++,cung cấp các hàm có sẵn để thao tác sửa,xóa,chèn,quản lý hay sắp xếp dữ liệu giúp tôi ưu thời gian viết code
+ các hàm bên trong STL được quản lý thông qua các template cho phép ta có thể thao tác với bất kỳ dữ liệu nào trên cùng 1 hàm mà không phải viết lại hàm xử lý riêng cho mỗi kiểu dữ liệu.

## 1.2 Lợi ích và ứng dụng của STL
### a) Lợi ích 

__+ Cải thiện năng suất:__ STL cung cấp các hàm cấu trúc dữ liệu và thuật toán có sẵn, giúp giảm thời gian phát triển phần mềm

__+ Tính tổng quát:__ Các hàm bên trong STL đều dược phát triển dựa trên template có thể hoạt động với bất kỳ kiểu dữ liệu nào

__+ Hiệu suất cao:__ Các hàm bên trong STL đã được tối ưu hóa để hoạt động chính xác và nhanh nhất
### b) Các thành phần 

<p align = "center">
<img src = "https://github.com/user-attachments/assets/369b6ce7-2887-4925-a86b-7e3d75377add" width = "550" height = "270".>

__Containers:__ là các class template sử dụng như những hộp chứa để lưu trữ dữ liệu

__Iterator:__ là đối tượng sử dụng như 1 con trỏ dể truy cập và lặp qua các dữ liệu bên trong Containers

__Algorithms:__ Là các method cho phép sắp xếp và thao tác dữ liệu theo cách mà ta mong muốn

### c) Ứng dụng  
+ Sử dụng các hàm thuật toán như sorting giúp tối ưu chương trình đối với đặc trưng về yêu cầu hạn chế memory và CPU trong 1 hệ thống embedded 

# 2. Triển khai cụ thể các thành phần
## 2.1 Container và Iterator
+ Thư viện khai báo: __#include<vector>__
+ Là các cấu trúc dữ liệu để lưu trữ và quản lý các phần tử
### a) thư viện vector
__Định nghĩa__

+ Đây 1 kiểu dữ liệu tương tự như array nhưng là 1 mảng động
+ Cho phép các thao tác như truy cập,thêm,sửa,xóa thông qua các hàm có sẵn 

__Ứng dụng trong lĩnh vực embedded__

+ Quản lý dữ liệu cảm biến thông qua các giao thức truyền thông
+ Quản lý dữ liệu tĩnh nhưng thay đổi theo thời gian như giá trị ADC
+ Quản lý danh sách dữ liệu theo tiêu chuẩn như cấu hình tham số của ngoại vi 

__Cách hoạt động của vector__

<p align = "center">
<img src = "https://github.com/user-attachments/assets/7a977dc5-4c28-4698-aa56-73171e7eea87" width = "500" height = "280".>
    
__khai báo và in ra các phần tử__

```bash
vector<char> vec = {'d','u','y','s','o','l','o'};

    //cach 1: use traditional for loop 
    for(int i = 0 ; i < vec.size() ; i++) // size() -> return total stored elements
        cout << vec.at(i);
    cout << endl;
    //cach 2: use the advance for loop 
    for(auto i : vec) // auto i -> return value of element with exact data type  
        cout << i;
    cout << endl;
    //cach 3: use pointer 
    vector<char> :: iterator it1; 
    for(it1 = vec.begin() ; it1 != vec.end() ; it1++) //it -> loop throught each element 
        cout << *it1;
    cout << endl;
```

__Thao tác thêm, sửa, xóa__
    
```bash
    vector<int> arr = {2, 5, 1, 5, 6};
    cout << "before" << endl;
    for (int i = 0; i < arr.size(); i++)
        cout << "element: " << arr[i] << endl;

    arr.at(2) = 10; // change value 

    arr.resize(8);  // realloc memory 

    arr.insert(arr.begin(), 12); //push new element to the front of vector

    arr.push_back(18); // push new element to the end of vector   

    arr.erase(arr.begin()); //delete begin element of vector

    cout << "after" << endl;
    for (int i = 0; i < arr.size(); i++)
        cout << "element: " << arr[i] << endl;
```
### b) thư viện list
__Định nghĩa__
+ Thư viện khai báo: __#include<list>__
+ Cung cấp các hàm để thao tác như là 1 danh sách liên kết
+ Cho phép thao tác với các phần tử tương tự như vector nhưng hiệu quả vì không yêu cầu về cấp phát bộ nhờ

__Ứng dụng trong lĩnh vực embedded__

+ Quản lý tác vụ: cho phép lưu danh sách các task thực thi, và có thể thêm/sửa/xóa nhanh chóng
+ Cấu trúc hàng đợi: cho phép tạo các queue để xử lý tác vụ 1 cách tuần tự 

__Cách hoạt động của list__

<p align = "center">
<img src = "https://github.com/user-attachments/assets/ec06a45f-f070-434d-9474-12fbc491148d" width = "500" height = "280".>

__Thêm các phần tử vào list__

```bash
  cout <<"add node and print" << endl;
    list<int> lst;
    for (int i = 0; i < 5; i++)
        lst.push_back(i + 1);
    auto i = 0;
    for(auto item : lst)
        cout << "node " << i++ << ":" << item << endl;
```
__Truy cập list thông qua iterator__

```bash
    cout << "address of last node" << endl;
    list<int>::iterator it;
    it = lst.end(); 
    cout << "add: " << &(*it) << endl;
    i = 0;
    cout << "address and value of node" << endl;
    for (it = lst.begin(); it != lst.end(); it++)
        cout << "add: " << &(*it) << ", node" << i++ << ":" << *it << endl;
    i = 0;
```
__Thêm phần tử tại vị trí bất kỳ__

```bash
    //traverse through each node
    cout <<"add node at certein position" << endl;
    for(it = lst.begin() ; it != lst.end() ; it++){
        if(i == 2){
            lst.insert(it,12); //insert at node 2
        }
        i++; //count each node
    }
    i = 0;
    cout << "print list after adding new node" << endl;
    for (it = lst.begin(); it != lst.end(); it++)
        cout << "add: " << &(*it) << ", node:" << i++ << " " << *it << endl;
```
__Xóa phần tử tại vị trí bất kỳ__

```bash
    i = 0;
     // delete node
    for(it = lst.begin() ; it != lst.end() ; it++){
        if(i == 4){
            it = lst.erase(it); //update new it after delete 
        }
        i++;
    }

    i = 0;
    cout << "print list after deleting node 2" << endl;
    for(auto value : lst)
        cout << "value " << i++ << ": " << value << endl;
    
    return 0;
```

__SO SÁNH VECTOR VÀ LIST__

Cả vector và list đều dùng để lưu trữ dữ liệu tuy nhiên lựa chọn cái nào để sử dụng tối ưu nhất sẽ phụ thuộc vào các trường hợp sau 

__Sử dụng list khi__

__+ thao tác sửa,thêm,xóa liên tục__: tói ưu hơn so với vector vì địa chỉ của các node không cố định và liền kể nhau -> không phải cấp phát lại memory như vector

__+ Ít truy cập ngẫu nhiên__: do phải dùng còn trõ để duyệt qua từng node -> tốn thời gian

__+ Yêu cầu về bộ nhớ hệ thống không hạn chế__:do list tốn thêm memory để lưu trữ con trỏ liên kết)

=> Ví du: quản lý task queue hoặc lưu trữ dữ liệu giao tiếp qua UART theo thời gian thực

__Sử dụng vector khi__

+ Dữ liệu có kích thước cố định và ít thay đổi
+ cần truy cập ngẫu nhiên nhanh chóng

=> ví dụ: lưu trữ dữ liệu ADC hoặc truyền qua SPI 

### c) Thư viện map

__Định nghĩa__
+ Thư viện khai báo __#include <map>__
+ Tương tự như kiểu json, dùng để lưu trữ các cặp key-value
+ Cung cấp các hàm để tìm kiếm,chèn,xóa 

__Ứng dụng trong lĩnh vực embedded__

+ Lưu trữ cấu hình hệ thống ví du: "baud_rate": 9600 
+ Tạo bảng mapping (ánh xạ) giữa các mã tín hiệu và ý nghĩa (mả lỗi va2 mô tả)

__Các thao tác với map__

```bash
/* KEY AND VALUE ARE STRING */
    map<string, string> mp; // locate at stack

    // locate at heap
    mp["Ten:"] = "Tan Tung";
    mp["Ten:"] = "Duy Pham"; // this will be printed out except the above -> the last one with similar key
    mp["MSSV"] = "17146011";
    mp["3"] = "123";
    mp["5"] = "456";
    mp["1"] = "789";
    mp["2"] = "159";
    mp["4"] = "168";
    for (auto item : mp)
        cout << "key: " << item.first << ", value:" << item.second << endl;
/* KEY IS INTEGER AND VALUE IS STRING */
    map<int, string> mp1;
    char* name_list[] = {"Cao Duy","Tan Tung","Le Hoang","Anh Tuan","Quang Nhat"};
    //add value to map./map
    for(int i = 0 ; i < sizeof(name_list) / sizeof(name_list[0]) ; i++)
       mp1[i] = string(name_list[i]);

    mp1.erase(1);
    //print map
    map<int, string>::iterator it;
    for (it = mp1.begin(); it != mp1.end(); it++)
        cout << "key: " << (*it).first << "\tvalue: " << (*it).second << endl;
```

## 2.2 Algorithm

__Định nghĩa__ 
+ Cung cấp các method để thao tác dữ liệu lưu trữ trong container
+ Thư viện khai báo __#include <algorithm>__

### a) Thuật toán For_Each()

Được sử dụng để duyệt qua từng phần tử của 1 dãy giá trị đầu vào và thực thi 1 hàm hoặc lambda trên từng phần tử

__Cú pháp__

__std::for_each(InputIterator first, InputIterator last, Function func);__

__+ first__: con trỏ đến phần tử đầu 

__+ last__: con trỏ đến ngay sau phần tử cuối cùng 

__+ func__: hàm hoặc lambda thực thi trên từng phần tử

__In ra các phần tử__

```bash
vector<int> vec = {1, 2, 3, 4, 5};

//sử dụng lambda để xây dựng hàm in 
auto print =  [](int x) {cout << x << " ";};
for_each(vec.begin(), vec.end(),print);
```

__Thay đổi giá trị các phần tử__


```bash
vector<int> vec = {1, 2, 3, 4, 5};
auto change = [](int& x){x*=2;};
for_each(vec.begin(),vec.end(),change);
for(auto i : vec)
   cout << i << " " << endl;
```
__Tính tổng các phần tử__

```bash
vector<int> vec = {1, 2, 3, 4, 5};
int sum = 0;
auto tong = [&sum](int x){sum += x;};
for_each(vec.begin(), vec.end(),tong);
cout << "sum :" << sum;
```
### b) Thuật toán find()

Được sử dụng để tìm phần tử đầu tiên trong dãy có giá trị khớp với giá trị được cung cấp 

__Cú pháp__

__template<class InputIterator, class T>__
__InputIterator find(InputIterator first, InputIterator last, const T& value);__

__+ first , last__ : iterator xác định phạm vi tìm kiếm

=> Hàm này trả về con trỏ đ16n phần tử đầu tiên bằng với value. Nếu không tìm thấy trả về 

__Ví dụ:__

```bash
vector<int> vec = {10, 20, 30, 40, 50};
auto it = find(vec.begin(), vec.end(), 30);
if (it != vec.end())
    cout << "Found: " << *it << endl;
else
    cout << "Not found" << endl;
```

### c) Thuật toán sort()

Được sử dụng để sắp xếp các phần tử theo thứ tự tăng/giảm dần

__Cú pháp__

__template<class RandomIt>__
__void sort(RandomIt first, RandomIt last);__
__template<class RandomIt, class Compare>__
__void sort(RandomIt first, RandomIt last, Compare comp);__

__+ first , last__ : xác định phạm vi để sắp xếp

__comp__: Hàm so sánh, nếu không cung cấp sẽ tự động sắp xếp theo thứ tự tăng dần

__Ví dụ__

```bash
std::vector<int> vec = {50, 20, 40, 10, 30};
std::sort(vec.begin(), vec.end()); //sắp xếp tăng dần
std::sort(vec.begin(), vec.end(),greater<int>()); //sắp xếp giảm dần
for (int val : vec) {
    std::cout << val << " ";
}
```
### d) Thuật toán merge()

đƯỢC sử dụng để hợp nhất 2 dãy đã được sắp xếp thành 1 dãy

__Cú pháp__

__template<class InputIterator1, class InputIterator2, class OutputIterator>__
__OutputIterator merge(InputIterator1 first1, InputIterator1 last1,__
                     __InputIterator2 first2, InputIterator2 last2,__
                     __OutputIterator result);__

__template<class InputIterator1, class InputIterator2, class OutputIterator, class Compare>__
__OutputIterator merge(InputIterator1 first1, InputIterator1 last1,__
                     __InputIterator2 first2, InputIterator2 last2,__
                     __OutputIterator result, Compare comp);__

__+ first1, last1__ : phạm vi của dãy thứ nhất đã sắp xếp

__+ first2, last2__ : phạm vi của dãy thứ hai đã sắp xếp

__+ result__ iterator trỏ đến kết quả đã hợp nhất

__+ comp__ : hàm so sánh 

__Ví dụ:__

```bash
  vector<int> vec1 = {10, 20, 30};
vector<int> vec2 = {15, 25, 35};
vector<int> result(vec1.size() + vec2.size());
merge(vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), result.begin());
for (int val : result)
   cout << val << " ";
```








    
    

