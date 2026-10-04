"""Build the DDM501 final-report slide deck from baocao/slide_dan_y.md."""

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

OUT = r"C:\Users\XPS\Desktop\CaoHoc\AI_DevOp\ddm501-lab1-starter\ml-monitoring\baocao\Bao_cao_cuoi_ky_DDM501.pptx"

W, H = 13.333, 7.5
FONT = "Segoe UI"

NAVY = RGBColor(0x0C, 0x23, 0x40)
NAVY_MID = RGBColor(0x14, 0x36, 0x5C)
INK = RGBColor(0x1A, 0x23, 0x32)
MUTED = RGBColor(0x5C, 0x6B, 0x7A)
ORANGE = RGBColor(0xE8, 0x6A, 0x17)
CREAM = RGBColor(0xF6, 0xF4, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xE3, 0xDD, 0xD4)
TEAL = RGBColor(0x0E, 0x6B, 0x64)
GREEN = RGBColor(0x1B, 0x7A, 0x4A)
SOFT_ORANGE = RGBColor(0xFF, 0xF1, 0xE6)
SOFT_TEAL = RGBColor(0xE6, 0xF4, 0xF2)
SOFT_NAVY = RGBColor(0xE8, 0xEE, 0xF6)
SOFT_GREEN = RGBColor(0xE7, 0xF6, 0xEE)
PALE = RGBColor(0xC5, 0xD0, 0xDC)
LIGHT = RGBColor(0xF0, 0xF4, 0xF8)

TOTAL = 9

STUDENTS = [
    ("Phạm Minh Hoàng", "25MS13285"),
    ("Nguyễn Công Trọng", "25MS13297"),
    ("Ngô Minh Khôi", "25MSA13236"),
]


def style_run(run, size, bold, color, font=FONT):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    for tag in ("latin", "ea", "cs"):
        el = rpr.find(qn(f"a:{tag}"))
        if el is None:
            el = etree.SubElement(rpr, qn(f"a:{tag}"))
        el.set("typeface", font)


def _box(slide, x, y, w, h):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    return shape, tf


