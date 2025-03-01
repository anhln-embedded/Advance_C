#ifndef ENUM_DEFINITIONS_HPP
#define ENUM_DEFINITIONS_HPP

#include <string>
#include <stdexcept>
#include <type_traits>

// Định nghĩa các enum biểu diễn trạng thái và thuộc tính hệ thống
//Enum cho trạng thái ON/OFF của thiết bị
enum class DeviceState{
    ON,
    OFF
};
// Enum cho trạng thái xi-nhan (TURN_SIGNAL)
enum class TurnSignalState
{
    OFF = 0,  // Xi-nhan tắt
    LEFT = 1, // Xi-nhan trái
    RIGHT = 2 // Xi-nhan phải
};

// Enum cho chế độ lái của xe
enum class DriveMode
{
    ECO,  // Chế độ tiết kiệm năng lượng
    SPORT, // Chế độ thể thao
};

// Enum cho trạng thái cần số của xe
enum class GearShift
{
    P, // Đậu xe
    R, // Lùi xe
    N, // Trung tính
    D  // Lái xe
};

// Enum cho trạng thái các phím điều khiển
enum class KeyState
{
    RELEASED = 0, // Phím không nhấn
    PRESSED = 1,   // Phím được nhấn
};

// Enum chung cho trạng thái của phanh (BRAKE) và chân ga (ACCELERATOR)
enum class PedalState
{
    RELEASED = 0, // Không nhấn
    PRESSED = 1,   // Đang nhấn
};

// Enum biểu diễn các thuộc tính trong hệ thống (các key trong Database.csv)
enum class SystemAttribute
{
    VEHICLE_SPEED,
    DRIVE_MODE,
    GEAR_SHIFT,
    TURN_SIGNAL,
    ROUTE_PLANNER,
    BATTERY_LEVEL,
    ODOMETER,
    BRAKE,
    ACCELERATOR,
    BATTERY_TEMP,
    AC_CONTROL,
    AC_STATUS,
    WIND_LEVEL,
    UP,
    DOWN,
    RIGHT,
    V,
    B,
    SPACE,
    ENTER,
    N,
    M,
    UNKNOWN
};

// Hàm chuyển đổi enum thành chuỗi
template <typename EnumType>
inline std::string enumToString(EnumType value)
{
    if constexpr (std::is_same_v<EnumType,TurnSignalState>)
    {
        switch (value)
        {
        case TurnSignalState::OFF:
            return "0";
        case TurnSignalState::LEFT:
            return "1";
        case TurnSignalState::RIGHT:
            return "2";
        default:
            return "UNKNOWN";
        }
    }
    else if constexpr (std::is_same_v<EnumType, DriveMode>)
    {
        switch (value)
        {
        case DriveMode::ECO:
            return "ECO";
        case DriveMode::SPORT:
            return "SPORT";
        default:
            return "UNKNOWN";
        }
    }
    else if constexpr (std::is_same_v<EnumType, GearShift>)
    {
        switch (value)
        {
        case GearShift::P:
            return "P";
        case GearShift::R:
            return "R";
        case GearShift::N:
            return "N";
        case GearShift::D:
            return "D";
        default:
            return "UNKNOWN";
        }
    }
    else if constexpr (std::is_same_v<EnumType, KeyState>)
    {
        switch (value)
        {
        case KeyState::RELEASED:
            return "0";
        case KeyState::PRESSED:
            return "1";
        default:
            return "UNKNOWN";
        }
    }
    else if constexpr (std::is_same_v<EnumType, PedalState>)
    {
        switch (value)
        {
        case PedalState::RELEASED:
            return "0";
        case PedalState::PRESSED:
            return "1";
        default:
            return "UNKNOWN";
        }
    }
    else if constexpr (std::is_same_v<EnumType, DeviceState>)
    {
        switch (value)
        {
        case DeviceState::OFF:
            return "0";
        case DeviceState::ON:
            return "1";
        default:
            return "UNKNOWN";
        }
    }
    
    else if constexpr (std::is_same_v<EnumType, SystemAttribute>)
    {
        switch (value)
        {
        case SystemAttribute::VEHICLE_SPEED:
            return "VEHICLE_SPEED";
        case SystemAttribute::DRIVE_MODE:
            return "DRIVE_MODE";
        case SystemAttribute::GEAR_SHIFT:
            return "GEAR_SHIFT";
        case SystemAttribute::TURN_SIGNAL:
            return "TURN_SIGNAL";
        case SystemAttribute::ROUTE_PLANNER:
            return "ROUTE_PLANNER";
        case SystemAttribute::BATTERY_LEVEL:
            return "BATTERY_LEVEL";
        case SystemAttribute::ODOMETER:
            return "ODOMETER";
        case SystemAttribute::BRAKE:
            return "BRAKE";
        case SystemAttribute::ACCELERATOR:
            return "ACCELERATOR";
        case SystemAttribute::BATTERY_TEMP:
            return "BATTERY_TEMP";
        case SystemAttribute::AC_CONTROL:
            return "AC_CONTROL";
        case SystemAttribute::AC_STATUS:
            return "AC_STATUS";
        case SystemAttribute::WIND_LEVEL:
            return "WIND_LEVEL";
        case SystemAttribute::UP:
            return "UP";
        case SystemAttribute::DOWN:
            return "DOWN";
        case SystemAttribute::RIGHT:
            return "RIGHT";
        case SystemAttribute::V:
            return "V";
        case SystemAttribute::B:
            return "B";
        case SystemAttribute::SPACE:
            return "SPACE";
        case SystemAttribute::ENTER:
            return "ENTER";
        case SystemAttribute::N:
            return "N";
        case SystemAttribute::M:
            return "M";
        default:
            return "UNKNOWN";
        }
    }
    else
    {
        return "UNKNOWN";
    }
}

// Hàm chuyển đổi chuỗi thành enum
template <typename EnumType>
EnumType stringToEnum(const std::string &str)
{
    if constexpr (std::is_same_v<EnumType, TurnSignalState>)
    {
        if (str == "0")
            return TurnSignalState::OFF;
        if (str == "1")
            return TurnSignalState::LEFT;
        if (str == "2")
            return TurnSignalState::RIGHT;
    }
    else if constexpr (std::is_same_v<EnumType, DriveMode>)
    {
        if (str == "ECO")
            return DriveMode::ECO;
        if (str == "SPORT")
            return DriveMode::SPORT;
    }
    else if constexpr (std::is_same_v<EnumType, GearShift>)
    {
        if (str == "P")
            return GearShift::P;
        if (str == "R")
            return GearShift::R;
        if (str == "N")
            return GearShift::N;
        if (str == "D")
            return GearShift::D;
    }
    else if constexpr (std::is_same_v<EnumType, KeyState>)
    {
        if (str == "0")
            return KeyState::RELEASED;
        if (str == "1")
            return KeyState::PRESSED;
    }
    else if constexpr (std::is_same_v<EnumType, PedalState>)
    {
        if (str == "0")
            return PedalState::RELEASED;
        if (str == "1")
            return PedalState::PRESSED;
    }
    else if constexpr (std::is_same_v<EnumType,DeviceState>)
    {
        if (str == "0")
            return DeviceState::OFF;
        if (str == "1")
            return DeviceState::ON;
    }
    else
    {
        throw std::invalid_argument("Hàm stringToEnum không hỗ trợ loại enum này");
    }
    throw std::invalid_argument("Giá trị chuỗi không hợp lệ cho enum");
}

#endif // ENUM_DEFINITIONS_HPP
