// #include "httplib.h" // Bao gồm thư viện httplib
// #include <fstream>
// #include <iostream>
// #include <sstream>
// #include <vector>
// #include <string>
// #include <cstdlib> // Thư viện cho hàm system()

// // Hàm thoát ký tự đặc biệt trong chuỗi để đảm bảo tính hợp lệ của JSON
// std::string escape_json(const std::string& str) {
//     std::string escaped;
//     for (char c : str) {
//         switch (c) {
//             case '\"': escaped += "\\\""; break;
//             case '\\': escaped += "\\\\"; break;
//             case '\n': escaped += "\\n"; break;
//             case '\r': escaped += "\\r"; break;
//             case '\t': escaped += "\\t"; break;
//             default: escaped += c;
//         }
//     }
//     return escaped;
// }

// // Hàm đọc file CSV và chuyển đổi thành chuỗi JSON
// std::string csv_to_json(const std::string& file_path) {
//     std::ifstream file(file_path);
//     if (!file.is_open()) {
//         return "{\"error\": \"File không tìm thấy: " + file_path + "\"}";
//     }

//     std::stringstream json;
//     json << "[";

//     std::string line;
//     std::vector<std::string> headers;
//     bool is_header = true;

//     while (std::getline(file, line)) {
//         std::stringstream line_stream(line);
//         std::string cell;
//         std::vector<std::string> row;

//         while (std::getline(line_stream, cell, ',')) {
//             row.push_back(escape_json(cell));
//         }

//         if (is_header) {
//             headers = row;
//             is_header = false;
//         } else {
//             json << "{";
//             for (size_t i = 0; i < headers.size() && i < row.size(); ++i) {
//                 json << "\"" << escape_json(headers[i]) << "\": \"" << row[i] << "\"";
//                 if (i < headers.size() - 1) {
//                     json << ", ";
//                 }
//             }
//             json << "}, ";
//         }
//     }

//     std::string result = json.str();
//     if (result.back() == ' ') {
//         result.pop_back();
//         result.pop_back();
//     }
//     result += "]";

//     return result;
// }

// // Hàm để phục vụ file bất kỳ
// std::function<void(const httplib::Request&, httplib::Response&)> serve_file(const std::string& file_path, const std::string& content_type) {
//     return [file_path, content_type](const httplib::Request& _req, httplib::Response& res) {
//         // Ép sử dụng _req để tránh cảnh báo unused parameter
//         (void)_req;
//         std::ifstream file(file_path);
//         if (file.is_open()) {
//             std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
//             res.set_content(content, content_type);
//         } else {
//             res.status = 404;
//             res.set_content("File không tìm thấy: " + file_path, "text/plain");
//         }
//     };
// }

// int main() {
//     httplib::Server svr;

//     // Endpoint để phục vụ file index.html
//     svr.Get("/", serve_file("UI\\index.html", "text/html"));
//     // Endpoint để phục vụ các file khác như CSS và JavaScript
//     svr.Get("/styles.css", serve_file("UI\\styles.css", "text/css"));
//     svr.Get("/script.js", serve_file("UI\\script.js", "application/javascript"));

//     // Endpoint để lấy dữ liệu từ file CSV và trả về dưới dạng JSON
//     svr.Get("/data", [](const httplib::Request& _req, httplib::Response& res) {
//         // Ép sử dụng _req để tránh cảnh báo unused parameter
//         (void)_req;
//         std::string json_content = csv_to_json("Data\\Database.csv");
//         if (json_content.find("error") != std::string::npos) {
//             res.status = 404;
//             res.set_content(json_content, "application/json");
//         } else {
//             res.set_content(json_content, "application/json");
//         }
//     });

//     // Thông báo server đã chạy
//     std::cout << "Server đang chạy tại http://localhost:8080\n";

//     // Tự động mở trình duyệt trên macOS hoặc Windows
//     #ifdef _WIN32
//         system("start http://localhost:8080");
//     #elif __APPLE__
//         system("open http://localhost:8080");
//     #endif

