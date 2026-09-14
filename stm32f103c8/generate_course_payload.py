import os
import glob
import re
import json

md_files = sorted(glob.glob("Bai *.md"))

def extract_metadata(filepath):
    content = open(filepath, "r", encoding="utf-8").read()
    
    # Title
    first_line = content.split("\n")[0].strip()
    title = re.sub(r"^#\s*", "", first_line)
    
    # Order from filename
    fname = os.path.basename(filepath)
    m = re.search(r"Bai\s*(\d+)", fname)
    order = int(m.group(1)) if m else 1
    
    # Slug
    slug = fname.lower()
    slug = re.sub(r"\.md$", "", slug)
    slug = slug.replace("bai ", "bai-")
    # Clean vietnamese accents
    import unicodedata
    slug = unicodedata.normalize("NFD", slug)
    slug = "".join([c for c in slug if not unicodedata.combining(c)])
    slug = slug.replace("đ", "d").replace("Đ", "d")
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    
    # Summary
    summary = ""
    sum_match = re.search(r"> Tóm tắt:\s*(.+)", content)
    if sum_match:
        summary = sum_match.group(1).strip()
    else:
        # First paragraph after # H1
        paras = [p.strip() for p in content.split("\n\n") if p.strip() and not p.strip().startswith("#") and not p.strip().startswith(">") and not p.strip().startswith("<")]
        if paras:
            summary = paras[0][:200]
    
    # Code snippet: extract first c block
    code_match = re.search(r"```c\n([\s\S]*?)```", content)
    code_snippet = code_match.group(1).strip() if code_match else ""
    # Limit snippet if too huge
    if len(code_snippet) > 2500:
        code_snippet = code_snippet[:2500] + "\n// ... (xem tiep trong bai giang)"
        
    return {
        "order": order,
        "title": title,
        "slug": slug,
        "duration": "25 phút" if order > 5 else "20 phút",
        "free": True if order <= 5 else False,
        "summary": summary,
        "contentMarkdown": content,
        "codeSnippet": code_snippet,
        "hasVideo": False,
        "videoUrl": ""
    }

lessons_by_order = {}
for f in md_files:
    meta = extract_metadata(f)
    lessons_by_order[meta["order"]] = meta

# 5 Modules
modules = [
    {
        "module": "Phần 1: Kiến Trúc Cốt Lõi ARM Cortex-M3 & Ngoại Vi Cơ Bản",
        "order": 1,
        "lessons": [lessons_by_order[i] for i in range(1, 6) if i in lessons_by_order]
    },
    {
        "module": "Phần 2: Hệ Thống Định Thời Timers, PWM & Xử Lý Tín Hiệu Tương Tự ADC",
        "order": 2,
        "lessons": [lessons_by_order[i] for i in range(6, 13) if i in lessons_by_order]
    },
    {
        "module": "Phần 3: Các Chuẩn Giao Tiếp Nối Tiếp Công Nghiệp & DMA Controller",
        "order": 3,
        "lessons": [lessons_by_order[i] for i in range(13, 18) if i in lessons_by_order]
    },
    {
        "module": "Phần 4: Quản Lý Năng Lượng & Hệ Điều Hành Thời Gian Thực FreeRTOS",
        "order": 4,
        "lessons": [lessons_by_order[i] for i in range(18, 23) if i in lessons_by_order]
    },
    {
        "module": "Phần 5: Giao Thức Nâng Cao (CAN Bus, USB FS) & Chuyên Gia Firmware",
        "order": 5,
        "lessons": [lessons_by_order[i] for i in range(23, 27) if i in lessons_by_order]
    }
]

course_data = {
    "title": "Lập Trình STM32F103 Chuyên Sâu: ARM Cortex-M3 Bare-Metal & SPL",
    "slug": "lap-trinh-stm32f103-chuyen-sau",
    "description": "Khóa học toàn diện 26 bài học thực chiến STM32F103C8T6 (Blue Pill) từ kiến trúc thanh ghi Cortex-M3, Bit-Banding, Clock Tree, GPIO, Timer PWM/Encoder, ADC, DMA, các chuẩn giao tiếp UART/I2C/SPI/CAN, USB Device, FreeRTOS đa nhiệm thời gian thực và Custom ISP Bootloader.",
    "category": "embedded-rtos",
    "level": "intermediate",
    "duration": "26 bài học (30 giờ)",
    "price": "free",
    "thumbnail": "/images/stm32f103/stm32f103c8.webp",
    "githubRepo": "https://github.com/anhln-embedded/embedded-lab-web",
    "featured": True,
    "tags": ["stm32", "arm-cortex-m3", "bare-metal", "freertos", "embedded-c", "can-bus", "spl"],
    "prerequisites": ["Ngôn ngữ C căn bản (Con trỏ, Struct, Toán tử Bitwise)", "Đã từng tiếp cận vi điều khiển cơ bản"],
    "instructor": "Lưu Ngọc Anh (Admin Lab PTIT)",
    "modules": modules
}

with open("stm32_course_payload.json", "w", encoding="utf-8") as f:
    json.dump(course_data, f, ensure_ascii=False, indent=2)

print(f"Generated stm32_course_payload.json with {len(lessons_by_order)} lessons across {len(modules)} modules.")
