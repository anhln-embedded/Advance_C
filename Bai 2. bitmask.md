# 1. KHÁI NIỆM
Đây là 1 kỹ thuật để ta thao tác với giá trị các bit của 1 số ở dạng nhị phân, mục đích là để sử dụng trạng thái của các bit để kích hoạt 1 tính năng nào đó mà ta mong muốn khi lập trình. Đièu này sẽ tối ưu hơn rất nhiều so với việc sử dụng các biến riêng lẽ để lưu trữ trạng thái các tính năng gây lãng phí vùng nhớ và chậm quá trình xử lý của CPU.
## 1. Ứng dụng của bitmask và các toán tử logic, phép dịch bit  
### 1.1 Sử dụng phép AND và NOT

<p align = "center">
<img src = "https://github.com/user-attachments/assets/4c163c2d-1581-4d29-8984-f37e854bc82f" width = "300" height = "200">


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
<img src = "https://github.com/user-attachments/assets/24f252f7-95db-4fa0-a161-dc2a958b669d" width = "300" height = "100">

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
## 1.2 Sử dụng phép OR

<p align = "center">
<img src = "https://github.com/user-attachments/assets/98abcf45-9b96-490d-9f82-b2d0332169d5" width = "300" height = "100">

### a) set giá trị của 1 bit
+ Ta sẽ sử dụng bitmask và dịch trái đến vị trí mà ta muốn đặt bit lên 1 và thực hiện phép OR
void set_bit(uint8_t *num, uint8_t pos)
{
    uint8_t bitmask = 1;
    *num |= (bitmask << pos);
}


    

    


    
  