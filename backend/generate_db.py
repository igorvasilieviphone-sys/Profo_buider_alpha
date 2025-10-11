import sqlite3
import json
from typing import List, Dict, Any

# Обновленные и очищенные данные о профессиях
CAREER_DATA: List[Dict[str, Any]] = [

    {
        "id": 1, "name": "Дата-сайентист", "industry": "ИТ/Аналитика", "university": "МГУ (ВМК), МФТИ (ФПМИ)",
        "link": "https://ds-example.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 1, 'art': 1}
    },
    {
        "id": 2, "name": "Графический дизайнер", "industry": "Креатив/Медиа", "university": "НИУ ВШЭ (Дизайн), МГХПА им. Строганова",
        "link": "https://design-info.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 3, "name": "Менеджер по продажам", "industry": "Продажи/Бизнес", "university": "РЭУ им. Плеханова, Финансовый университет",
        "link": "https://sales-prof.ru", "junior_salary": 55000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 4, "name": "Бухгалтер", "industry": "Финансы/Учет", "university": "Финансовый университет, СПбГЭУ",
        "link": "https://buh-help.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 5, "name": "Инженер-электронщик", "industry": "Промышленность/Технологии", "university": "МГТУ им. Баумана, СПбПУ Петра Великого",
        "link": "https://engineer-el.ru", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 6, "name": "Врач-кардиолог", "industry": "Медицина", "university": "Первый МГМУ им. Сеченова, ПСПбГМУ им. Павлова",
        "link": "https://cardio-med.ru", "junior_salary": 50000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 7, "name": "Frontend-разработчик", "industry": "ИТ", "university": "МТУСИ, ИТМО",
        "link": "https://front-dev.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 3}
    },
    {
        "id": 8, "name": "Юрист (Корпоративное право)", "industry": "Юриспруденция", "university": "МГУ (Юрфак), МГЮА им. Кутафина",
        "link": "https://law-corp.ru", "junior_salary": 60000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 9, "name": "SMM-менеджер", "industry": "Маркетинг/Медиа", "university": "РАНХиГС (Маркетинг), НИУ ВШЭ (Коммуникации)",
        "link": "https://smm-pro.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 10, "name": "Архитектор", "industry": "Строительство/Дизайн", "university": "МАРХИ, СПбГАСУ",
        "link": "https://arch-prof.ru", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 11, "name": "PR-менеджер", "industry": "Коммуникации", "university": "МГИМО, СПбГУ (Журналистика)",
        "link": "https://pr-career.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 12, "name": "Аналитик BI", "industry": "ИТ/Финансы", "university": "РЭУ им. Плеханова, ИТМО",
        "link": "https://bi-analyst.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 13, "name": "Повар-технолог", "industry": "Общепит/Производство", "university": "РЭУ им. Плеханова (Технология)",
        "link": "https://cook-tech.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 4}
    },
    {
        "id": 14, "name": "Риелтор", "industry": "Недвижимость", "university": "ГУУ (Менеджмент)",
        "link": "https://realty-pro.ru", "junior_salary": 40000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 15, "name": "Сварщик", "industry": "Рабочие/Промышленность", "university": "Технические колледжи",
        "link": "https://welder-job.ru", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 16, "name": "Педагог-дефектолог", "industry": "Образование/Медицина", "university": "МПГУ, РГПУ им. Герцена",
        "link": "https://defectology-edu.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 17, "name": "DevOps-инженер", "industry": "ИТ", "university": "СПбГУ (Математика), НИУ ВШЭ (Прикладная математика)",
        "link": "https://devops-tech.ru", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 18, "name": "Аудитор", "industry": "Финансы/Консалтинг", "university": "МГИМО, Финансовый университет",
        "link": "https://audit-career.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 19, "name": "Копирайтер", "industry": "Медиа/Маркетинг", "university": "МГУ (Журфак), РГГУ",
        "link": "https://copywriting-pro.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 20, "name": "Логист-международник", "industry": "Транспорт/ВЭД", "university": "МИИТ, СПбГЭУ",
        "link": "https://logistics-int.ru", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 21, "name": "Арт-директор", "industry": "Креатив/Медиа", "university": "БВШД, НИУ ВШЭ (Дизайн)",
        "link": "https://artdirector-job.ru", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 1, 'art': 5}
    },
    {
        "id": 22, "name": "Специалист по кибербезопасности", "industry": "ИТ/Безопасность", "university": "МИФИ, МГТУ им. Баумана (ИБ)",
        "link": "https://cybersecurity-ru.ru", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 23, "name": "Геолог", "industry": "Добыча/Геология", "university": "МГУ (Геологический), СПбГУ",
        "link": "https://geology-prof.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 24, "name": "Спортивный тренер", "industry": "Спорт/Фитнес", "university": "РГУФКСМиТ, НГУ им. Лесгафта",
        "link": "https://coach-rus.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 25, "name": "Web-аналитик", "industry": "Маркетинг/ИТ", "university": "НИУ ВШЭ (Экономика), СПбГУ",
        "link": "https://web-analytics-pro.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 3, 'art': 1}
    },
    {
        "id": 26, "name": "Менеджер проектов (IT)", "industry": "ИТ", "university": "МИРЭА, НИУ ВШЭ (Бизнес-информатика)",
        "link": "https://pm-it-pro.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 27, "name": "Режиссер монтажа", "industry": "Медиа/Кино", "university": "ВГИК, СПбГИКиТ",
        "link": "https://editing-pro.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 28, "name": "Инженер по охране труда", "industry": "Промышленность/ОТ", "university": "МГСУ",
        "link": "https://safety-engineer.ru", "junior_salary": 50000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 29, "name": "Фармацевт", "industry": "Медицина/Фармацевтика", "university": "РХТУ им. Менделеева",
        "link": "https://pharmacy-job.ru", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 30, "name": "Полицейский/Следователь", "industry": "Госслужба/Право", "university": "МВД РФ, Университет Прокуратуры",
        "link": "https://police-career.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 31, "name": "UX/UI-дизайнер", "industry": "ИТ/Дизайн", "university": "НИУ ВШЭ (Дизайн), ИТМО",
        "link": "https://uxui-design.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 4}
    },
    {
        "id": 32, "name": "Финансовый аналитик", "industry": "Финансы/Банки", "university": "Финансовый университет, РЭУ им. Плеханова",
        "link": "https://finance-analyst.ru", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 33, "name": "Прораб (Производитель работ)", "industry": "Строительство", "university": "МГСУ, СПбГАСУ",
        "link": "https://builder-pro.ru", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 34, "name": "Специалист по тендерам", "industry": "Госзакупки/Юриспруденция", "university": "Академии Госзакупок",
        "link": "https://tender-spec.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 35, "name": "Ветеринарный врач", "industry": "Медицина/Биология", "university": "МГАВМиБ им. Скрябина",
        "link": "https://vet-doc.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 36, "name": "Инженер-нефтяник", "industry": "Нефтегаз", "university": "РГУ нефти и газа им. Губкина",
        "link": "https://oil-engineer.ru", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 37, "name": "Сценарист", "industry": "Кино/ТВ/Медиа", "university": "ВГИК, МГУ (Журфак)",
        "link": "https://scenarist-pro.ru", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 1, 'art': 5}
    },
    {
        "id": 38, "name": "Переводчик (синхронный)", "industry": "Лингвистика/Коммуникации", "university": "МГИМО, МГЛУ",
        "link": "https://translator-int.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 39, "name": "HR-менеджер (Рекрутер)", "industry": "Управление персоналом", "university": "НИУ ВШЭ (Управление), РГГУ",
        "link": "https://hr-recruiter.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 40, "name": "Бармен-бариста", "industry": "Общепит/Сервис", "university": "Колледжи, Проф. курсы",
        "link": "https://barista-job.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 41, "name": "Системный администратор", "industry": "ИТ/Поддержка", "university": "МТУСИ, МГТУ им. Баумана",
        "link": "https://sysadmin-pro.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 42, "name": "Учитель математики/физики", "industry": "Образование", "university": "МПГУ, МФТИ (Пед. Фак.)",
        "link": "https://math-teacher.ru", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 43, "name": "Маркетолог-аналитик", "industry": "Маркетинг/Аналитика", "university": "НИУ ВШЭ (Маркетинг), СПбГЭУ",
        "link": "https://market-analyst.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 44, "name": "Химик-технолог", "industry": "Промышленность/Наука", "university": "РХТУ им. Менделеева, СПбГТИ(ТУ)",
        "link": "https://chem-tech.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 45, "name": "Эколог", "industry": "Экология/Госслужба", "university": "МГУ (Географический), РУДН",
        "link": "https://ecologist-rus.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 46, "name": "3D-моделлер/Аниматор", "industry": "Геймдев/Медиа", "university": "НИУ ВШЭ (Дизайн), Scream School",
        "link": "https://3d-artist.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 1, 'routine': 2, 'art': 5}
    },
    {
        "id": 47, "name": "Главный инженер проекта (ГИП)", "industry": "Строительство/Проектирование", "university": "МГСУ, МГТУ им. Баумана",
        "link": "https://gip-pro.ru", "junior_salary": 100000, "avg_salary": 170000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 48, "name": "Экскурсовод/Гид", "industry": "Туризм/Сервис", "university": "РГУТиС, МГУ (Географический)",
        "link": "https://guide-job.ru", "junior_salary": 30000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 49, "name": "Адвокат (Уголовное право)", "industry": "Юриспруденция", "university": "МГЮА им. Кутафина, СПбГУ (Юрфак)",
        "link": "https://law-criminal.ru", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 50, "name": "Брокер на фондовом рынке", "industry": "Финансы", "university": "Финансовый университет, НИУ ВШЭ (Финансы)",
        "link": "https://broker-pro.ru", "junior_salary": 90000, "avg_salary": 250000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 1, 'art': 1}
    },
    {
        "id": 51, "name": "Инженер по машинному обучению (ML Engineer)", "industry": "ИТ/Искусственный интеллект", "university": "МФТИ (ФПМИ), НИУ ВШЭ (ФКН), ИТМО",
        "link": "https://ml-engineer-pro.ru", "junior_salary": 110000, "avg_salary": 220000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 1}
    },
    {
        "id": 52, "name": "Менеджер по работе с маркетплейсами", "industry": "E-commerce/Продажи", "university": "РЭУ им. Плеханова, НИУ ВШЭ (Маркетинг)",
        "link": "https://marketplace-manager.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 1}
    },
    {
        "id": 53, "name": "Педагогический дизайнер", "industry": "Образование/EdTech", "university": "НИУ ВШЭ (Институт образования), МПГУ",
        "link": "https://edtech-designer.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 3}
    },
    {
        "id": 54, "name": "Психолог-консультант", "industry": "Психология/Здравоохранение", "university": "МГУ (Психфак), НИУ ВШЭ (Психология)",
        "link": "https://psychologist-help.ru", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 55, "name": "Геймдизайнер", "industry": "Геймдев/Креатив", "university": "НИУ ВШЭ (Геймдизайн), Scream School",
        "link": "https://gamedesigner-pro.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 4}
    },
    {
        "id": 56, "name": "Агроном (точное земледелие)", "industry": "Сельское хозяйство/Технологии", "university": "РГАУ-МСХА им. Тимирязева, КубГАУ",
        "link": "https://agro-tech.ru", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 57, "name": "SEO-специалист", "industry": "Маркетинг/ИТ", "university": "Профильные курсы, НИУ ВШЭ (Маркетинг)",
        "link": "https://seo-master-rus.ru", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 58, "name": "Пилот гражданской авиации", "industry": "Транспорт/Авиация", "university": "УИ ГА (Ульяновск), СПбГУ ГА (Санкт-Петербург)",
        "link": "https://pilot-career.ru", "junior_salary": 100000, "avg_salary": 350000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 59, "name": "Электромонтажник", "industry": "Строительство/Рабочие", "university": "Технические колледжи и училища",
        "link": "https://electric-profi.ru", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 60, "name": "Биоинформатик", "industry": "Наука/ИТ/Биотехнологии", "university": "МГУ (Биоинженерия и биоинформатика), СПбАУ РАН",
        "link": "https://bioinformatics-job.ru", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 61, "name": "Backend-разработчик", "industry": "ИТ", "university": "МГТУ им. Баумана, ИТМО, МИФИ",
        "link": "https://backend-dev-pro.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 62, "name": "Продуктовый менеджер (IT)", "industry": "ИТ/Менеджмент", "university": "НИУ ВШЭ, МФТИ",
        "link": "https://product-manager-it.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 63, "name": "QA-инженер (Тестировщик ПО)", "industry": "ИТ", "university": "Политех, ЛЭТИ, профильные курсы",
        "link": "https://qa-engineer-job.ru", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 64, "name": "Стоматолог-ортодонт", "industry": "Медицина", "university": "МГМСУ им. Евдокимова, ПСПбГМУ им. Павлова",
        "link": "https://orthodontist-care.ru", "junior_salary": 80000, "avg_salary": 200000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 65, "name": "Инженер-конструктор (Машиностроение)", "industry": "Промышленность/Инженерия", "university": "МГТУ им. Баумана, Самарский университет",
        "link": "https://construct-engineer.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 66, "name": "Оператор БПЛА (Дронов)", "industry": "Технологии/Логистика/Агро", "university": "МАИ, Профильные центры подготовки",
        "link": "https://drone-operator-pro.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 1, 'routine': 4, 'art': 2}
    },
    {
        "id": 67, "name": "Шеф-повар", "industry": "Общепит/HoReCa", "university": "Кулинарные школы (Novikov School, Swissam)",
        "link": "https://chef-master.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 68, "name": "Data Engineer", "industry": "ИТ/Big Data", "university": "МГУ (ВМК), СПбГУ (Матмех)",
        "link": "https://data-engineer-world.ru", "junior_salary": 100000, "avg_salary": 190000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 69, "name": "Нейрохирург", "industry": "Медицина", "university": "НМИЦ им. Бурденко, Первый МГМУ им. Сеченова",
        "link": "https://neurosurgery-rus.ru", "junior_salary": 80000, "avg_salary": 250000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 70, "name": "GR-менеджер (Government Relations)", "industry": "Бизнес/Госуправление", "university": "МГИМО, РАНХиГС",
        "link": "https://gr-manager-pro.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 71, "name": "Мобильный разработчик (iOS/Android)", "industry": "ИТ", "university": "НИУ ВШЭ (ПМИ), МИРЭА",
        "link": "https://mobile-developer-job.ru", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 3}
    },
    {
        "id": 72, "name": "Косметолог-эстетист", "industry": "Красота/Медицина", "university": "Медицинские колледжи, РУДН (Эстетическая косметология)",
        "link": "https://cosmetologist-esthetic.ru", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 4}
    },
    {
        "id": 73, "name": "Бизнес-аналитик", "industry": "ИТ/Консалтинг/Финансы", "university": "НИУ ВШЭ (Бизнес-информатика), Финансовый университет",
        "link": "https://business-analyst-career.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 74, "name": "Инженер-робототехник", "industry": "ИТ/Инженерия/Промышленность", "university": "Университет Иннополис, Сколтех, ИТМО",
        "link": "https://robotics-engineer.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 2}
    },
    {
        "id": 75, "name": "Ландшафтный дизайнер", "industry": "Дизайн/Архитектура", "university": "МАРХИ, РГАУ-МСХА им. Тимирязева",
        "link": "https://landscape-design-pro.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 76, "name": "Motion-дизайнер", "industry": "Креатив/Медиа/Реклама", "university": "БВШД, Scream School",
        "link": "https://motion-design-job.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 2, 'art': 5}
    },
    {
        "id": 77, "name": "Менеджер по ВЭД", "industry": "Логистика/Торговля", "university": "РАНХиГС (Таможенное дело), СПбГЭУ",
        "link": "https://ved-manager-pro.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 78, "name": "Парикмахер-стилист", "industry": "Красота/Сервис", "university": "Академии (TONI&GUY, Pivot Point), Технологические колледжи",
        "link": "https://hair-stylist-career.ru", "junior_salary": 40000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 79, "name": "Генетик", "industry": "Наука/Медицина", "university": "МГУ (Биофак), СПбГУ (Биофак)",
        "link": "https://geneticist-rus.ru", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 80, "name": "Блокчейн-разработчик", "industry": "ИТ/Финтех", "university": "МФТИ, МИФИ, ИТМО",
        "link": "https://blockchain-dev-pro.ru", "junior_salary": 120000, "avg_salary": 250000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 81, "name": "Промышленный дизайнер", "industry": "Дизайн/Промышленность", "university": "МГХПА им. Строганова, СПбГХПА им. Штиглица",
        "link": "https://industrial-designer-job.ru", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 82, "name": "Автомеханик-диагност", "industry": "Автосервис/Рабочие", "university": "МАДИ, Политехнические колледжи",
        "link": "https://automechanic-pro.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 83, "name": "Логопед", "industry": "Образование/Медицина", "university": "МПГУ (Дефектологический), РГПУ им. Герцена",
        "link": "https://logoped-career.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 84, "name": "Event-менеджер", "industry": "Маркетинг/Организация мероприятий", "university": "РГУТиС, СПбГИК",
        "link": "https://event-manager-rus.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 85, "name": "Технический писатель", "industry": "ИТ/Документация", "university": "МГЛУ, МГУ (Филологический)",
        "link": "https://tech-writer-pro.ru", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 86, "name": "Директор по маркетингу (CMO)", "industry": "Маркетинг/Менеджмент", "university": "НИУ ВШЭ, Стокгольмская школа экономики в России",
        "link": "https://cmo-career.ru", "junior_salary": 150000, "avg_salary": 300000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 1, 'art': 2}
    },
    {
        "id": 87, "name": "Сомелье/Кавист", "industry": "Рестораны/Ритейл", "university": "Школы сомелье (Enotria, Wine People)",
        "link": "https://sommelier-job.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 88, "name": "Медиатор (разрешение споров)", "industry": "Юриспруденция/Консалтинг", "university": "Центры медиации при ВУЗах (МГУ, СПбГУ)",
        "link": "https://mediator-pro.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 89, "name": "Финансовый контролер", "industry": "Финансы/Менеджмент", "university": "Финансовый университет, РЭУ им. Плеханова",
        "link": "https://financial-controller-rus.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 90, "name": "T&D-менеджер", "industry": "HR/Обучение персонала", "university": "НИУ ВШЭ (Управление персоналом), МГУ (Психология)",
        "link": "https://td-manager-career.ru", "junior_salary": 70000, "avg_salary": 125000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 91, "name": "Инженер ПТО", "industry": "Строительство", "university": "МГСУ, СПбГАСУ",
        "link": "https://pto-engineer.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 92, "name": "Фармаколог (клинические исследования)", "industry": "Фармацевтика/Наука", "university": "Первый МГМУ им. Сеченова, РХТУ им. Менделеева",
        "link": "https://pharmacologist-research.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 93, "name": "Коммерческий фотограф", "industry": "Фотография/Реклама/Медиа", "university": "Школы фотографии (Photoplay, Академия Фотографии)",
        "link": "https://commercial-photographer.ru", "junior_salary": 45000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 94, "name": "Специалист по автоматизации зданий", "industry": "ИТ/Строительство/Инженерия", "university": "МЭИ, МГСУ",
        "link": "https://smarthome-engineer.ru", "junior_salary": 75000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 2}
    },
    {
        "id": 95, "name": "Веб-дизайнер", "industry": "ИТ/Дизайн", "university": "НИУ ВШЭ (Дизайн), Британская высшая школа дизайна",
        "link": "https://webdesigner-pro.ru", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 96, "name": "Токарь с ЧПУ", "industry": "Промышленность/Рабочие", "university": "Политехнические колледжи",
        "link": "https://turner-cnc-job.ru", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 97, "name": "Авиадиспетчер", "industry": "Авиация/Транспорт", "university": "СПбГУ ГА, МГТУ ГА",
        "link": "https://air-traffic-controller.ru", "junior_salary": 80000, "avg_salary": 180000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 98, "name": "Нутрициолог", "industry": "Здоровье/Фитнес/Консалтинг", "university": "РНИМУ им. Пирогова, профильные курсы",
        "link": "https://nutritionist-care.ru", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 99, "name": "Комьюнити-менеджер", "industry": "Маркетинг/Геймдев/ИТ", "university": "НИУ ВШЭ (Коммуникации), РГГУ",
        "link": "https://community-manager-rus.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 100, "name": "Специалист по ESG", "industry": "Консалтинг/Финансы/Экология", "university": "МГИМО, РАНХиГС",
        "link": "https://esg-specialist.ru", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 101, "name": "Промышленный альпинист", "industry": "Строительство/Сервис", "university": "Центры профессиональной подготовки",
        "link": "https://promalp-pro.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 102, "name": "Налоговый консультант", "industry": "Финансы/Юриспруденция/Консалтинг", "university": "Финансовый университет, МГЮА им. Кутафина",
        "link": "https://tax-consultant-rus.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 103, "name": "Реставратор (искусство)", "industry": "Искусство/Культура", "university": "МГХПА им. Строганова, Академия художеств им. Репина",
        "link": "https://art-restorer.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 5, 'art': 5}
    },
    {
        "id": 104, "name": "Fullstack-разработчик", "industry": "ИТ", "university": "МФТИ, ИТМО, онлайн-школы",
        "link": "https://fullstack-dev-career.ru", "junior_salary": 90000, "avg_salary": 185000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 2}
    },
    {
        "id": 105, "name": "Байер (Fashion)", "industry": "Мода/Ритейл", "university": "БВШД, МГУ (Менеджмент)",
        "link": "https://fashion-buyer-pro.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 106, "name": "Спасатель МЧС", "industry": "Госслужба/Безопасность", "university": "Академия ГПС МЧС России",
        "link": "https://mchs-rescuer-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 107, "name": "Продуктовый аналитик", "industry": "ИТ/Аналитика", "university": "НИУ ВШЭ (ПМИ), МФТИ",
        "link": "https://product-analyst-pro.ru", "junior_salary": 85000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 108, "name": "Клинический психолог", "industry": "Медицина/Психология", "university": "МГУ (Психфак), РНИМУ им. Пирогова",
        "link": "https://clinical-psychologist.ru", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 109, "name": "Звукорежиссер", "industry": "Медиа/Музыка/Кино", "university": "ВГИК, СПбГИКиТ, ИСИ",
        "link": "https://sound-director-pro.ru", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 110, "name": "Геодезист/Картограф", "industry": "Строительство/Геология", "university": "МИИГАиК, СПбГУ",
        "link": "https://geodesist-career.ru", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 111, "name": "CRM-маркетолог", "industry": "Маркетинг/ИТ", "university": "НИУ ВШЭ (Маркетинг), РЭУ им. Плеханова",
        "link": "https://crm-marketer.ru", "junior_salary": 60000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 112, "name": "Тату-мастер", "industry": "Сервис/Искусство", "university": "Профессиональные студии и курсы",
        "link": "https://tattoo-artist-job.ru", "junior_salary": 40000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 113, "name": "Сметчик", "industry": "Строительство/Финансы", "university": "МГСУ, Профильные курсы",
        "link": "https://estimator-pro.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 114, "name": "Вирусолог", "industry": "Наука/Медицина", "university": "МГУ (Биофак), НГУ (Новосибирск)",
        "link": "https://virologist-rus.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 115, "name": "Политтехнолог", "industry": "Политика/Консалтинг/PR", "university": "МГУ (Философский), НИУ ВШЭ (Политология)",
        "link": "https://political-strategist.ru", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 116, "name": "C++ разработчик", "industry": "ИТ/Геймдев/Финтех", "university": "МФТИ, МГУ (ВМК), СПбГУ (Матмех)",
        "link": "https://cpp-developer-pro.ru", "junior_salary": 95000, "avg_salary": 200000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 117, "name": "Дизайнер интерьеров", "industry": "Дизайн/Строительство", "university": "МГХПА им. Строганова, Школа 'Детали'",
        "link": "https://interior-designer-career.ru", "junior_salary": 55000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 118, "name": "Оценщик (недвижимость, бизнес)", "industry": "Финансы/Недвижимость/Консалтинг", "university": "Финансовый университет, РЭУ им. Плеханова",
        "link": "https://appraiser-job.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 119, "name": "Агроинженер", "industry": "Сельское хозяйство/Инженерия", "university": "РГАУ-МСХА им. Тимирязева, Ставропольский ГАУ",
        "link": "https://agro-engineer-pro.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 120, "name": "Специалист по контекстной рекламе (PPC)", "industry": "Маркетинг/ИТ", "university": "Профильные курсы и сертификации (Яндекс)",
        "link": "https://ppc-specialist.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 121, "name": "Нотариус", "industry": "Юриспруденция", "university": "МГЮА им. Кутафина, МГУ (Юрфак)",
        "link": "https://notary-rus.ru", "junior_salary": 80000, "avg_salary": 250000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 122, "name": "Кондитер", "industry": "Общепит/Производство", "university": "Колледжи пищевой промышленности, кулинарные школы",
        "link": "https://pastry-chef-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 123, "name": "Кинолог", "industry": "Госслужба (МВД, ФТС)/Сервис", "university": "Аграрные вузы, ведомственные учебные центры",
        "link": "https://cynologist-career.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 124, "name": "Метеоролог", "industry": "Наука/Госслужба", "university": "МГУ (Географический), РГГМУ (Санкт-Петербург)",
        "link": "https://meteorologist-pro.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 125, "name": "Системный аналитик", "industry": "ИТ/Консалтинг", "university": "НИУ ВШЭ (Бизнес-информатика), МГТУ им. Баумана",
        "link": "https://system-analyst-career.ru", "junior_salary": 75000, "avg_salary": 145000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 126, "name": "Консультант по управлению", "industry": "Консалтинг/Бизнес", "university": "НИУ ВШЭ, РЭШ, МФТИ",
        "link": "https://mgmt-consultant-pro.ru", "junior_salary": 100000, "avg_salary": 250000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 127, "name": "Коммерческий иллюстратор", "industry": "Дизайн/Искусство/Медиа", "university": "БВШД, МГХПА им. Строганова",
        "link": "https://illustrator-commercial.ru", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 128, "name": "Финансовый директор (CFO)", "industry": "Финансы/Менеджмент", "university": "Финансовый университет, НИУ ВШЭ (Экономфак)",
        "link": "https://cfo-career-rus.ru", "junior_salary": 180000, "avg_salary": 450000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 129, "name": "Разработчик игр (Game Developer)", "industry": "Геймдев/ИТ", "university": "НИУ ВШЭ (Программная инженерия), ИТМО",
        "link": "https://gamedev-pro-rus.ru", "junior_salary": 80000, "avg_salary": 165000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 130, "name": "Реабилитолог/Физический терапевт", "industry": "Медицина/Спорт", "university": "РГУФКСМиТ, НГУ им. Лесгафта",
        "link": "https://phys-therapist.ru", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 131, "name": "Облачный архитектор (Cloud Architect)", "industry": "ИТ", "university": "Технические ВУЗы + сертификации (Yandex.Cloud, AWS, Azure)",
        "link": "https://cloud-architect-pro.ru", "junior_salary": 140000, "avg_salary": 280000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 1}
    },
    {
        "id": 132, "name": "Патентный поверенный", "industry": "Юриспруденция/Интеллектуальная собственность", "university": "РГАИС, МГЮА им. Кутафина",
        "link": "https://patent-attorney-rus.ru", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 133, "name": "Урбанист-планировщик", "industry": "Архитектура/Госуправление", "university": "МАРХИ, НИУ ВШЭ (Высшая школа урбанистики)",
        "link": "https://urban-planner-job.ru", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 134, "name": "Диктор/Актер озвучания", "industry": "Медиа/Искусство", "university": "Театральные ВУЗы (ВТУ им. Щепкина, ГИТИС), курсы",
        "link": "https://voice-actor-career.ru", "junior_salary": 40000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 135, "name": "Технолог пищевого производства", "industry": "Промышленность/Общепит", "university": "МГУПП, РЭУ им. Плеханова",
        "link": "https://food-technologist-pro.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 136, "name": "Профориентолог/Карьерный консультант", "industry": "HR/Образование/Консалтинг", "university": "НИУ ВШЭ (Психология), МГУ (Психфак)",
        "link": "https://career-consultant-rus.ru", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 137, "name": "Оператор станков с ЧПУ", "industry": "Промышленность/Рабочие", "university": "Среднее профессиональное образование, учебные центры",
        "link": "https://cnc-operator-job.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 138, "name": "Анестезиолог-реаниматолог", "industry": "Медицина", "university": "Ведущие медицинские ВУЗы + ординатура",
        "link": "https://anesthesiologist-pro.ru", "junior_salary": 70000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 139, "name": "Научный сотрудник (Research Scientist)", "industry": "Наука", "university": "ВУЗы с сильными научными школами (МГУ, СПбГУ, НГУ, МФТИ)",
        "link": "https://research-scientist-rus.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 140, "name": "Таргетолог", "industry": "Маркетинг/SMM", "university": "Онлайн-курсы, НИУ ВШЭ (Коммуникации)",
        "link": "https://targetologist-career.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 141, "name": "Машинист поезда/метрополитена", "industry": "Транспорт/Госслужба", "university": "Железнодорожные колледжи и техникумы, УТЦ метрополитена",
        "link": "https://train-driver-job.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 142, "name": "Архитектор IT-решений (Solution Architect)", "industry": "ИТ/Консалтинг", "university": "МГТУ им. Баумана, МФТИ",
        "link": "https://solution-architect-rus.ru", "junior_salary": 150000, "avg_salary": 300000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 143, "name": "Креативный директор", "industry": "Реклама/Медиа/Дизайн", "university": "БВШД, MADS",
        "link": "https://creative-director-pro.ru", "junior_salary": 120000, "avg_salary": 250000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 1, 'art': 5}
    },
    {
        "id": 144, "name": "Зоотехник", "industry": "Сельское хозяйство", "university": "РГАУ-МСХА им. Тимирязева, СПбГАВМ",
        "link": "https://zootechnician-career.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 145, "name": "Микробиолог", "industry": "Наука/Медицина/Промышленность", "university": "МГУ (Биофак), РХТУ им. Менделеева",
        "link": "https://microbiologist-job.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 146, "name": "Начальник строительного участка", "industry": "Строительство", "university": "МГСУ, СПбГАСУ",
        "link": "https://construction-site-manager.ru", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 147, "name": "Python-разработчик", "industry": "ИТ/Data Science/Web", "university": "МФТИ, НИУ ВШЭ (ФКН), ИТМО",
        "link": "https://python-developer-pro.ru", "junior_salary": 85000, "avg_salary": 175000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 148, "name": "Специалист по таможенному оформлению", "industry": "Логистика/Госслужба/Торговля", "university": "РАНХиГС (Таможенное дело), РТА",
        "link": "https://customs-specialist-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 149, "name": "Тифлопедагог", "industry": "Образование/Дефектология", "university": "МПГУ, РГПУ им. Герцена",
        "link": "https://typhlopedagogue-edu.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 150, "name": "Инвестиционный аналитик", "industry": "Финансы/Инвестиции/Банки", "university": "РЭШ, НИУ ВШЭ (МИЭФ), Финансовый университет",
        "link": "https://investment-analyst-career.ru", "junior_salary": 100000, "avg_salary": 190000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 151, "name": "UX-исследователь", "industry": "ИТ/Дизайн/Маркетинг", "university": "НИУ ВШЭ (Социология, Психология), МГУ",
        "link": "https://ux-researcher-pro.ru", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 152, "name": "Дипломат", "industry": "Госслужба/Международные отношения", "university": "МГИМО, Дипломатическая академия МИД РФ",
        "link": "https://diplomat-career.ru", "junior_salary": 80000, "avg_salary": 200000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 153, "name": "Художник по костюмам", "industry": "Искусство/Кино/Театр", "university": "ВГИК, Школа-студия МХАТ",
        "link": "https://costume-designer-art.ru", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 154, "name": "Java-разработчик", "industry": "ИТ/Enterprise/Финтех", "university": "МГТУ им. Баумана, СПбПУ, КФУ",
        "link": "https://java-developer-pro.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 155, "name": "Спортивный психолог", "industry": "Спорт/Психология", "university": "МГУ (Психфак), РГУФКСМиТ",
        "link": "https://sports-psychologist-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 156, "name": "Антикризисный управляющий", "industry": "Менеджмент/Финансы/Юриспруденция", "university": "РАНХиГС, НИУ ВШЭ",
        "link": "https://crisis-manager-pro.ru", "junior_salary": 150000, "avg_salary": 350000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 157, "name": "Специалист по информационной безопасности", "industry": "ИТ/Безопасность", "university": "МИФИ, МГТУ им. Баумана (ИУ-8), ИТМО",
        "link": "https://infosec-specialist.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 158, "name": "Lean-менеджер", "industry": "Промышленность/Менеджмент", "university": "Технические ВУЗы + доп. образование",
        "link": "https://lean-manager-career.ru", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 159, "name": "Няня/Гувернантка", "industry": "Сервис/Образование", "university": "Педагогические и медицинские колледжи, МПГУ",
        "link": "https://nanny-guvernantka-job.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 160, "name": "Врач-онколог", "industry": "Медицина", "university": "НМИЦ онкологии им. Блохина, ПМГМУ им. Сеченова",
        "link": "https://oncologist-doctor-rus.ru", "junior_salary": 70000, "avg_salary": 190000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 161, "name": "Комплаенс-менеджер", "industry": "Юриспруденция/Финансы/Безопасность", "university": "МГЮА им. Кутафина, НИУ ВШЭ (Право)",
        "link": "https://compliance-manager-pro.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 162, "name": "Разработчик встраиваемых систем", "industry": "ИТ/Инженерия/Электроника", "university": "МИЭТ, МГТУ им. Баумана, ИТМО",
        "link": "https://embedded-developer-job.ru", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 163, "name": "Бренд-менеджер", "industry": "Маркетинг/Менеджмент", "university": "НИУ ВШЭ (Маркетинг), МГУ (Экономфак)",
        "link": "https://brand-manager-career.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 164, "name": "Врач-радиолог (МРТ/КТ)", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по рентгенологии",
        "link": "https://radiologist-doctor.ru", "junior_salary": 80000, "avg_salary": 170000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 165, "name": "Актуарий", "industry": "Страхование/Финансы", "university": "МГУ (Мехмат), НИУ ВШЭ (Экономика)",
        "link": "https://actuary-pro-rus.ru", "junior_salary": 100000, "avg_salary": 220000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 166, "name": "Продюсер (кино/ТВ/медиа)", "industry": "Медиа/Кино/ТВ", "university": "ВГИК, СПбГИКиТ, Школа-студия МХАТ",
        "link": "https://producer-career.ru", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 167, "name": "Гидрогеолог", "industry": "Геология/Экология/Строительство", "university": "МГУ (Геологический), МГРИ",
        "link": "https://hydrogeologist-job.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 168, "name": "Парикмахер-колорист", "industry": "Красота/Сервис", "university": "Профессиональные академии и школы (L'Oréal, Wella)",
        "link": "https://hair-colorist-pro.ru", "junior_salary": 50000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 169, "name": "Нанотехнолог", "industry": "Наука/Промышленность/Технологии", "university": "МИФИ, МФТИ, МИСиС",
        "link": "https://nanotechnologist-rus.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 170, "name": "Конфликтолог", "industry": "HR/Консалтинг/Госслужба", "university": "СПбГУ (Факультет социологии), РГСУ",
        "link": "https://conflictologist-career.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 171, "name": "Scrum-мастер", "industry": "ИТ/Менеджмент", "university": "Сертификация (PSM, CSM) + опыт в IT",
        "link": "https://scrum-master-pro.ru", "junior_salary": 100000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 172, "name": "Эрготерапевт", "industry": "Медицина/Реабилитация", "university": "ПСПбГМУ им. Павлова, РНИМУ им. Пирогова",
        "link": "https://ergotherapist-job.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 173, "name": "Специалист по лизингу", "industry": "Финансы/Продажи", "university": "Финансовый университет, РЭУ им. Плеханова",
        "link": "https://leasing-specialist.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 174, "name": "Технический художник", "industry": "Геймдев/ИТ", "university": "Scream School, НИУ ВШЭ (Дизайн)",
        "link": "https://technical-artist-pro.ru", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 175, "name": "Судья", "industry": "Юриспруденция/Госслужба", "university": "Высшее юридическое образование + большой стаж",
        "link": "https://judge-career-rus.ru", "junior_salary": 100000, "avg_salary": 300000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 176, "name": "Customer Success Manager", "industry": "ИТ/Сервис", "university": "Любой ВУЗ + коммуникативные навыки",
        "link": "https://customer-success-manager.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 177, "name": "Астрофизик", "industry": "Наука", "university": "МГУ (Физфак), СПбГУ (Астрономическое отделение)",
        "link": "https://astrophysicist-job.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 178, "name": "BIM-менеджер", "industry": "Строительство/Проектирование", "university": "МГСУ, СПбГАСУ",
        "link": "https://bim-manager-pro.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 2}
    },
    {
        "id": 179, "name": "Заводчик животных", "industry": "Животноводство/Сервис", "university": "Аграрные вузы (зоотехния, ветеринария)",
        "link": "https://animal-breeder-rus.ru", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 2}
    },
    {
        "id": 180, "name": "Мастер по ремонту бытовой техники", "industry": "Сервис/Рабочие", "university": "Технические колледжи, учебные центры производителей",
        "link": "https://appliance-repair-tech.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 181, "name": "DevRel менеджер", "industry": "ИТ/Маркетинг/Коммуникации", "university": "Технические ВУЗы + опыт в IT-комьюнити",
        "link": "https://devrel-manager-pro.ru", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 182, "name": "Искусствовед", "industry": "Искусство/Культура/Образование", "university": "МГУ (Истфак), РГГУ, Академия художеств им. Репина",
        "link": "https://art-historian-career.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 4, 'art': 5}
    },
    {
        "id": 183, "name": "Каскадер", "industry": "Кино/ТВ", "university": "Школы каскадеров, спортивные разряды",
        "link": "https://stunt-performer-job.ru", "junior_salary": 60000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 3}
    },
    {
        "id": 184, "name": "Инженер по качеству", "industry": "Промышленность/Производство", "university": "МГТУ им. Баумана, Политехнические университеты",
        "link": "https://quality-engineer-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 185, "name": "Флорист", "industry": "Сервис/Дизайн", "university": "Школы флористики ('Николь', 'Moscow Flower School')",
        "link": "https://florist-designer-pro.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 186, "name": "Эндокринолог", "industry": "Медицина", "university": "НМИЦ эндокринологии, ведущие медицинские ВУЗы",
        "link": "https://endocrinologist-doc.ru", "junior_salary": 60000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 187, "name": "Администратор баз данных (DBA)", "industry": "ИТ", "university": "МГТУ им. Баумана, МИРЭА",
        "link": "https://database-administrator-pro.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 188, "name": "Офицер вооруженных сил", "industry": "Госслужба/Армия", "university": "Военные училища и академии",
        "link": "https://military-officer-career.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 189, "name": "Компьютерный лингвист", "industry": "ИТ/Наука", "university": "НИУ ВШЭ (ФКН), МГУ (Филологический/ВМК), СПбГУ",
        "link": "https://computational-linguist-job.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 190, "name": "Ортопед-травматолог", "industry": "Медицина", "university": "НМИЦ ТО им. Приорова, РНИМУ им. Пирогова",
        "link": "https://orthopedist-traumatologist.ru", "junior_salary": 65000, "avg_salary": 165000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 191, "name": "Священнослужитель", "industry": "Религия", "university": "Духовные академии и семинарии",
        "link": "https://clergyman-rus.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 4}
    },
    {
        "id": 192, "name": "Парфюмер", "industry": "Красота/Химия", "university": "РХТУ им. Менделеева, МГУ (Химфак) + спец. курсы",
        "link": "https://perfumer-career.ru", "junior_salary": 80000, "avg_salary": 200000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 5}
    },
    {
        "id": 193, "name": "Мастер по ремонту цифровой техники", "industry": "Сервис/Электроника", "university": "Технические колледжи, учебные центры",
        "link": "https://digital-repair-pro.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 194, "name": "Социолог-исследователь", "industry": "Наука/Маркетинг/Госслужба", "university": "НИУ ВШЭ (Социология), МГУ (Соцфак)",
        "link": "https://sociologist-researcher.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 195, "name": "Кредитный аналитик", "industry": "Банки/Финансы", "university": "Финансовый университет, РЭУ им. Плеханова",
        "link": "https://credit-analyst-job.ru", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 196, "name": "Инженер-эколог", "industry": "Экология/Промышленность", "university": "РУДН (Экологический факультет), МГСУ",
        "link": "https://environmental-engineer-pro.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 197, "name": "NLP-инженер", "industry": "ИТ/Искусственный интеллект", "university": "МФТИ, НИУ ВШЭ (ФКН), Сколтех",
        "link": "https://nlp-engineer-career.ru", "junior_salary": 115000, "avg_salary": 230000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 198, "name": "Оперный певец", "industry": "Искусство/Музыка", "university": "Консерватории (Москва, Санкт-Петербург), ГИТИС",
        "link": "https://opera-singer-rus.ru", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 5, 'art': 5}
    },
    {
        "id": 199, "name": "Экономист-международник", "industry": "Экономика/ВЭД/Госслужба", "university": "МГИМО, НИУ ВШЭ (МЭиМП)",
        "link": "https://international-economist-pro.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 200, "name": "VFX-художник", "industry": "Кино/Геймдев/Медиа", "university": "Scream School, онлайн-школы (XYZ, CGLab)",
        "link": "https://vfx-artist-career.ru", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    # --- НАЧАЛО БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    {
        "id": 201, "name": "Продюсер онлайн-курсов", "industry": "EdTech/Образование", "university": "НИУ ВШЭ, Нетология, Skillbox",
        "link": "https://online-producer-pro.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 202, "name": "Трекер (стартап-трекер)", "industry": "Венчур/Консалтинг/ИТ", "university": "ФРИИ, Сколково",
        "link": "https://startup-tracker-job.ru", "junior_salary": 90000, "avg_salary": 200000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 203, "name": "Генетический консультант", "industry": "Медицина/Наука/Биотехнологии", "university": "РНИМУ им. Пирогова, МГУ (ФФМ)",
        "link": "https://genetic-counselor-rus.ru", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, "social": 5, "routine": 4, "art": 1}
    },
    {
        "id": 204, "name": "Инженер по 3D-печати", "industry": "Промышленность/Инженерия/Прототипирование", "university": "МГТУ им. Баумана, МИСиС, СПбПУ",
        "link": "https://3d-print-engineer.ru", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 205, "name": "Специалист по возобновляемым источникам энергии", "industry": "Энергетика/Экология", "university": "МЭИ, Сколтех",
        "link": "https://renewable-energy-pro.ru", "junior_salary": 85000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 206, "name": "Медицинский физик", "industry": "Медицина/Наука/Физика", "university": "МИФИ, МГУ (Физфак)",
        "link": "https://medical-physicist-job.ru", "junior_salary": 70000, "avg_salary": 125000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 207, "name": "Prompt-инженер", "industry": "ИТ/Искусственный интеллект", "university": "Профильные курсы, технические ВУЗы",
        "link": "https://prompt-engineer-pro.ru", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 3}
    },
    {
        "id": 208, "name": "Chief Data Officer (CDO)", "industry": "Менеджмент/ИТ/Аналитика", "university": "Опыт + МГУ (ВМК), МФТИ, НИУ ВШЭ",
        "link": "https://cdo-russia-career.ru", "junior_salary": 250000, "avg_salary": 500000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 209, "name": "VR/AR-разработчик", "industry": "ИТ/Геймдев/Инженерия", "university": "Университет Иннополис, ИТМО, ДВФУ",
        "link": "https://vrar-developer-pro.ru", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 210, "name": "Агробиотехнолог", "industry": "Сельское хозяйство/Наука/Биотехнологии", "university": "РГАУ-МСХА им. Тимирязева, МГУ (Биофак)",
        "link": "https://agrobiotech-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 211, "name": "Тьютор (в образовании)", "industry": "Образование/Педагогика", "university": "МПГУ, НИУ ВШЭ (Институт образования)",
        "link": "https://tutor-edu-career.ru", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 212, "name": "Подкастер/Продюсер подкастов", "industry": "Медиа/Журналистика", "university": "МГУ (Журфак), профильные школы (Soundstream)",
        "link": "https://podcast-producer-job.ru", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 213, "name": "Нейросетевой художник / AI-художник", "industry": "Искусство/Дизайн/ИТ", "university": "Онлайн-платформы и курсы",
        "link": "https://ai-artist-pro.ru", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 214, "name": "Специалист по этике ИИ", "industry": "ИТ/Юриспруденция/Философия", "university": "МГУ, НИУ ВШЭ, СПбГУ",
        "link": "https://ai-ethics-officer.ru", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 215, "name": "Low-code/No-code разработчик", "industry": "ИТ/Бизнес", "university": "Платформы (Tilda, Bubble), онлайн-курсы",
        "link": "https://lowcode-developer.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 216, "name": "Цифровой куратор", "industry": "Культура/Искусство/ИТ", "university": "НИУ ВШЭ, РГГУ, Университет ИТМО",
        "link": "https://digital-curator-art.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 217, "name": "Разработчик голосовых интерфейсов", "industry": "ИТ/Искусственный интеллект", "university": "МФТИ, МИРЭА + курсы (Yandex)",
        "link": "https://voice-ui-developer.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 2}
    },
    {
        "id": 218, "name": "Менеджер по цифровой трансформации", "industry": "Менеджмент/ИТ/Консалтинг", "university": "РАНХиГС, Сколково, ВШБ НИУ ВШЭ",
        "link": "https://digital-transformation-manager.ru", "junior_salary": 120000, "avg_salary": 250000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 219, "name": "Специалист по большим данным в медицине", "industry": "Медицина/ИТ/Аналитика", "university": "Первый МГМУ им. Сеченова (Цифровая медицина), ИТМО",
        "link": "https://medical-bigdata.ru", "junior_salary": 95000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 220, "name": "Фандрайзер", "industry": "НКО/Социальная сфера/Маркетинг", "university": "МГИМО, НИУ ВШЭ, РГСУ",
        "link": "https://fundraiser-pro.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 221, "name": "Молекулярный диетолог", "industry": "Медицина/Биотехнологии/Wellness", "university": "РНИМУ им. Пирогова, МГУ",
        "link": "https://molecular-nutritionist.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 222, "name": "Архитектор 'умных' городов", "industry": "Архитектура/ИТ/Госуправление", "university": "МАРХИ, НИУ ВШЭ (Высшая школа урбанистики), ИТМО",
        "link": "https://smart-city-architect.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 3}
    },
    {
        "id": 223, "name": "Цифровой лингвист", "industry": "ИТ/Наука/Лингвистика", "university": "НИУ ВШЭ, РГГУ, МГУ (Филологический)",
        "link": "https://digital-linguist-job.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 224, "name": "Фэшн-стилист", "industry": "Мода/Медиа/Ритейл", "university": "БВШД, МГУ, профильные школы (Marangoni)",
        "link": "https://fashion-stylist-pro.ru", "junior_salary": 50000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 225, "name": "Специалист по геймификации", "industry": "ИТ/HR/Маркетинг/Образование", "university": "НИУ ВШЭ, онлайн-курсы",
        "link": "https://gamification-expert.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 3}
    },
    {
        "id": 226, "name": "Performance-маркетолог", "industry": "Маркетинг/ИТ/Аналитика", "university": "НИУ ВШЭ, РЭУ им. Плеханова, онлайн-платформы",
        "link": "https://performance-marketer.ru", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 227, "name": "Проектировщик 'умных' домов", "industry": "Строительство/ИТ/Дизайн", "university": "МГСУ, МЭИ",
        "link": "https://smarthome-designer-pro.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 228, "name": "Нейромаркетолог", "industry": "Маркетинг/Наука/Аналитика", "university": "НИУ ВШЭ, МГУ (Экономфак, Психфак)",
        "link": "https://neuromarketing-specialist.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 229, "name": "Специалист по работе с клиентами (в IT)", "industry": "ИТ/Сервис/Продажи", "university": "Любой ВУЗ + курсы",
        "link": "https://it-account-manager.ru", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 230, "name": "Монтажник слаботочных систем", "industry": "Строительство/Безопасность/ИТ", "university": "Технические колледжи",
        "link": "https://low-voltage-installer.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 231, "name": "Data Steward (Распорядитель данных)", "industry": "ИТ/Аналитика/Менеджмент", "university": "Технические и экономические ВУЗы",
        "link": "https://data-steward-pro.ru", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 232, "name": "Коуч (бизнес, лайф)", "industry": "Консалтинг/Психология/HR", "university": "Сертификационные программы (ICF), ВУЗы (психология)",
        "link": "https://coach-rus-pro.ru", "junior_salary": 50000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 233, "name": "Мастер-сыровар", "industry": "Производство/Сельское хозяйство/HoReCa", "university": "ВНИИМС (Углич), аграрные ВУЗы, частные школы",
        "link": "https://cheese-maker-pro.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 4}
    },
    {
        "id": 234, "name": "Киберследователь", "industry": "Безопасность/Госслужба/ИТ", "university": "МИФИ, МГТУ им. Баумана, ведомственные ВУЗы",
        "link": "https://cyber-detective-rus.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 235, "name": "Дизайнер одежды", "industry": "Мода/Дизайн/Производство", "university": "БВШД, МХПИ, РГУ им. Косыгина",
        "link": "https://fashion-designer-rus.ru", "junior_salary": 50000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 236, "name": "Специалист по интеллектуальной собственности", "industry": "Юриспруденция/ИТ/Наука", "university": "РГАИС, МГЮА им. Кутафина",
        "link": "https://ip-lawyer-pro.ru", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 237, "name": "Аналитик мобильных приложений", "industry": "ИТ/Аналитика/Маркетинг", "university": "НИУ ВШЭ, МФТИ",
        "link": "https://mobile-app-analyst.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 238, "name": "Воспитатель в детском саду", "industry": "Образование/Социальная сфера", "university": "МПГУ, РГПУ им. Герцена, педагогические колледжи",
        "link": "https://kindergarten-teacher-rus.ru", "junior_salary": 30000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 4}
    },
    {
        "id": 239, "name": "Орнитолог", "industry": "Наука/Экология", "university": "МГУ (Биофак), СПбГУ (Биофак)",
        "link": "https://ornithologist-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 240, "name": "DevSecOps-инженер", "industry": "ИТ/Безопасность", "university": "МГТУ им. Баумана, ИТМО + доп. образование",
        "link": "https://devsecops-engineer.ru", "junior_salary": 120000, "avg_salary": 230000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
# --- КОНЕЦ БЛОКА ДЛЯ КОПИРОВАНИЯ ---
# --- НАЧАЛО БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    # --- НАЧАЛО БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    {
        "id": 241, "name": "Электрик/Электромонтажник", "industry": "Строительство/ЖКХ/Рабочие", "university": "Технические колледжи, учебные центры",
        "link": "https://electrician-profi-rus.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 242, "name": "Сантехник", "industry": "Строительство/ЖКХ/Рабочие", "university": "Технические колледжи",
        "link": "https://plumber-master-job.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 243, "name": "Медсестра/Медбрат", "industry": "Медицина", "university": "Медицинские колледжи и училища",
        "link": "https://nurse-career-rus.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 244, "name": "Повар", "industry": "Общепит/HoReCa", "university": "Кулинарные колледжи и техникумы",
        "link": "https://cook-job-rus.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 4}
    },
    {
        "id": 245, "name": "Водитель-дальнобойщик", "industry": "Транспорт/Логистика", "university": "Автошколы (категория C+E), курсы",
        "link": "https://truck-driver-pro.ru", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 246, "name": "Продавец-консультант", "industry": "Ритейл/Торговля", "university": "Не требуется, тренинги на месте работы",
        "link": "https://sales-consultant-job.ru", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 247, "name": "Секретарь/Офис-менеджер", "industry": "Административная работа", "university": "Колледжи, профильные курсы",
        "link": "https://office-manager-career.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 248, "name": "Кладовщик", "industry": "Логистика/Склад", "university": "Среднее профессиональное образование",
        "link": "https://storekeeper-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 249, "name": "Охранник", "industry": "Безопасность", "university": "Школы охранников, лицензирование",
        "link": "https://security-guard-rus.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 250, "name": "Уборщик/Клинер", "industry": "Сервис/ЖКХ", "university": "Не требуется",
        "link": "https://cleaner-service-job.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 251, "name": "Автослесарь", "industry": "Автосервис/Рабочие", "university": "Технические колледжи и училища",
        "link": "https://auto-mechanic-rus.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 252, "name": "Лаборант (химический, медицинский)", "industry": "Наука/Медицина/Производство", "university": "Медицинские и химические колледжи",
        "link": "https://lab-assistant-pro.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 253, "name": "Социальный работник", "industry": "Социальная сфера/Госслужба", "university": "РГСУ, колледжи социальной работы",
        "link": "https://social-worker-rus.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 254, "name": "Кассир", "industry": "Ритейл/Торговля/Банки", "university": "Не требуется, обучение на месте",
        "link": "https://cashier-job-pro.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 255, "name": "Курьер", "industry": "Логистика/Сервис/Доставка", "university": "Не требуется",
        "link": "https://courier-delivery-job.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 256, "name": "Крановщик", "industry": "Строительство/Промышленность", "university": "Учебные центры, колледжи",
        "link": "https://crane-operator-rus.ru", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 257, "name": "Швея/Портной", "industry": "Легкая промышленность/Сервис/Ателье", "university": "Колледжи легкой промышленности",
        "link": "https://seamstress-tailor-job.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 4}
    },
    {
        "id": 258, "name": "Маляр-штукатур", "industry": "Строительство/Ремонт", "university": "Строительные колледжи",
        "link": "https://painter-plasterer-pro.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 259, "name": "Плотник/Столяр", "industry": "Строительство/Производство мебели", "university": "Профессиональные училища",
        "link": "https://carpenter-joiner-rus.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 260, "name": "Бурильщик (нефть и газ)", "industry": "Нефтегаз/Добыча", "university": "Профильные колледжи и ВУЗы (РГУ нефти и газа)",
        "link": "https://driller-oil-gas.ru", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 261, "name": "Фельдшер", "industry": "Медицина", "university": "Медицинские колледжи",
        "link": "https://paramedic-career-rus.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 262, "name": "Водитель такси", "industry": "Транспорт/Сервис", "university": "Автошколы (категория B), стаж вождения",
        "link": "https://taxi-driver-job.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 263, "name": "Пожарный", "industry": "Госслужба/Безопасность (МЧС)", "university": "Академия ГПС МЧС, учебные центры МЧС",
        "link": "https://firefighter-career-rus.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 264, "name": "Оператор call-центра", "industry": "Сервис/Продажи", "university": "Не требуется, тренинги",
        "link": "https://call-center-operator-job.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 265, "name": "Мастер маникюра/педикюра", "industry": "Красота/Сервис", "university": "Профильные школы и курсы",
        "link": "https://manicure-master-pro.ru", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 5, 'art': 5}
    },
    {
        "id": 266, "name": "Агент по недвижимости (Риелтор)", "industry": "Недвижимость/Продажи", "university": "Курсы, тренинги в агентствах",
        "link": "https://real-estate-agent-rus.ru", "junior_salary": 40000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 267, "name": "Менеджер по туризму", "industry": "Туризм/Сервис", "university": "РГУТиС, профильные ВУЗы и колледжи",
        "link": "https://tourism-manager-job.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 268, "name": "Официант", "industry": "Общепит/HoReCa", "university": "Не требуется, школы ресторанного сервиса",
        "link": "https://waiter-job-rus.ru", "junior_salary": 35000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 269, "name": "Фотограф", "industry": "Медиа/Сервис/Искусство", "university": "Школы фотографии, курсы",
        "link": "https://photographer-career-rus.ru", "junior_salary": 40000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 270, "name": "Мерчендайзер", "industry": "Ритейл/Торговля/Маркетинг", "university": "Не требуется",
        "link": "https://merchandiser-pro.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 2}
    },
    {
        "id": 271, "name": "Библиотекарь", "industry": "Культура/Образование", "university": "МГИК, СПбГИК, колледжи культуры",
        "link": "https://librarian-career-rus.ru", "junior_salary": 25000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 3}
    },
    {
        "id": 272, "name": "Сборщик мебели", "industry": "Сервис/Производство", "university": "Профессиональные училища",
        "link": "https://furniture-assembler-job.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 273, "name": "Монтажник окон", "industry": "Строительство/Сервис", "university": "Учебные центры производителей",
        "link": "https://window-installer-pro.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 274, "name": "Работник почты (Оператор связи)", "industry": "Госслужба/Логистика", "university": "Колледжи связи",
        "link": "https://post-office-worker.ru", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 275, "name": "Дорожный рабочий", "industry": "Строительство/ЖКХ", "university": "Строительные колледжи",
        "link": "https://road-worker-job.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 276, "name": "Дворник", "industry": "ЖКХ", "university": "Не требуется",
        "link": "https://janitor-career-rus.ru", "junior_salary": 25000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 277, "name": "Зубной техник", "industry": "Медицина/Стоматология", "university": "Медицинские колледжи",
        "link": "https://dental-technician-pro.ru", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 278, "name": "Аниматор (детский, отельный)", "industry": "Развлечения/Сервис", "university": "Педагогические и культурные ВУЗы, курсы",
        "link": "https://animator-job-rus.ru", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 279, "name": "Водитель автобуса/троллейбуса", "industry": "Транспорт/Госслужба", "university": "Учебно-курсовые комбинаты",
        "link": "https://bus-driver-career.ru", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 280, "name": "Работник конвейера/фабрики", "industry": "Промышленность/Производство", "university": "Не требуется",
        "link": "https://factory-worker-job.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 281, "name": "Менеджер по закупкам", "industry": "Торговля/Логистика/Производство", "university": "РЭУ им. Плеханова, НИУ ВШЭ",
        "link": "https://purchasing-manager-pro.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 282, "name": "Инструктор по вождению", "industry": "Образование/Сервис", "university": "Свидетельство на право обучения вождению",
        "link": "https://driving-instructor-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 283, "name": "Мясник", "industry": "Ритейл/Производство/Общепит", "university": "Колледжи пищевой промышленности",
        "link": "https://butcher-career-rus.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 284, "name": "Пекарь", "industry": "Общепит/Производство/Ритейл", "university": "Колледжи пищевой промышленности",
        "link": "https://baker-job-pro.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 285, "name": "Страховой агент", "industry": "Страхование/Финансы/Продажи", "university": "Курсы при страховых компаниях",
        "link": "https://insurance-agent-career.ru", "junior_salary": 40000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 286, "name": "Визажист", "industry": "Красота/Сервис/Медиа", "university": "Школы визажа, курсы",
        "link": "https://makeup-artist-pro-rus.ru", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 287, "name": "Монтажник натяжных потолков", "industry": "Строительство/Ремонт/Сервис", "university": "Обучение в компаниях",
        "link": "https://stretch-ceiling-installer.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 288, "name": "Комплектовщик заказов", "industry": "Склад/Логистика/Ритейл", "university": "Не требуется",
        "link": "https://order-picker-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 289, "name": "Массажист", "industry": "Медицина/Красота/Фитнес", "university": "Медицинские колледжи, курсы массажа",
        "link": "https://massage-therapist-pro.ru", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 290, "name": "Администратор гостиницы/отеля", "industry": "Гостиничный бизнес/HoReCa", "university": "Колледжи и ВУЗы гостиничного дела",
        "link": "https://hotel-administrator-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 2}
    },
