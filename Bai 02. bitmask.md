# 1. KHÁI NIỆM
Đây là 1 kỹ thuật để ta thao tác với giá trị các bit của 1 số ở dạng nhị phân, mục đích là để lưu trữ nhiều tính năng bằng trạng thái của các bit. Đièu này sẽ tối ưu hơn rất nhiều so với việc sử dụng các biến riêng lẽ để lưu trữ trạng thái các tính năng gây lãng phí vùng nhớ và chậm quá trình xử lý của CPU.
# 2. Ứng dụng của bitmask và các toán tử logic, phép dịch bit  
## 2.1 Phép dịch bit
Được sử dụng khi ta muốn đọc/ghi/xóa/kiểm tra 1 bit

__+ Dịch trái <<__ : Khi ta cần đẩy các bit từ phải sang trái
```bash
uint8_t num = 5; //0b0000 0101 -> biểu diễn binary 
//cách 1
num = num << 5;  //0b1010 0000 -> dịch các bit của num 5 lần
//cách 2
num <<= 5;
```

__+ Dịch phải >>__ : Khi ta cần đẩy các bit từ trái sang phải
```bash
uint8_t num = 255; //0b1111 1111 -> biểu diễn binary 
//cách 1
num = num >> 5;    //0b0000 0111 -> dịch các bit của num 5 lần
//cách 2
num >>= 5;
```
## 2.2 Sử dụng phép AND và NOT

<p align = "center">
<img src = "https://github.com/user-attachments/assets/894c6a30-9022-404a-ab9a-076522058968" width = "800" height = "200">

### a) Đọc giá trị của 1 bit
+ Ta sử sử dụng cơ chế bitmask và thực hiện phép AND tại vị trí mà ta muốn đọc ra trạng thái bit và phép dịch trái << như đoạn code sau đây 
+ nếu kết quả là 1 số khác 0 thì ta sẽ trả về giá trị là 1 và ngược lại
```bash
int read_bit(uint8_t num , uint8_t position){
    return ((num & (bitmask << pos)) != 0 )? 1 : 0);
}
int main(){
    printf("bit ở vị trí thứ 2 là : %d",read_bit(12,2));
    return 0;
}
```
<p align = "center">
<img src = "https://github.com/user-attachments/assets/24f252f7-95db-4fa0-a161-dc2a958b669d" width = "400" height = "200">

### b) lấy giá trị của 1 bit

+ Ta sẽ thực hiện dịch phải >> với số lần tương ứng với vị trí bit mà ta muốn lấy ra và AND với bitmask 

```bash
int get_bit(uint8_t num, uint8_t pos)
{
    uint8_t bitmask = 1;
    return ((num >> pos) & bitmask);
}
```
### c) reset giá trị của 1 bit
+ Đầu tiên ta sẽ sử dụng bitmask và dịch trái << đến vị trí của bit mà ta muốn reset
+ Sau đó ta sẽ sử dụng phép NOT để đảo trạng thái các bit
+ Cuối cùng là thực hiện phép AND với kêt quả trên ta sẽ reset được bit ở vị trí mà ta muốn, trong khi giá trị các bit khác giữ nguyên

```bash
void reset_bit(uint8_t *num, uint8_t pos)
{
    uint8_t bitmask = 1;
    *num &= ~(bitmask << pos);
}
```
## 2.3 Sử dụng phép OR

<p align = "center">
<img src = "https://github.com/user-attachments/assets/98abcf45-9b96-490d-9f82-b2d0332169d5" width = "400" height = "200">

### a) set giá trị của 1 bit
+ Ta sẽ sử dụng bitmask và dịch trái đến vị trí mà ta muốn đặt bit lên 1 và thực hiện phép OR
```bash
void set_bit(uint8_t *num, uint8_t pos)
{
    uint8_t bitmask = 1;
    *num |= (bitmask << pos);
}
```
## 2.4 Sử dụng phép XOR

<p align = "center">
<img src ="https://github.com/user-attachments/assets/8ae6614c-b1d2-458b-98d6-2b2ea496948c" width ="400" height = "200">

Ta sẽ sử dụng phép toán này để đảo trạng thái của 1 bit
+ ví dụ: tìm sự khác giữa số bit 1 trong 2 số.

```bash
int countBitDifference(int x, int y) {
    int count = 0;
//thực hiện XOR với tất cả bit trên x và y
//z sẽ chứa tổng các bit 1 là giá trị bit 1 chênh lệch giữa x và y   
    int z = x ^ y; 
    while (z) {
        if(z & 1) count += 1;
        z >>= 1;
    }
    return count;
}

```
=> Khi ta truyền vào 2 giá trị x = 255 và y = 1, thì kết quả trả về là 7 , tương ứng với số bit 1 chênh lệch 

# 3. Ứng dụng thực tế 
+ Các phép toán Bitwise thường được sử dụng trong việc thao tác với các thanh ghi trong lập trình embedded thông qua các con trỏ. Tùy thuộc vào MCU 8,16, hay 32 bit thì các thanh ghi bên trong nó sẽ có số lượng bit tương ứng, với mỗi bit được sử dụng để bật hay tắt 1 chức năng nào đó 
## 3.1 Quản lý trạng thái các chân GPIO của MCU
+ Giả sử ta có thanh ghi __GPIO_PORT__ sử dụng 4 bit để lưu trữ trạng thái mỗi __PIN__, ta sẽ khai báo các macro bitmask với bit tương ứng của chúng 
  
```bash
#define LED1 1 << 0 // 0001
#define LED2 1 << 1 // 0010
#define LED3 1 << 2 // 0100
#define LED4 1 << 3 // 1000

```
+ Ta tạo ra hai hàm đùng để chọn hoặc vô hiệu hóa chức năng nào đó, trong trường hợp này ta sẽ quản lý việc enable/disable các chân __GPIO__
```bash
void enableLED(unsigned int *GPIO_PORT, unsigned int LED)
{
    *GPIO_PORT |= LED;
}

void disableLED(unsigned int *GPIO_PORT, unsigned int LED)
{
    *GPIO_PORT &= ~LED;
}
``` 
+ Ta sử dụng hàm sau để kiểm tra trạng thái bit trên __GPIO_PORT__ thông qua các bitmask cho từng __PIN__ đã định nghĩa 

```bash
void display_LED(unsigned int GPIO_PORT)
{
    if (GPIO_PORT & LED1)
    {
        printf("LED1 is on\t");
    }

    if (GPIO_PORT & LED2)
    {
        printf("LED2 is on\t");
    }

    if (GPIO_PORT & LED3)
    {
        printf("LED3 is on\t");
    }

    if (GPIO_PORT & LED4)
    {
        printf("LED4 is on\t");
    }
}
``` 
+ Trong chường trỉnh chính ta thực hiện chọn các tính năng sẽ được kích hoạt hay vô hiệu hóa như sau

```bash
int main()
{
    unsigned int GPIO_PORT = 0; // Giả sử là biến điều khiển cổng GPIO

    // Bật LED1 và LED3
    enableLED(&GPIO_PORT, LED1 | LED2 | LED3 | LED4);
    display_LED(GPIO_PORT);
    printf("\n");
    disableLED(&GPIO_PORT, LED2);
    display_LED(GPIO_PORT);
    return 0;
}

```
+ Kết quả in ra màn hình
```bash
LED1 is on      LED2 is on      LED3 is on      LED4 is on
LED1 is on      LED3 is on      LED4 is on
```


    

    


    
  
