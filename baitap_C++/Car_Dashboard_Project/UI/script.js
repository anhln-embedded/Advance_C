// Biến toàn cục để quản lý các interval của xi nhan
let leftInterval = null;
let rightInterval = null;

// Biến toàn cục để lưu giá trị trước đó của TURN_SIGNAL
let previousTurnSignal = null;

// Bản đồ ánh xạ tên phím đầu vào với ký tự hiển thị trong HTML
const keyMap = {
    'UP': '↑',
    'DOWN': '↓',
    'RIGHT': '→',
    'V': 'V',
    'B': 'B',
    'SPACE': 'Space',
    'ENTER': 'Enter',
    'N': 'N',
    'M': 'M'
};

/* ========================
   Các hàm chính của hệ thống
   ======================== */

/**
 * Hàm điều khiển xi nhan (trái, phải, tắt)
 * @param {number} input - Giá trị đầu vào (1: xi nhan trái, 2: xi nhan phải, 0: tắt)
 */
function controlTurnSignal(input) {
    clearIntervals(); // Xóa các interval cũ để tránh xung đột

    if (input === 1) {
        // Tắt cả hai xi nhan phải
        setVisibility('.indicator-right', 'hidden');
        // Xi nhan trái
        leftInterval = setInterval(() => {
            toggleVisibility('.indicator-left');
        }, 500);
    } else if (input === 2) {
        // Tắt cả hai xi nhan trái
        setVisibility('.indicator-left', 'hidden');
        // Xi nhan phải
        rightInterval = setInterval(() => {
            toggleVisibility('.indicator-right');
        }, 500);
    } else if (input === 0) {
        // Tắt cả hai xi nhan
        setVisibility('.indicator-left', 'hidden');
        setVisibility('.indicator-right', 'hidden');
    }
}

/**
 * Hàm thay đổi trạng thái hiển thị của phần tử
 * @param {string} selector - CSS selector của phần tử
 */
function toggleVisibility(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.style.visibility = (element.style.visibility === 'hidden') ? 'visible' : 'hidden';
    }
}

/**
 * Hàm thiết lập trạng thái hiển thị cụ thể cho phần tử
 * @param {string} selector - CSS selector của phần tử
 * @param {string} state - Trạng thái hiển thị ('hidden' hoặc 'visible')
 */
function setVisibility(selector, state) {
    const element = document.querySelector(selector);
    if (element) {
        element.style.visibility = state;
    }
}

/**
 * Hàm xóa các interval hiện tại
 */
function clearIntervals() {
    if (leftInterval !== null) {
        clearInterval(leftInterval);
        leftInterval = null;
    }
    if (rightInterval !== null) {
        clearInterval(rightInterval);
        rightInterval = null;
    }
}

/**
 * Hàm thay đổi trạng thái phím trong giao diện
 * @param {string} keyName - Tên phím
 * @param {number} state - Trạng thái phím (1: nhấn, 0: thả)
 */
function changeKeyState(keyName, state) {
    state = parseInt(state, 10);
    const keyToChange = keyMap[keyName.toUpperCase()];

    if (!keyToChange) {
        console.warn(`Key "${keyName}" không tìm thấy trong bản đồ ánh xạ.`);
        return;
    }

    const keys = document.querySelectorAll('.key');
    keys.forEach(key => {
        if (key.textContent.trim() === keyToChange) {
            if (state === 1) {
                key.classList.add('active');
            } else {
                key.classList.remove('active');
            }
        }
    });
}

/* ========================
   Các hàm cập nhật hiển thị thông tin
   ======================== */

/**
 * Hàm cập nhật trạng thái gạch chân cho chế độ lái
 * @param {string} mode - Chế độ lái (ECO, SPORT, NORMAL, v.v.)
 */
function underlineStatus(mode) {
    const statusItems = document.querySelectorAll('.status-item');
    statusItems.forEach(item => {
        item.style.textDecoration = 'none';
        if (item.textContent.trim() === mode) {
            item.style.textDecoration = 'underline';
            item.style.textDecorationColor = 'red';
            item.style.textDecorationThickness = '3px';
        }
    });
}

