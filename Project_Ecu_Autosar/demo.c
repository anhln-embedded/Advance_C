#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdatomic.h>
#include <unistd.h>

//định nghĩa giá trị chia sẻ đa luồng 1 cách an toàn (giúp tránh xung đột giữa các luồng)
atomic_int val; 

// Cờ điều khiển task
bool run_flag = false;      //kiểm soát chạy/tạm dừng hệ thống
bool exit_flag = false;     //kiểm soát việc dừng hoàn toàn hệ thống
bool dataReady = false;     //kiểm soát trạng thái data truyền/nhận

//khởi tạo khóa mutex hỗ trợ các luồng chia sẻ và sử dụng tài nguyên chung 1 cách an toàn
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;  

//Khởi tạo các triggered event để kích hoạt 1 luồng dựa trên điều kiện mong muốn
pthread_cond_t sen_cond = PTHREAD_COND_INITIALIZER;
pthread_cond_t control_cond = PTHREAD_COND_INITIALIZER;

// Task đọc cảm biến
void* TASK_Sensor(void* arg) {
    printf("[TASK_SENSOR] đã khởi tạo\n");

    //cơ chế khởi tạo giá trị ban đầu cho biến toàn cục đa luồng
    atomic_init(&val,0); 
    
    while (1) {
        //khóa mutex để truy cập tài nguyên an toàn
        pthread_mutex_lock(&mutex);

        // Chờ điều kiện cho phép chạy từ luồng phụ thuộc
        while (!run_flag && !exit_flag) {
            pthread_cond_wait(&sen_cond,&mutex);  
        }

        //kiểm tra điều kiện dừng luồng
        if (exit_flag) {
            pthread_cond_signal(&control_cond); //đánh thức task Control
            pthread_mutex_unlock(&mutex);       
            break;
        }
        // Thực hiện công việc
        printf("[TASK_Sensor] Đang đọc...\n");

        //giả lập dữ liệu cảm biến
        int temp = rand() % 123;

        //ghi giá trị vào biến toàn cục đa luồng
        atomic_store(&val,temp);

        dataReady = true;   //set event cho task Control
        pthread_cond_signal(&control_cond); //đánh thức task Control

        //mở khóa mutex cho phép các luồng truy cập tài nguyên 
        pthread_mutex_unlock(&mutex);
        usleep(500000); // Giả lập công việc
    }

    printf("[TASK_Sensor] Kết thúc.\n");
    return NULL;
}

// Task xử lý dữ liệu cảm biến
void* TASK_Control(void* arg){
    printf("[TASK_CONTROL] đã khởi tạo\n");
    while(1){
        pthread_mutex_lock(&mutex);
        while(!dataReady && !exit_flag){
            pthread_cond_wait(&control_cond,&mutex);    
        }
        if(exit_flag){
            printf("task control erased\n");
            pthread_mutex_unlock(&mutex);
            break;
        }

        //đọc giá trị từ biến toàn cục đa luồng
        int temp = atomic_load(&val);
        
        printf("[TASK_Control] dữ liệu sensor: %d\n",temp);
        
        //xóa event
        dataReady = false;      
        pthread_mutex_unlock(&mutex);

    }
    printf("[TASK_Control] kết thúc\n");
    return NULL;
}
//task xử lý yêu cầu từ bàn phím
void* TASK_Keyboards(void* arg){
    char cmd;

    printf("Nhấn 'r' để RUN, 's' để STOP, 'q' để QUIT\n");

    printf("[TASK_Keyboard]: đã khởi tạo\n");    
    while (1) {
        scanf(" %c", &cmd);

        pthread_mutex_lock(&mutex);
        if (cmd == 'r') {
            run_flag = true;
            pthread_cond_signal(&sen_cond); // Đánh thức task
        } else if (cmd == 's') {
            run_flag = false;
        } else if (cmd == 'q') {
            exit_flag = true;
            pthread_cond_signal(&sen_cond); // Đánh thức nếu đang chờ
            pthread_mutex_unlock(&mutex);
            break;
        }
        pthread_mutex_unlock(&mutex);
    }
    printf("[TASK_Keyboard]: kết thúc\n");
    return NULL;
}
// Main: điều khiển start / stop
int main() {
    srand(time(0));    //thiết lập seed để bắt đầu mô phỏng khi chạy chương trình

    pthread_t sensor_thread,control_thread,keyboard_thread;
    //khởi tạo và chạy các luồng
    pthread_create(&keyboard_thread,NULL,TASK_Keyboards,NULL);
    pthread_create(&sensor_thread, NULL, TASK_Sensor, NULL);
    pthread_create(&control_thread,NULL,TASK_Control,NULL);
   
    //các luồng chạy đồng thời và chờ đợi lần nhau
    pthread_join(keyboard_thread,NULL);
    pthread_join(sensor_thread,NULL);
    pthread_join(control_thread, NULL);

    //giải phóng các luồng
    pthread_mutex_destroy(&mutex);
    printf("Chương trình kết thúc.\n");
    return 0;
}