//     // Lắng nghe trên cổng 8080
//     svr.listen("localhost", 8080);

//     return 0;
// }


#include "httplib.h" // Bao gồm thư viện httplib
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib> // Thư viện cho hàm system()

// Hàm thoát ký tự đặc biệt trong chuỗi để đảm bảo tính hợp lệ của JSON
std::string escape_json(const std::string& str) {
    std::string escaped;
    for (char c : str) {
        switch (c) {
            case '\"': escaped += "\\\""; break;
            case '\\': escaped += "\\\\"; break;
            case '\n': escaped += "\\n"; break;
            case '\r': escaped += "\\r"; break;
            case '\t': escaped += "\\t"; break;
            default: escaped += c;
        }
    }
    return escaped;
}

// Hàm đọc file CSV và chuyển đổi thành chuỗi JSON
std::string csv_to_json(const std::string& file_path) {
    std::ifstream file(file_path);
    if (!file.is_open()) {
        return "{\"error\": \"File không tìm thấy: " + file_path + "\"}";
    }

    std::stringstream json;
    json << "[";

    std::string line;
    std::vector<std::string> headers;
    bool is_header = true;

    while (std::getline(file, line)) {
        std::stringstream line_stream(line);
        std::string cell;
        std::vector<std::string> row;

        while (std::getline(line_stream, cell, ',')) {
            row.push_back(escape_json(cell));
        }

        if (is_header) {
            headers = row;
            is_header = false;
        } else {
            json << "{";
            for (size_t i = 0; i < headers.size() && i < row.size(); ++i) {
                json << "\"" << escape_json(headers[i]) << "\": \"" << row[i] << "\"";
                if (i < headers.size() - 1) {
                    json << ", ";
                }
            }
            json << "}, ";
        }
    }

    std::string result = json.str();
    if (result.back() == ' ') {
        result.pop_back();
        result.pop_back();
    }
    result += "]";

    return result;
}

// Hàm để phục vụ file bất kỳ
std::function<void(const httplib::Request&, httplib::Response&)> serve_file(const std::string& file_path, const std::string& content_type) {
    return [file_path, content_type](const httplib::Request& _req, httplib::Response& res) {
        // Ép sử dụng _req để tránh cảnh báo unused parameter
        (void)_req;
        std::ifstream file(file_path);
        if (file.is_open()) {
            std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
            res.set_content(content, content_type);
        } else {
            res.status = 404;
            res.set_content("File không tìm thấy: " + file_path, "text/plain");
        }
    };
}

int main() {
    httplib::Server svr;

    // Endpoint để phục vụ file index.html
    svr.Get("/", serve_file("UI\\index.html", "text/html"));
    // Endpoint để phục vụ các file khác như CSS và JavaScript
    svr.Get("/styles.css", serve_file("UI\\styles.css", "text/css"));
    svr.Get("/script.js", serve_file("UI\\script.js", "application/javascript"));

    // Endpoint để lấy dữ liệu từ file CSV và trả về dưới dạng JSON
    svr.Get("/data", [](const httplib::Request& _req, httplib::Response& res) {
        // Ép sử dụng _req để tránh cảnh báo unused parameter
        (void)_req;
        std::string json_content = csv_to_json("Data\\Database.csv");
        if (json_content.find("error") != std::string::npos) {
            res.status = 404;
            res.set_content(json_content, "application/json");
        } else {
            res.set_content(json_content, "application/json");
        }
    });

    // Thông báo server đã chạy
    std::cout << "Server đang chạy tại http://localhost:8080\n";

    // Tự động mở trình duyệt trên Windows
    #ifdef _WIN32
        system("start http://localhost:8080");
    #elif __APPLE__
        system("open http://localhost:8080");
    #endif

    // Lắng nghe trên cổng 8080
    svr.listen("localhost", 8080);

    return 0;
}