/**
 * Hàm thay đổi màu số xe
 * @param {string} gear - Tên số xe (P, R, N, D, v.v.)
 */
function changeGearColor(gear) {
    const gears = document.querySelectorAll('.dashboard-gear span');
    gears.forEach(element => {
        element.style.color = '';
        if (element.textContent.trim() === gear) {
            element.style.color = 'limegreen';
        }
    });
}

/**
 * Hàm cập nhật khoảng cách dự kiến
 * @param {number} distance - Khoảng cách (km)
 */
function updateDistance(distance) {
    const batteryDistanceElement = document.querySelector('.battery-distance');
    const distanceValueElement = document.querySelector('.details-value');
    if (batteryDistanceElement && distanceValueElement) {
        batteryDistanceElement.textContent = `${distance} km`;
        distanceValueElement.textContent = `${distance} km`;
    }
}

/**
 * Hàm cập nhật phần trăm pin
 * @param {number} percentage - Phần trăm pin (0-100)
 */
function updateBattery(percentage) {
    percentage = Math.min(Math.max(percentage, 0), 100);
    const batteryBarFill = document.querySelector('.battery-bar-fill');
    const batteryPercentageElement = document.querySelector('.battery-percentage');
    if (batteryBarFill && batteryPercentageElement) {
        batteryBarFill.style.width = `${percentage}%`;
        batteryPercentageElement.textContent = `${percentage}%`;
    }
}

/**
 * Hàm cập nhật quãng đường trên đồng hồ đo
 * @param {number} distance - Quãng đường (km)
 */
function updateOdometer(distance) {
    const odometerValueElement = document.querySelector('.odometer-value');
    if (odometerValueElement) {
        odometerValueElement.textContent = `${distance} km`;
    }
}

/**
 * Hàm xử lý trạng thái phanh
 * @param {number} value - Trạng thái phanh (1: đang phanh, 0: không phanh)
 */
function handleBrakeStatus(value) {
    value = parseInt(value, 10);
    const brakeButton = document.querySelector('.brake-button');
    if (brakeButton) {
        brakeButton.style.backgroundColor = value === 1 ? 'gray' : '';
    }
}

/**
 * Hàm xử lý trạng thái ga
 * @param {number} value - Trạng thái ga (1: đang đạp, 0: không đạp)
 */
function handleAcceleratorStatus(value) {
    value = parseInt(value, 10);
    const handbrakeButton = document.querySelector('.handbrake-button');
    if (handbrakeButton) {
        handbrakeButton.style.backgroundColor = value === 1 ? 'gray' : '';
    }
}

/**
 * Hàm cập nhật mức pin
 * @param {number} percentage - Mức phần trăm pin (0-100)
 */
function updateBatteryLevel(percentage) {
    percentage = Math.min(Math.max(percentage, 0), 100);
    const batteryLevelFill = document.querySelector('.battery-level-fill');
    const batteryLevelPercentage = document.querySelector('.battery-level-percentage');
    if (batteryLevelFill && batteryLevelPercentage) {
        batteryLevelFill.style.width = `${percentage}%`;
        batteryLevelPercentage.textContent = `${percentage}%`;
        batteryLevelFill.style.backgroundColor = percentage > 50 ? 'limegreen' : (percentage > 20 ? 'orange' : 'red');
    }
}

/**
 * Hàm cập nhật nhiệt độ pin
 * @param {number} temperature - Nhiệt độ (°C)
 */
function updateTemperature(temperature) {
    temperature = parseFloat(temperature);
    const temperatureValueElement = document.querySelector('.details-item:nth-child(2) .details-value');
    if (temperatureValueElement) {
        temperatureValueElement.textContent = `${temperature}°C`;
    }
}

/**
 * Hàm cập nhật giá trị điều hòa
 * @param {number} temperature - Nhiệt độ điều hòa (°C)
 */
