import os
from PIL import Image, ImageDraw, ImageFont

def generate_certificate_for_student(student_name, event_name, event_date, issuer_name,
                                      director_name, director_position, methodist_name, methodist_position):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Путь к шаблону сертификата
    image_path = os.path.join(current_dir, "app", "static", "images", "certificate.png")
    if not os.path.exists(image_path):
        return None  # Если файл не найден

    signature_director_path = os.path.join(current_dir, "app", "static", "images", "podpis_1.png")
    signature_methodist_path = os.path.join(current_dir, "app", "static", "images", "podpis_2.png")

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    signature_director = Image.open(signature_director_path).resize((200, 100))
    signature_methodist = Image.open(signature_methodist_path).resize((200, 100))

    font_path = os.path.join(current_dir, "arial.ttf")
    font_large = ImageFont.truetype(font_path, 52)
    font_medium = ImageFont.truetype(font_path, 38)
    font_small = ImageFont.truetype(font_path, 32)

    # Координаты для текста
    name_coords = (700, 600)
    event_coords = (650, 700)
    date_coords = (480, 1230)
    issuer_coords = (1060, 1230)

    director_text_coords = (600, 1100)
    methodist_text_coords = (1150, 1100)

    # Добавляем текст на сертификат
    draw.text(name_coords, student_name, fill="black", font=font_large)
    draw.text(event_coords, event_name, fill="black", font=font_medium)
    draw.text(date_coords, event_date, fill="black", font=font_medium)
    draw.text(issuer_coords, issuer_name, fill="black", font=font_medium)

    draw.text(director_text_coords, f"{director_name}\n{director_position}", fill="black", font=font_small)
    draw.text(methodist_text_coords, f"{methodist_name}\n{methodist_position}", fill="black", font=font_small)

    # Наложить подписи
    signature_coords_director = (650, 930)
    signature_coords_methodist = (1200, 930)
    image.paste(signature_director, signature_coords_director, mask=signature_director)
    image.paste(signature_methodist, signature_coords_methodist, mask=signature_methodist)

    # Сохранить изображение
    output_path = os.path.join(current_dir, "app", "static", "images", "certificate_completed.png")
    image.save(output_path)
    
    return output_path
