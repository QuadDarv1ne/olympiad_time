import logging
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from docx import Document
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Путь для сохранения сертификатов
BASE_DIR = Path(__file__).resolve().parent.parent
CERTIFICATE_DIR = BASE_DIR / "static" / "certificates"  # Основная папка для сертификатов

# Подкаталоги для различных форматов
IMAGES_DIR = CERTIFICATE_DIR / "images"
PDF_DIR = CERTIFICATE_DIR / "pdf"
WORD_DIR = CERTIFICATE_DIR / "word"

# Путь к файлам изображений и шрифтам
IMAGE_TEMPLATE_PATH = IMAGES_DIR / "certificate.png"  # Шаблон сертификата
SIGNATURE_DIRECTOR_PATH = IMAGES_DIR / "podpis_1.png"  # Подпись директора
SIGNATURE_METHODIST_PATH = IMAGES_DIR / "podpis_2.png"  # Подпись методиста
FONT_PATH = BASE_DIR / "arial.ttf"  # Или шрифт по умолчанию, если arial.ttf не найден

def load_font(font_path, size):
    try:
        logger.debug(f"Загружаем шрифт: {font_path} размер {size}")
        return ImageFont.truetype(str(font_path), size)
    except IOError:
        logger.warning(f"Шрифт {font_path} не найден, используется стандартный.")
        return ImageFont.load_default()

def check_and_create_directories():
    """Проверяет и создает все необходимые папки для сертификатов."""
    try:
        CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        PDF_DIR.mkdir(parents=True, exist_ok=True)
        WORD_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug("Директории для сертификатов проверены и созданы при необходимости.")
    except Exception as e:
        logger.error(f"Ошибка при создании директорий: {e}")
        raise

def generate_certificate_full(student_name, event_name, event_date, issuer_name, director_name,
                              director_position, methodist_name, methodist_position, format_type="png"):
    logger.debug("Начинаем генерацию сертификата...")
    try:
        # Проверка существования файлов шаблонов
        if not IMAGE_TEMPLATE_PATH.exists():
            logger.error(f"Не найден шаблон сертификата: {IMAGE_TEMPLATE_PATH}")
            raise FileNotFoundError(f"Не найден шаблон сертификата: {IMAGE_TEMPLATE_PATH}")

        if not SIGNATURE_DIRECTOR_PATH.exists():
            logger.error(f"Не найдена подпись директора: {SIGNATURE_DIRECTOR_PATH}")
            raise FileNotFoundError(f"Не найдена подпись директора: {SIGNATURE_DIRECTOR_PATH}")
        
        if not SIGNATURE_METHODIST_PATH.exists():
            logger.error(f"Не найдена подпись методиста: {SIGNATURE_METHODIST_PATH}")
            raise FileNotFoundError(f"Не найдена подпись методиста: {SIGNATURE_METHODIST_PATH}")
        
        logger.debug(f"Все необходимые файлы найдены. Формат сертификата: {format_type}")

        # Генерация сертификата в указанном формате
        if format_type == "png":
            return generate_png_certificate(student_name, event_name, event_date, issuer_name, director_name, director_position, methodist_name, methodist_position)
        elif format_type == "pdf":
            return generate_pdf_certificate(student_name, event_name, event_date, issuer_name, director_name, director_position, methodist_name, methodist_position)
        elif format_type == "docx":
            return generate_word_certificate(student_name, event_name, event_date, issuer_name, director_name, director_position, methodist_name, methodist_position)
        else:
            raise ValueError("Неверный формат сертификата. Поддерживаемые форматы: png, pdf, docx.")
    
    except Exception as e:
        logger.error(f"Ошибка при генерации сертификата: {e}")
        return None

# Генерация сертификата в формате PNG
def generate_png_certificate(student_name, event_name, event_date, issuer_name,
                              director_name, director_position, methodist_name, methodist_position):
    logger.debug("Начинаем генерацию сертификата в формате PNG...")
    try:
        check_and_create_directories()  # Проверка и создание директорий перед генерацией

        image = Image.open(IMAGE_TEMPLATE_PATH)
        signature_director = Image.open(SIGNATURE_DIRECTOR_PATH).resize((200, 100))
        signature_methodist = Image.open(SIGNATURE_METHODIST_PATH).resize((200, 100))

        font_large = load_font(FONT_PATH, 52)
        font_medium = load_font(FONT_PATH, 38)
        font_small = load_font(FONT_PATH, 32)

        draw = ImageDraw.Draw(image)
        # Добавление текста на сертификат
        logger.debug(f"Добавление текста: {student_name}, {event_name}, {event_date}, {issuer_name}")
        draw.text((700, 600), student_name, fill="black", font=font_large)
        draw.text((650, 700), event_name, fill="black", font=font_medium)
        draw.text((480, 1230), event_date, fill="black", font=font_medium)
        draw.text((1060, 1230), issuer_name, fill="black", font=font_medium)
        draw.text((600, 1100), f"{director_name}\n{director_position}", fill="black", font=font_small)
        draw.text((1150, 1100), f"{methodist_name}\n{methodist_position}", fill="black", font=font_small)

        # Наложение подписей
        image.paste(signature_director, (650, 930), signature_director)
        image.paste(signature_methodist, (1200, 930), signature_methodist)

        output_path = IMAGES_DIR / "certificate_completed.png"
        image.save(output_path)

        logger.info(f"Сертификат PNG сохранен по пути {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Ошибка при генерации сертификата PNG: {e}")
        return None

# Генерация сертификата в формате PDF
def generate_pdf_certificate(student_name, event_name, event_date, issuer_name,
                              director_name, director_position, methodist_name, methodist_position):
    logger.debug("Начинаем генерацию сертификата в формате PDF...")
    try:
        check_and_create_directories()  # Проверка и создание директорий перед генерацией

        output_path = PDF_DIR / "certificate_completed.pdf"

        c = canvas.Canvas(str(output_path), pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Сертификат участника")
        c.drawString(100, 730, f"Настоящим подтверждается, что {student_name}")
        c.drawString(100, 710, f"принял(а) участие в мероприятии '{event_name}'")
        c.drawString(100, 690, f"Дата проведения: {event_date}")
        c.drawString(100, 670, f"Организатор: {issuer_name}")
        c.drawString(100, 650, f"Подписано: {director_name}, {director_position}")
        c.drawString(100, 630, f"Методист: {methodist_name}, {methodist_position}")
        c.showPage()
        c.save()

        logger.info(f"Сертификат PDF сохранен по пути {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Ошибка при генерации PDF сертификата: {e}")
        return None

# Генерация сертификата в формате DOCX
def generate_word_certificate(student_name, event_name, event_date, issuer_name,
                               director_name, director_position, methodist_name, methodist_position):
    logger.debug("Начинаем генерацию сертификата в формате DOCX...")
    try:
        check_and_create_directories()  # Проверка и создание директорий перед генерацией

        output_path = WORD_DIR / "certificate_completed.docx"
        doc = Document()
        doc.add_heading("Сертификат участника", 0)
        doc.add_paragraph(f"Настоящим подтверждается, что {student_name} принял(а) участие в мероприятии '{event_name}'.")
        doc.add_paragraph(f"Дата проведения: {event_date}")
        doc.add_paragraph(f"Организатор: {issuer_name}")
        doc.add_paragraph(f"Подписано: {director_name}, {director_position}")
        doc.add_paragraph(f"Методист: {methodist_name}, {methodist_position}")
        doc.save(str(output_path))

        logger.info(f"Сертификат DOCX сохранен по пути {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Ошибка при генерации Word сертификата: {e}")
        return None