function updateACValue(temperature) {
    temperature = parseFloat(temperature);
    const acValueElement = document.querySelector('.ac-value');
    if (acValueElement) {
        acValueElement.textContent = `${temperature}°C`;
    }
}

/**
 * Hàm cập nhật mức gió của quạt
 * @param {number} level - Mức gió (1-n)
 */
function updateFanLevel(level) {
    const fanIndicatorsContainer = document.querySelector('.fan-level-indicators');
    if (fanIndicatorsContainer) {
        fanIndicatorsContainer.innerHTML = '';
        for (let i = 1; i <= level; i++) {
            const fanLevelBar = document.createElement('div');
            fanLevelBar.classList.add('fan-level-bar', `level-${i}`);
            fanIndicatorsContainer.appendChild(fanLevelBar);
        }
    }
}

/* ========================
   Hàm cập nhật dữ liệu từ server
   ======================== */

/**
 * Hàm lấy dữ liệu từ server và cập nhật giao diện
 */
async function fetchData() {
    try {
        const response = await fetch('/data');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();

        data.forEach(item => {
            switch (item.key) {
                case 'VEHICLE_SPEED':
                    document.querySelector('.speed-value').textContent = item.value;
                    break;
                case 'GEAR_SHIFT':
                    changeGearColor(item.value.trim());
                    break;
                case 'DRIVE_MODE':
                    underlineStatus(item.value.trim());
                    break;
                case 'TURN_SIGNAL':
                    // Kiểm tra nếu giá trị mới khác giá trị trước đó
                    if (parseInt(item.value, 10) !== previousTurnSignal) {
                        controlTurnSignal(parseInt(item.value, 10));
                        // Cập nhật giá trị trước đó
                        previousTurnSignal = parseInt(item.value, 10);
                    }
                    break;
                case 'ROUTE_PLANNER':
                    updateDistance(item.value);
                    break;
                case 'BATTERY_LEVEL':
                    updateBattery(item.value);
                    updateBatteryLevel(item.value);
                    break;
                case 'ODOMETER':
                    updateOdometer(item.value);
                    break;
                case 'BRAKE':
                    handleBrakeStatus(item.value);
                    break;
                case 'ACCELERATOR':
                    handleAcceleratorStatus(item.value);
                    break;
                case 'BATTERY_TEMP':
                    updateTemperature(item.value);
                    break;
                case 'AC_CONTROL':
                    updateACValue(item.value);
                    break;
                case 'WIND_LEVEL':
                    updateFanLevel(item.value);
                    break;
                case 'UP':
                case 'DOWN':
                case 'RIGHT':
                case 'V':
                case 'B':
                case 'SPACE':
                case 'ENTER':
                case 'N':
                case 'M':
                    changeKeyState(item.key, item.value);
                    break;
                default:
                    console.warn(`Unhandled key: ${item.key}`, item);
                    break;
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateDashboardTime() {
    // Lấy phần tử HTML có class 'dashboard-time'
    const timeElement = document.querySelector('.dashboard-time');
    
    // Kiểm tra xem phần tử có tồn tại không
    if (timeElement) {
        // Lấy thời gian hiện tại
        const now = new Date();
        
        // Định dạng giờ và phút với định dạng 2 chữ số (HH:MM)
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        // Cập nhật nội dung của phần tử với thời gian hiện tại
        timeElement.textContent = `${hours}:${minutes}`;
    }
}

// Gọi hàm để cập nhật thời gian ban đầu
updateDashboardTime();

// Cập nhật thời gian mỗi phút một lần
setInterval(updateDashboardTime, 60000);


/* ========================
   Khởi chạy quá trình cập nhật dữ liệu
   ======================== */
   document.addEventListener('DOMContentLoaded', () => {
    // Cập nhật dữ liệu lần đầu khi tải trang
    fetchData();
    
    // Cập nhật dữ liệu từ server mỗi 100ms
    setInterval(fetchData, 100);

    // Gọi hàm để cập nhật thời gian ban đầu
    updateDashboardTime();

    // Cập nhật thời gian trên dashboard mỗi phút một lần
    setInterval(updateDashboardTime, 60000);
});

