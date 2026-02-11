import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

def generate_career_pdf(saved_careers, project_root, font_path):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    font_name = 'Helvetica'
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('CustomRoboto', font_path))
            font_name = 'CustomRoboto'
        except:
            pass

    bg_image_path = os.path.join(project_root, 'img', 'bg_pdf.jpg')

    def draw_header():
        if os.path.exists(bg_image_path):
            c.drawImage(bg_image_path, 0, 0, width=width, height=height)
        
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.setFont(font_name, 22)
        # Переместили вправо (width - 40) и вверх (height - 50)
        c.drawRightString(width - 40, height - 50, "ProfoBuilder: Мой Путь")
        
        c.setStrokeColorRGB(1, 0.6, 0)
        c.setLineWidth(3)
        c.line(width - 240, height - 60, width - 40, height - 60)

    draw_header()
    
    # Сдвинули начало сетки карточек выше (height - 90)
    y = height - 90
    card_h = 220
    # Увеличили ширину карточки (width - 80)
    card_w = width - 80
    x_start = 40
    spacing = 25

    for index, item in enumerate(saved_careers):
        if index > 0 and index % 3 == 0:
            c.showPage()
            draw_header()
            y = height - 90

        # Фон карточки (Оранжевый)
        c.setFillColorRGB(1, 0.6, 0)
        c.setStrokeColorRGB(1, 0.6, 0)
        c.roundRect(x_start, y - card_h, card_w, card_h, 25, stroke=1, fill=1)
        
        c.setFillColorRGB(1, 1, 1)
        
        # Левая колонка
        c.setFont(font_name, 20)
        # Ширина для текста названия теперь больше
        name_lines = simpleSplit(item['name'], font_name, 20, card_w/2 - 40)
        curr_name_y = y - 35
        for line in name_lines[:2]:
            c.drawString(x_start + 25, curr_name_y, line)
            curr_name_y -= 25
        
        c.setFont(font_name, 12)
        c.drawString(x_start + 25, curr_name_y - 10, f"Отрасль: {item['industry']}")
        
        c.setFont(font_name, 11)
        c.drawString(x_start + 25, y - 130, f"Начало: {item['junior_salary']} RUB")
        c.drawString(x_start + 25, y - 150, f"Средняя: {item['avg_salary']} RUB")
        c.drawString(x_start + 25, y - 170, f"Рост: {item['growth_rate']}")
        
        # Разделитель ровно посередине карточки
        c.setStrokeColorRGB(1, 1, 1)
        c.setLineWidth(1.2)
        c.line(width/2, y - 30, width/2, y - card_h + 50)
        
        # Правая колонка
        desc = item.get('description', '...')
        c.setFont(font_name, 11)
        # Увеличили ширину для описания
        desc_lines = simpleSplit(desc, font_name, 11, card_w/2 - 40)
        curr_desc_y = y - 35
        for line in desc_lines[:9]:
            c.drawString(width/2 + 20, curr_desc_y, line)
            curr_desc_y -= 15
        
        # ВУЗы
        c.setFont(font_name, 10)
        uni = f"ВУЗы: {item.get('university', '...')}"
        uni_lines = simpleSplit(uni, font_name, 10, card_w/2 - 40)
        if uni_lines:
            c.drawString(width/2 + 20, y - card_h + 75, uni_lines[0])

        # Ссылка внизу правой части
        link_url = item.get('link', 'https://hh.ru')
        link_text = "Узнать больше на внешнем ресурсе"
        c.setFont(font_name, 10)
        lx, ly = width/2 + 20, y - card_h + 50
        c.drawString(lx, ly, link_text)
        # Зона клика (Rectangle: x1, y1, x2, y2)
        c.linkURL(link_url, (lx, ly - 5, lx + 200, ly + 15), relative=0)

        y -= (card_h + spacing)

    c.save()
    buffer.seek(0)
    return buffer