# --- КОНЕЦ БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    {
        "id": 291, "name": "Слесарь-ремонтник", "industry": "Промышленность/ЖКХ/Рабочие", "university": "Технические колледжи и училища",
        "link": "https://fitter-repairman-job.ru", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 292, "name": "Врач-терапевт", "industry": "Медицина", "university": "Медицинские ВУЗы (Лечебное дело)",
        "link": "https://therapist-doctor-rus.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, "art": 1}
    },
    {
        "id": 293, "name": "Каменщик", "industry": "Строительство", "university": "Строительные колледжи и училища",
        "link": "https://bricklayer-pro-rus.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 294, "name": "Учитель начальных классов", "industry": "Образование", "university": "Педагогические ВУЗы и колледжи",
        "link": "https://primary-teacher-career.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 3}
    },
    {
        "id": 295, "name": "Машинист экскаватора", "industry": "Строительство/Добыча", "university": "Учебные центры, колледжи",
        "link": "https://excavator-operator-job.ru", "junior_salary": 80000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 296, "name": "Врач-педиатр", "industry": "Медицина", "university": "Медицинские ВУЗы (Педиатрия)",
        "link": "https://pediatrician-doctor-rus.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 297, "name": "Специалист по кадрам (Кадровик)", "industry": "HR/Административная работа", "university": "Профильные курсы, ВУЗы (Управление персоналом)",
        "link": "https://hr-specialist-rus.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 298, "name": "Бортпроводник", "industry": "Авиация/Транспорт/Сервис", "university": "Школы бортпроводников при авиакомпаниях",
        "link": "https://flight-attendant-career.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 299, "name": "Садовник/Озеленитель", "industry": "ЖКХ/Сервис/Ландшафтный дизайн", "university": "Аграрные и лесотехнические колледжи",
        "link": "https://gardener-rus-job.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 300, "name": "Контент-менеджер", "industry": "Маркетинг/ИТ/Медиа", "university": "Онлайн-курсы, ВУЗы (Журналистика, Филология)",
        "link": "https://content-manager-pro-rus.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 3}
    },
    {
        "id": 301, "name": "Фрезеровщик", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи",
        "link": "https://milling-operator-job.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 302, "name": "Сиделка", "industry": "Социальная сфера/Медицина", "university": "Медицинские колледжи, курсы",
        "link": "https://caregiver-rus-job.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 303, "name": "Горничная", "industry": "Гостиничный бизнес/Сервис", "university": "Не требуется",
        "link": "https://housekeeper-hotel-job.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 304, "name": "Экономист", "industry": "Финансы/Бухгалтерия/Менеджмент", "university": "Экономические ВУЗы (Финансовый университет, РЭУ, ВШЭ)",
        "link": "https://economist-career-pro.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 305, "name": "Водитель погрузчика", "industry": "Склад/Логистика/Производство", "university": "Учебные центры",
        "link": "https://forklift-driver-rus.ru", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 306, "name": "Рентгенолаборант", "industry": "Медицина", "university": "Медицинские колледжи",
        "link": "https://xray-technician-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 307, "name": "Хореограф/Преподаватель танцев", "industry": "Искусство/Образование/Фитнес", "university": "Институты культуры (МГИК, СПбГИК), театральные ВУЗы",
        "link": "https://choreographer-rus-career.ru", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 308, "name": "Специалист технической поддержки", "industry": "ИТ/Сервис", "university": "Технические колледжи, онлайн-курсы",
        "link": "https://tech-support-pro.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 309, "name": "Кровельщик", "industry": "Строительство", "university": "Строительные колледжи",
        "link": "https://roofer-pro-job.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 310, "name": "Врач-хирург", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по хирургии",
        "link": "https://surgeon-doctor-rus.ru", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 311, "name": "Грузчик", "industry": "Логистика/Сервис/Ритейл", "university": "Не требуется",
        "link": "https://loader-job-rus.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 312, "name": "Почтальон", "industry": "Логистика/Госслужба", "university": "Не требуется",
        "link": "https://postman-rus-career.ru", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 313, "name": "Оператор котельной", "industry": "ЖКХ/Промышленность", "university": "Учебные центры",
        "link": "https://boiler-operator-job.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 314, "name": "Учитель истории и обществознания", "industry": "Образование", "university": "Педагогические ВУЗы (Исторический факультет)",
        "link": "https://history-teacher-career.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 315, "name": "Диспетчер (транспорт, ЖКХ, аварийная служба)", "industry": "Транспорт/Логистика/ЖКХ", "university": "Профильные курсы, колледжи",
        "link": "https://dispatcher-rus-job.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 316, "name": "Маркшейдер", "industry": "Добыча/Геодезия/Строительство", "university": "Горные и политехнические ВУЗы (МГРИ)",
        "link": "https://mine-surveyor-pro.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 317, "name": "Санитар/Санитарка", "industry": "Медицина", "university": "Не требуется, курсы младшего медперсонала",
        "link": "https://hospital-attendant-job.ru", "junior_salary": 28000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 318, "name": "Инструктор тренажерного зала", "industry": "Фитнес/Спорт/Сервис", "university": "Колледжи и ВУЗы физкультуры (РГУФКСМиТ), курсы",
        "link": "https://gym-instructor-career.ru", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 319, "name": "Операционист в банке", "industry": "Банки/Финансы", "university": "Финансовые колледжи, тренинги в банках",
        "link": "https://bank-teller-rus.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 320, "name": "Грумер", "industry": "Сервис/Животные", "university": "Курсы и школы груминга",
        "link": "https://pet-groomer-pro.ru", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 4}
    },
    {
        "id": 321, "name": "Врач-офтальмолог (окулист)", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://ophthalmologist-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 322, "name": "Упаковщик/Комплектовщик", "industry": "Производство/Склад/Ритейл", "university": "Не требуется",
        "link": "https://packer-job-rus.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 323, "name": "Лесник/Егерь", "industry": "Лесное хозяйство/Экология", "university": "Лесотехнические ВУЗы и колледжи",
        "link": "https://forester-rus-career.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 324, "name": "Делопроизводитель/Архивариус", "industry": "Административная работа/Госслужба", "university": "Колледжи, РГГУ (Историко-архивный институт)",
        "link": "https://archivist-clerk-job.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 325, "name": "Кондитер", "industry": "Общепит/Производство", "university": "Колледжи пищевой промышленности, кулинарные школы",
        "link": "https://confectioner-pro-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 326, "name": "Монтажник вентиляции и кондиционирования", "industry": "Строительство/ЖКХ", "university": "Технические колледжи",
        "link": "https://hvac-installer-rus.ru", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 327, "name": "Животновод (Доярка, скотник)", "industry": "Сельское хозяйство", "university": "Аграрные колледжи",
        "link": "https://livestock-farmer-job.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 328, "name": "Секретарь суда", "industry": "Юриспруденция/Госслужба", "university": "Юридические колледжи, ВУЗы",
        "link": "https://court-clerk-career.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 329, "name": "Учитель физкультуры", "industry": "Образование/Спорт", "university": "Институты физкультуры, педагогические ВУЗы",
        "link": "https://pe-teacher-rus.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 330, "name": "Заправщик на АЗС", "industry": "Сервис/Ритейл", "university": "Не требуется",
        "link": "https://gas-station-attendant.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 331, "name": "Врач-ЛОР (Оториноларинголог)", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://ent-doctor-rus.ru", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 332, "name": "Машинист автокрана", "industry": "Строительство", "university": "Учебные центры",
        "link": "https://mobile-crane-operator.ru", "junior_salary": 75000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 333, "name": "Облицовщик-плиточник", "industry": "Строительство/Ремонт", "university": "Строительные колледжи",
        "link": "https://tile-setter-pro.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 334, "name": "Консьерж/Вахтер", "industry": "ЖКХ/Сервис", "university": "Не требуется",
        "link": "https://concierge-rus-job.ru", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 335, "name": "Водолаз", "industry": "Промышленность/Строительство/МЧС", "university": "Водолазные школы",
        "link": "https://diver-pro-rus.ru", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 336, "name": "Контролер ОТК", "industry": "Промышленность/Производство", "university": "Технические колледжи",
        "link": "https://quality-control-inspector.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 337, "name": "Проводник поезда", "industry": "Транспорт/Сервис (РЖД)", "university": "Учебные центры РЖД",
        "link": "https://train-conductor-rus.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 338, "name": "Бетонщик", "industry": "Строительство", "university": "Строительные колледжи",
        "link": "https://concrete-worker-pro.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 339, "name": "Стекольщик", "industry": "Строительство/Производство", "university": "Профессиональные училища",
        "link": "https://glazier-job-rus.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 340, "name": "Посудомойщица/Посудомойщик", "industry": "Общепит/HoReCa", "university": "Не требуется",
        "link": "https://dishwasher-job-rus.ru", "junior_salary": 30000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    # --- НАЧАЛО БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    {
        "id": 341, "name": "Наладчик станков с ЧПУ", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи, учебные центры",
        "link": "https://cnc-setter-pro.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 342, "name": "Врач-стоматолог-терапевт", "industry": "Медицина/Стоматология", "university": "Медицинские ВУЗы (Стоматология)",
        "link": "https://dentist-therapist-rus.ru", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 3}
    },
    {
        "id": 343, "name": "Домработница", "industry": "Сервис/Частные услуги", "university": "Не требуется, рекомендации",
        "link": "https://housekeeper-rus-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 344, "name": "Юрисконсульт", "industry": "Юриспруденция/Бизнес", "university": "Юридические ВУЗы (МГЮА, МГУ)",
        "link": "https://legal-counsel-pro.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 345, "name": "Тракторист-машинист", "industry": "Сельское хозяйство/Строительство", "university": "Аграрные и технические колледжи",
        "link": "https://tractor-driver-rus.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 346, "name": "Врач-дерматолог", "industry": "Медицина/Красота", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://dermatologist-doc-rus.ru", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 347, "name": "Торговый представитель", "industry": "Продажи/FMCG/Ритейл", "university": "Не требуется, тренинги",
        "link": "https://sales-representative-pro.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 348, "name": "Музыкальный руководитель (в ДОУ)", "industry": "Образование/Искусство", "university": "Педагогические колледжи, консерватории, институты культуры",
        "link": "https://music-teacher-preschool.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 349, "name": "Арматурщик", "industry": "Строительство", "university": "Строительные колледжи",
        "link": "https://rebar-worker-rus.ru", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 350, "name": "Заведующий складом", "industry": "Логистика/Ритейл/Производство", "university": "Колледжи, ВУЗы (Логистика)",
        "link": "https://warehouse-manager-rus.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 351, "name": "Закройщик", "industry": "Легкая промышленность/Ателье", "university": "Колледжи легкой промышленности",
        "link": "https://pattern-cutter-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 4}
    },
    {
        "id": 352, "name": "Оптометрист (специалист по подбору очков)", "industry": "Медицина/Ритейл/Сервис", "university": "Медицинские колледжи (оптика)",
        "link": "https://optometrist-rus-pro.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 353, "name": "Шахтер", "industry": "Добыча/Промышленность", "university": "Горные техникумы и ВУЗы",
        "link": "https://miner-career-rus.ru", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 354, "name": "Аппаратчик (химическое производство)", "industry": "Промышленность/Химия", "university": "Химико-технологические колледжи",
        "link": "https://chemical-operator-job.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 355, "name": "Секретарь-референт", "industry": "Административная работа", "university": "Колледжи, курсы, ВУЗы (Документоведение)",
        "link": "https://personal-assistant-rus.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 356, "name": "Лифтер", "industry": "ЖКХ/Сервис", "university": "Курсы, инструктаж",
        "link": "https://elevator-operator-job.ru", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 357, "name": "Инженер-теплотехник", "industry": "Энергетика/ЖКХ/Промышленность", "university": "Энергетические ВУЗы (МЭИ)",
        "link": "https://heat-engineer-pro.ru", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 358, "name": "Суши-повар (сушист)", "industry": "Общепит/HoReCa", "university": "Кулинарные курсы, обучение на месте",
        "link": "https://sushi-chef-rus.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 359, "name": "Такелажник", "industry": "Промышленность/Строительство", "university": "Учебные центры",
        "link": "https://rigger-rus-job.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 360, "name": "Врач-невролог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://neurologist-rus-doc.ru", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 361, "name": "Водитель трамвая", "industry": "Транспорт/Госслужба", "university": "Учебно-курсовые комбинаты",
        "link": "https://tram-driver-career.ru", "junior_salary": 55000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 362, "name": "Банщик", "industry": "Сервис/Здоровье", "university": "Курсы, школы банного мастерства",
        "link": "https://banya-attendant-pro.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 363, "name": "Шлифовщик", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи",
        "link": "https://grinder-operator-job.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 364, "name": "Школьный психолог", "industry": "Образование/Психология", "university": "Психологические и педагогические ВУЗы (МГУ, МПГУ)",
        "link": "https://school-psychologist-rus.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 365, "name": "Работник мусоровоза", "industry": "ЖКХ", "university": "Не требуется",
        "link": "https://waste-collector-job.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 366, "name": "Кальянщик", "industry": "Общепит/HoReCa/Сервис", "university": "Курсы, обучение на месте",
        "link": "https://hookah-master-job.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 367, "name": "Врач-гинеколог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://gynecologist-rus-doc.ru", "junior_salary": 65000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 368, "name": "Изолировщик", "industry": "Строительство/Промышленность", "university": "Строительные колледжи",
        "link": "https://insulator-worker-job.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 369, "name": "Репетитор", "industry": "Образование/Частные услуги", "university": "Педагогические и профильные ВУЗы",
        "link": "https://tutor-private-job.ru", "junior_salary": 40000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 370, "name": "Слесарь КИПиА", "industry": "Промышленность/Энергетика", "university": "Технические и политехнические колледжи",
        "link": "https://instrumentation-fitter.ru", "junior_salary": 70000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 371, "name": "Инспектор ДПС", "industry": "Госслужба/Право (МВД)", "university": "Учебные центры МВД, юридические ВУЗы",
        "link": "https://traffic-police-inspector.ru", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 372, "name": "Рамщик (пилорамщик)", "industry": "Деревообработка/Лесная промышленность", "university": "Лесотехнические колледжи",
        "link": "https://sawmill-operator-job.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 373, "name": "Мастер по ремонту обуви", "industry": "Сервис/Частные услуги", "university": "Колледжи, обучение у мастера",
        "link": "https://shoe-repairman-pro.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 4, 'routine': 5, 'art': 3}
    },
    {
        "id": 374, "name": "Инспектор по кадрам", "industry": "HR/Административная работа", "university": "Курсы, ВУЗы (Управление персоналом, Юриспруденция)",
        "link": "https://hr-inspector-career.ru", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 375, "name": "Пчеловод", "industry": "Сельское хозяйство", "university": "Аграрные колледжи, курсы",
        "link": "https://beekeeper-rus-job.ru", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 376, "name": "Врач скорой помощи", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по скорой помощи",
        "link": "https://ambulance-doctor-pro.ru", "junior_salary": 75000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 377, "name": "Пескоструйщик", "industry": "Промышленность/Строительство/Ремонт", "university": "Учебные центры",
        "link": "https://sandblaster-pro-job.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 378, "name": "Часовщик", "industry": "Сервис/Ремонт/Ритейл", "university": "Профильные колледжи, обучение у мастера",
        "link": "https://watchmaker-rus-job.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 3}
    },
    {
        "id": 379, "name": "Литейщик", "industry": "Промышленность/Металлургия", "university": "Металлургические колледжи",
        "link": "https://foundry-worker-pro.ru", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 380, "name": "Заведующий хозяйством (Завхоз)", "industry": "Административная работа/Образование/Медицина", "university": "Не требуется специального",
        "link": "https://facilities-manager-rus.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 381, "name": "Машинист бульдозера", "industry": "Строительство/Добыча", "university": "Учебные центры, колледжи",
        "link": "https://bulldozer-operator-job.ru", "junior_salary": 80000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 382, "name": "Врач-инфекционист", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://infectious-disease-doc.ru", "junior_salary": 65000, "avg_salary": 125000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 383, "name": "Ювелир", "industry": "Производство/Ритейл/Искусство", "university": "Колледжи декоративно-прикладного искусства, курсы",
        "link": "https://jeweler-rus-pro.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 5, 'art': 5}
    },
    {
        "id": 384, "name": "Сталевар", "industry": "Промышленность/Металлургия", "university": "Металлургические техникумы и ВУЗы",
        "link": "https://steelmaker-pro-job.ru", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 385, "name": "Воспитатель группы продленного дня", "industry": "Образование", "university": "Педагогические колледжи и ВУЗы",
        "link": "https://after-school-teacher.ru", "junior_salary": 28000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 3}
    },
    {
        "id": 386, "name": "Доярка/Оператор машинного доения", "industry": "Сельское хозяйство", "university": "Аграрные колледжи",
        "link": "https://milking-operator-job.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 387, "name": "Гардеробщик", "industry": "Сервис/Культура/Общепит", "university": "Не требуется",
        "link": "https://cloakroom-attendant-job.ru", "junior_salary": 20000, "avg_salary": 28000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 388, "name": "Обвальщик мяса", "industry": "Производство/Ритейл", "university": "Колледжи пищевой промышленности",
        "link": "https://meat-deboner-pro.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 389, "name": "Стекловар", "industry": "Промышленность/Производство", "university": "Химико-технологические колледжи",
        "link": "https://glassmaker-job-rus.ru", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 2}
    },
    {
        "id": 390, "name": "Младший воспитатель (помощник воспитателя)", "industry": "Образование", "university": "Педагогические колледжи, курсы",
        "link": "https://assistant-teacher-rus.ru", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 2}
    },