def text(slide, content, x, y, w, h, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    shape, tf = _box(slide, x, y, w, h)
    tf.anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    run = p.add_run()
    run.text = content
    style_run(run, size, bold, color)
    return shape


def rich(slide, paragraphs, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    """paragraphs: list of list of (text, size, bold, color)."""
    shape, tf = _box(slide, x, y, w, h)
    tf.anchor = anchor
    for i, parts in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(0)
        p.space_after = Pt(parts[-1] if isinstance(parts[-1], (int, float)) else 0)
        runs = parts[:-1] if isinstance(parts[-1], (int, float)) else parts
        if isinstance(parts[-1], (int, float)):
            p.space_after = Pt(parts[-1])
        for item in runs:
            run = p.add_run()
            run.text = item[0]
            style_run(run, item[1], item[2], item[3])
    return shape


def rect(slide, x, y, w, h, fill, line=None, radius=0.08):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    if radius:
        try:
            shape.adjustments[0] = radius
        except Exception:
            pass
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    return shape


def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def chrome(slide, kicker, title, page):
    set_bg(slide, CREAM)
    rect(slide, 0, 0, W, 0.08, ORANGE, radius=0)
    text(slide, kicker.upper(), 0.48, 0.2, 9.5, 0.26, 11, True, ORANGE)
    text(slide, title, 0.46, 0.44, 12.2, 0.48, 26, True, NAVY)
    rect(slide, 0.48, 1.02, 1.15, 0.045, ORANGE, radius=0)
    rect(slide, 0.48, 7.08, 12.38, 0.01, LINE, radius=0)
    text(slide, "DDM501  ·  AI trong sản xuất  ·  FPT University", 0.48, 7.14, 9.2, 0.28, 11, False, MUTED)
    text(slide, f"{page:02d}  /  {TOTAL:02d}", 10.5, 7.14, 2.35, 0.28, 11, True, NAVY, PP_ALIGN.RIGHT)


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def slide_title(prs):
    s = new_slide(prs)
    set_bg(s, NAVY)
    rect(s, 0, 0, 0.14, H, ORANGE, radius=0)
    rect(s, 0, 0, W, 0.08, ORANGE, radius=0)

    text(s, "FPT UNIVERSITY", 0.62, 0.38, 6, 0.28, 13, True, ORANGE)
    text(s, "Đại học FPT   ·   Tháng 10 / 2026", 0.62, 0.68, 7, 0.26, 13, False, PALE)

    text(s, "BÁO CÁO CUỐI KỲ", 0.62, 1.55, 8, 0.32, 15, True, ORANGE)
    text(s, "Hệ thống MLOps\nEnd-to-End", 0.58, 1.95, 8.2, 1.7, 40, True, WHITE)
    rect(s, 0.64, 3.82, 2.1, 0.055, ORANGE, radius=0)
    text(
        s,
        "Phân loại chất lượng rượu vang với giám sát Data Drift\nvà tự động tái huấn luyện mô hình",
        0.62, 4.02, 7.6, 0.7, 16, False, RGBColor(0xD5, 0xDE, 0xE8),
    )

    rect(s, 0.5, 5.05, 12.35, 2.05, NAVY_MID, radius=0.06)

    text(s, "MÔN HỌC", 0.78, 5.22, 3.6, 0.24, 11, True, ORANGE)
    text(s, "AI trong sản xuất", 0.78, 5.5, 3.8, 0.3, 15, True, WHITE)
    text(s, "DevOps, DataOps, MLOps", 0.78, 5.84, 3.8, 0.26, 13, False, PALE)
    text(s, "Mã môn: DDM501", 0.78, 6.16, 3.8, 0.26, 13, False, PALE)

    rect(s, 4.75, 5.32, 0.012, 1.5, RGBColor(0x2C, 0x4E, 0x74), radius=0)
    text(s, "GIẢNG VIÊN HƯỚNG DẪN", 5.05, 5.22, 3.3, 0.24, 11, True, ORANGE)
    text(s, "Nguyen Doan Dong", 5.05, 5.58, 3.4, 0.36, 18, True, WHITE)

    rect(s, 8.45, 5.32, 0.012, 1.5, RGBColor(0x2C, 0x4E, 0x74), radius=0)
    text(s, "SINH VIÊN THỰC HIỆN", 8.75, 5.22, 3.8, 0.24, 11, True, ORANGE)
    for i, (name, sid) in enumerate(STUDENTS):
        y = 5.54 + i * 0.42
        text(s, name, 8.75, y, 2.45, 0.32, 13, True, WHITE)
        text(s, sid, 11.15, y, 1.45, 0.32, 13, False, PALE, PP_ALIGN.RIGHT)


def slide_problem(prs):
    s = new_slide(prs)
    chrome(s, "01  ·  Mở đầu", "Đặt vấn đề và mục tiêu dự án", 2)

    rect(s, 0.42, 1.28, 5.55, 5.55, WHITE, radius=0.05)
    rect(s, 0.42, 1.28, 0.08, 5.55, ORANGE, radius=0)
    text(s, "BỐI CẢNH", 0.72, 1.46, 4.8, 0.26, 12, True, ORANGE)
    text(s, "Mô hình rời production\nvì thiếu vòng đời khép kín", 0.72, 1.78, 4.9, 0.85, 20, True, NAVY)

    rect(s, 0.72, 2.8, 4.9, 1.55, SOFT_ORANGE, radius=0.08)
    text(s, "80%+", 0.92, 2.95, 4.5, 0.55, 32, True, ORANGE)
    text(
        s,
        "mô hình ML không vào được production, hoặc suy giảm hiệu năng theo thời gian.",
        0.92, 3.55, 4.5, 0.65, 13, False, INK,
    )

    text(s, "Hidden technical debt", 0.72, 4.55, 4.9, 0.28, 14, True, NAVY)
    text(
        s,
        "Nợ kỹ thuật ẩn khiến mô hình khó vận hành, khó kiểm soát và khó sửa khi dữ liệu đổi.",
        0.72, 4.88, 4.9, 0.7, 13, False, MUTED,
    )
    text(s, "Đứt gãy quy trình", 0.72, 5.55, 4.9, 0.28, 14, True, NAVY)
    text(
        s,
        "Thiếu cầu nối tự động giữa dữ liệu, huấn luyện, triển khai và giám sát.",
        0.72, 5.88, 4.9, 0.65, 13, False, MUTED,
    )

    rect(s, 6.15, 1.28, 6.75, 5.55, WHITE, radius=0.05)
    text(s, "MỤC TIÊU", 6.42, 1.46, 6.2, 0.26, 12, True, ORANGE)
    text(s, "Xây dựng MLOps khép kín", 6.42, 1.76, 6.2, 0.36, 18, True, NAVY)

    goals = [
        ("01", "Kiến trúc microservices", "8 dịch vụ Docker, tách serving, tracking, giám sát và điều phối."),
        ("02", "Dự đoán thời gian thực", "REST API độ trễ thấp, nhận request và trả kết quả trực tiếp."),
        ("03", "Vòng đời mô hình", "MLflow theo dõi thí nghiệm và Model Registry quản lý phiên bản."),
        ("04", "Quan sát và phát hiện drift", "Prometheus, Grafana và Evidently so sánh dữ liệu mới với baseline."),
        ("05", "Tái huấn luyện liên tục", "Airflow tự chạy lại pipeline khi tỷ lệ drift vượt ngưỡng."),
        ("06", "Chất lượng mã nguồn", "Unit test coverage ≥ 80% và CI/CD tự động trên GitHub Actions."),
    ]
    for i, (num, title, desc) in enumerate(goals):
        y = 2.28 + i * 0.72
        text(s, num, 6.42, y, 0.48, 0.32, 13, True, ORANGE)
        text(s, title, 6.98, y - 0.02, 5.6, 0.28, 14, True, NAVY)
        text(s, desc, 6.98, y + 0.26, 5.65, 0.36, 12, False, MUTED)


def slide_architecture(prs):
    s = new_slide(prs)
    chrome(s, "02  ·  Thiết kế", "Kiến trúc hệ thống tổng thể", 3)
    text(s, "Tám dịch vụ Docker, một vòng dữ liệu khép kín.", 0.48, 1.16, 10, 0.3, 14, False, MUTED)

    services = [
        ("API", "FastAPI", ":8000", "Nhận request, dự đoán, xuất metrics"),
        ("TRACKING", "MLflow", ":5000", "Metadata, artifact và registry"),
        ("FLOW", "Airflow Web", ":8080", "Điều phối pipeline 5 bước"),
        ("FLOW", "Scheduler", "Airflow", "Lên lịch và thực thi DAG"),
        ("DRIFT", "Evidently", ":8001", "So sánh reference với current"),
        ("OBS", "Prometheus", ":9090", "Cào metrics vận hành"),
        ("OBS", "Grafana", ":3000", "Dashboard thời gian thực"),
        ("DATA", "PostgreSQL", ":5432", "State cho Airflow và MLflow"),
    ]
    colors = {
        "API": ORANGE,
        "TRACKING": TEAL,
        "FLOW": NAVY,
        "DRIFT": RGBColor(0xB4, 0x53, 0x09),
        "OBS": RGBColor(0x1D, 0x4E, 0x89),
        "DATA": RGBColor(0x3D, 0x4F, 0x63),
    }
    gap = 0.16
    card_w = (12.42 - 3 * gap) / 4
    card_h = 1.42
    for i, (kind, name, port, desc) in enumerate(services):
        col, row = i % 4, i // 4
        x = 0.46 + col * (card_w + gap)
        y = 1.56 + row * (card_h + 0.14)
        rect(s, x, y, card_w, card_h, WHITE, radius=0.08)
        rect(s, x, y, card_w, 0.08, colors[kind], radius=0)
        text(s, kind, x + 0.16, y + 0.18, card_w - 0.3, 0.22, 10, True, colors[kind])
        text(s, name, x + 0.16, y + 0.4, card_w - 0.3, 0.32, 16, True, NAVY)
        text(s, port, x + 0.16, y + 0.74, card_w - 0.3, 0.22, 12, True, ORANGE)
        text(s, desc, x + 0.16, y + 0.98, card_w - 0.32, 0.34, 11, False, MUTED)

    rect(s, 0.46, 4.72, 12.42, 2.18, WHITE, radius=0.05)
    text(s, "LUỒNG KHÉP KÍN", 0.68, 4.86, 4, 0.24, 11, True, ORANGE)

    def flow(y, nodes, fills):
        count = len(nodes)
        arrow_w = 0.32
        node_w = (11.7 - (count - 1) * arrow_w) / count
        x = 0.72
        for i, (label, fill) in enumerate(zip(nodes, fills)):
            font_c = WHITE if fill in (NAVY, TEAL, ORANGE) else NAVY
            pill = rect(s, x, y, node_w, 0.46, fill, radius=0.3)
            tf = pill.text_frame
            tf.word_wrap = False
            tf.anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = Inches(0.04)
            tf.margin_right = Inches(0.04)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = label
            style_run(run, 12, True, font_c)
            x += node_w
            if i < count - 1:
                text(s, "→", x, y + 0.04, arrow_w, 0.38, 16, True, ORANGE, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
                x += arrow_w

    text(s, "Phục vụ", 0.68, 5.2, 1.2, 0.22, 11, True, MUTED)
    flow(5.42, ["User request", "FastAPI", "Prometheus", "Grafana"], [SOFT_NAVY, ORANGE, NAVY, TEAL])
    text(s, "Tái huấn luyện", 0.68, 6.02, 2.2, 0.22, 11, True, MUTED)
    flow(
        6.24,
        ["Dữ liệu mới", "Evidently", "Airflow DAG", "MLflow Production"],
        [SOFT_NAVY, ORANGE, NAVY, TEAL],
    )


def slide_data(prs):
    s = new_slide(prs)
    chrome(s, "03  ·  Mô hình", "Dữ liệu và pipeline học máy", 4)

    rect(s, 0.42, 1.24, 6.15, 2.35, WHITE, radius=0.05)
    text(s, "BỘ DỮ LIỆU", 0.64, 1.38, 5.6, 0.22, 11, True, ORANGE)
    text(s, "Wine Quality", 0.64, 1.62, 5.6, 0.34, 20, True, NAVY)
    facts = [
        ("Nguồn", "sklearn.datasets.load_wine()"),
        ("Quy mô", "178 mẫu hóa nghiệm, vùng Piedmont, Ý"),
        ("Bài toán", "Phân loại 3 lớp chất lượng rượu"),
    ]
    for i, (k, v) in enumerate(facts):
        y = 2.06 + i * 0.32
        text(s, k, 0.64, y, 1.15, 0.28, 12, True, TEAL)
        text(s, v, 1.85, y, 4.5, 0.28, 12, False, INK)
    text(s, "Đặc trưng", 0.64, 3.04, 1.15, 0.24, 12, True, TEAL)
    text(s, "13 chỉ số hóa học, gồm Alcohol, Flavanoids, Color Intensity và Proline.", 1.85, 3.02, 4.45, 0.46, 12, False, INK)

    rect(s, 6.75, 1.24, 6.15, 2.35, WHITE, radius=0.05)
    text(s, "MÔ HÌNH", 6.97, 1.38, 5.6, 0.22, 11, True, ORANGE)
    text(s, "Random Forest", 6.97, 1.62, 5.6, 0.34, 20, True, NAVY)
    chips = [("100 cây", SOFT_ORANGE, ORANGE), ("random_state = 42", SOFT_TEAL, TEAL), ("Đa lớp", SOFT_NAVY, NAVY)]
    cx = 6.97
    for label, bg, fg in chips:
        width = 0.42 + len(label) * 0.105
        chip = rect(s, cx, 2.08, width, 0.34, bg, radius=0.4)
        tf = chip.text_frame
        tf.anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = label
        style_run(run, 11, True, fg)
        cx += width + 0.1
    reasons = [
        "Ổn định trên tập nhỏ, ít nhạy với nhiễu đơn lẻ.",
        "Chống overfitting tốt hơn một cây quyết định.",
        "Trích được feature importance để giải thích dự đoán.",
    ]
    for i, line in enumerate(reasons):
        y = 2.56 + i * 0.3
        text(s, "▸", 6.97, y, 0.28, 0.28, 13, True, ORANGE)
        text(s, line, 7.28, y, 5.3, 0.28, 13, False, INK)

    text(s, "NĂM MODULE TRONG src/", 0.48, 3.78, 6, 0.26, 12, True, ORANGE)
    modules = [
        ("01", "data_pipeline.py", "Nạp dữ liệu, kiểm tra định dạng, chia train/test stratified 80/20."),
        ("02", "feature_engineering.py", "Chuẩn hóa đặc trưng bằng StandardScaler."),
        ("03", "train.py", "Huấn luyện Random Forest, cross-validation 5-fold, ghi MLflow."),
        ("04", "evaluate.py", "Accuracy, Precision, Recall, F1-score và confusion matrix."),
        ("05", "explainability.py", "Xếp hạng mức quan trọng của từng đặc trưng hóa học."),
    ]
    for i, (num, name, desc) in enumerate(modules):
        x = 0.42 + i * 2.55
        rect(s, x, 4.18, 2.42, 2.55, WHITE, radius=0.06)
        rect(s, x, 4.18, 2.42, 0.08, ORANGE if i % 2 == 0 else TEAL, radius=0)
        text(s, num, x + 0.14, 4.36, 2.14, 0.22, 12, True, ORANGE)
        text(s, name, x + 0.14, 4.6, 2.16, 0.46, 12, True, NAVY)
        text(s, desc, x + 0.14, 5.12, 2.14, 1.4, 13, False, INK)


def slide_monitor(prs):
    s = new_slide(prs)
    chrome(s, "04  ·  Vận hành", "Giám sát hệ thống và phát hiện Data Drift", 5)

    rect(s, 0.42, 1.24, 6.15, 2.55, WHITE, radius=0.05)
    text(s, "PROMETHEUS  +  GRAFANA", 0.64, 1.4, 5.7, 0.24, 12, True, ORANGE)
    text(s, "Sức khỏe dịch vụ, theo thời gian thực", 0.64, 1.68, 5.7, 0.32, 16, True, NAVY)
    metrics = [
        ("RPS", "Số request mỗi giây"),
        ("Latency", "P50, P95, P99"),
        ("Error rate", "HTTP 4xx và 5xx"),
        ("Output", "Phân phối 3 nhóm chất lượng"),
    ]
    for i, (k, v) in enumerate(metrics):
        col, row = i % 2, i // 2
        x = 0.64 + col * 2.95
        y = 2.16 + row * 0.72
        rect(s, x, y, 2.8, 0.6, SOFT_NAVY, radius=0.08)
        text(s, k, x + 0.14, y + 0.05, 2.5, 0.24, 12, True, NAVY)
        text(s, v, x + 0.14, y + 0.28, 2.5, 0.24, 12, False, MUTED)

    rect(s, 6.75, 1.24, 6.15, 2.55, WHITE, radius=0.05)
    text(s, "EVIDENTLY AI", 6.97, 1.4, 5.7, 0.24, 12, True, ORANGE)
    text(s, "So sánh phân phối với baseline", 6.97, 1.68, 5.7, 0.32, 16, True, NAVY)
    text(
        s,
        "Đo sai khác giữa dữ liệu thực nghiệm và tập tham chiếu ban đầu. Cảnh báo khi đủ nhiều đặc trưng đổi phân phối.",
        6.97, 2.12, 5.7, 0.7, 13, False, INK,
    )
    rect(s, 6.97, 2.9, 5.7, 0.64, SOFT_ORANGE, radius=0.08)
    text(s, "Ngưỡng kích hoạt", 7.15, 2.96, 2.4, 0.24, 12, False, MUTED)
    text(s, "≥ 30% đặc trưng bị drift", 7.15, 3.18, 5.3, 0.28, 16, True, ORANGE)

    text(s, "KỊCH BẢN MÔ PHỎNG", 0.48, 3.98, 6, 0.26, 12, True, ORANGE)

    rect(s, 0.42, 4.34, 6.15, 2.52, WHITE, radius=0.05)
    rect(s, 0.42, 4.34, 0.08, 2.52, TEAL, radius=0)
    text(s, "GIAI ĐOẠN 1  ·  BASELINE", 0.7, 4.5, 5.6, 0.24, 12, True, TEAL)
    text(s, "100 request bình thường", 0.7, 4.8, 5.6, 0.36, 18, True, NAVY)
    text(
        s,
        "Dữ liệu giữ phân phối gốc. Evidently không vượt ngưỡng. Hệ thống ở trạng thái an toàn, chưa tái huấn luyện.",
        0.7, 5.28, 5.6, 0.85, 13, False, MUTED,
    )
    text(s, "Kết quả: an toàn", 0.7, 6.28, 5.4, 0.3, 14, True, TEAL)

    rect(s, 6.75, 4.34, 6.15, 2.52, WHITE, radius=0.05)
    rect(s, 6.75, 4.34, 0.08, 2.52, ORANGE, radius=0)
    text(s, "GIAI ĐOẠN 2  ·  DRIFT", 7.03, 4.5, 5.6, 0.24, 12, True, ORANGE)
    text(s, "250 request có nhiễu", 7.03, 4.8, 5.6, 0.36, 18, True, NAVY)
    text(
        s,
        "Nhiễu Gaussian μ = 0, σ = 2.0. Evidently thấy drift vượt 30% và gửi tín hiệu kích hoạt tái huấn luyện.",
        7.03, 5.28, 5.6, 0.85, 13, False, MUTED,
    )
    text(s, "Kết quả: trigger Airflow", 7.03, 6.28, 5.4, 0.3, 14, True, ORANGE)


def slide_cicd(prs):
    s = new_slide(prs)
    chrome(s, "05  ·  Tự động hóa", "Điều phối tái huấn luyện và CI/CD", 6)

    rect(s, 0.42, 1.24, 8.05, 5.6, WHITE, radius=0.05)
    text(s, "AIRFLOW DAG", 0.66, 1.4, 5, 0.22, 12, True, ORANGE)
    text(s, "ml_training_pipeline  ·  6 task tuần tự", 0.66, 1.66, 7.4, 0.34, 18, True, NAVY)

    tasks = [
        ("1", "data_ingestion", "Nạp tập dữ liệu mới tích lũy."),
        ("2", "data_cleaning", "Xử lý giá trị thiếu và làm sạch nhiễu."),
        ("3", "feature_engineering", "Chuẩn hóa và fit-transform đặc trưng."),
        ("4", "model_training", "Huấn luyện lại mô hình trên dữ liệu mới."),
        ("5", "evaluation & registration", "Chỉ promote nếu không kém model Production."),
        ("6", "deploy_model", "Reload API và cập nhật reference cho Evidently."),
    ]
    rect(s, 0.98, 2.22, 0.025, 3.65, SOFT_ORANGE, radius=0)
    for i, (num, name, desc) in enumerate(tasks):
        y = 2.08 + i * 0.72
        bubble = rect(s, 0.8, y, 0.38, 0.38, ORANGE if i < 4 else TEAL, radius=0.5)
        tf = bubble.text_frame
        tf.anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = num
        style_run(run, 14, True, WHITE)
        text(s, name, 1.36, y - 0.02, 6.8, 0.26, 14, True, NAVY)
        text(s, desc, 1.36, y + 0.26, 6.8, 0.28, 12, False, MUTED)

    rect(s, 8.65, 1.24, 4.26, 3.35, NAVY, radius=0.05)
    text(s, "GITHUB ACTIONS", 8.88, 1.42, 3.85, 0.22, 12, True, ORANGE)
    text(s, "CI/CD trên mỗi commit", 8.88, 1.7, 3.85, 0.55, 16, True, WHITE)
    steps = [
        ("Trigger", "Push hoặc pull request vào main và develop."),
        ("Lint", "flake8 kiểm tra phong cách mã nguồn."),
        ("Test", "Unit test và báo cáo coverage."),
        ("Build", "Đóng Docker image cho các service."),
    ]
    for i, (k, v) in enumerate(steps):
        y = 2.4 + i * 0.5
        text(s, f"0{i+1}", 8.88, y, 0.4, 0.28, 13, True, ORANGE)
        text(s, k, 9.32, y, 3.3, 0.22, 13, True, WHITE)
        text(s, v, 9.32, y + 0.2, 3.3, 0.24, 11, False, PALE)

    rect(s, 8.65, 4.75, 4.26, 2.09, SOFT_TEAL, radius=0.05)
    text(s, "CỔNG CHẤT LƯỢNG", 8.88, 4.92, 3.85, 0.22, 12, True, TEAL)
    text(s, "Không kém Production", 8.88, 5.2, 3.85, 0.55, 18, True, NAVY)
    text(
        s,
        "Đo trên cùng test set. Bản kém hơn không được ghi đè. Task 6 chỉ deploy khi đã promote.",
        8.88, 5.8, 3.8, 0.8, 13, False, INK,
    )


def slide_safety(prs):
    s = new_slide(prs)
    chrome(s, "06  ·  An toàn", "Rollback và bảo vệ model Production", 7)
    text(s, "Model kém không được ghi đè. Bản cũ vẫn còn để quay lại ngay.", 0.48, 1.16, 11, 0.28, 14, False, MUTED)

    blocks = [
        (
            ORANGE,
            "01",
            "Cổng chất lượng",
            "Task 5 · should_promote()",
            "Candidate và model Production được chấm trên cùng một tập test.",
            "Accuracy mới thấp hơn thì promote = False. Task deploy bị bỏ qua, bản đang chạy giữ nguyên.",
        ),
        (
            TEAL,
            "02",
            "Giữ version cũ",
            "register_and_promote()",
            "Bản mới lên Production thì bản trước chuyển sang Archived, không bị xóa.",
            "Model wine_quality_model. Rollback là đưa version Archived trở lại Production.",
        ),
        (
            NAVY,
            "03",
            "Hot-reload",
            "load_model() theo stage",
            "API luôn nạp model ở stage Production, không gắn cứng một số version.",
            "POST /model/reload nạp lại model đang active. Không cần khởi động lại dịch vụ.",
        ),
    ]
    gap = 0.16
    card_w = (12.42 - 2 * gap) / 3
    for i, (color, num, title, where, lead, detail) in enumerate(blocks):
        x = 0.46 + i * (card_w + gap)
        rect(s, x, 1.56, card_w, 3.05, WHITE, radius=0.06)
        rect(s, x, 1.56, card_w, 0.08, color, radius=0)
        text(s, num, x + 0.22, 1.76, 1.2, 0.26, 12, True, color)
        text(s, title, x + 0.22, 2.04, card_w - 0.44, 0.36, 18, True, NAVY)
        text(s, where, x + 0.22, 2.44, card_w - 0.44, 0.28, 13, True, color)
        text(s, lead, x + 0.22, 2.86, card_w - 0.44, 0.7, 13, False, INK)
        text(s, detail, x + 0.22, 3.58, card_w - 0.44, 0.85, 13, False, MUTED)

    rect(s, 0.46, 4.78, 12.42, 2.08, NAVY, radius=0.05)
    text(s, "ROLLBACK CHỦ ĐỘNG", 0.7, 4.94, 4, 0.22, 12, True, ORANGE)
    text(s, "Khi model mới đã lên Production nhưng phát sinh lỗi", 0.7, 5.18, 8, 0.3, 15, True, WHITE)
    steps = [
        ("1", "MLflow UI :5000", "Mở wine_quality_model, chọn version cũ, chuyển stage thành Production."),
        ("2", "POST /model/reload", "Gọi http://localhost:8000/model/reload để API nạp lại stage Production."),
        ("3", "Phục vụ model cũ", "Request tiếp theo dùng version vừa khôi phục, không cần deploy lại."),
    ]
    for i, (num, title, desc) in enumerate(steps):
        x = 0.7 + i * 4.05
        text(s, num, x, 5.58, 0.32, 0.28, 14, True, ORANGE)
        text(s, title, x + 0.36, 5.58, 3.4, 0.28, 14, True, WHITE)
        text(s, desc, x, 5.92, 3.75, 0.7, 12, False, PALE)


def slide_results(prs):
    s = new_slide(prs)
    chrome(s, "07  ·  Kết quả", "Kết quả thực nghiệm", 8)
    text(s, "Đối chiếu trực tiếp với tiêu chí của môn học.", 0.48, 1.16, 10, 0.28, 14, False, MUTED)

    kpis = [
        ("100%", "Test accuracy", "P = R = F1 = 1.0", ORANGE),
        ("97.9%", "5-fold CV", "Độ lệch ± 2.8%", TEAL),
        ("74/74", "Test cases", "API, pipeline, train", NAVY),
        ("90%", "Coverage", "Vượt mốc 80%", ORANGE),
        ("~15s", "Thời gian DAG", "Các task đều SUCCESS", TEAL),
    ]
    gap = 0.14
    card_w = (12.42 - 4 * gap) / 5
    for i, (value, label, note, color) in enumerate(kpis):
        x = 0.46 + i * (card_w + gap)
        rect(s, x, 1.56, card_w, 2.22, WHITE, radius=0.07)
        rect(s, x, 1.56, card_w, 0.08, color, radius=0)
        text(s, value, x + 0.08, 1.78, card_w - 0.16, 0.58, 28, True, color, PP_ALIGN.CENTER)
        text(s, label, x + 0.1, 2.4, card_w - 0.2, 0.32, 14, True, NAVY, PP_ALIGN.CENTER)
        text(s, note, x + 0.1, 2.76, card_w - 0.2, 0.7, 12, False, MUTED, PP_ALIGN.CENTER)

    checks = [
        ("Tổng quát hóa", "Cross-validation 97.9% ± 2.8% cho thấy accuracy trên tập test không đến từ một lần chia dữ liệu may mắn."),
        ("Drift kích hoạt đúng", "Airflow REST API nhận tín hiệu khi Evidently vượt ngưỡng. Không chạy lại khi dữ liệu còn sạch."),
        ("Không gián đoạn", "Sau khi promote, Airflow gọi POST /model/reload. API nạp model Production mới mà không cần khởi động lại."),
    ]
    for i, (title, desc) in enumerate(checks):
        x = 0.46 + i * 4.2
        rect(s, x, 4.02, 4.02, 2.82, WHITE, radius=0.06)
        text(s, f"0{i+1}", x + 0.24, 4.22, 1, 0.26, 12, True, ORANGE)
        text(s, title, x + 0.24, 4.54, 3.54, 0.4, 18, True, NAVY)
        text(s, desc, x + 0.24, 5.08, 3.54, 1.45, 14, False, INK)


def slide_close(prs):
    s = new_slide(prs)
    chrome(s, "08  ·  Khép lại", "Kết luận và hướng phát triển", 9)

    rect(s, 0.42, 1.24, 6.15, 4.15, WHITE, radius=0.05)
    text(s, "ĐÃ LÀM ĐƯỢC", 0.66, 1.42, 5.6, 0.24, 12, True, ORANGE)
    done = [
        ("Vòng đời khép kín", "Từ request, giám sát, phát hiện drift đến tái huấn luyện, cổng chất lượng và rollback."),
        ("Đủ chuẩn vận hành", "CI/CD, Docker, Airflow, Prometheus, Grafana và coverage 90%."),
        ("Tái lập được", "Xử lý lệch phiên bản thư viện và lưu artifact tại chỗ để pipeline chạy lại trên máy nhóm."),
    ]
    for i, (title, desc) in enumerate(done):
        y = 1.86 + i * 1.1
        text(s, f"0{i+1}", 0.66, y, 0.5, 0.3, 14, True, ORANGE)
        text(s, title, 1.2, y, 5.0, 0.3, 16, True, NAVY)
        text(s, desc, 1.2, y + 0.34, 5.05, 0.62, 13, False, MUTED)

    rect(s, 6.75, 1.24, 6.15, 4.15, WHITE, radius=0.05)
    text(s, "BƯỚC TIẾP THEO", 6.99, 1.42, 5.6, 0.24, 12, True, TEAL)
    nxt = [
        ("Kubernetes", "Đưa serving lên cụm với KServe hoặc Seldon Core khi lưu lượng tăng."),
        ("Feature Store", "Feast quản lý và chia sẻ đặc trưng dùng chung giữa train và serve."),
        ("Canary / A/B", "So sánh model mới với model đang chạy trước khi chuyển toàn bộ traffic."),
    ]
    for i, (title, desc) in enumerate(nxt):
        y = 1.86 + i * 1.1
        text(s, f"0{i+1}", 6.99, y, 0.5, 0.3, 14, True, TEAL)
        text(s, title, 7.52, y, 5.0, 0.3, 16, True, NAVY)
        text(s, desc, 7.52, y + 0.34, 5.05, 0.62, 13, False, MUTED)

    rect(s, 0.42, 5.55, 12.48, 1.32, NAVY, radius=0.05)
    text(s, "Cảm ơn thầy Nguyen Doan Dong và Hội đồng.", 0.68, 5.72, 8.5, 0.38, 18, True, WHITE)
    text(s, "Nhóm sẵn sàng trao đổi thêm về kiến trúc, số liệu và phần demo.", 0.68, 6.16, 8.2, 0.36, 13, False, PALE)
    text(s, "Q&A", 10.5, 5.82, 2.1, 0.55, 28, True, ORANGE, PP_ALIGN.RIGHT)


def main():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = "Báo cáo cuối kỳ — Hệ thống MLOps End-to-End"
    prs.core_properties.subject = "DDM501 — AI trong sản xuất: DevOps, DataOps, MLOps"
    prs.core_properties.author = "Phạm Minh Hoàng, Nguyễn Công Trọng, Ngô Minh Khôi"
    prs.core_properties.category = "FPT University"

    slide_title(prs)
    slide_problem(prs)
    slide_architecture(prs)
    slide_data(prs)
    slide_monitor(prs)
    slide_cicd(prs)
    slide_safety(prs)
    slide_results(prs)
    slide_close(prs)
    prs.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
