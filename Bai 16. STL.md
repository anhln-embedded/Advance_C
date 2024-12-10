# 1. Tổng quan về STL 
## 1.1 Định nghĩa 
+ Đây là thư viện tiêu chuẩn của C++,cung cấp các hàm có sẵn để thao tác sửa,xóa,chèn,quản lý hay sắp xếp dữ liệu giúp tôi ưu thời gian viết code
+ các hàm bên trong STL được quản lý thông qua các template cho phép ta có thể thao tác với bất kỳ dữ liệu nào trên cùng 1 hàm mà không phải viết lại hàm xử lý riêng cho mỗi kiểu dữ liệu.

## 1.2 Lợi ích và ứng dụng của STL
### a) Lợi ích 

__+ Cải thiện năng suất:__ STL cung cấp các hàm cấu trúc dữ liệu và thuật toán có sẵn, giúp giảm thời gian phát triển phần mềm

__+ Tính tổng quát:__ Các hàm bên trong STL đều dược phát triển dựa trên template có thể hoạt động với bất kỳ kiểu dữ liệu nào

__+ Hiệu suất cao:__ Các hàm bên trong STL đã được tối ưu hóa để hoạt động chính xác và nhanh nhất

### b) Ứng dụng 
+ Lưu trũ dữ liệu linh hoạt và tiết kiệm tài nguyên với các container như __vector__ hay __list__ 
+ Sử dụng các hàm thuật toán như sorting giúp tối ưu chương trình đối với đặc trưng về yêu cầu hạn chế memory và CPU trong 1 hệ thống embedded 

# 2. Các thành phần của STL
## 2.1 Container (hộp chứa)
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
+ Kết quả in ra 
    
```bash
before
element: 2
element: 5
element: 1
element: 5
element: 6
after
element: 2
element: 5
element: 10
element: 5
element: 6
element: 0
element: 0
element: 0
element: 18
```
### b) thư viện iist
__Định nghĩa__
+ Thư viện khai báo: __#include<list>__
+ Cung cấp các hàm để thao tác như là 1 danh sách liên kết
+ Cho phép thao tác với các phần tử tương tự như vector nhưng hiệu quả vì không yêu cầu về cấp phát bộ nhờ

__Ứng dụng trong lĩnh vực embedded__

+ Quản lý tác vụ: cho phép lưu danh sách các task thực thi, và có thể thêm/sửa/xóa nhanh chóng
+ Cấu trúc hàng đợi: cho phép tạo các queue để xử lý tác vụ 1 cách tuần tự 

__Các thao tác với list__


```bash
  cout <<"add node and print" << endl;
    list<int> lst;
    for (int i = 0; i < 5; i++)
        lst.push_back(i + 1);
    auto i = 0;
    for(auto item : lst)
        cout << "node " << i++ << ":" << item << endl;
    cout << "address of last node" << endl;
    list<int>::iterator it;
    it = lst.end(); 
    cout << "add: " << &(*it) << endl;
    i = 0;
    cout << "address and value of node" << endl;
    for (it = lst.begin(); it != lst.end(); it++)
        cout << "add: " << &(*it) << ", node" << i++ << ":" << *it << endl;
    i = 0;
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
    i = 0;
    //delete node
    cout << "print list after deleting node 2" << endl;
    for(it = lst.begin() ; it != lst.end() ; it++)
        cout << "node " << i++ << *it << endl;
```
+ Kết quả in ra ta được 

```bash
add node and print
node 0:1
node 1:2
node 2:3
node 3:4
node 4:5
address of last node
add: 0x61fed0
address and value of node
add: 0xf61720, node0:1
add: 0xf61738, node1:2
add: 0xf61750, node2:3
add: 0xf617c8, node3:4
add: 0xf617e0, node4:5
add node at certein position
print list after adding new node
add: 0xf61720, node:0 1
add: 0xf61738, node:1 2
add: 0xf617f8, node:2 12
add: 0xf61750, node:3 3
add: 0xf617c8, node:4 4
add: 0xf617e0, node:5 5
print list after deleting node 2
node 01
node 12
node 212
node 33
node 44
node 55
```
__SO SÁNH VECTOR VÀ LIST__

__Sử dụng list khi__

+ Cần thao tác sửa,thêm,xóa liên tục (tói ưu hơn so với vector vì địa chỉ của các node không cố định và liền kể nhau -> không phải cấp phát lại memory như vector)
+ Ít truy cập ngẫu nhiên (do phải dùng còn trõ để duyệt qua từng node -> tốn thời gian)
+ Yêu cầu về bộ nhớ hệ thống không hạn chế (do list tốn thêm memory để lưu trữ con trỏ liên kết)

=> Ví du: quản lý task queue hoặc lưu trữ dữ liệu giao tiếp qua UART heo thời gian thực

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
    
    