# --- КОНЕЦ БЛОКА ДЛЯ КОПИРОВАНИЯ ---
# --- НАЧАЛО БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    {
        "id": 391, "name": "Обивщик мебели", "industry": "Производство/Сервис/Рабочие", "university": "Профессиональные училища, обучение на производстве",
        "link": "https://upholsterer-rus-job.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 392, "name": "Врач-УЗИст (специалист УЗИ)", "industry": "Медицина/Диагностика", "university": "Медицинские ВУЗы + курсы переподготовки",
        "link": "https://ultrasound-doctor-pro.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 393, "name": "Инженер-сметчик", "industry": "Строительство/Финансы", "university": "МГСУ, профильные курсы",
        "link": "https://estimator-engineer-pro.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 394, "name": "Чиновник / Государственный служащий", "industry": "Госслужба/Административная работа", "university": "РАНХиГС, МГУ (Гос. управление), профильные ВУЗы",
        "link": "https://civil-servant-rus.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 395, "name": "Вулканизаторщик/Шиномонтажник", "industry": "Автосервис/Рабочие", "university": "Технические колледжи, курсы",
        "link": "https://tire-fitter-job.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 396, "name": "Помощник юриста", "industry": "Юриспруденция", "university": "Юридические колледжи, студенты юрфаков",
        "link": "https://paralegal-rus-career.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 397, "name": "Рыбак (промысловик)", "industry": "Добыча/Сельское хозяйство", "university": "Морские и рыбопромышленные колледжи",
        "link": "https://fisherman-pro-rus.ru", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 398, "name": "Таможенный инспектор", "industry": "Госслужба/Логистика", "university": "РТА, РАНХиГС (Таможенное дело)",
        "link": "https://customs-inspector-job.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 399, "name": "Стеклодув", "industry": "Производство/Искусство", "university": "Художественно-промышленные академии, колледжи",
        "link": "https://glassblower-art-rus.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 1, 'routine': 4, 'art': 5}
    },
    {
        "id": 400, "name": "Врач-психиатр", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по психиатрии",
        "link": "https://psychiatrist-doc-rus.ru", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 401, "name": "Обходчик железнодорожных путей", "industry": "Транспорт/РЖД", "university": "Железнодорожные колледжи и техникумы",
        "link": "https://track-walker-job.ru", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 402, "name": "Оператор дробильной установки", "industry": "Добыча/Промышленность", "university": "Горные техникумы",
        "link": "https://crusher-operator-pro.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 403, "name": "Заточник инструментов", "industry": "Сервис/Рабочие", "university": "Профессиональные училища, курсы",
        "link": "https://tool-sharpener-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, "social": 3, "routine": 5, "art": 2}
    },
    {
        "id": 404, "name": "Учитель музыки", "industry": "Образование/Искусство", "university": "Консерватории, педагогические ВУЗы, институты культуры",
        "link": "https://music-school-teacher.ru", "junior_salary": 30000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 405, "name": "Сборщик урожая/Полевод", "industry": "Сельское хозяйство", "university": "Аграрные колледжи",
        "link": "https://field-worker-rus.ru", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 406, "name": "Работник химчистки", "industry": "Сервис", "university": "Колледжи, обучение на месте",
        "link": "https://dry-cleaner-job.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 407, "name": "Дезинфектор", "industry": "Сервис/Медицина/ЖКХ", "university": "Профильные курсы, медицинские колледжи",
        "link": "https://disinfector-pro-rus.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 408, "name": "Сотрудник планетария", "industry": "Культура/Образование/Наука", "university": "Педагогические, физические, астрономические ВУЗы",
        "link": "https://planetarium-worker-job.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 409, "name": "Мастер по изготовлению ключей", "industry": "Сервис", "university": "Обучение у мастера",
        "link": "https://key-maker-pro.ru", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 410, "name": "Врач-гастроэнтеролог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://gastroenterologist-doc.ru", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 411, "name": "Вальцовщик", "industry": "Промышленность/Металлургия", "university": "Металлургические колледжи",
        "link": "https://rolling-mill-operator.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 412, "name": "Технолог швейного производства", "industry": "Легкая промышленность", "university": "РГУ им. Косыгина, технологические колледжи",
        "link": "https://sewing-technologist-pro.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 2}
    },
    {
        "id": 413, "name": "Машинист асфальтоукладчика", "industry": "Строительство", "university": "Учебные центры, колледжи",
        "link": "https://asphalt-paver-operator.ru", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 414, "name": "Смотритель музея", "industry": "Культура", "university": "Гуманитарные ВУЗы (История, Искусствоведение)",
        "link": "https://museum-attendant-job.ru", "junior_salary": 28000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 3}
    },
    {
        "id": 415, "name": "Парковщик", "industry": "Сервис/Транспорт", "university": "Не требуется",
        "link": "https://parking-attendant-rus.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 416, "name": "Судебный пристав", "industry": "Госслужба/Юриспруденция", "university": "Юридические и экономические ВУЗы",
        "link": "https://bailiff-rus-career.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 417, "name": "Инженер по бурению", "industry": "Нефтегаз/Добыча", "university": "РГУ нефти и газа им. Губкина, горные ВУЗы",
        "link": "https://drilling-engineer-pro.ru", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 418, "name": "Художник-оформитель/Декоратор", "industry": "Искусство/Дизайн/Ритейл", "university": "Художественные училища, академии",
        "link": "https://decorator-artist-job.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 419, "name": "Табельщик", "industry": "Административная работа/Производство", "university": "Экономические колледжи, курсы",
        "link": "https://timekeeper-job-rus.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 420, "name": "Врач-фтизиатр", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://tb-doctor-rus.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 421, "name": "Товаровед", "industry": "Ритейл/Торговля/Логистика", "university": "Торгово-экономические колледжи и ВУЗы",
        "link": "https://merchandise-expert-pro.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 422, "name": "Рыбовод", "industry": "Сельское хозяйство", "university": "Аграрные и рыбохозяйственные ВУЗы",
        "link": "https://fish-farmer-pro.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 423, "name": "Асфальтобетонщик", "industry": "Строительство", "university": "Строительные колледжи",
        "link": "https://asphalt-worker-job.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 424, "name": "Учитель русского языка и литературы", "industry": "Образование", "university": "Педагогические и классические ВУЗы (Филология)",
        "link": "https://russian-teacher-career.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 4}
    },
    {
        "id": 425, "name": "Оператор заправочных станций", "industry": "Ритейл/Сервис", "university": "Обучение на рабочем месте",
        "link": "https://gas-station-operator.ru", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 426, "name": "Ассистент ветеринарного врача", "industry": "Медицина/Животные", "university": "Аграрные и медицинские колледжи",
        "link": "https://vet-assistant-job.ru", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 427, "name": "Копировальщик/Оператор печатного оборудования", "industry": "Сервис/Полиграфия", "university": "Колледжи, курсы",
        "link": "https://copy-operator-pro.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 428, "name": "Судостроитель/Сборщик корпусов", "industry": "Промышленность/Судостроение", "university": "Судостроительные колледжи и ВУЗы",
        "link": "https://shipbuilder-rus-job.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 429, "name": "Лаборант-эколог", "industry": "Экология/Наука/Промышленность", "university": "Экологические и химические факультеты ВУЗов, колледжи",
        "link": "https://eco-lab-assistant.ru", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 430, "name": "Врач-эндоскопист", "industry": "Медицина/Диагностика", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://endoscopist-doctor-pro.ru", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 431, "name": "Оператор ЧПУ (деревообработка)", "industry": "Производство/Деревообработка", "university": "Технические колледжи",
        "link": "https://cnc-wood-operator.ru", "junior_salary": 65000, "avg_salary": 105000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 2}
    },
    {
        "id": 432, "name": "Заготовщик (в общепите)", "industry": "Общепит/HoReCa", "university": "Кулинарные колледжи",
        "link": "https://kitchen-prep-worker.ru", "junior_salary": 38000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 433, "name": "Мойщик автомобилей", "industry": "Автосервис", "university": "Не требуется",
        "link": "https://car-washer-job.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 434, "name": "Паспортист", "industry": "ЖКХ/Госслужба", "university": "Курсы, среднее профессиональное образование",
        "link": "https://passport-clerk-job.ru", "junior_salary": 30000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 435, "name": "Лифтовой механик", "industry": "ЖКХ/Сервис/Рабочие", "university": "Технические колледжи, учебные центры",
        "link": "https://elevator-mechanic-pro.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 436, "name": "Сборщик ПК", "industry": "ИТ/Ритейл/Сервис", "university": "Курсы, самостоятельное обучение",
        "link": "https://pc-assembler-pro.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 437, "name": "Кастелянша", "industry": "Гостиничный бизнес/Медицина/Сервис", "university": "Не требуется",
        "link": "https://linen-keeper-job.ru", "junior_salary": 28000, "avg_salary": 38000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 438, "name": "Мастер участка (производство)", "industry": "Промышленность/Менеджмент", "university": "Технические ВУЗы и колледжи",
        "link": "https://production-foreman-job.ru", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 439, "name": "Билетер", "industry": "Культура/Развлечения", "university": "Не требуется",
        "link": "https://ticket-collector-job.ru", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 440, "name": "Врач-патологоанатом", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://pathologist-rus-doc.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 441, "name": "Преподаватель ВУЗа", "industry": "Образование/Наука", "university": "Аспирантура, ученая степень",
        "link": "https://university-lecturer-pro.ru", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 442, "name": "Коневод", "industry": "Сельское хозяйство/Спорт", "university": "Аграрные ВУЗы (зоотехния), курсы",
        "link": "https://horse-breeder-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 443, "name": "Расклейщик объявлений", "industry": "Реклама/Сервис", "university": "Не требуется",
        "link": "https://flyer-poster-job.ru", "junior_salary": 25000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 444, "name": "Стекольщик (автомобильный)", "industry": "Автосервис", "university": "Курсы, обучение на месте",
        "link": "https://auto-glass-installer.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 445, "name": "Приемщик заказов (в химчистке, ремонте)", "industry": "Сервис", "university": "Не требуется",
        "link": "https://service-receptionist-job.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 446, "name": "Музейный работник/Хранитель фондов", "industry": "Культура/Наука", "university": "РГГУ, ВУЗы (История, Искусствоведение)",
        "link": "https://museum-curator-rus.ru", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 447, "name": "Термист", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи",
        "link": "https://heat-treater-pro.ru", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 448, "name": "Врач-диетолог", "industry": "Медицина/Здоровье/Фитнес", "university": "Медицинские ВУЗы + курсы переподготовки",
        "link": "https://dietitian-doctor-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 449, "name": "Стропальщик", "industry": "Строительство/Промышленность/Логистика", "university": "Учебные центры (удостоверение)",
        "link": "https://slinger-rigger-job.ru", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 450, "name": "Помощник повара", "industry": "Общепит/HoReCa", "university": "Кулинарные колледжи",
        "link": "https://assistant-cook-job.ru", "junior_salary": 40000, "avg_salary": 55000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 2}
        # --- НАЧАЛО БЛОКА ДЛЯ КОПИРОВАНИЯ ---
    },
    {
        "id": 451, "name": "Дата-аналитик (Data Analyst)", "industry": "ИТ/Аналитика/Маркетинг", "university": "НИУ ВШЭ, РЭУ им. Плеханова, онлайн-курсы",
        "link": "https://data-analyst-career-rus.ru", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 452, "name": "Врач-уролог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по урологии",
        "link": "https://urologist-doctor-pro.ru", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 453, "name": "Сетевой инженер", "industry": "ИТ/Телекоммуникации", "university": "МТУСИ, МГТУ им. Баумана",
        "link": "https://network-engineer-rus.ru", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 454, "name": "Врач-аллерголог-иммунолог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://allergist-immunologist-doc.ru", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 455, "name": "Инженер по автоматизации тестирования (QA Automation)", "industry": "ИТ", "university": "Технические ВУЗы + профильные курсы",
        "link": "https://qa-automation-pro-rus.ru", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 456, "name": "Медицинский лабораторный техник", "industry": "Медицина/Диагностика", "university": "Медицинские колледжи",
        "link": "https://med-lab-technician.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 457, "name": "Разработчик баз данных (Database Developer)", "industry": "ИТ", "university": "МГТУ им. Баумана, МИРЭА, ИТМО",
        "link": "https://database-developer-rus.ru", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 458, "name": "Врач-ревматолог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://rheumatologist-doc-pro.ru", "junior_salary": 60000, "avg_salary": 125000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 459, "name": "Авиамеханик/Авиатехник", "industry": "Авиация/Транспорт/Инженерия", "university": "МГТУ ГА, Самарский университет, авиационные колледжи",
        "link": "https://aviation-mechanic-pro.ru", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 460, "name": "Врач-пульмонолог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://pulmonologist-doctor-rus.ru", "junior_salary": 65000, "avg_salary": 135000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 461, "name": "Логист (координатор по логистике)", "industry": "Логистика/Транспорт/Торговля", "university": "МАДИ, ВУЗы с направлением 'Логистика'",
        "link": "https://logistics-coordinator-rus.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 462, "name": "Врач-нефролог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://nephrologist-doc-pro.ru", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 463, "name": "Специалист по тендерам", "industry": "Закупки/Юриспруденция/Продажи", "university": "Курсы, ВУЗы (Юриспруденция, Экономика)",
        "link": "https://tender-specialist-pro.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 464, "name": "Младший медицинский персонал (санитар, сестра-хозяйка)", "industry": "Медицина", "university": "Курсы, инструктаж",
        "link": "https://junior-medical-staff.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 465, "name": "Менеджер по работе с клиентами", "industry": "Продажи/Сервис/ИТ", "university": "Любой ВУЗ + тренинги",
        "link": "https://account-manager-rus.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 466, "name": "Фельдшер-лаборант", "industry": "Медицина/Диагностика", "university": "Медицинские колледжи",
        "link": "https://paramedic-lab-tech.ru", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 467, "name": "Машинист компрессорных установок", "industry": "Промышленность/Энергетика", "university": "Технические колледжи",
        "link": "https://compressor-operator-pro.ru", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 468, "name": "Врач-гематолог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://hematologist-doctor-rus.ru", "junior_salary": 75000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 469, "name": "Начальник отдела продаж", "industry": "Продажи/Менеджмент", "university": "Опыт + любой ВУЗ",
        "link": "https://head-of-sales-rus.ru", "junior_salary": 100000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 470, "name": "Техник-протезист (ортопед)", "industry": "Медицина/Производство", "university": "Медицинские колледжи по специальности 'Ортопедическая и реабилитационная техника'",
        "link": "https://prosthetist-technician-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 5, 'art': 3}
    },
    {
        "id": 471, "name": "Бухгалтер-калькулятор (в общепите)", "industry": "Бухгалтерия/Общепит", "university": "Экономические колледжи, курсы",
        "link": "https://cost-accountant-horeca.ru", "junior_salary": 50000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 472, "name": "Татуировщик", "industry": "Искусство/Сервис", "university": "Художественные школы, обучение у мастера",
        "link": "https://tattooer-rus-pro.ru", "junior_salary": 50000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 473, "name": "Сурдолог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "link": "https://audiologist-doctor-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 474, "name": "Электрогазосварщик", "industry": "Строительство/Промышленность/Рабочие", "university": "Технические колледжи",
        "link": "https://electric-gas-welder-pro.ru", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 475, "name": "Составитель поездов", "industry": "Транспорт/РЖД", "university": "Железнодорожные колледжи",
        "link": "https://train-compiler-job.ru", "junior_salary": 60000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 476, "name": "Налоговый инспектор", "industry": "Госслужба/Финансы", "university": "Финансовый университет, РЭУ, экономические ВУЗы",
        "link": "https://tax-inspector-rus.ru", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 477, "name": "Сотрудник ППС (Патрульно-постовая служба)", "industry": "Госслужба/Право (МВД)", "university": "Учебные центры МВД",
        "link": "https://patrol-officer-rus.ru", "junior_salary": 55000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 478, "name": "Регистратор (в поликлинике)", "industry": "Медицина/Административная работа", "university": "Медицинские колледжи, курсы",
        "link": "https://medical-registrar-job.ru", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 479, "name": "Оценщик автомобилей", "industry": "Автосервис/Страхование/Финансы", "university": "Технические ВУЗы (МАДИ), курсы оценщиков",
        "link": "https://auto-appraiser-pro.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 480, "name": "Кредитный специалист", "industry": "Банки/Финансы/Ритейл", "university": "Финансовые колледжи, экономические ВУЗы",
        "link": "https://credit-specialist-rus.ru", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 481, "name": "Мастер по ремонту стиральных машин", "industry": "Сервис/Рабочие", "university": "Технические колледжи, курсы",
        "link": "https://washing-machine-repair.ru", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 482, "name": "Пивовар", "industry": "Производство/Общепит", "university": "Технологические ВУЗы (пищевое производство), курсы",
        "link": "https://brewer-pro-rus.ru", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 483, "name": "Лепщик (пельменей, вареников)", "industry": "Производство/Общепит", "university": "Не требуется",
        "link": "https://dumpling-maker-job.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 2}
    },
    {
        "id": 484, "name": "Инженер по охране окружающей среды (Инженер-эколог)", "industry": "Промышленность/Экология/Госслужба", "university": "РУДН (Экологический), РХТУ",
        "link": "https://environmental-protection-engineer.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 485, "name": "Начальник АХО (административно-хозяйственного отдела)", "industry": "Административная работа/Менеджмент", "university": "Любой ВУЗ + опыт",
        "link": "https://head-of-admin-dep.ru", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 486, "name": "Винодел", "industry": "Сельское хозяйство/Производство", "university": "Аграрные ВУЗы (КубГАУ), курсы",
        "link": "https://winemaker-rus-pro.ru", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 4}
    },
    {
        "id": 487, "name": "Мастер по ремонту холодильников", "industry": "Сервис/Рабочие", "university": "Технические колледжи, курсы",
        "link": "https://refrigerator-repair-pro.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 488, "name": "Сотрудник архива", "industry": "Административная работа/Госслужба/Культура", "university": "РГГУ (Историко-архивный институт), колледжи",
        "link": "https://archive-worker-career.ru", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 489, "name": "Газорезчик", "industry": "Промышленность/Строительство/Металлообработка", "university": "Технические колледжи",
        "link": "https://gas-cutter-pro.ru", "junior_salary": 65000, "avg_salary": 105000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 490, "name": "Сотрудник исправительной колонии (инспектор ФСИН)", "industry": "Госслужба/Право", "university": "Ведомственные ВУЗы ФСИН, юридические факультеты",
        "link": "https://corrections-officer-rus.ru", "junior_salary": 50000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 491, "name": "Коллектор/Специалист по взысканию задолженности", "industry": "Финансы/Юриспруденция", "university": "Экономические и юридические колледжи/ВУЗы",
        "link": "https://debt-collector-rus.ru", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 492, "name": "Специалист по мобильной технике/Телемастер", "industry": "Сервис/Ремонт/Ритейл", "university": "Технические колледжи, курсы",
        "link": "https://mobile-repair-master.ru", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 493, "name": "Пограничник", "industry": "Госслужба/Безопасность (ФСБ)", "university": "Пограничные институты ФСБ",
        "link": "https://border-guard-rus.ru", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 494, "name": "Оценщик в ломбарде", "industry": "Финансы/Ритейл/Сервис", "university": "Курсы, геммологическое образование",
        "link": "https://pawnshop-appraiser-job.ru", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 495, "name": "Лесопатолог", "industry": "Лесное хозяйство/Экология", "university": "Лесотехнические ВУЗы",
        "link": "https://forest-pathologist-rus.ru", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 496, "name": "Машинист насосных установок", "industry": "ЖКХ/Промышленность", "university": "Технические колледжи",
        "link": "https://pump-operator-pro.ru", "junior_salary": 50000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 497, "name": "Финансовый консультант", "industry": "Финансы/Консалтинг/Страхование", "university": "Финансовый университет, РЭУ, ВШЭ, курсы",
        "link": "https://financial-advisor-rus.ru", "junior_salary": 60000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 498, "name": "Инженер по наладке и испытаниям", "industry": "Промышленность/Энергетика/Строительство", "university": "Технические ВУЗы (МЭИ, МГТУ)",
        "link": "https://commissioning-engineer-rus.ru", "junior_salary": 75000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 499, "name": "Слесарь по ремонту автомобилей", "industry": "Автосервис/Рабочие", "university": "Технические колледжи",
        "link": "https://auto-repair-fitter.ru", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 500, "name": "Ди-джей (DJ)", "industry": "Развлечения/Музыка/HoReCa", "university": "Школы диджеинга, курсы",
        "link": "https://dj-career-rus.ru", "junior_salary": 40000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    }
]


DB_NAME = 'careers.db'

def create_and_populate_db():
    """Создает базу данных SQLite и заполняет таблицу careers."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Удаление старой таблицы, если она существует
    cursor.execute("DROP TABLE IF EXISTS careers")

    # 2. Создание таблицы careers с новым столбцом junior_salary.
    cursor.execute('''
        CREATE TABLE careers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT,
            university TEXT,
            link TEXT,
            junior_salary INTEGER,
            avg_salary INTEGER,
            growth_rate TEXT,
            score_vector TEXT
        )
    ''')

    # 3. Заполнение данными
    for career in CAREER_DATA:
        # Конвертация score_vector в строку JSON
        score_vector_json = json.dumps(career['score_vector'], ensure_ascii=False)

        cursor.execute('''
            INSERT INTO careers (
                id, name, industry, university, link, junior_salary, avg_salary, growth_rate, score_vector
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            career['id'],
            career['name'],
            career['industry'],
            career['university'],
            career['link'],
            career['junior_salary'],
            career['avg_salary'],
            career['growth_rate'],
            score_vector_json
        ))

    conn.commit()
    conn.close()
    print(f"База данных '{DB_NAME}' успешно создана и заполнена {len(CAREER_DATA)} записями.")

if __name__ == '__main__':
    # Удаление дубликатов по имени и переиндексация (для гарантии чистоты данных)
    unique_careers = []
    seen_names = set()
    for career in CAREER_DATA:
        if career['name'] not in seen_names:
            unique_careers.append(career)
            seen_names.add(career['name'])
    
    # Переназначаем ID
    for i, career in enumerate(unique_careers):
        career['id'] = i + 1
        
    CAREER_DATA = unique_careers

    create_and_populate_db()