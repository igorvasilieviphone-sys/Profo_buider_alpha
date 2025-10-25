import sqlite3
import json
from typing import List, Dict, Any

# Обновленные и очищенные данные о профессиях
CAREER_DATA: List[Dict[str, Any]] = [

    {
        "id": 1, "name": "Дата-сайентист", "industry": "ИТ/Аналитика", "university": "МГУ (ВМК), МФТИ (ФПМИ)",
        "description": "Анализирует большие данные для оптимизации бизнес-процессов в российских IT-гигантах, банках и ритейле. Одна из самых высокооплачиваемых и востребованных профессий на рынке.",
        "link": "https://postupi.online/professiya/data-scientist/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 1, 'art': 1}
    },
    {
        "id": 2, "name": "Графический дизайнер", "industry": "Креатив/Медиа", "university": "НИУ ВШЭ (Дизайн), МГХПА им. Строганова",
        "description": "Создает визуальные концепции для брендов, сайтов и рекламы. Востребован в студиях, маркетинговых агентствах и на фрилансе по всей России.",
        "link": "https://postupi.online/professiya/graficheskij-dizajner/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 3, "name": "Менеджер по продажам", "industry": "Продажи/Бизнес", "university": "РЭУ им. Плеханова, Финансовый университет",
        "description": "Ключевой специалист в любой коммерческой компании РФ, от стартапа до корпорации. Отвечает за поиск клиентов и выполнение плана продаж. Доход часто сильно зависит от KPI.",
        "link": "https://postupi.online/professiya/menedzher-po-prodazham/", "junior_salary": 55000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 4, "name": "Бухгалтер", "industry": "Финансы/Учет", "university": "Финансовый университет, СПбГЭУ",
        "description": "Обеспечивает финансовый порядок в компании, работает с налогами и отчетностью в соответствии с российским законодательством. Стабильная и востребованная профессия.",
        "link": "https://postupi.online/professiya/buhgalter/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 5, "name": "Инженер-электронщик", "industry": "Промышленность/Технологии", "university": "МГТУ им. Баумана, СПбПУ Петра Великого",
        "description": "Разрабатывает и обслуживает электронные устройства и системы на промышленных предприятиях, в ВПК и наукоемких стартапах России.",
        "link": "https://postupi.online/professiya/inzhener-elektronshchik/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 6, "name": "Врач-кардиолог", "industry": "Медицина", "university": "Первый МГМУ им. Сеченова, ПСПбГМУ им. Павлова",
        "description": "Диагностирует и лечит заболевания сердца и сосудов. Работает в государственных поликлиниках, больницах и частных медицинских центрах по всей стране.",
        "link": "https://postupi.online/professiya/kardiolog/", "junior_salary": 50000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 7, "name": "Frontend-разработчик", "industry": "ИТ", "university": "МТУСИ, ИТМО",
        "description": "Создает пользовательские интерфейсы сайтов и веб-приложений. Одна из самых популярных IT-профессий в России с возможностью удаленной работы.",
        "link": "https://postupi.online/professiya/frontend-razrabotchik/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 3}
    },
    {
        "id": 8, "name": "Юрист (Корпоративное право)", "industry": "Юриспруденция", "university": "МГУ (Юрфак), МГЮА им. Кутафина",
        "description": "Сопровождает деятельность компаний: от регистрации и реорганизации до крупных сделок. Работает в юридических фирмах и инхаус-командах.",
        "link": "https://postupi.online/professiya/yurist/", "junior_salary": 60000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 9, "name": "SMM-менеджер", "industry": "Маркетинг/Медиа", "university": "РАНХиГС (Маркетинг), НИУ ВШЭ (Коммуникации)",
        "description": "Продвигает бренды и продукты в российских социальных сетях (VK, Telegram). Отвечает за контент, рекламу и коммуникацию с аудиторией.",
        "link": "https://postupi.online/professiya/smm-menedzher/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 10, "name": "Архитектор", "industry": "Строительство/Дизайн", "university": "МАРХИ, СПбГАСУ",
        "description": "Проектирует здания и городские пространства. Работает в архитектурных бюро, строительных компаниях и госструктурах, формируя облик российских городов.",
        "link": "https://postupi.online/professiya/arhitektor/", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 11, "name": "PR-менеджер", "industry": "Коммуникации", "university": "МГИМО, СПбГУ (Журналистика)",
        "description": "Формирует и поддерживает положительный имидж компании в российских СМИ и обществе. Организует мероприятия и работает с журналистами и блогерами.",
        "link": "https://postupi.online/professiya/pr-menedzher/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 12, "name": "Аналитик BI", "industry": "ИТ/Финансы", "university": "РЭУ им. Плеханова, ИТМО",
        "description": "Превращает сырые данные в понятные отчеты и дашборды, помогая российскому бизнесу принимать верные решения. Востребован в финансах, ритейле и IT.",
        "link": "https://postupi.online/professiya/biznes-analitik/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 13, "name": "Повар-технолог", "industry": "Общепит/Производство", "university": "РЭУ им. Плеханова (Технология)",
        "description": "Разрабатывает рецептуры и контролирует технологию приготовления блюд на пищевых производствах, в столовых и крупных ресторанных сетях.",
        "link": "https://postupi.online/professiya/povar-tehnolog/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 4}
    },
    {
        "id": 14, "name": "Риелтор", "industry": "Недвижимость", "university": "ГУУ (Менеджмент)",
        "description": "Помогает людям покупать, продавать и арендовать недвижимость. Динамичная работа с высоким потенциалом дохода, особенно в крупных городах России.",
        "link": "https://postupi.online/professiya/rieltor/", "junior_salary": 40000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 15, "name": "Сварщик", "industry": "Рабочие/Промышленность", "university": "Технические колледжи",
        "description": "Востребованный рабочий специалист в строительстве, промышленности и ЖКХ. Квалифицированные сварщики с опытом высоко ценятся на рынке труда России.",
        "link": "https://postupi.online/professiya/svarshchik/", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 16, "name": "Педагог-дефектолог", "industry": "Образование/Медицина", "university": "МПГУ, РГПУ им. Герцена",
        "description": "Помогает детям с особенностями развития (речь, слух, интеллект) адаптироваться к учебе и жизни. Работает в школах, детских садах и центрах коррекции.",
        "link": "https://postupi.online/professiya/pedagog-defektolog/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 17, "name": "DevOps-инженер", "industry": "ИТ", "university": "СПбГУ (Математика), НИУ ВШЭ (Прикладная математика)",
        "description": "Автоматизирует процессы разработки и развертывания ПО, объединяя разработчиков и системных администраторов. Критически важен для современных IT-компаний.",
        "link": "https://postupi.online/professiya/devops-inzhener/", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 18, "name": "Аудитор", "industry": "Финансы/Консалтинг", "university": "МГИМО, Финансовый университет",
        "description": "Проверяет финансовую отчетность компаний на соответствие стандартам и законодательству. Работает в 'Большой четверке' и крупных российских аудиторских фирмах.",
        "link": "https://postupi.online/professiya/auditor/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 19, "name": "Копирайтер", "industry": "Медиа/Маркетинг", "university": "МГУ (Журфак), РГГУ",
        "description": "Пишет тексты для сайтов, рекламы, соцсетей и email-рассылок. Может работать в штате или на фрилансе, спрос на качественные тексты стабильно высокий.",
        "link": "https://postupi.online/professiya/kopirajter/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 20, "name": "Логист-международник", "industry": "Транспорт/ВЭД", "university": "МИИТ, СПбГЭУ",
        "description": "Организует доставку грузов через границы, решая таможенные и транспортные задачи в условиях постоянно меняющихся торговых путей.",
        "link": "https://postupi.online/professiya/logist/", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 21, "name": "Арт-директор", "industry": "Креатив/Медиа", "university": "БВШД, НИУ ВШЭ (Дизайн)",
        "description": "Отвечает за визуальную концепцию проекта в рекламных агентствах, издательствах и IT-компаниях. Управляет командой дизайнеров и креативщиков.",
        "link": "https://postupi.online/professiya/art-direktor/", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 1, 'art': 5}
    },
    {
        "id": 22, "name": "Специалист по кибербезопасности", "industry": "ИТ/Безопасность", "university": "МИФИ, МГТУ им. Баумана (ИБ)",
        "description": "Защищает IT-инфраструктуру компаний от хакерских атак и утечек данных. Спрос на этих специалистов в России огромен, особенно в госсекторе и банках.",
        "link": "https://postupi.online/professiya/specialist-po-kiberbezopasnosti/", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 23, "name": "Геолог", "industry": "Добыча/Геология", "university": "МГУ (Геологический), СПбГУ",
        "description": "Изучает строение Земли, ищет месторождения полезных ископаемых. Работа часто связана с экспедициями в разные регионы России.",
        "link": "https://postupi.online/professiya/geolog/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 24, "name": "Спортивный тренер", "industry": "Спорт/Фитнес", "university": "РГУФКСМиТ, НГУ им. Лесгафта",
        "description": "Готовит спортсменов к соревнованиям или проводит занятия в фитнес-клубах. Работает со взрослыми и детьми, развивая их физические качества.",
        "link": "https://postupi.online/professiya/trener/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 25, "name": "Web-аналитик", "industry": "Маркетинг/ИТ", "university": "НИУ ВШЭ (Экономика), СПбГУ",
        "description": "Анализирует поведение пользователей на сайтах и в приложениях, помогая улучшать продукт и повышать эффективность рекламы. Работает в digital-агентствах и IT-компаниях.",
        "link": "https://postupi.online/professiya/web-analitik/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 3, 'art': 1}
    },
    {
        "id": 26, "name": "Менеджер проектов (IT)", "industry": "ИТ", "university": "МИРЭА, НИУ ВШЭ (Бизнес-информатика)",
        "description": "Руководит командой разработчиков, дизайнеров и аналитиков для создания IT-продуктов в срок и в рамках бюджета. Ключевая роль в любой технологической компании.",
        "link": "https://postupi.online/professiya/menedzher-proektov-v-it/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 27, "name": "Режиссер монтажа", "industry": "Медиа/Кино", "university": "ВГИК, СПбГИКиТ",
        "description": "Собирает отснятый материал в единое целое, создавая фильмы, сериалы, клипы или рекламные ролики. Работает на телеканалах, в продакшн-студиях и на фрилансе.",
        "link": "https://postupi.online/professiya/rezhisser-montazha/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 28, "name": "Инженер по охране труда", "industry": "Промышленность/ОТ", "university": "МГСУ",
        "description": "Обеспечивает безопасность на производстве, контролирует соблюдение норм и правил охраны труда. Обязательная должность на любом крупном предприятии.",
        "link": "https://postupi.online/professiya/inzhener-po-ohrane-truda/", "junior_salary": 50000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 29, "name": "Фармацевт", "industry": "Медицина/Фармацевтика", "university": "РХТУ им. Менделеева",
        "description": "Работает в аптеке, консультирует покупателей по лекарственным препаратам, отпускает рецептурные и безрецептурные средства.",
        "link": "https://postupi.online/professiya/farmacevt/", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 30, "name": "Полицейский/Следователь", "industry": "Госслужба/Право", "university": "МВД РФ, Университет Прокуратуры",
        "description": "Обеспечивает правопорядок, расследует преступления. Государственная служба с социальными гарантиями, требующая высокой ответственности.",
        "link": "https://postupi.online/professiya/sledovatel/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 31, "name": "UX/UI-дизайнер", "industry": "ИТ/Дизайн", "university": "НИУ ВШЭ (Дизайн), ИТМО",
        "description": "Проектирует удобные и красивые интерфейсы для сайтов и мобильных приложений. Одна из ключевых и хорошо оплачиваемых ролей в IT-продуктовой разработке.",
        "link": "https://postupi.online/professiya/ux-ui-dizajner/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 4}
    },
    {
        "id": 32, "name": "Финансовый аналитик", "industry": "Финансы/Банки", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Анализирует финансовые данные компании для принятия инвестиционных и управленческих решений. Работает в банках, инвестиционных фондах и крупных корпорациях.",
        "link": "https://postupi.online/professiya/finansovyj-analitik/", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 33, "name": "Прораб (Производитель работ)", "industry": "Строительство", "university": "МГСУ, СПбГАСУ",
        "description": "Руководит строительными работами непосредственно на объекте, отвечает за качество, сроки и команду рабочих. Ключевая фигура на любой стройке.",
        "link": "https://postupi.online/professiya/prorab/", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 34, "name": "Специалист по тендерам", "industry": "Госзакупки/Юриспруденция", "university": "Академии Госзакупок",
        "description": "Помогает компаниям участвовать в государственных и коммерческих закупках, готовит документацию и сопровождает торги. Востребован в B2B и B2G секторах.",
        "link": "https://postupi.online/professiya/specialist-po-tenderam/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 35, "name": "Ветеринарный врач", "industry": "Медицина/Биология", "university": "МГАВМиБ им. Скрябина",
        "description": "Лечит домашних и сельскохозяйственных животных. Работает в ветеринарных клиниках, на агропредприятиях и в госструктурах. Спрос на услуги постоянно растет.",
        "link": "https://postupi.online/professiya/veterinar/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 36, "name": "Инженер-нефтяник", "industry": "Нефтегаз", "university": "РГУ нефти и газа им. Губкина",
        "description": "Занимается разведкой, бурением и эксплуатацией нефтяных и газовых месторождений. Одна из самых высокооплачиваемых инженерных профессий в России.",
        "link": "https://postupi.online/professiya/inzhener-neftyanik/", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 37, "name": "Сценарист", "industry": "Кино/ТВ/Медиа", "university": "ВГИК, МГУ (Журфак)",
        "description": "Создает истории и диалоги для фильмов, сериалов, компьютерных игр и рекламных роликов. Работа в основном проектная, требует таланта и упорства.",
        "link": "https://postupi.online/professiya/scenarist/", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 1, 'art': 5}
    },
    {
        "id": 38, "name": "Переводчик (синхронный)", "industry": "Лингвистика/Коммуникации", "university": "МГИМО, МГЛУ",
        "description": "Осуществляет устный перевод речи в реальном времени на конференциях и переговорах. Элитная и высокооплачиваемая специализация для лингвистов.",
        "link": "https://postupi.online/professiya/perevodchik/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 39, "name": "HR-менеджер (Рекрутер)", "industry": "Управление персоналом", "university": "НИУ ВШЭ (Управление), РГГУ",
        "description": "Занимается поиском, подбором и адаптацией персонала. Важный специалист для любой растущей компании, особенно в IT и других конкурентных отраслях.",
        "link": "https://postupi.online/professiya/hr-menedzher/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 40, "name": "Бармен-бариста", "industry": "Общепит/Сервис", "university": "Колледжи, Проф. курсы",
        "description": "Готовит кофе и коктейли, создает атмосферу в кафе и барах. Популярная профессия в сфере гостеприимства, особенно в больших городах.",
        "link": "https://postupi.online/professiya/barista/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 41, "name": "Системный администратор", "industry": "ИТ/Поддержка", "university": "МТУСИ, МГТУ им. Баумана",
        "description": "Поддерживает работу компьютерной техники и сетей в компании. Обеспечивает стабильность IT-инфраструктуры в офисах по всей России.",
        "link": "https://postupi.online/professiya/sistemnyj-administrator/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 42, "name": "Учитель математики/физики", "industry": "Образование", "university": "МПГУ, МФТИ (Пед. Фак.)",
        "description": "Преподает точные науки в школах и лицеях. Важная и уважаемая профессия, спрос на сильных педагогов всегда высок, также есть возможности для репетиторства.",
        "link": "https://postupi.online/professiya/uchitel-matematiki/", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 43, "name": "Маркетолог-аналитик", "industry": "Маркетинг/Аналитика", "university": "НИУ ВШЭ (Маркетинг), СПбГЭУ",
        "description": "Исследует рынок, конкурентов и потребителей, чтобы строить эффективные маркетинговые стратегии. Работает на стыке креатива и данных.",
        "link": "https://skillbox.ru/media/marketing/marketologanalitik-chem-on-zanimaetsya-i-kak-osvoit-etu-spetsializatsiyu/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 44, "name": "Химик-технолог", "industry": "Промышленность/Наука", "university": "РХТУ им. Менделеева, СПбГТИ(ТУ)",
        "description": "Разрабатывает и контролирует технологические процессы на химических, пищевых и фармацевтических производствах в России.",
        "link": "https://postupi.online/professiya/himik-tehnolog/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 45, "name": "Эколог", "industry": "Экология/Госслужба", "university": "МГУ (Географический), РУДН",
        "description": "Оценивает воздействие деятельности человека на окружающую среду, работает на промышленных предприятиях и в надзорных органах (Росприроднадзор).",
        "link": "https://postupi.online/professiya/ekolog/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 46, "name": "3D-моделлер/Аниматор", "industry": "Геймдев/Медиа", "university": "НИУ ВШЭ (Дизайн), Scream School",
        "description": "Создает трехмерные модели и анимацию для компьютерных игр, кино и рекламы. Российская игровая индустрия и анимационные студии активно ищут таких специалистов.",
        "link": "https://postupi.online/professiya/3d-animator/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 1, 'routine': 2, 'art': 5}
    },
    {
        "id": 47, "name": "Главный инженер проекта (ГИП)", "industry": "Строительство/Проектирование", "university": "МГСУ, МГТУ им. Баумана",
        "description": "Комплексно руководит разработкой проектной документации для строительства, несет ответственность за все технические решения. Высокостатусная и ответственная должность.",
        "link": "https://postupi.online/professiya/glavnyj-inzhener-proekta/", "junior_salary": 100000, "avg_salary": 170000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 48, "name": "Экскурсовод/Гид", "industry": "Туризм/Сервис", "university": "РГУТиС, МГУ (Географический)",
        "description": "Проводит экскурсии для российских и иностранных туристов, знакомя их с историей и культурой городов и регионов России. Работа часто сезонная.",
        "link": "https://postupi.online/professiya/ekskursovod/", "junior_salary": 30000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 49, "name": "Адвокат (Уголовное право)", "industry": "Юриспруденция", "university": "МГЮА им. Кутафина, СПбГУ (Юрфак)",
        "description": "Защищает права граждан на стадии следствия и в суде по уголовным делам. Требует глубоких знаний закона, стрессоустойчивости и ораторского мастерства.",
        "link": "https://postupi.online/professiya/advokat/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 50, "name": "Брокер на фондовом рынке", "industry": "Финансы", "university": "Финансовый университет, НИУ ВШЭ (Финансы)",
        "description": "Помогает частным и корпоративным клиентам совершать сделки с ценными бумагами на Московской бирже. Работа в инвестиционных компаниях и банках.",
        "link": "https://postupi.online/professiya/broker/", "junior_salary": 90000, "avg_salary": 250000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 1, 'art': 1}
    },
    {
        "id": 51, "name": "Инженер по машинному обучению (ML Engineer)", "industry": "ИТ/Искусственный интеллект", "university": "МФТИ (ФПМИ), НИУ ВШЭ (ФКН), ИТМО",
        "description": "Разрабатывает и внедряет алгоритмы искусственного интеллекта (например, нейросети) для решения задач бизнеса. Работает в Яндексе, Сбере и других техно-гигантах.",
        "link": "https://practicum.yandex.ru/blog/kto-takoy-ml-engineer/", "junior_salary": 110000, "avg_salary": 220000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 1}
    },
    {
        "id": 52, "name": "Менеджер по работе с маркетплейсами", "industry": "E-commerce/Продажи", "university": "РЭУ им. Плеханова, НИУ ВШЭ (Маркетинг)",
        "description": "Отвечает за продажи товаров на Ozon, Wildberries, Яндекс.Маркете. Управляет карточками товаров, ценами, рекламой и логистикой. Очень востребованная профессия.",
        "link": "https://postupi.online/professiya/menedzher-marketplejsov/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 1}
    },
    {
        "id": 53, "name": "Педагогический дизайнер", "industry": "Образование/EdTech", "university": "НИУ ВШЭ (Институт образования), МПГУ",
        "description": "Проектирует эффективные и увлекательные онлайн-курсы и образовательные программы. Ключевой специалист в бурно растущей сфере российского EdTech.",
        "link": "https://postupi.online/professiya/pedagogicheskij-dizajner/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 3}
    },
    {
        "id": 54, "name": "Психолог-консультант", "industry": "Психология/Здравоохранение", "university": "МГУ (Психфак), НИУ ВШЭ (Психология)",
        "description": "Помогает людям справляться с жизненными трудностями, стрессом и эмоциональными проблемами через индивидуальные и групповые консультации. Часто ведет частную практику.",
        "link": "https://postupi.online/professiya/psiholog-konsultant/", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 55, "name": "Геймдизайнер", "industry": "Геймдев/Креатив", "university": "НИУ ВШЭ (Геймдизайн), Scream School",
        "description": "Придумывает правила, механики и мир компьютерной игры. Отвечает за то, чтобы в игру было интересно играть. Работает в российских студиях разработки игр.",
        "link": "https://hi-tech.mail.ru/review/123791-gejmdizajne/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 4}
    },
    {
        "id": 56, "name": "Агроном (точное земледелие)", "industry": "Сельское хозяйство/Технологии", "university": "РГАУ-МСХА им. Тимирязева, КубГАУ",
        "description": "Управляет растениеводством с помощью современных технологий: дронов, спутниковых данных и 'умной' техники. Повышает урожайность в агрохолдингах России.",
        "link": "https://postupi.online/professiya/agronom/", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 57, "name": "SEO-специалист", "industry": "Маркетинг/ИТ", "university": "Профильные курсы, НИУ ВШЭ (Маркетинг)",
        "description": "Продвигает сайты в поисковых системах Яндекс и Google, чтобы они занимали первые места в выдаче. Цель — привлечь больше бесплатных посетителей на сайт.",
        "link": "https://postupi.online/professiya/seo-specialist/", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 58, "name": "Пилот гражданской авиации", "industry": "Транспорт/Авиация", "university": "УИ ГА (Ульяновск), СПбГУ ГА (Санкт-Петербург)",
        "description": "Управляет пассажирскими и грузовыми самолетами в российских авиакомпаниях. Престижная, ответственная и высокооплачиваемая профессия.",
        "link": "https://www.s7.ru/ru/media/blog/kak-stat-pilotom-grazhdanskoj-aviacii/", "junior_salary": 100000, "avg_salary": 350000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 59, "name": "Электромонтажник", "industry": "Строительство/Рабочие", "university": "Технические колледжи и училища",
        "description": "Прокладывает и подключает электрические сети и оборудование на строительных объектах и промышленных предприятиях. Квалифицированный специалист всегда востребован.",
        "link": "https://postupi.online/professiya/elektromontazhnik/", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 60, "name": "Биоинформатик", "industry": "Наука/ИТ/Биотехнологии", "university": "МГУ (Биоинженерия и биоинформатика), СПбАУ РАН",
        "description": "Анализирует биологические данные (например, ДНК) с помощью компьютерных методов. Работает в научных институтах и биотехнологических компаниях над задачами генетики и медицины.",
        "link": "https://postupi.online/professiya/bioinformatik/", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 61, "name": "Backend-разработчик", "industry": "ИТ", "university": "МГТУ им. Баумана, ИТМО, МИФИ",
        "description": "Создает 'мозг' сайтов и приложений — серверную часть, которая обрабатывает данные и логику. Одна из самых фундаментальных и востребованных профессий в IT.",
        "link": "https://postupi.online/professiya/backend-razrabotchik/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 62, "name": "Продуктовый менеджер (IT)", "industry": "ИТ/Менеджмент", "university": "НИУ ВШЭ, МФТИ",
        "description": "Отвечает за создание и развитие IT-продукта (сайта, приложения), определяет его стратегию, функционал и ценность для пользователя и бизнеса. Ключевая роль в продуктовых компаниях.",
        "link": "https://practicum.yandex.ru/blog/kto-takoy-product-manager/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 63, "name": "QA-инженер (Тестировщик ПО)", "industry": "ИТ", "university": "Политех, ЛЭТИ, профильные курсы",
        "description": "Ищет ошибки и уязвимости в программном обеспечении перед его выпуском. Обеспечивает качество IT-продуктов, является важной частью команды разработки.",
        "link": "https://postupi.online/professiya/testirovshchik-po/", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 64, "name": "Стоматолог-ортодонт", "industry": "Медицина", "university": "МГМСУ им. Евдокимова, ПСПбГМУ им. Павлова",
        "description": "Исправляет прикус и выравнивает зубы с помощью брекетов и элайнеров. Одно из самых востребованных и прибыльных направлений в российской стоматологии.",
        "link": "https://postupi.online/professiya/stomatolog-ortodont/", "junior_salary": 80000, "avg_salary": 200000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 65, "name": "Инженер-конструктор (Машиностроение)", "industry": "Промышленность/Инженерия", "university": "МГТУ им. Баумана, Самарский университет",
        "description": "Проектирует детали, узлы и механизмы для машин и оборудования. Работает на заводах, в конструкторских бюро, в том числе в оборонной промышленности.",
        "link": "https://postupi.online/professiya/inzhener-konstruktor/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 66, "name": "Оператор БПЛА (Дронов)", "industry": "Технологии/Логистика/Агро", "university": "МАИ, Профильные центры подготовки",
        "description": "Управляет беспилотными летательными аппаратами для аэросъемки, доставки грузов, мониторинга объектов. Новая и быстрорастущая профессия в России.",
        "link": "https://sky.pro/wiki/profession/professiya-operator-bespilotnykh-letatelnykh-apparatov-obyazannosti-navyki/", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 1, 'routine': 4, 'art': 2}
    },
    {
        "id": 67, "name": "Шеф-повар", "industry": "Общепит/HoReCa", "university": "Кулинарные школы (Novikov School, Swissam)",
        "description": "Руководит кухней ресторана, разрабатывает меню, контролирует качество блюд и управляет командой поваров. Ключевая фигура в ресторанном бизнесе.",
        "link": "https://postupi.online/professiya/shef-povar/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 68, "name": "Data Engineer", "industry": "ИТ/Big Data", "university": "МГУ (ВМК), СПбГУ (Матмех)",
        "description": "Строит и обслуживает 'трубопроводы' для больших данных: собирает, обрабатывает и хранит информацию, делая ее доступной для аналитиков и дата-сайентистов.",
        "link": "https://skillbox.ru/media/code/data-engineer-kto-eto-takoy-chem-zanimaetsya-kak-im-stat/", "junior_salary": 100000, "avg_salary": 190000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 69, "name": "Нейрохирург", "industry": "Медицина", "university": "НМИЦ им. Бурденко, Первый МГМУ им. Сеченова",
        "description": "Проводит сложнейшие операции на головном и спинном мозге. Одна из самых элитных и ответственных медицинских специальностей.",
        "link": "https://postupi.online/professiya/nejrohirurg/", "junior_salary": 80000, "avg_salary": 250000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 70, "name": "GR-менеджер (Government Relations)", "industry": "Бизнес/Госуправление", "university": "МГИМО, РАНХиГС",
        "description": "Выстраивает отношения компании с органами государственной власти, лоббирует ее интересы. Работает в крупных российских корпорациях.",
        "link": "https://postupi.online/professiya/gr-menedzher/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 71, "name": "Мобильный разработчик (iOS/Android)", "industry": "ИТ", "university": "НИУ ВШЭ (ПМИ), МИРЭА",
        "description": "Создает приложения для смартфонов и планшетов. В России высокий спрос на разработчиков как под Android, так и под iOS со стороны банков, ритейла и IT-компаний.",
        "link": "https://skillbox.ru/media/code/kto_takoy_mobilnyy_razrabotchik_i_kak_im_stat/", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 3}
    },
    {
        "id": 72, "name": "Косметолог-эстетист", "industry": "Красота/Медицина", "university": "Медицинские колледжи, РУДН (Эстетическая косметология)",
        "description": "Проводит уходовые процедуры для лица и тела, аппаратные и инъекционные методики. Работает в салонах красоты и клиниках, имеет стабильный поток клиентов.",
        "link": "https://postupi.online/professiya/kosmetolog-estetist/", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 4}
    },
    {
        "id": 73, "name": "Бизнес-аналитик", "industry": "ИТ/Консалтинг/Финансы", "university": "НИУ ВШЭ (Бизнес-информатика), Финансовый университет",
        "description": "Выявляет проблемы бизнеса и предлагает решения по их оптимизации, часто с помощью IT. 'Переводчик' с языка бизнеса на язык разработчиков.",
        "link": "https://postupi.online/professiya/biznes-analitik/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 74, "name": "Инженер-робототехник", "industry": "ИТ/Инженерия/Промышленность", "university": "Университет Иннополис, Сколтех, ИТМО",
        "description": "Проектирует, создает и обслуживает роботов для промышленности, медицины и других сфер. Перспективная профессия на фоне автоматизации производств в России.",
        "link": "https://postupi.online/professiya/robototehnik/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 2}
    },
    {
        "id": 75, "name": "Ландшафтный дизайнер", "industry": "Дизайн/Архитектура", "university": "МАРХИ, РГАУ-МСХА им. Тимирязева",
        "description": "Проектирует сады, парки и приусадебные участки, создавая гармоничное пространство. Востребован в частном секторе и в проектах благоустройства городов.",
        "link": "https://postupi.online/professiya/landshaftnyj-dizajner/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 76, "name": "Motion-дизайнер", "industry": "Креатив/Медиа/Реклама", "university": "БВШД, Scream School",
        "description": "Создает анимированную графику для видео, рекламы, телевидения и интерфейсов. 'Оживляет' статичные изображения, делая их динамичными и привлекательными.",
        "link": "https://postupi.online/professiya/motion-dizajner/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 2, 'art': 5}
    },
    {
        "id": 77, "name": "Менеджер по ВЭД", "industry": "Логистика/Торговля", "university": "РАНХиГС (Таможенное дело), СПбГЭУ",
        "description": "Сопровождает экспортные и импортные сделки компании, работает с таможней, поставщиками и перевозчиками. Важный специалист в торговых и производственных компаниях.",
        "link": "https://postupi.online/professiya/menedzher-po-ved/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 78, "name": "Парикмахер-стилист", "industry": "Красота/Сервис", "university": "Академии (TONI&GUY, Pivot Point), Технологические колледжи",
        "description": "Создает стрижки, укладки и окрашивания, подбирая клиенту индивидуальный образ. Может работать в салоне или на себя, доход сильно зависит от мастерства и клиентской базы.",
        "link": "https://postupi.online/professiya/parikmaher-stilist/", "junior_salary": 40000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 79, "name": "Генетик", "industry": "Наука/Медицина", "university": "МГУ (Биофак), СПбГУ (Биофак)",
        "description": "Изучает наследственность и изменчивость генов. Работает в медицинских центрах, консультируя пары, и в научных лабораториях, исследуя генетические заболевания.",
        "link": "https://postupi.online/professiya/genetik/", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 80, "name": "Блокчейн-разработчик", "industry": "ИТ/Финтех", "university": "МФТИ, МИФИ, ИТМО",
        "description": "Создает децентрализованные приложения и системы на основе технологии блокчейн. Высокооплачиваемая и нишевая специализация в российском финтехе и IT-стартапах.",
        "link": "https://postupi.online/professiya/blokchejn-razrabotchik/", "junior_salary": 120000, "avg_salary": 250000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 81, "name": "Промышленный дизайнер", "industry": "Дизайн/Промышленность", "university": "МГХПА им. Строганова, СПбГХПА им. Штиглица",
        "description": "Проектирует внешний вид и эргономику промышленных товаров: от бытовой техники до автомобилей. Работает в дизайн-студиях и на производственных предприятиях.",
        "link": "https://postupi.online/professiya/promyshlennyj-dizajner/", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 82, "name": "Автомеханик-диагност", "industry": "Автосервис/Рабочие", "university": "МАДИ, Политехнические колледжи",
        "description": "Находит и устраняет неисправности в современных автомобилях с помощью специального диагностического оборудования. Высококвалифицированный рабочий.",
        "link": "https://postupi.online/professiya/avtomehanik/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 83, "name": "Логопед", "industry": "Образование/Медицина", "university": "МПГУ (Дефектологический), РГПУ им. Герцена",
        "description": "Корректирует нарушения речи у детей и взрослых. Работает в детских садах, школах, поликлиниках, а также ведет востребованную частную практику.",
        "link": "https://postupi.online/professiya/logoped/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 84, "name": "Event-менеджер", "industry": "Маркетинг/Организация мероприятий", "university": "РГУТиС, СПбГИК",
        "description": "Организует мероприятия 'под ключ': от корпоративов и конференций до фестивалей. Динамичная и стрессовая работа для коммуникабельных и организованных людей.",
        "link": "https://postupi.online/professiya/event-menedzher/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 85, "name": "Технический писатель", "industry": "ИТ/Документация", "university": "МГЛУ, МГУ (Филологический)",
        "description": "Создает понятную документацию для сложного программного обеспечения: инструкции, руководства, API-справки. Важный специалист в крупных IT-компаниях.",
        "link": "https://postupi.online/professiya/tehnicheskij-pisatel/", "junior_salary": 60000, "avg_salary": 105000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 86, "name": "Директор по маркетингу (CMO)", "industry": "Маркетинг/Менеджмент", "university": "НИУ ВШЭ, Стокгольмская школа экономики в России",
        "description": "Руководит всей маркетинговой деятельностью в компании, отвечает за стратегию, бюджет и достижение бизнес-целей. Топ-менеджерская позиция.",
        "link": "https://postupi.online/professiya/direktor-po-marketingu/", "junior_salary": 150000, "avg_salary": 300000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 1, 'art': 2}
    },
    {
        "id": 87, "name": "Сомелье/Кавист", "industry": "Рестораны/Ритейл", "university": "Школы сомелье (Enotria, Wine People)",
        "description": "Помогает гостям ресторана или покупателям винотеки выбрать вино, составляет винную карту. Эксперт в области вина и других напитков.",
        "link": "https://postupi.online/professiya/somele/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 88, "name": "Медиатор (разрешение споров)", "industry": "Юриспруденция/Консалтинг", "university": "Центры медиации при ВУЗах (МГУ, СПбГУ)",
        "description": "Помогает сторонам конфликта (в бизнесе или семье) найти взаимовыгодное решение без обращения в суд. Развивающееся направление в российской юриспруденции.",
        "link": "https://postupi.online/professiya/mediator/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 89, "name": "Финансовый контролер", "industry": "Финансы/Менеджмент", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Контролирует исполнение бюджета компании, анализирует финансовые показатели и готовит управленческую отчетность. Работает в крупных российских и международных компаниях.",
        "link": "https://postupi.online/professiya/finansovyj-kontroler/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 90, "name": "T&D-менеджер", "industry": "HR/Обучение персонала", "university": "НИУ ВШЭ (Управление персоналом), МГУ (Психология)",
        "description": "Организует обучение и развитие сотрудников внутри компании: проводит тренинги, разрабатывает программы, оценивает эффективность.",
        "link": "https://postupi.online/professiya/menedzher-po-obucheniyu-personala/", "junior_salary": 70000, "avg_salary": 125000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 91, "name": "Инженер ПТО", "industry": "Строительство", "university": "МГСУ, СПбГАСУ",
        "description": "Ведет исполнительную и техническую документацию на стройке, контролирует объемы работ. 'Бумажное сердце' любого строительного проекта.",
        "link": "https://postupi.online/professiya/inzhener-pto/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 92, "name": "Фармаколог (клинические исследования)", "industry": "Фармацевтика/Наука", "university": "Первый МГМУ им. Сеченова, РХТУ им. Менделеева",
        "description": "Организует и контролирует процесс испытаний новых лекарственных препаратов в России. Работа в фармацевтических компаниях и исследовательских центрах.",
        "link": "https://postupi.online/professiya/farmakolog/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 93, "name": "Коммерческий фотограф", "industry": "Фотография/Реклама/Медиа", "university": "Школы фотографии (Photoplay, Академия Фотографии)",
        "description": "Создает фотографии для брендов, рекламы, каталогов и маркетплейсов. Доход зависит от специализации (предметная, fashion, фуд-фото) и портфолио.",
        "link": "https://postupi.online/professiya/fotograf/", "junior_salary": 45000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 94, "name": "Специалист по автоматизации зданий", "industry": "ИТ/Строительство/Инженерия", "university": "МЭИ, МГСУ",
        "description": "Проектирует и настраивает системы 'умного дома' и 'умного здания': управление климатом, светом, безопасностью. Перспективное направление на стыке IT и инженерии.",
        "link": "https://postupi.online/professiya/proektirovshchik-umnogo-doma/", "junior_salary": 75000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 2}
    },
    {
        "id": 95, "name": "Веб-дизайнер", "industry": "ИТ/Дизайн", "university": "НИУ ВШЭ (Дизайн), Британская высшая школа дизайна",
        "description": "Создает дизайн и макеты для сайтов, отвечает за их визуальное оформление и удобство. Может работать в студии или на фрилансе.",
        "link": "https://postupi.online/professiya/veb-dizajner/", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 96, "name": "Токарь с ЧПУ", "industry": "Промышленность/Рабочие", "university": "Политехнические колледжи",
        "description": "Обрабатывает металлические детали на станках с числовым программным управлением. Высококвалифицированная и востребованная рабочая профессия на российских заводах.",
        "link": "https://postupi.online/professiya/tokar/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 97, "name": "Авиадиспетчер", "industry": "Авиация/Транспорт", "university": "СПбГУ ГА, МГТУ ГА",
        "description": "Управляет воздушным движением, обеспечивая безопасность полетов. Крайне ответственная работа, требующая предельной концентрации и стрессоустойчивости.",
        "link": "https://postupi.online/professiya/aviadispetcher/", "junior_salary": 80000, "avg_salary": 180000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 98, "name": "Нутрициолог", "industry": "Здоровье/Фитнес/Консалтинг", "university": "РНИМУ им. Пирогова, профильные курсы",
        "description": "Консультирует по вопросам правильного питания, помогает составить сбалансированный рацион для достижения различных целей (похудение, набор массы, здоровье).",
        "link": "https://postupi.online/professiya/nutriciolog/", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 99, "name": "Комьюнити-менеджер", "industry": "Маркетинг/Геймдев/ИТ", "university": "НИУ ВШЭ (Коммуникации), РГГУ",
        "description": "Создает и развивает сообщество вокруг бренда или продукта в соцсетях и на форумах. Общается с аудиторией, решает конфликты и повышает лояльность.",
        "link": "https://postupi.online/professiya/komyuniti-menedzher/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 100, "name": "Специалист по ESG", "industry": "Консалтинг/Финансы/Экология", "university": "МГИМО, РАНХиГС",
        "description": "Помогает компаниям внедрять принципы устойчивого развития (экология, социальная ответственность, корпоративное управление). Новое и перспективное направление в России.",
        "link": "https://postupi.online/professiya/specialist-po-ustojchivomu-razvitiyu/", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 101, "name": "Промышленный альпинист", "industry": "Строительство/Сервис", "university": "Центры профессиональной подготовки",
        "description": "Выполняет высотные работы на зданиях и сооружениях: мойка фасадов, монтаж, ремонт. Опасная, но хорошо оплачиваемая работа для физически подготовленных людей.",
        "link": "https://postupi.online/professiya/promyshlennyj-alpinist/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 102, "name": "Налоговый консультант", "industry": "Финансы/Юриспруденция/Консалтинг", "university": "Финансовый университет, МГЮА им. Кутафина",
        "description": "Помогает компаниям и частным лицам оптимизировать налогообложение и решать споры с ФНС в рамках российского законодательства.",
        "link": "https://postupi.online/professiya/nalogovyj-konsultant/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 103, "name": "Реставратор (искусство)", "industry": "Искусство/Культура", "university": "МГХПА им. Строганова, Академия художеств им. Репина",
        "description": "Восстанавливает произведения искусства — картины, иконы, скульптуры. Редкая и кропотливая работа в музеях, галереях и частных мастерских.",
        "link": "https://postupi.online/professiya/restavrator/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 5, 'art': 5}
    },
    {
        "id": 104, "name": "Fullstack-разработчик", "industry": "ИТ", "university": "МФТИ, ИТМО, онлайн-школы",
        "description": "Универсальный разработчик, который умеет создавать и фронтенд (пользовательский интерфейс), и бэкенд (серверную часть) веб-приложений. Очень ценится в стартапах.",
        "link": "https://msk.top-academy.ru/articles/fullstack-developer", "junior_salary": 90000, "avg_salary": 185000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 2}
    },
    {
        "id": 105, "name": "Байер (Fashion)", "industry": "Мода/Ритейл", "university": "БВШД, МГУ (Менеджмент)",
        "description": "Формирует ассортимент магазина одежды, отбирая и закупая коллекции у российских и зарубежных дизайнеров и брендов. Требует 'чутья' на тренды.",
        "link": "https://postupi.online/professiya/baier/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 106, "name": "Спасатель МЧС", "industry": "Госслужба/Безопасность", "university": "Академия ГПС МЧС России",
        "description": "Оказывает помощь людям в чрезвычайных ситуациях: при пожарах, наводнениях, ДТП. Героическая профессия, требующая отличной физической и психологической подготовки.",
        "link": "https://postupi.online/professiya/spasatel/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 107, "name": "Продуктовый аналитик", "industry": "ИТ/Аналитика", "university": "НИУ ВШЭ (ПМИ), МФТИ",
        "description": "Исследует данные о поведении пользователей в IT-продукте, чтобы найти точки роста и предложить улучшения. Работает в тесной связке с продуктовым менеджером.",
        "link": "https://postupi.online/professiya/produktovyj-analitik/", "junior_salary": 85000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 108, "name": "Клинический психолог", "industry": "Медицина/Психология", "university": "МГУ (Психфак), РНИМУ им. Пирогова",
        "description": "Диагностирует и лечит психические расстройства и пограничные состояния (депрессии, тревожность), работая в медицинских учреждениях.",
        "link": "https://postupi.online/professiya/klinicheskij-psiholog/", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 109, "name": "Звукорежиссер", "industry": "Медиа/Музыка/Кино", "university": "ВГИК, СПбГИКиТ, ИСИ",
        "description": "Отвечает за качество звука при записи музыки, съемках кино, на концертах и в прямом эфире. Техническая и творческая профессия одновременно.",
        "link": "https://postupi.online/professiya/zvukorezhisser/", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 110, "name": "Геодезист/Картограф", "industry": "Строительство/Геология", "university": "МИИГАиК, СПбГУ",
        "description": "Проводит измерения на местности для создания карт, планов и сопровождения строительства. Работа сочетает полевые выезды и обработку данных в офисе.",
        "link": "https://postupi.online/professiya/geodezist/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 111, "name": "CRM-маркетолог", "industry": "Маркетинг/ИТ", "university": "НИУ ВШЭ (Маркетинг), РЭУ им. Плеханова",
        "description": "Выстраивает коммуникацию с текущими клиентами компании через email, push-уведомления и мессенджеры, повышая их лояльность и повторные продажи.",
        "link": "https://postupi.online/professiya/crm-menedzher/", "junior_salary": 60000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 112, "name": "Тату-мастер", "industry": "Сервис/Искусство", "university": "Профессиональные студии и курсы",
        "description": "Создает художественные татуировки на теле. Творческая профессия, требующая художественных навыков, дохода зависит от узнаваемости и мастерства.",
        "link": "https://postupi.online/professiya/tatu-master/", "junior_salary": 40000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 113, "name": "Сметчик", "industry": "Строительство/Финансы", "university": "МГСУ, Профильные курсы",
        "description": "Рассчитывает стоимость строительства или ремонта, составляя сметную документацию. Требует внимательности и знания строительных норм.",
        "link": "https://postupi.online/professiya/smetchik/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 114, "name": "Вирусолог", "industry": "Наука/Медицина", "university": "МГУ (Биофак), НГУ (Новосибирск)",
        "description": "Изучает вирусы, разрабатывает вакцины и противовирусные препараты. Работает в научных центрах, таких как новосибирский 'Вектор'.",
        "link": "https://postupi.online/professiya/virusolog/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 115, "name": "Политтехнолог", "industry": "Политика/Консалтинг/PR", "university": "МГУ (Философский), НИУ ВШЭ (Политология)",
        "description": "Разрабатывает и реализует стратегии для политических кампаний и избирательных процессов в России. Проектная и непубличная работа.",
        "link": "https://postupi.online/professiya/polittehnolog/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 116, "name": "C++ разработчик", "industry": "ИТ/Геймдев/Финтех", "university": "МФТИ, МГУ (ВМК), СПбГУ (Матмех)",
        "description": "Создает высокопроизводительное ПО: игровые движки, торговых роботов для бирж, операционные системы. Сложная, но фундаментальная и высокооплачиваемая специализация.",
        "link": "https://postupi.online/professiya/programmist-c-plus-plus/", "junior_salary": 95000, "avg_salary": 200000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 117, "name": "Дизайнер интерьеров", "industry": "Дизайн/Строительство", "university": "МГХПА им. Строганова, Школа 'Детали'",
        "description": "Проектирует внутреннее пространство квартир, домов и коммерческих помещений, создавая функциональный и эстетичный интерьер. Работает в студиях или на себя.",
        "link": "https://postupi.online/professiya/dizajner-interera/", "junior_salary": 55000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 118, "name": "Оценщик (недвижимость, бизнес)", "industry": "Финансы/Недвижимость/Консалтинг", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Определяет рыночную стоимость активов: квартир, зданий, земельных участков или целых компаний. Услуги востребованы при сделках, кредитовании и в судах.",
        "link": "https://postupi.online/professiya/ocenshhik/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 119, "name": "Агроинженер", "industry": "Сельское хозяйство/Инженерия", "university": "РГАУ-МСХА им. Тимирязева, Ставропольский ГАУ",
        "description": "Отвечает за эксплуатацию и ремонт сельскохозяйственной техники в агрохолдингах и фермерских хозяйствах России.",
        "link": "https://postupi.online/professiya/agroinzhener/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 120, "name": "Специалист по контекстной рекламе (PPC)", "industry": "Маркетинг/ИТ", "university": "Профильные курсы и сертификации (Яндекс)",
        "description": "Настраивает и ведет рекламные кампании в Яндекс.Директе, привлекая клиентов на сайт. Ключевая роль в интернет-маркетинге.",
        "link": "https://postupi.online/professiya/specialist-po-kontekstnoj-reklame/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 121, "name": "Нотариус", "industry": "Юриспруденция", "university": "МГЮА им. Кутафина, МГУ (Юрфак)",
        "description": "Удостоверяет сделки, доверенности, завещания и другие юридически значимые документы. Статусная и высокодоходная профессия, но стать нотариусом очень сложно.",
        "link": "https://postupi.online/professiya/notarius/", "junior_salary": 80000, "avg_salary": 250000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 122, "name": "Кондитер", "industry": "Общепит/Производство", "university": "Колледжи пищевой промышленности, кулинарные школы",
        "description": "Создает торты, пирожные, десерты и выпечку. Работает в кондитерских, ресторанах или открывает собственный бизнес. Требует творческого подхода и аккуратности.",
        "link": "https://postupi.online/professiya/konditer/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 123, "name": "Кинолог", "industry": "Госслужба (МВД, ФТС)/Сервис", "university": "Аграрные вузы, ведомственные учебные центры",
        "description": "Дрессирует собак для службы в полиции, на таможне, в МЧС или для частных лиц. Профессия для тех, кто любит животных и умеет находить с ними общий язык.",
        "link": "https://postupi.online/professiya/kinolog/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 124, "name": "Метеоролог", "industry": "Наука/Госслужба", "university": "МГУ (Географический), РГГМУ (Санкт-Петербург)",
        "description": "Составляет прогнозы погоды, анализируя данные с метеостанций и спутников. Работает в структурах Росгидромета.",
        "link": "https://postupi.online/professiya/meteorolog/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 125, "name": "Системный аналитик", "industry": "ИТ/Консалтинг", "university": "НИУ ВШЭ (Бизнес-информатика), МГТУ им. Баумана",
        "description": "Проектирует IT-системы, описывая их логику, компоненты и взаимодействие. Составляет технические задания для разработчиков. Важная роль в сложных IT-проектах.",
        "link": "https://postupi.online/professiya/sistemnyj-analitik/", "junior_salary": 75000, "avg_salary": 145000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 126, "name": "Консультант по управлению", "industry": "Консалтинг/Бизнес", "university": "НИУ ВШЭ, РЭШ, МФТИ",
        "description": "Помогает крупным компаниям решать сложные бизнес-задачи: разрабатывает стратегии, оптимизирует процессы. Работа в 'Большой тройке' и других консалтинговых фирмах.",
        "link": "https://postupi.online/professiya/menedzhment-konsultant/", "junior_salary": 100000, "avg_salary": 250000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 127, "name": "Коммерческий иллюстратор", "industry": "Дизайн/Искусство/Медиа", "university": "БВШД, МГХПА им. Строганова",
        "description": "Создает иллюстрации для книг, журналов, сайтов, упаковки и рекламы. Работает на фрилансе или в издательствах и агентствах.",
        "link": "https://postupi.online/professiya/illyustrator/", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 128, "name": "Финансовый директор (CFO)", "industry": "Финансы/Менеджмент", "university": "Финансовый университет, НИУ ВШЭ (Экономфак)",
        "description": "Управляет всеми финансовыми потоками компании, отвечает за финансовую стратегию и устойчивость. Ключевая топ-менеджерская позиция.",
        "link": "https://postupi.online/professiya/finansovyj-direktor/", "junior_salary": 180000, "avg_salary": 450000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 129, "name": "Разработчик игр (Game Developer)", "industry": "Геймдев/ИТ", "university": "НИУ ВШЭ (Программная инженерия), ИТМО",
        "description": "Пишет код для компьютерных и мобильных игр, реализуя игровую логику, графику и физику. Востребован в российской индустрии разработки игр.",
        "link": "https://edu.sravni.ru/kursy/info/razrabotchik-igr/", "junior_salary": 80000, "avg_salary": 165000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 130, "name": "Реабилитолог/Физический терапевт", "industry": "Медицина/Спорт", "university": "РГУФКСМиТ, НГУ им. Лесгафта",
        "description": "Помогает людям восстанавливаться после травм, операций и болезней с помощью лечебной физкультуры и физиотерапии. Работает в медцентрах и санаториях.",
        "link": "https://postupi.online/professiya/reabilitolog/", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 131, "name": "Облачный архитектор (Cloud Architect)", "industry": "ИТ", "university": "Технические ВУЗы + сертификации (Yandex.Cloud, AWS, Azure)",
        "description": "Проектирует IT-инфраструктуру компании в облачных сервисах (например, Yandex.Cloud). Высокооплачиваемая и ответственная роль в современном IT.",
        "link": "https://postupi.online/professiya/cloud-inzhener/", "junior_salary": 140000, "avg_salary": 280000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 1}
    },
    {
        "id": 132, "name": "Патентный поверенный", "industry": "Юриспруденция/Интеллектуальная собственность", "university": "РГАИС, МГЮА им. Кутафина",
        "description": "Помогает изобретателям и компаниям регистрировать патенты на изобретения и товарные знаки в Роспатенте. Редкая и сложная юридическая специализация.",
        "link": "https://postupi.online/professiya/patentoved/", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 133, "name": "Урбанист-планировщик", "industry": "Архитектура/Госуправление", "university": "МАРХИ, НИУ ВШЭ (Высшая школа урбанистики)",
        "description": "Исследует и проектирует развитие городских территорий, делая их удобными для жизни. Работает в консалтинге и органах власти, отвечая за мастер-планы городов.",
        "link": "https://postupi.online/professiya/urbanist-ekolog/", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 134, "name": "Диктор/Актер озвучания", "industry": "Медиа/Искусство", "university": "Театральные ВУЗы (ВТУ им. Щепкина, ГИТИС), курсы",
        "description": "Озвучивает рекламные ролики, аудиокниги, фильмы и мультфильмы. Узнаваемый голос может принести известность и хороший доход.",
        "link": "https://postupi.online/professiya/akter-ozvuchivaniya-i-dublyazha/", "junior_salary": 40000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 135, "name": "Технолог пищевого производства", "industry": "Промышленность/Общепит", "university": "МГУПП, РЭУ им. Плеханова",
        "description": "Отвечает за технологию и качество производства продуктов питания на заводах и фабриках. Контролирует все этапы от сырья до готовой упаковки.",
        "link": "https://postupi.online/professiya/tehnolog-pishchevoj-promyshlennosti/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 136, "name": "Профориентолог/Карьерный консультант", "industry": "HR/Образование/Консалтинг", "university": "НИУ ВШЭ (Психология), МГУ (Психфак)",
        "description": "Помогает школьникам и взрослым выбрать профессию или спланировать карьерный путь, составляет резюме и готовит к собеседованиям. Растущий рынок услуг в России.",
        "link": "https://postupi.online/professiya/karernyj-konsultant/", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 137, "name": "Оператор станков с ЧПУ", "industry": "Промышленность/Рабочие", "university": "Среднее профессиональное образование, учебные центры",
        "description": "Управляет работой станков с числовым программным управлением, изготавливая детали по заданной программе. Востребованная рабочая специальность на современных производствах.",
        "link": "https://postupi.online/professiya/operator-stankov-s-chpu/", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 138, "name": "Анестезиолог-реаниматолог", "industry": "Медицина", "university": "Ведущие медицинские ВУЗы + ординатура",
        "description": "Обеспечивает обезболивание во время операций и борется за жизнь пациентов в критических состояниях в отделениях реанимации. Одна из самых сложных врачебных профессий.",
        "link": "https://postupi.online/professiya/anesteziolog-reanimatolog/", "junior_salary": 70000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 139, "name": "Научный сотрудник (Research Scientist)", "industry": "Наука", "university": "ВУЗы с сильными научными школами (МГУ, СПбГУ, НГУ, МФТИ)",
        "description": "Проводит научные исследования в лабораториях и институтах РАН, пишет статьи и участвует в конференциях. Путь в большую науку.",
        "link": "https://postupi.online/professiya/nauchnyj-sotrudnik/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 140, "name": "Таргетолог", "industry": "Маркетинг/SMM", "university": "Онлайн-курсы, НИУ ВШЭ (Коммуникации)",
        "description": "Настраивает таргетированную рекламу в социальных сетях (например, VK Реклама), чтобы показывать ее определенной аудитории. Очень востребован в малом и среднем бизнесе.",
        "link": "https://postupi.online/professiya/targetolog/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 141, "name": "Машинист поезда/метрополитена", "industry": "Транспорт/Госслужба", "university": "Железнодорожные колледжи и техникумы, УТЦ метрополитена",
        "description": "Управляет составами поездов в РЖД или в метрополитене. Ответственная работа со сменным графиком и хорошим социальным пакетом.",
        "link": "https://postupi.online/professiya/mashinist-poezda/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 142, "name": "Архитектор IT-решений (Solution Architect)", "industry": "ИТ/Консалтинг", "university": "МГТУ им. Баумана, МФТИ",
        "description": "Проектирует общую структуру сложных IT-систем, выбирая технологии и способы их взаимодействия для решения конкретных бизнес-задач. Высокоуровневая инженерная роль.",
        "link": "https://sky.pro/wiki/profession/solution-arhitektor-klyuchevye-kompetencii-i-zadachi-it-specialista/", "junior_salary": 150000, "avg_salary": 300000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 143, "name": "Креативный директор", "industry": "Реклама/Медиа/Дизайн", "university": "БВШД, MADS",
        "description": "Руководит творческой командой в рекламном агентстве, отвечает за разработку и реализацию креативных концепций для крупных брендов.",
        "link": "https://postupi.online/professiya/kreativnyj-direktor/", "junior_salary": 120000, "avg_salary": 250000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 1, 'art': 5}
    },
    {
        "id": 144, "name": "Зоотехник", "industry": "Сельское хозяйство", "university": "РГАУ-МСХА им. Тимирязева, СПбГАВМ",
        "description": "Занимается разведением, кормлением и содержанием сельскохозяйственных животных на фермах и в агрокомплексах.",
        "link": "https://postupi.online/professiya/zootehnik/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 145, "name": "Микробиолог", "industry": "Наука/Медицина/Промышленность", "university": "МГУ (Биофак), РХТУ им. Менделеева",
        "description": "Изучает микроорганизмы (бактерии, грибы) и их влияние на человека и окружающую среду. Работает в лабораториях, на пищевых и фармацевтических предприятиях.",
        "link": "https://postupi.online/professiya/mikrobiolog/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 146, "name": "Начальник строительного участка", "industry": "Строительство", "university": "МГСУ, СПбГАСУ",
        "description": "Руководит всеми процессами на своем участке стройки: управляет прорабами, контролирует сроки, бюджет и взаимодействие с подрядчиками.",
        "link": "https://postupi.online/professiya/nachalnik-stroitelnogo-uchastka/", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 147, "name": "Python-разработчик", "industry": "ИТ/Data Science/Web", "university": "МФТИ, НИУ ВШЭ (ФКН), ИТМО",
        "description": "Программирует на языке Python, который используется в веб-разработке, анализе данных, машинном обучении и автоматизации. Одна из самых универсальных и востребованных IT-профессий.",
        "link": "https://blog.skillbox.by/kod/professija-python-razrabotchika-chem-zanimajutsja-programmisty-chto-nuzhno-znat-i-umet-skillbox-media/", "junior_salary": 85000, "avg_salary": 175000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 148, "name": "Специалист по таможенному оформлению", "industry": "Логистика/Госслужба/Торговля", "university": "РАНХиГС (Таможенное дело), РТА",
        "description": "Готовит и подает документы для прохождения товаров через таможню (декларации, сертификаты). Работает в логистических компаниях или у брокеров.",
        "link": "https://postupi.online/professiya/specialist-po-tamozhennomu-oformleniyu/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 149, "name": "Тифлопедагог", "industry": "Образование/Дефектология", "university": "МПГУ, РГПУ им. Герцена",
        "description": "Обучает и воспитывает слепых и слабовидящих детей, помогая им адаптироваться к жизни и получить образование. Редкая и социально значимая профессия.",
        "link": "https://postupi.online/professiya/tifdopedagog/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 150, "name": "Инвестиционный аналитик", "industry": "Финансы/Инвестиции/Банки", "university": "РЭШ, НИУ ВШЭ (МИЭФ), Финансовый университет",
        "description": "Анализирует компании и рынки для принятия решений о вложении денег. Работает в инвестиционных фондах, банках и управляющих компаниях.",
        "link": "https://postupi.online/professiya/investicionnyj-analitik/", "junior_salary": 100000, "avg_salary": 190000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 151, "name": "UX-исследователь", "industry": "ИТ/Дизайн/Маркетинг", "university": "НИУ ВШЭ (Социология, Психология), МГУ",
        "description": "Изучает пользовательский опыт через интервью и тесты, чтобы сделать IT-продукты максимально удобными и понятными. Работает в крупных IT-компаниях и дизайн-студиях.",
        "link": "https://blog.skillbox.by/dizajn/advokat-polzovatelja-kto-takoj-ux-issledovatel-i-pochemu-on-delaet-mir-luchshe-skillbox-media/", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 152, "name": "Дипломат", "industry": "Госслужба/Международные отношения", "university": "МГИМО, Дипломатическая академия МИД РФ",
        "description": "Представляет интересы России за рубежом, работает в посольствах и консульствах. Престижная, но очень закрытая карьера на госслужбе.",
        "link": "https://postupi.online/professiya/diplomat/", "junior_salary": 80000, "avg_salary": 200000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 153, "name": "Художник по костюмам", "industry": "Искусство/Кино/Театр", "university": "ВГИК, Школа-студия МХАТ",
        "description": "Создает костюмы для персонажей в кино, театре и на телевидении, помогая раскрыть их характеры. Творческая и проектная работа.",
        "link": "https://postupi.online/professiya/hudozhnik-po-kostyumu/", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 154, "name": "Java-разработчик", "industry": "ИТ/Enterprise/Финтех", "university": "МГТУ им. Баумана, СПбПУ, КФУ",
        "description": "Разрабатывает сложные и надежные корпоративные системы, особенно в банковском секторе и крупном бизнесе. Один из столпов 'enterprise'-разработки в России.",
        "link": "https://postupi.online/professiya/java-razrabotchik/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 155, "name": "Спортивный психолог", "industry": "Спорт/Психология", "university": "МГУ (Психфак), РГУФКСМиТ",
        "description": "Помогает спортсменам и командам справляться с давлением, настраиваться на победу и достигать лучших результатов. Работает в профессиональных клубах и сборных.",
        "link": "https://postupi.online/professiya/sportivnyj-psiholog/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 156, "name": "Антикризисный управляющий", "industry": "Менеджмент/Финансы/Юриспруденция", "university": "РАНХиГС, НИУ ВШЭ",
        "description": "Руководит компанией в предбанкротном состоянии, разрабатывая план по ее финансовому оздоровлению. Сложная и высокооплачиваемая работа для опытных менеджеров.",
        "link": "https://postupi.online/professiya/antikrizisnyj-upravlyayushchij/", "junior_salary": 150000, "avg_salary": 350000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 157, "name": "Специалист по информационной безопасности", "industry": "ИТ/Безопасность", "university": "МИФИ, МГТУ им. Баумана (ИУ-8), ИТМО",
        "description": "Защищает корпоративные сети, системы и данные от кибератак. 'Белый хакер' на страже интересов бизнеса. Критически важная профессия в цифровом мире.",
        "link": "https://practicum.yandex.ru/blog/kto-takoy-specialist-po-informacionnoy-bezopasnosti/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 158, "name": "Lean-менеджер", "industry": "Промышленность/Менеджмент", "university": "Технические ВУЗы + доп. образование",
        "description": "Внедряет на производстве принципы 'бережливого производства', чтобы устранить потери и повысить эффективность. Востребован на современных российских заводах.",
        "link": "https://postupi.online/professiya/lean-menedzher/", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 159, "name": "Няня/Гувернантка", "industry": "Сервис/Образование", "university": "Педагогические и медицинские колледжи, МПГУ",
        "description": "Ухаживает за детьми и занимается их развитием в семье. Спрос на квалифицированных специалистов с хорошими рекомендациями в крупных городах очень высок.",
        "link": "https://postupi.online/professiya/nyanya/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 160, "name": "Врач-онколог", "industry": "Медицина", "university": "НМИЦ онкологии им. Блохина, ПМГМУ им. Сеченова",
        "description": "Диагностирует и лечит злокачественные опухоли. Эмоционально тяжелая, но жизненно важная и уважаемая медицинская специальность.",
        "link": "https://postupi.online/professiya/onkolog/", "junior_salary": 70000, "avg_salary": 190000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 161, "name": "Комплаенс-менеджер", "industry": "Юриспруденция/Финансы/Безопасность", "university": "МГЮА им. Кутафина, НИУ ВШЭ (Право)",
        "description": "Контролирует, чтобы деятельность компании соответствовала законодательству и внутренним правилам, минимизируя риски. Востребован в банках и крупных корпорациях.",
        "link": "https://postupi.online/professiya/komplaens-menedzher/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 162, "name": "Разработчик встраиваемых систем", "industry": "ИТ/Инженерия/Электроника", "university": "МИЭТ, МГТУ им. Баумана, ИТМО",
        "description": "Программирует 'железо': микроконтроллеры в бытовой технике, автомобилях, промышленном оборудовании. Глубокая инженерная специальность на стыке ПО и электроники.",
        "link": "https://postupi.online/professiya/razrabotchik-vstraivaemyh-sistem/", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 163, "name": "Бренд-менеджер", "industry": "Маркетинг/Менеджмент", "university": "НИУ ВШЭ (Маркетинг), МГУ (Экономфак)",
        "description": "Отвечает за развитие и продвижение конкретного бренда на российском рынке. Анализирует рынок, управляет ассортиментом, ценой и коммуникациями.",
        "link": "https://postupi.online/professiya/brend-menedzher/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 164, "name": "Врач-радиолог (МРТ/КТ)", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по рентгенологии",
        "description": "Проводит и интерпретирует исследования на аппаратах МРТ и КТ, помогая ставить точные диагнозы. Технологичная и востребованная медицинская специальность.",
        "link": "https://postupi.online/professiya/vrach-radiolog/", "junior_salary": 80000, "avg_salary": 170000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 165, "name": "Актуарий", "industry": "Страхование/Финансы", "university": "МГУ (Мехмат), НИУ ВШЭ (Экономика)",
        "description": "Рассчитывает страховые тарифы и резервы, используя сложные математические модели. Редкая и высокооплачиваемая профессия в страховых компаниях и пенсионных фондах.",
        "link": "https://postupi.online/professiya/aktuarij/", "junior_salary": 100000, "avg_salary": 220000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 166, "name": "Продюсер (кино/ТВ/медиа)", "industry": "Медиа/Кино/ТВ", "university": "ВГИК, СПбГИКиТ, Школа-студия МХАТ",
        "description": "Организует весь процесс создания медиапродукта: от поиска идеи и финансирования до съемок и выпуска. 'Мотор' любого проекта в кино или на ТВ.",
        "link": "https://postupi.online/professiya/prodyuser/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 167, "name": "Гидрогеолог", "industry": "Геология/Экология/Строительство", "university": "МГУ (Геологический), МГРИ",
        "description": "Изучает подземные воды, ищет их источники для водоснабжения, оценивает влияние строительства на водные горизонты.",
        "link": "https://postupi.online/professiya/gidrogeolog/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 168, "name": "Парикмахер-колорист", "industry": "Красота/Сервис", "university": "Профессиональные академии и школы (L'Oréal, Wella)",
        "description": "Специализируется на сложных техниках окрашивания волос. Востребованная и высокооплачиваемая специализация в индустрии красоты.",
        "link": "https://postupi.online/professiya/parikmaher-kolorist/", "junior_salary": 50000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 169, "name": "Нанотехнолог", "industry": "Наука/Промышленность/Технологии", "university": "МИФИ, МФТИ, МИСиС",
        "description": "Работает с материалами на нано-уровне, создавая новые технологии для медицины, электроники. Работает в научных центрах, например, в 'Курчатовском институте'.",
        "link": "https://postupi.online/professiya/inzhener-nanotehnolog/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 170, "name": "Конфликтолог", "industry": "HR/Консалтинг/Госслужба", "university": "СПбГУ (Факультет социологии), РГСУ",
        "description": "Анализирует и разрешает конфликты в организациях и социальных группах. Может работать в HR-отделах, профсоюзах и консалтинге.",
        "link": "https://postupi.online/professiya/konfliktolog/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 171, "name": "Scrum-мастер", "industry": "ИТ/Менеджмент", "university": "Сертификация (PSM, CSM) + опыт в IT",
        "description": "Помогает IT-команде эффективно работать по гибкой методологии Scrum: проводит встречи, устраняет препятствия. Не руководитель, а 'слуга-лидер'.",
        "link": "https://postupi.online/professiya/scrum-master/", "junior_salary": 100000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 172, "name": "Эрготерапевт", "industry": "Медицина/Реабилитация", "university": "ПСПбГМУ им. Павлова, РНИМУ им. Пирогова",
        "description": "Помогает людям с ограниченными возможностями восстановить бытовые навыки и адаптироваться к повседневной жизни. Новое направление реабилитации в России.",
        "link": "https://postupi.online/professiya/ergoterapevt/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 173, "name": "Специалист по лизингу", "industry": "Финансы/Продажи", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Продает услуги финансовой аренды (лизинга) автомобилей, оборудования и спецтехники для бизнеса. Работа на стыке финансов и продаж.",
        "link": "https://postupi.online/professiya/menedzher-po-lizingu/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 174, "name": "Технический художник", "industry": "Геймдев/ИТ", "university": "Scream School, НИУ ВШЭ (Дизайн)",
        "description": "Связующее звено между художниками и программистами в разработке игр. Адаптирует графику для игрового движка и создает сложные визуальные эффекты.",
        "link": "https://postupi.online/professiya/tehnicheskij-hudozhnik/", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 175, "name": "Судья", "industry": "Юриспруденция/Госслужба", "university": "Высшее юридическое образование + большой стаж",
        "description": "Вершит правосудие от имени государства. Высшая точка в юридической карьере, требующая безупречной репутации, огромного опыта и сдачи сложного экзамена.",
        "link": "https://postupi.online/professiya/sudya/", "junior_salary": 100000, "avg_salary": 300000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 176, "name": "Customer Success Manager", "industry": "ИТ/Сервис", "university": "Любой ВУЗ + коммуникативные навыки",
        "description": "Помогает клиентам получить максимальную пользу от использования IT-продукта (обычно в B2B), чтобы они оставались с компанией надолго. Проактивная поддержка.",
        "link": "https://postupi.online/professiya/menedzher-po-uspehu-klientov/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 177, "name": "Астрофизик", "industry": "Наука", "university": "МГУ (Физфак), СПбГУ (Астрономическое отделение)",
        "description": "Изучает Вселенную: звезды, галактики, черные дыры. Работает в обсерваториях и научно-исследовательских институтах.",
        "link": "https://postupi.online/professiya/astrofizik/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 178, "name": "BIM-менеджер", "industry": "Строительство/Проектирование", "university": "МГСУ, СПбГАСУ",
        "description": "Руководит процессом информационного моделирования зданий (BIM), создавая цифровой двойник объекта. Ключевой специалист в современном цифровом строительстве.",
        "link": "https://vc.ru/edu/1637206-bim-menedzher-kto-eto-chem-zanimaetsya-i-kak-im-stat", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 2}
    },
    {
        "id": 179, "name": "Заводчик животных", "industry": "Животноводство/Сервис", "university": "Аграрные вузы (зоотехния, ветеринария)",
        "description": "Профессионально занимается разведением породистых животных (собак, кошек). Требует больших знаний, любви к животным и является скорее бизнесом, чем работой по найму.",
        "link": "https://ru.wikipedia.org/wiki/Заводчик", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 2}
    },
    {
        "id": 180, "name": "Мастер по ремонту бытовой техники", "industry": "Сервис/Рабочие", "university": "Технические колледжи, учебные центры производителей",
        "description": "Ремонтирует на дому у клиентов или в сервисном центре стиральные машины, холодильники и другую технику. Доход зависит от количества и сложности заказов.",
        "link": "https://trudvsem.ru/professions/detail/13769", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 181, "name": "DevRel менеджер", "industry": "ИТ/Маркетинг/Коммуникации", "university": "Технические ВУЗы + опыт в IT-комьюнити",
        "description": "Выстраивает отношения IT-компании с сообществом разработчиков: выступает на конференциях, пишет статьи, организует митапы. 'Евангелист' технологий.",
        "link": "https://habr.com/ru/articles/570594/", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 182, "name": "Искусствовед", "industry": "Искусство/Культура/Образование", "university": "МГУ (Истфак), РГГУ, Академия художеств им. Репина",
        "description": "Исследует и анализирует произведения искусства. Работает в музеях, галереях, аукционных домах, читает лекции и пишет статьи.",
        "link": "https://postupi.online/professiya/iskusstvoved/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 4, 'art': 5}
    },
    {
        "id": 183, "name": "Каскадер", "industry": "Кино/ТВ", "university": "Школы каскадеров, спортивные разряды",
        "description": "Выполняет сложные и опасные трюки в кино, заменяя актеров. Требует великолепной физической подготовки и узкой специализации (автотрюки, высотные падения).",
        "link": "https://postupi.online/professiya/kaskader/", "junior_salary": 60000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 3}
    },
    {
        "id": 184, "name": "Инженер по качеству", "industry": "Промышленность/Производство", "university": "МГТУ им. Баумана, Политехнические университеты",
        "description": "Контролирует качество продукции на всех этапах производства на заводе, чтобы минимизировать брак. Работает в отделе технического контроля (ОТК).",
        "link": "https://postupi.online/professiya/inzhener-po-kachestvu/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 185, "name": "Флорист", "industry": "Сервис/Дизайн", "university": "Школы флористики ('Николь', 'Moscow Flower School')",
        "description": "Составляет букеты и цветочные композиции. Творческая работа в цветочном салоне или собственном бизнесе.",
        "link": "https://postupi.online/professiya/florist/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 186, "name": "Эндокринолог", "industry": "Медицина", "university": "НМИЦ эндокринологии, ведущие медицинские ВУЗы",
        "description": "Диагностирует и лечит заболевания желез внутренней секреции, в первую очередь — сахарный диабет и болезни щитовидной железы.",
        "link": "https://postupi.online/professiya/endokrinolog/", "junior_salary": 60000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 187, "name": "Администратор баз данных (DBA)", "industry": "ИТ", "university": "МГТУ им. Баумана, МИРЭА",
        "description": "Отвечает за стабильную, быструю и безопасную работу баз данных в компании. Обеспечивает резервное копирование и восстановление данных.",
        "link": "https://postupi.online/professiya/administrator-baz-dannyh/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 188, "name": "Офицер вооруженных сил", "industry": "Госслужба/Армия", "university": "Военные училища и академии",
        "description": "Командует подразделениями в армии или на флоте. Государственная служба, связанная с защитой страны, требующая дисциплины и готовности к переездам.",
        "link": "https://postupi.online/professiya/oficer/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 189, "name": "Компьютерный лингвист", "industry": "ИТ/Наука", "university": "НИУ ВШЭ (ФКН), МГУ (Филологический/ВМК), СПбГУ",
        "description": "Обучает компьютеры понимать и обрабатывать человеческий язык. Работает над созданием голосовых помощников, чат-ботов и машинных переводчиков.",
        "link": "https://blog.skillfactory.ru/kompyuternyi-lingvist-professiya/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 190, "name": "Ортопед-травматолог", "industry": "Медицина", "university": "НМИЦ ТО им. Приорова, РНИМУ им. Пирогова",
        "description": "Лечит травмы и заболевания опорно-двигательного аппарата: переломы, вывихи, артрозы. Работает в травмпунктах, больницах и частных клиниках.",
        "link": "https://postupi.online/professiya/travmatolog-ortoped/", "junior_salary": 65000, "avg_salary": 165000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 191, "name": "Священнослужитель", "industry": "Религия", "university": "Духовные академии и семинарии",
        "description": "Проводит богослужения и обряды, духовно окормляет прихожан. Это не профессия, а призвание и служение.",
        "link": "https://ru.wikipedia.org/wiki/Духовенство", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 4}
    },
    {
        "id": 192, "name": "Парфюмер", "industry": "Красота/Химия", "university": "РХТУ им. Менделеева, МГУ (Химфак) + спец. курсы",
        "description": "Создает ароматические композиции для духов, косметики и бытовой химии. Очень редкая, творческая профессия на стыке искусства и химии.",
        "link": "https://postupi.online/professiya/parfyumer/", "junior_salary": 80000, "avg_salary": 200000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 5}
    },
    {
        "id": 193, "name": "Мастер по ремонту цифровой техники", "industry": "Сервис/Электроника", "university": "Технические колледжи, учебные центры",
        "description": "Ремонтирует смартфоны, ноутбуки, планшеты. Может работать в сервисном центре или на себя. Спрос на услуги стабильно высокий.",
        "link": "https://postupi.online/professiya/inzhener-po-remontu-cifrovoj-tehniki/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 194, "name": "Социолог-исследователь", "industry": "Наука/Маркетинг/Госслужба", "university": "НИУ ВШЭ (Социология), МГУ (Соцфак)",
        "description": "Изучает общественное мнение и социальные процессы с помощью опросов, интервью и анализа данных. Работает в исследовательских центрах (ВЦИОМ, ФОМ) и маркетинговых агентствах.",
        "link": "https://postupi.online/professiya/sociolog/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 195, "name": "Кредитный аналитик", "industry": "Банки/Финансы", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Оценивает платежеспособность заемщиков (физических и юридических лиц), чтобы принять решение о выдаче кредита. Ключевая роль в управлении рисками банка.",
        "link": "https://postupi.online/professiya/kreditnyj-specialist/", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 196, "name": "Инженер-эколог", "industry": "Экология/Промышленность", "university": "РУДН (Экологический факультет), МГСУ",
        "description": "Разрабатывает и внедряет на предприятиях технологии для снижения вредного воздействия на окружающую среду. Контролирует соблюдение экологических норм.",
        "link": "https://postupi.online/professiya/inzhener-ekolog/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 197, "name": "NLP-инженер", "industry": "ИТ/Искусственный интеллект", "university": "МФТИ, НИУ ВШЭ (ФКН), Сколтех",
        "description": "Специалист по обработке естественного языка (Natural Language Processing). Учит машины понимать текст и речь, создавая умных чат-ботов и голосовых ассистентов.",
        "link": "https://netology.ru/blog/04-2022-nlp-engineer", "junior_salary": 115000, "avg_salary": 230000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 198, "name": "Оперный певец", "industry": "Искусство/Музыка", "university": "Консерватории (Москва, Санкт-Петербург), ГИТИС",
        "description": "Исполняет оперные партии на сценах музыкальных театров, таких как Большой или Мариинский. Путь к успеху требует уникального таланта и огромного труда.",
        "link": "https://postupi.online/professiya/opernyj-pevec/", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 3, 'routine': 5, 'art': 5}
    },
    {
        "id": 199, "name": "Экономист-международник", "industry": "Экономика/ВЭД/Госслужба", "university": "МГИМО, НИУ ВШЭ (МЭиМП)",
        "description": "Анализирует мировую экономику и международные торговые отношения. Работает в крупных экспортно-ориентированных компаниях и государственных структурах (Минэкономразвития).",
        "link": "https://postupi.online/professiya/ekonomist-mezhdunarodnik/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 200, "name": "VFX-художник", "industry": "Кино/Геймдев/Медиа", "university": "Scream School, онлайн-школы (XYZ, CGLab)",
        "description": "Создает визуальные эффекты для кино и игр: взрывы, магию, фантастических существ. Совмещает творчество и сложные технические навыки.",
        "link": "https://postupi.online/professiya/vfx-hudozhnik/", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 201, "name": "Продюсер онлайн-курсов", "industry": "EdTech/Образование", "university": "НИУ ВШЭ, Нетология, Skillbox",
        "description": "Создает и запускает образовательные онлайн-продукты. Отвечает за проект от идеи и поиска экспертов до маркетинга и продаж. Ключевая роль в российском EdTech.",
        "link": "https://netology.ru/blog/10-2022-edmarket-who-is-producer-online-kursov", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 202, "name": "Трекер (стартап-трекер)", "industry": "Венчур/Консалтинг/ИТ", "university": "ФРИИ, Сколково",
        "description": "Помогает стартапам быстро расти и достигать бизнес-целей, задавая правильные вопросы и фокусируя команду на главном. Работает в акселераторах и венчурных фондах.",
        "link": "https://ru.wikipedia.org/wiki/Трекинг_(бизнес)", "junior_salary": 90000, "avg_salary": 200000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 203, "name": "Генетический консультант", "industry": "Медицина/Наука/Биотехнологии", "university": "РНИМУ им. Пирогова, МГУ (ФФМ)",
        "description": "Консультирует пациентов по результатам генетических тестов, объясняя риски наследственных заболеваний. Новая профессия на стыке медицины и генетики.",
        "link": "https://postupi.online/professiya/vrach-genetik/", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, "social": 5, "routine": 4, "art": 1}
    },
    {
        "id": 204, "name": "Инженер по 3D-печати", "industry": "Промышленность/Инженерия/Прототипирование", "university": "МГТУ им. Баумана, МИСиС, СПбПУ",
        "description": "Создает физические объекты на 3D-принтерах: от прототипов и деталей до медицинских имплантов. Работает в инжиниринговых компаниях и на современных производствах.",
        "link": "https://postupi.online/professiya/specialist-po-additivnym-tehnologiyam/", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 205, "name": "Специалист по возобновляемым источникам энергии", "industry": "Энергетика/Экология", "university": "МЭИ, Сколтех",
        "description": "Проектирует и обслуживает солнечные и ветряные электростанции. Развивающееся, но пока нишевое направление в российской энергетике.",
        "link": "https://postupi.online/professiya/specialist-po-vozobnovlyaemoj-energetike/", "junior_salary": 85000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 206, "name": "Медицинский физик", "industry": "Медицина/Наука/Физика", "university": "МИФИ, МГУ (Физфак)",
        "description": "Обеспечивает безопасную и эффективную работу сложного медицинского оборудования (МРТ, КТ, ускорители для лучевой терапии). Работает в онкологических центрах.",
        "link": "https://postupi.online/professiya/medicinskij-fizik/", "junior_salary": 70000, "avg_salary": 125000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 207, "name": "Prompt-инженер", "industry": "ИТ/Искусственный интеллект", "university": "Профильные курсы, технические ВУЗы",
        "description": "Составляет 'запросы' (промпты) для нейросетей типа YandexGPT, чтобы получать от них наилучшие результаты. Новая профессия, возникшая с развитием генеративного ИИ.",
        "link": "https://ru.wikipedia.org/wiki/Инженерия_подсказок", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 3}
    },
    {
        "id": 208, "name": "Chief Data Officer (CDO)", "industry": "Менеджмент/ИТ/Аналитика", "university": "Опыт + МГУ (ВМК), МФТИ, НИУ ВШЭ",
        "description": "Топ-менеджер, отвечающий за всю стратегию работы с данными в компании. Управляет командами аналитиков, дата-сайентистов и инженеров.",
        "link": "https://ru.wikipedia.org/wiki/Директор_по_данным", "junior_salary": 250000, "avg_salary": 500000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 209, "name": "VR/AR-разработчик", "industry": "ИТ/Геймдев/Инженерия", "university": "Университет Иннополис, ИТМО, ДВФУ",
        "description": "Создает приложения и симуляторы для виртуальной (VR) и дополненной (AR) реальности. Работает в геймдеве, промышленности (тренажеры) и маркетинге.",
        "link": "https://edu.sravni.ru/kursy/info/vr-ar-razrabotchik/", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 210, "name": "Агробиотехнолог", "industry": "Сельское хозяйство/Наука/Биотехнологии", "university": "РГАУ-МСХА им. Тимирязева, МГУ (Биофак)",
        "description": "Использует биотехнологии для создания новых сортов растений, устойчивых к болезням и климату, и для улучшения качества сельхозпродукции.",
        "link": "https://postupi.online/professiya/agrobiotehnolog/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 211, "name": "Тьютор (в образовании)", "industry": "Образование/Педагогика", "university": "МПГУ, НИУ ВШЭ (Институт образования)",
        "description": "Сопровождает индивидуальный образовательный путь ученика, помогая ему ставить цели, выбирать курсы и развивать свои сильные стороны. Работает в частных школах.",
        "link": "https://postupi.online/professiya/tyutor/", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 212, "name": "Подкастер/Продюсер подкастов", "industry": "Медиа/Журналистика", "university": "МГУ (Журфак), профильные школы (Soundstream)",
        "description": "Создает аудио-шоу (подкасты): придумывает концепцию, записывает и монтирует выпуски, занимается продвижением. Растущий сегмент российского медиарынка.",
        "link": "https://postupi.online/professiya/podkaster/", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 213, "name": "Нейросетевой художник / AI-художник", "industry": "Искусство/Дизайн/ИТ", "university": "Онлайн-платформы и курсы",
        "description": "Создает изображения с помощью нейросетей (Midjourney, Kandinsky), генерируя идеи и подбирая точные запросы. Новое направление в цифровом искусстве.",
        "link": "https://ru.wikipedia.org/wiki/Искусство_искусственного_интеллекта", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 214, "name": "Специалист по этике ИИ", "industry": "ИТ/Юриспруденция/Философия", "university": "МГУ, НИУ ВШЭ, СПбГУ",
        "description": "Анализирует этические проблемы, связанные с использованием искусственного интеллекта (например, предвзятость алгоритмов). Новая междисциплинарная профессия.",
        "link": "https://ru.wikipedia.org/wiki/Этика_искусственного_интеллекта", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 215, "name": "Low-code/No-code разработчик", "industry": "ИТ/Бизнес", "university": "Платформы (Tilda, Bubble), онлайн-курсы",
        "description": "Создает сайты и приложения без написания кода, используя визуальные конструкторы. Позволяет быстро запускать простые проекты для бизнеса.",
        "link": "https://ru.wikipedia.org/wiki/Разработка_без_кода", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 216, "name": "Цифровой куратор", "industry": "Культура/Искусство/ИТ", "university": "НИУ ВШЭ, РГГУ, Университет ИТМО",
        "description": "Создает и проводит онлайн-выставки и другие цифровые проекты в сфере культуры. Работает в музеях и галереях, адаптируя искусство к digital-среде.",
        "link": "https://ru.wikipedia.org/wiki/Цифровое_курирование", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 217, "name": "Разработчик голосовых интерфейсов", "industry": "ИТ/Искусственный интеллект", "university": "МФТИ, МИРЭА + курсы (Yandex)",
        "description": "Проектирует и создает навыки для голосовых ассистентов (Алиса) и другие системы, управляемые голосом. Перспективное направление в IT.",
        "link": "https://www.ucheba.ru/prof/5368", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 2}
    },
    {
        "id": 218, "name": "Менеджер по цифровой трансформации", "industry": "Менеджмент/ИТ/Консалтинг", "university": "РАНХиГС, Сколково, ВШБ НИУ ВШЭ",
        "description": "Руководит внедрением цифровых технологий в крупных, часто не-IT компаниях, чтобы сделать их бизнес более современным и эффективным.",
        "link": "https://ru.wikipedia.org/wiki/Цифровая_трансформация", "junior_salary": 120000, "avg_salary": 250000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 219, "name": "Специалист по большим данным в медицине", "industry": "Медицина/ИТ/Аналитика", "university": "Первый МГМУ им. Сеченова (Цифровая медицина), ИТМО",
        "description": "Анализирует большие массивы медицинских данных (истории болезней, снимки) для выявления закономерностей и помощи врачам в постановке диагнозов.",
        "link": "https://habr.com/ru/companies/geekbrains/articles/555932/", "junior_salary": 95000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 220, "name": "Фандрайзер", "industry": "НКО/Социальная сфера/Маркетинг", "university": "МГИМО, НИУ ВШЭ, РГСУ",
        "description": "Привлекает пожертвования и гранты для некоммерческих организаций и благотворительных фондов. Специалист по поиску денег на добрые дела.",
        "link": "https://postupi.online/professiya/fandrajzer/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 221, "name": "Молекулярный диетолог", "industry": "Медицина/Биотехнологии/Wellness", "university": "РНИМУ им. Пирогова, МГУ",
        "description": "Разрабатывает персональные планы питания на основе генетических тестов и анализов, учитывая индивидуальные особенности метаболизма.",
        "link": "https://postupi.online/professiya/molekulyarnyj-dietolog/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 222, "name": "Архитектор 'умных' городов", "industry": "Архитектура/ИТ/Госуправление", "university": "МАРХИ, НИУ ВШЭ (Высшая школа урбанистики), ИТМО",
        "description": "Проектирует городскую среду с использованием IT-технологий: умные светофоры, системы безопасности, онлайн-сервисы для горожан.",
        "link": "https://plan-your-time.com/profession/smart-city-architect/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 3}
    },
    {
        "id": 223, "name": "Цифровой лингвист", "industry": "ИТ/Наука/Лингвистика", "university": "НИУ ВШЭ, РГГУ, МГУ (Филологический)",
        "description": "Специалист, который помогает машинам понимать нюансы человеческого языка. Разрабатывает словари и правила для чат-ботов, переводчиков и поисковых систем.",
        "link": "https://postupi.online/professiya/cifrovoj-lingvist/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 224, "name": "Фэшн-стилист", "industry": "Мода/Медиа/Ритейл", "university": "БВШД, МГУ, профильные школы (Marangoni)",
        "description": "Создает образы для фотосессий в журналах, рекламных кампаний и для частных клиентов. Работает со звездами, брендами и обычными людьми.",
        "link": "https://postupi.online/professiya/fashion-stilist/", "junior_salary": 50000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 225, "name": "Специалист по геймификации", "industry": "ИТ/HR/Маркетинг/Образование", "university": "НИУ ВШЭ, онлайн-курсы",
        "description": "Внедряет игровые механики (очки, бейджи, рейтинги) в неигровые процессы — обучение, работу, маркетинг — чтобы повысить вовлеченность пользователей.",
        "link": "https://postupi.online/professiya/specialist-po-gejmifikacii/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 3}
    },
    {
        "id": 226, "name": "Performance-маркетолог", "industry": "Маркетинг/ИТ/Аналитика", "university": "НИУ ВШЭ, РЭУ им. Плеханова, онлайн-платформы",
        "description": "Отвечает за интернет-рекламу, нацеленную на конкретный результат (продажи, заявки). Работает с цифрами, анализирует эффективность каждого вложенного рубля.",
        "link": "https://postupi.online/professiya/performance-marketolog/", "junior_salary": 75000, "avg_salary": 150000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 227, "name": "Проектировщик 'умных' домов", "industry": "Строительство/ИТ/Дизайн", "university": "МГСУ, МЭИ",
        "description": "Разрабатывает проекты систем автоматизации для частных домов и квартир, объединяя управление светом, климатом и мультимедиа в единый интерфейс.",
        "link": "https://postupi.online/professiya/proektirovshchik-umnogo-doma/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 228, "name": "Нейромаркетолог", "industry": "Маркетинг/Наука/Аналитика", "university": "НИУ ВШЭ, МГУ (Экономфак, Психфак)",
        "description": "Изучает, как мозг потребителя реагирует на рекламу и продукты, используя специальное оборудование (ЭЭГ, ай-трекеры). Новое направление на стыке маркетинга и нейробиологии.",
        "link": "https://postupi.online/professiya/nejromarketolog/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 229, "name": "Специалист по работе с клиентами (в IT)", "industry": "ИТ/Сервис/Продажи", "university": "Любой ВУЗ + курсы",
        "description": "Сопровождает корпоративных клиентов, помогает им решать возникающие проблемы и развивает долгосрочные отношения. Ключевая роль в B2B IT-компаниях.",
        "link": "https://postupi.online/professiya/menedzher-po-rabote-s-klientami/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 230, "name": "Монтажник слаботочных систем", "industry": "Строительство/Безопасность/ИТ", "university": "Технические колледжи",
        "description": "Прокладывает и настраивает интернет, видеонаблюдение, охранную и пожарную сигнализацию в жилых домах и офисах.",
        "link": "https://postupi.online/professiya/montazhnik-slabotochnyh-sistem/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 231, "name": "Data Steward (Распорядитель данных)", "industry": "ИТ/Аналитика/Менеджмент", "university": "Технические и экономические ВУЗы",
        "description": "Отвечает за качество, доступность и безопасность определенного набора данных в крупной компании. 'Хранитель' данных, обеспечивающий порядок.",
        "link": "https://ru.wikipedia.org/wiki/Управление_данными", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 232, "name": "Коуч (бизнес, лайф)", "industry": "Консалтинг/Психология/HR", "university": "Сертификационные программы (ICF), ВУЗы (психология)",
        "description": "Помогает клиентам достигать личных или профессиональных целей, раскрывать свой потенциал через диалог и специальные техники. Рынок коучинга в России активно растет.",
        "link": "https://postupi.online/professiya/kouch/", "junior_salary": 50000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 233, "name": "Мастер-сыровар", "industry": "Производство/Сельское хозяйство/HoReCa", "university": "ВНИИМС (Углич), аграрные ВУЗы, частные школы",
        "description": "Производит ремесленные (крафтовые) сыры. Перспективное направление в России на фоне роста интереса к фермерским продуктам.",
        "link": "https://postupi.online/professiya/syrodel/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 4}
    },
    {
        "id": 234, "name": "Киберследователь", "industry": "Безопасность/Госслужба/ИТ", "university": "МИФИ, МГТУ им. Баумана, ведомственные ВУЗы",
        "description": "Расследует киберпреступления: взломы, кражи данных, мошенничество в интернете. Работает в правоохранительных органах или в компаниях по кибербезопасности.",
        "link": "https://www.ucheba.ru/prof/5006", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 235, "name": "Дизайнер одежды", "industry": "Мода/Дизайн/Производство", "university": "БВШД, МХПИ, РГУ им. Косыгина",
        "description": "Придумывает и создает новые модели одежды. Может работать на крупный бренд или развивать собственную марку на российском рынке моды.",
        "link": "https://postupi.online/professiya/dizajner-odezhdy/", "junior_salary": 50000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 236, "name": "Специалист по интеллектуальной собственности", "industry": "Юриспруденция/ИТ/Наука", "university": "РГАИС, МГЮА им. Кутафина",
        "description": "Защищает права на товарные знаки, патенты, авторские права. Помогает компаниям управлять их нематериальными активами.",
        "link": "https://postupi.online/professiya/specialist-po-intellektualnoj-sobstvennosti/", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 237, "name": "Аналитик мобильных приложений", "industry": "ИТ/Аналитика/Маркетинг", "university": "НИУ ВШЭ, МФТИ",
        "description": "Анализирует данные об использовании мобильных приложений, чтобы улучшить их функциональность, удержать пользователей и увеличить доход.",
        "link": "https://postupi.online/professiya/mobilnyj-analitik/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 238, "name": "Воспитатель в детском саду", "industry": "Образование/Социальная сфера", "university": "МПГУ, РГПУ им. Герцена, педагогические колледжи",
        "description": "Организует досуг, обучение и развитие детей дошкольного возраста. Социально значимая, но низкооплачиваемая работа в государственной системе.",
        "link": "https://postupi.online/professiya/vospitatel-detskogo-sada/", "junior_salary": 30000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 4}
    },
    {
        "id": 239, "name": "Орнитолог", "industry": "Наука/Экология", "university": "МГУ (Биофак), СПбГУ (Биофак)",
        "description": "Изучает птиц, их поведение, миграции и места обитания. Работает в заповедниках, научных институтах, участвует в экспедициях.",
        "link": "https://postupi.online/professiya/ornitolog/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 240, "name": "DevSecOps-инженер", "industry": "ИТ/Безопасность", "university": "МГТУ им. Баумана, ИТМО + доп. образование",
        "description": "Встраивает практики безопасности непосредственно в процесс разработки ПО (DevOps), чтобы делать продукты безопасными 'по умолчанию'. Передовое направление в IT.",
        "link": "https://ru.wikipedia.org/wiki/DevSecOps", "junior_salary": 120000, "avg_salary": 230000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 241, "name": "Электрик/Электромонтажник", "industry": "Строительство/ЖКХ/Рабочие", "university": "Технические колледжи, учебные центры",
        "description": "Обеспечивает работу электросетей в жилых домах и на предприятиях. Стабильная рабочая профессия, востребованная по всей России.",
        "link": "https://postupi.online/professiya/elektrik/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 242, "name": "Сантехник", "industry": "Строительство/ЖКХ/Рабочие", "university": "Технические колледжи",
        "description": "Монтирует и ремонтирует системы отопления, водоснабжения и канализации. Квалифицированные мастера высоко ценятся в сфере ЖКХ и частных услуг.",
        "link": "https://postupi.online/professiya/santehnik/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 243, "name": "Медсестра/Медбрат", "industry": "Медицина", "university": "Медицинские колледжи и училища",
        "description": "Выполняет врачебные назначения, ухаживает за пациентами в больницах и поликлиниках. Основа системы здравоохранения, всегда востребованная профессия.",
        "link": "https://postupi.online/professiya/medsestra/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 244, "name": "Повар", "industry": "Общепит/HoReCa", "university": "Кулинарные колледжи и техникумы",
        "description": "Готовит блюда в ресторанах, кафе, столовых. Востребованная профессия в сфере гостеприимства с возможностью карьерного роста до шеф-повара.",
        "link": "https://postupi.online/professiya/povar/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 4}
    },
    {
        "id": 245, "name": "Водитель-дальнобойщик", "industry": "Транспорт/Логистика", "university": "Автошколы (категория C+E), курсы",
        "description": "Перевозит грузы на большие расстояния по России и за ее пределы. Тяжелая работа с ненормированным графиком, но с хорошим заработком.",
        "link": "https://postupi.online/professiya/voditel-dalnobojshchik/", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 246, "name": "Продавец-консультант", "industry": "Ритейл/Торговля", "university": "Не требуется, тренинги на месте работы",
        "description": "Помогает покупателям в магазине выбрать товар, консультирует по ассортименту. Массовая и доступная профессия, хороший старт для карьеры в продажах.",
        "link": "https://postupi.online/professiya/prodavec-konsultant/", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 247, "name": "Секретарь/Офис-менеджер", "industry": "Административная работа", "university": "Колледжи, профильные курсы",
        "description": "Обеспечивает жизнедеятельность офиса: отвечает на звонки, ведет документооборот, заказывает канцтовары. 'Лицо' компании для посетителей и сотрудников.",
        "link": "https://postupi.online/professiya/ofis-menedzher/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 248, "name": "Кладовщик", "industry": "Логистика/Склад", "university": "Среднее профессиональное образование",
        "description": "Принимает, хранит и отпускает товары на складе, ведет их учет. Востребован в любой торговой или производственной компании.",
        "link": "https://postupi.online/professiya/kladovshchik/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 249, "name": "Охранник", "industry": "Безопасность", "university": "Школы охранников, лицензирование",
        "description": "Обеспечивает безопасность на объекте: в магазине, офисе, на предприятии. Массовая профессия, требующая бдительности и ответственности.",
        "link": "https://postupi.online/professiya/ohrannik/", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 250, "name": "Уборщик/Клинер", "industry": "Сервис/ЖКХ", "university": "Не требуется",
        "description": "Поддерживает чистоту в офисах, торговых центрах, жилых домах. Профессия не требует квалификации, всегда есть спрос на услуги.",
        "link": "https://trudvsem.ru/professions/detail/19305", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 251, "name": "Автослесарь", "industry": "Автосервис/Рабочие", "university": "Технические колледжи и училища",
        "description": "Ремонтирует и обслуживает автомобили. Стабильная и востребованная профессия, так как автопарк в России постоянно растет.",
        "link": "https://postupi.online/professiya/avtoslesar/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 252, "name": "Лаборант (химический, медицинский)", "industry": "Наука/Медицина/Производство", "university": "Медицинские и химические колледжи",
        "description": "Проводит анализы и исследования в лаборатории под руководством специалистов. Работает на производствах, в поликлиниках и научных институтах.",
        "link": "https://postupi.online/professiya/laborant-himicheskogo-analiza/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 253, "name": "Социальный работник", "industry": "Социальная сфера/Госслужба", "university": "РГСУ, колледжи социальной работы",
        "description": "Помогает пожилым людям, инвалидам и семьям в трудной ситуации. Социально важная, но эмоционально тяжелая и низкооплачиваемая работа.",
        "link": "https://postupi.online/professiya/socialnyj-rabotnik/", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 254, "name": "Кассир", "industry": "Ритейл/Торговля/Банки", "university": "Не требуется, обучение на месте",
        "description": "Принимает оплату за товары и услуги в магазинах, на заправках, в банках. Массовая профессия, требующая внимательности и вежливости.",
        "link": "https://postupi.online/professiya/kassir/", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 255, "name": "Курьер", "industry": "Логистика/Сервис/Доставка", "university": "Не требуется",
        "description": "Доставляет еду, товары из интернет-магазинов и документы. Очень востребованная работа в крупных городах с гибким графиком.",
        "link": "https://postupi.online/professiya/kurer/", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 256, "name": "Крановщик", "industry": "Строительство/Промышленность", "university": "Учебные центры, колледжи",
        "description": "Управляет башенными и автомобильными кранами на стройках и производствах. Ответственная и хорошо оплачиваемая рабочая специальность.",
        "link": "https://postupi.online/professiya/kranovshchik/", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 257, "name": "Швея/Портной", "industry": "Легкая промышленность/Сервис/Ателье", "university": "Колледжи легкой промышленности",
        "description": "Шьет одежду на фабриках или в ателье по индивидуальным заказам. Спрос на качественный пошив одежды в России стабилен.",
        "link": "https://postupi.online/professiya/portnoj/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 4}
    },
    {
        "id": 258, "name": "Маляр-штукатур", "industry": "Строительство/Ремонт", "university": "Строительные колледжи",
        "description": "Выполняет отделочные работы при строительстве и ремонте помещений. Востребованная рабочая профессия, доход зависит от скорости и качества работы.",
        "link": "https://postupi.online/professiya/malyar-shtukatur/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 259, "name": "Плотник/Столяр", "industry": "Строительство/Производство мебели", "university": "Профессиональные училища",
        "description": "Работает с деревом: строит дома, изготавливает мебель, окна, двери. Квалифицированные мастера ценятся как в строительстве, так и в мебельном производстве.",
        "link": "https://postupi.online/professiya/stolyar/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 260, "name": "Бурильщик (нефть и газ)", "industry": "Нефтегаз/Добыча", "university": "Профильные колледжи и ВУЗы (РГУ нефти и газа)",
        "description": "Работает в составе буровой бригады на нефтяных и газовых месторождениях. Тяжелая вахтовая работа с очень высокой оплатой.",
        "link": "https://postupi.online/professiya/burilshchik/", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 261, "name": "Фельдшер", "industry": "Медицина", "university": "Медицинские колледжи",
        "description": "Работает на скорой помощи или в фельдшерско-акушерских пунктах в сельской местности, оказывая первую медицинскую помощь. Очень ответственная работа.",
        "link": "https://postupi.online/professiya/feldsher/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 262, "name": "Водитель такси", "industry": "Транспорт/Сервис", "university": "Автошколы (категория B), стаж вождения",
        "description": "Перевозит пассажиров в городе. Работа через агрегаторы (Яндекс.Такси) дает гибкий график, но требует стрессоустойчивости.",
        "link": "https://trudvsem.ru/professions/detail/11188", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 263, "name": "Пожарный", "industry": "Госслужба/Безопасность (МЧС)", "university": "Академия ГПС МЧС, учебные центры МЧС",
        "description": "Тушит пожары и спасает людей. Героическая и опасная государственная служба с социальными льготами и ранним выходом на пенсию.",
        "link": "https://postupi.online/professiya/pozharnyj/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 264, "name": "Оператор call-центра", "industry": "Сервис/Продажи", "university": "Не требуется, тренинги",
        "description": "Отвечает на звонки клиентов, консультирует по продуктам или продает услуги по телефону. Массовая стартовая позиция в банках, телекоме и других крупных компаниях.",
        "link": "https://postupi.online/professiya/operator-call-centra/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 265, "name": "Мастер маникюра/педикюра", "industry": "Красота/Сервис", "university": "Профильные школы и курсы",
        "description": "Выполняет процедуры по уходу за ногтями. Востребованная профессия в индустрии красоты с возможностью работать в салоне или на себя.",
        "link": "https://postupi.online/professiya/master-manikyura/", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 5, 'art': 5}
    },
    {
        "id": 266, "name": "Агент по недвижимости (Риелтор)", "industry": "Недвижимость/Продажи", "university": "Курсы, тренинги в агентствах",
        "description": "Помогает людям покупать, продавать и арендовать недвижимость. Динамичная работа с высоким потенциалом дохода, особенно в крупных городах России.",
        "link": "https://postupi.online/professiya/rieltor/", "junior_salary": 40000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 267, "name": "Менеджер по туризму", "industry": "Туризм/Сервис", "university": "РГУТиС, профильные ВУЗы и колледжи",
        "description": "Подбирает и продает туры, бронирует отели и билеты. Работа в турагентствах, сильно зависит от общей ситуации в стране и мире.",
        "link": "https://postupi.online/professiya/menedzher-po-turizmu/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 268, "name": "Официант", "industry": "Общепит/HoReCa", "university": "Не требуется, школы ресторанного сервиса",
        "description": "Обслуживает гостей в ресторане или кафе. Хорошая стартовая позиция в ресторанном бизнесе, доход сильно зависит от чаевых.",
        "link": "https://postupi.online/professiya/oficiant/", "junior_salary": 35000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 269, "name": "Фотограф", "industry": "Медиа/Сервис/Искусство", "university": "Школы фотографии, курсы",
        "description": "Проводит фотосессии (свадебные, семейные, репортажные). Творческая профессия, чаще всего на фрилансе, с высокой конкуренцией.",
        "link": "https://postupi.online/professiya/fotograf/", "junior_salary": 40000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 270, "name": "Мерчендайзер", "industry": "Ритейл/Торговля/Маркетинг", "university": "Не требуется",
        "description": "Отвечает за выкладку товаров в магазине так, чтобы они лучше продавались. Работа в торговых сетях и компаниях-производителях.",
        "link": "https://postupi.online/professiya/merchendajzer/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 2}
    },
    {
        "id": 271, "name": "Библиотекарь", "industry": "Культура/Образование", "university": "МГИК, СПбГИК, колледжи культуры",
        "description": "Работает с книжным фондом, обслуживает читателей, проводит культурные мероприятия. Спокойная, но низкооплачиваемая работа в госучреждениях.",
        "link": "https://postupi.online/professiya/bibliotekar/", "junior_salary": 25000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 3}
    },
    {
        "id": 272, "name": "Сборщик мебели", "industry": "Сервис/Производство", "university": "Профессиональные училища",
        "description": "Собирает корпусную и мягкую мебель на производстве или на дому у клиентов. Доход зависит от скорости и аккуратности.",
        "link": "https://trudvsem.ru/professions/detail/18329", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 273, "name": "Монтажник окон", "industry": "Строительство/Сервис", "university": "Учебные центры производителей",
        "description": "Устанавливает пластиковые и деревянные окна в квартирах и домах. Работа, требующая физической силы и аккуратности, с хорошим сезонным заработком.",
        "link": "https://trudvsem.ru/professions/detail/14295", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 274, "name": "Работник почты (Оператор связи)", "industry": "Госслужба/Логистика", "university": "Колледжи связи",
        "description": "Принимает и выдает посылки, письма, оформляет подписку в отделениях Почты России. Стабильная, но низкооплачиваемая работа.",
        "link": "https://trudvsem.ru/professions/detail/15975", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 275, "name": "Дорожный рабочий", "industry": "Строительство/ЖКХ", "university": "Строительные колледжи",
        "description": "Строит и ремонтирует автомобильные дороги, укладывает асфальт. Тяжелая физическая работа на открытом воздухе.",
        "link": "https://postupi.online/professiya/dorozhnyj-rabochij/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 276, "name": "Дворник", "industry": "ЖКХ", "university": "Не требуется",
        "description": "Поддерживает чистоту на придомовой территории. Физическая работа на свежем воздухе, часто с предоставлением служебного жилья.",
        "link": "https://trudvsem.ru/professions/detail/11728", "junior_salary": 25000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 277, "name": "Зубной техник", "industry": "Медицина/Стоматология", "university": "Медицинские колледжи",
        "description": "Изготавливает в лаборатории зубные протезы, коронки и виниры по слепкам врачей-стоматологов. Кропотливая 'ювелирная' работа.",
        "link": "https://postupi.online/professiya/zubnoj-tehnik/", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 278, "name": "Аниматор (детский, отельный)", "industry": "Развлечения/Сервис", "university": "Педагогические и культурные ВУЗы, курсы",
        "description": "Организует досуг и развлекательные программы для детей на праздниках или для туристов в отелях. Веселая и активная работа.",
        "link": "https://postupi.online/professiya/animator/", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 279, "name": "Водитель автобуса/троллейбуса", "industry": "Транспорт/Госслужба", "university": "Учебно-курсовые комбинаты",
        "description": "Перевозит пассажиров по городским маршрутам. Ответственная работа в системе общественного транспорта со стабильным заработком.",
        "link": "https://trudvsem.ru/professions/detail/11186", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 280, "name": "Работник конвейера/фабрики", "industry": "Промышленность/Производство", "university": "Не требуется",
        "description": "Выполняет однотипные операции на производственной линии. Монотонная работа, не требующая высокой квалификации.",
        "link": "https://ru.wikipedia.org/wiki/Конвейер", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 281, "name": "Менеджер по закупкам", "industry": "Торговля/Логистика/Производство", "university": "РЭУ им. Плеханова, НИУ ВШЭ",
        "description": "Ищет поставщиков и закупает товары или сырье для компании по наилучшим ценам. Важная роль в ритейле и на производстве.",
        "link": "https://postupi.online/professiya/menedzher-po-zakupkam/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 282, "name": "Инструктор по вождению", "industry": "Образование/Сервис", "university": "Свидетельство на право обучения вождению",
        "description": "Обучает будущих водителей управлению автомобилем. Работает в автошколе или как частный инструктор. Требует терпения и стрессоустойчивости.",
        "link": "https://postupi.online/professiya/instruktor-po-vozhdeniyu/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 283, "name": "Мясник", "industry": "Ритейл/Производство/Общепит", "university": "Колледжи пищевой промышленности",
        "description": "Разделывает мясные туши на производстве или в магазине. Профессия, требующая физической силы и специальных навыков.",
        "link": "https://postupi.online/professiya/myasnik/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 284, "name": "Пекарь", "industry": "Общепит/Производство/Ритейл", "university": "Колледжи пищевой промышленности",
        "description": "Выпекает хлеб и хлебобулочные изделия на хлебозаводах, в пекарнях и супермаркетах. Востребованная рабочая профессия.",
        "link": "https://postupi.online/professiya/pekar/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 285, "name": "Страховой агент", "industry": "Страхование/Финансы/Продажи", "university": "Курсы при страховых компаниях",
        "description": "Продает страховые полисы (ОСАГО, КАСКО, страхование жизни). Доход напрямую зависит от количества проданных страховок.",
        "link": "https://postupi.online/professiya/strahovoj-agent/", "junior_salary": 40000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 286, "name": "Визажист", "industry": "Красота/Сервис/Медиа", "university": "Школы визажа, курсы",
        "description": "Создает макияж для клиентов, работает на фотосессиях, в салонах красоты или на себя. Творческая профессия в индустрии красоты.",
        "link": "https://postupi.online/professiya/vizazhist/", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 287, "name": "Монтажник натяжных потолков", "industry": "Строительство/Ремонт/Сервис", "university": "Обучение в компаниях",
        "description": "Устанавливает натяжные потолки в квартирах и офисах. Востребованная услуга на рынке ремонта, заработок сдельный.",
        "link": "https://trudvsem.ru/professions/detail/14238", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 288, "name": "Комплектовщик заказов", "industry": "Склад/Логистика/Ритейл", "university": "Не требуется",
        "description": "Собирает товары на складе по накладной для отправки клиентам. Востребован на складах интернет-магазинов и маркетплейсов.",
        "link": "https://postupi.online/professiya/komplektovshchik/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 289, "name": "Массажист", "industry": "Медицина/Красота/Фитнес", "university": "Медицинские колледжи, курсы массажа",
        "description": "Выполняет лечебный или расслабляющий массаж. Работает в медицинских центрах, спа-салонах или ведет частную практику.",
        "link": "https://postupi.online/professiya/massazhist/", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 290, "name": "Администратор гостиницы/отеля", "industry": "Гостиничный бизнес/HoReCa", "university": "Колледжи и ВУЗы гостиничного дела",
        "description": "Встречает и регистрирует гостей, отвечает на их вопросы, решает возникающие проблемы. 'Лицо' отеля, работа с людьми.",
        "link": "https://postupi.online/professiya/administrator-gostinicy/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 291, "name": "Слесарь-ремонтник", "industry": "Промышленность/ЖКХ/Рабочие", "university": "Технические колледжи и училища",
        "description": "Ремонтирует и обслуживает промышленное оборудование на заводах или сантехнику в системе ЖКХ. Универсальная и востребованная рабочая профессия.",
        "link": "https://postupi.online/professiya/slesar-remontnik/", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 292, "name": "Врач-терапевт", "industry": "Медицина", "university": "Медицинские ВУЗы (Лечебное дело)",
        "description": "Врач первого контакта в поликлинике. Проводит первичный осмотр, ставит диагноз и направляет к узким специалистам. Основа первичного звена здравоохранения.",
        "link": "https://postupi.online/professiya/terapevt/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, "art": 1}
    },
    {
        "id": 293, "name": "Каменщик", "industry": "Строительство", "university": "Строительные колледжи и училища",
        "description": "Возводит стены и перегородки из кирпича и блоков. Одна из основных и востребованных профессий на стройке, требующая физической силы и точности.",
        "link": "https://postupi.online/professiya/kamenshchik/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 294, "name": "Учитель начальных классов", "industry": "Образование", "university": "Педагогические ВУЗы и колледжи",
        "description": "Обучает детей с 1 по 4 класс всем основным предметам. Закладывает фундамент образования. Очень важная, но низкооплачиваемая государственная работа.",
        "link": "https://postupi.online/professiya/uchitel-nachalnyh-klassov/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 3}
    },
    {
        "id": 295, "name": "Машинист экскаватора", "industry": "Строительство/Добыча", "university": "Учебные центры, колледжи",
        "description": "Управляет экскаватором на стройке или в карьере, роет котлованы и траншеи. Хорошо оплачиваемая рабочая специальность.",
        "link": "https://postupi.online/professiya/mashinist-ekskavatora/", "junior_salary": 80000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 296, "name": "Врач-педиатр", "industry": "Медицина", "university": "Медицинские ВУЗы (Педиатрия)",
        "description": "Лечит детей от рождения до 18 лет. Работает в детских поликлиниках и больницах. Требует не только медицинских знаний, но и умения находить подход к детям.",
        "link": "https://postupi.online/professiya/pediatr/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 297, "name": "Специалист по кадрам (Кадровик)", "industry": "HR/Административная работа", "university": "Профильные курсы, ВУЗы (Управление персоналом)",
        "description": "Ведет кадровый документооборот в компании в соответствии с Трудовым кодексом РФ: прием, увольнение, отпуска, больничные.",
        "link": "https://postupi.online/professiya/specialist-po-kadram/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 298, "name": "Бортпроводник", "industry": "Авиация/Транспорт/Сервис", "university": "Школы бортпроводников при авиакомпаниях",
        "description": "Обеспечивает безопасность и комфорт пассажиров во время полета. Работа в российских авиакомпаниях, связанная с путешествиями и общением с людьми.",
        "link": "https://postupi.online/professiya/bortprovodnik/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 299, "name": "Садовник/Озеленитель", "industry": "ЖКХ/Сервис/Ландшафтный дизайн", "university": "Аграрные и лесотехнические колледжи",
        "description": "Ухаживает за растениями в парках, скверах или на частных участках. Работа для тех, кто любит природу и физический труд на свежем воздухе.",
        "link": "https://postupi.online/professiya/sadovnik/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 300, "name": "Контент-менеджер", "industry": "Маркетинг/ИТ/Медиа", "university": "Онлайн-курсы, ВУЗы (Журналистика, Филология)",
        "description": "Наполняет сайт или соцсети информацией: пишет тексты, подбирает изображения, публикует материалы. Востребованная стартовая позиция в digital.",
        "link": "https://postupi.online/professiya/kontent-menedzher/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 3}
    },
    {
        "id": 301, "name": "Фрезеровщик", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи",
        "description": "Обрабатывает детали на фрезерном станке. Квалифицированный рабочий, востребованный на машиностроительных и оборонных предприятиях России.",
        "link": "https://postupi.online/professiya/frezerovshchik/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 302, "name": "Сиделка", "industry": "Социальная сфера/Медицина", "university": "Медицинские колледжи, курсы",
        "description": "Ухаживает за больными и пожилыми людьми на дому или в больнице. Социально важная работа, спрос на которую в России растет из-за старения населения.",
        "link": "https://postupi.online/professiya/sidelka/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 303, "name": "Горничная", "industry": "Гостиничный бизнес/Сервис", "university": "Не требуется",
        "description": "Убирает номера в гостиницах и отелях. Работа, не требующая квалификации, востребована в туристических центрах России.",
        "link": "https://postupi.online/professiya/gornichnaya/", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 304, "name": "Экономист", "industry": "Финансы/Бухгалтерия/Менеджмент", "university": "Экономические ВУЗы (Финансовый университет, РЭУ, ВШЭ)",
        "description": "Планирует и анализирует финансово-хозяйственную деятельность предприятия. Универсальная и массовая профессия в любой отрасли экономики.",
        "link": "https://postupi.online/professiya/ekonomist/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 305, "name": "Водитель погрузчика", "industry": "Склад/Логистика/Производство", "university": "Учебные центры",
        "description": "Управляет погрузчиком на складе, перемещая товары. Востребованная рабочая профессия в логистике и ритейле.",
        "link": "https://postupi.online/professiya/voditel-pogruzchika/", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 306, "name": "Рентгенолаборант", "industry": "Медицина", "university": "Медицинские колледжи",
        "description": "Делает рентгеновские снимки и флюорографию в поликлиниках и больницах под руководством врача-рентгенолога.",
        "link": "https://postupi.online/professiya/rentgenolaborant/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 307, "name": "Хореограф/Преподаватель танцев", "industry": "Искусство/Образование/Фитнес", "university": "Институты культуры (МГИК, СПбГИК), театральные ВУЗы",
        "description": "Обучает танцам детей и взрослых, ставит танцевальные номера. Работает в танцевальных школах, фитнес-клубах, домах культуры.",
        "link": "https://postupi.online/professiya/horeograf/", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 308, "name": "Специалист технической поддержки", "industry": "ИТ/Сервис", "university": "Технические колледжи, онлайн-курсы",
        "description": "Помогает пользователям решать технические проблемы с программным обеспечением или услугами. Стартовая позиция для карьеры в IT.",
        "link": "https://postupi.online/professiya/specialist-tehnicheskoj-podderzhki/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 309, "name": "Кровельщик", "industry": "Строительство", "university": "Строительные колледжи",
        "description": "Монтирует и ремонтирует крыши зданий. Физически тяжелая и опасная работа, но с хорошим уровнем оплаты.",
        "link": "https://trudvsem.ru/professions/detail/13358", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 310, "name": "Врач-хирург", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по хирургии",
        "description": "Проводит операции для лечения заболеваний и травм. Одна из самых уважаемых и ответственных профессий в медицине.",
        "link": "https://postupi.online/professiya/hirurg/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 311, "name": "Грузчик", "industry": "Логистика/Сервис/Ритейл", "university": "Не требуется",
        "description": "Выполняет погрузочно-разгрузочные работы на складах, в магазинах, при переездах. Тяжелая физическая работа.",
        "link": "https://postupi.online/professiya/gruzchik/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 312, "name": "Почтальон", "industry": "Логистика/Госслужба", "university": "Не требуется",
        "description": "Доставляет письма, газеты и пенсии адресатам. Социально значимая работа в структуре 'Почты России', особенно в сельской местности.",
        "link": "https://postupi.online/professiya/pochtalon/", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 313, "name": "Оператор котельной", "industry": "ЖКХ/Промышленность", "university": "Учебные центры",
        "description": "Обслуживает котельное оборудование, обеспечивая подачу тепла и горячей воды. Ответственная работа в сфере ЖКХ и на промышленных предприятиях.",
        "link": "https://trudvsem.ru/professions/detail/15726", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 314, "name": "Учитель истории и обществознания", "industry": "Образование", "university": "Педагогические ВУЗы (Исторический факультет)",
        "description": "Преподает гуманитарные дисциплины в школе, формируя у учеников знания о прошлом и понимание устройства современного общества.",
        "link": "https://postupi.online/professiya/uchitel-istorii/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 315, "name": "Диспетчер (транспорт, ЖКХ, аварийная служба)", "industry": "Транспорт/Логистика/ЖКХ", "university": "Профильные курсы, колледжи",
        "description": "Принимает и координирует заявки, управляет движением транспорта или работой ремонтных бригад. Стрессовая работа, требующая быстрой реакции.",
        "link": "https://postupi.online/professiya/dispetcher/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 316, "name": "Маркшейдер", "industry": "Добыча/Геодезия/Строительство", "university": "Горные и политехнические ВУЗы (МГРИ)",
        "description": "'Горный геодезист', который проводит пространственные измерения в недрах земли при добыче полезных ископаемых или строительстве тоннелей метро.",
        "link": "https://postupi.online/professiya/markshejder/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 317, "name": "Санитар/Санитарка", "industry": "Медицина", "university": "Не требуется, курсы младшего медперсонала",
        "description": "Младший медицинский персонал, который помогает в уходе за больными и поддержании чистоты в лечебном учреждении. Тяжелая, но необходимая работа.",
        "link": "https://postupi.online/professiya/sanitar/", "junior_salary": 28000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 318, "name": "Инструктор тренажерного зала", "industry": "Фитнес/Спорт/Сервис", "university": "Колледжи и ВУЗы физкультуры (РГУФКСМиТ), курсы",
        "description": "Проводит персональные тренировки в фитнес-клубе, помогает клиентам составить программу занятий и правильно выполнять упражнения.",
        "link": "https://postupi.online/professiya/fitnes-instruktor/", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 319, "name": "Операционист в банке", "industry": "Банки/Финансы", "university": "Финансовые колледжи, тренинги в банках",
        "description": "Обслуживает клиентов в отделении банка: открывает счета, делает переводы, консультирует по банковским продуктам. Начальная позиция в банковской сфере.",
        "link": "https://postupi.online/professiya/operacionist/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 320, "name": "Грумер", "industry": "Сервис/Животные", "university": "Курсы и школы груминга",
        "description": "Делает стрижки и проводит гигиенические процедуры для домашних животных, в основном собак и кошек. Растущий рынок услуг в крупных городах.",
        "link": "https://postupi.online/professiya/grumer/", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 4}
    },
    {
        "id": 321, "name": "Врач-офтальмолог (окулист)", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Диагностирует и лечит заболевания глаз, подбирает очки и контактные линзы. Работает в поликлиниках и салонах оптики.",
        "link": "https://postupi.online/professiya/oftalmolog/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 322, "name": "Упаковщик/Комплектовщик", "industry": "Производство/Склад/Ритейл", "university": "Не требуется",
        "description": "Упаковывает готовую продукцию на производстве или собирает заказы на складе. Монотонная работа, не требующая квалификации.",
        "link": "https://postupi.online/professiya/upakovshchik/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 323, "name": "Лесник/Егерь", "industry": "Лесное хозяйство/Экология", "university": "Лесотехнические ВУЗы и колледжи",
        "description": "Охраняет лес от пожаров и браконьеров, следит за состоянием лесного фонда и популяциями животных. Работа для тех, кто любит природу и уединение.",
        "link": "https://postupi.online/professiya/lesnik/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 324, "name": "Делопроизводитель/Архивариус", "industry": "Административная работа/Госслужба", "university": "Колледжи, РГГУ (Историко-архивный институт)",
        "description": "Ведет учет и обеспечивает хранение документов в организации или государственном архиве. Работа, требующая аккуратности и системности.",
        "link": "https://postupi.online/professiya/arhivist/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 325, "name": "Кондитер", "industry": "Общепит/Производство", "university": "Колледжи пищевой промышленности, кулинарные школы",
        "description": "Создает торты, пирожные, десерты и выпечку. Работает в кондитерских, ресторанах или открывает собственный бизнес. Требует творческого подхода и аккуратности.",
        "link": "https://postupi.online/professiya/konditer/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 326, "name": "Монтажник вентиляции и кондиционирования", "industry": "Строительство/ЖКХ", "university": "Технические колледжи",
        "description": "Устанавливает и обслуживает системы вентиляции и кондиционеры в зданиях. Востребованная рабочая профессия, особенно в летний сезон.",
        "link": "https://postupi.online/professiya/inzhener-po-ventilyacii-i-kondicionirovaniyu/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 327, "name": "Животновод (Доярка, скотник)", "industry": "Сельское хозяйство", "university": "Аграрные колледжи",
        "description": "Ухаживает за коровами, свиньями и другими сельскохозяйственными животными на ферме. Тяжелый физический труд в аграрном секторе.",
        "link": "https://postupi.online/professiya/zhivotnovod/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 328, "name": "Секретарь суда", "industry": "Юриспруденция/Госслужба", "university": "Юридические колледжи, ВУЗы",
        "description": "Ведет протокол судебного заседания, оформляет дела и выполняет поручения судьи. Стартовая позиция в судебной системе.",
        "link": "https://postupi.online/professiya/sekretar-suda/", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 329, "name": "Учитель физкультуры", "industry": "Образование/Спорт", "university": "Институты физкультуры, педагогические ВУЗы",
        "description": "Проводит уроки физической культуры в школе, организует спортивные мероприятия. Работа, направленная на физическое развитие детей.",
        "link": "https://postupi.online/professiya/uchitel-fizkultury/", "junior_salary": 35000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 330, "name": "Заправщик на АЗС", "industry": "Сервис/Ритейл", "university": "Не требуется",
        "description": "Заправляет автомобили топливом на автозаправочной станции. Работа на открытом воздухе, не требующая специальной подготовки.",
        "link": "https://trudvsem.ru/professions/detail/12247", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 331, "name": "Врач-ЛОР (Оториноларинголог)", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Лечит заболевания уха, горла и носа у взрослых и детей. Одна из самых востребованных врачебных специальностей в поликлиниках.",
        "link": "https://postupi.online/professiya/otorinolaringolog/", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 332, "name": "Машинист автокрана", "industry": "Строительство", "university": "Учебные центры",
        "description": "Управляет автомобильным краном, перемещая тяжелые грузы на строительных площадках. Ответственная и хорошо оплачиваемая рабочая профессия.",
        "link": "https://trudvsem.ru/professions/detail/13904", "junior_salary": 75000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 333, "name": "Облицовщик-плиточник", "industry": "Строительство/Ремонт", "university": "Строительные колледжи",
        "description": "Кладет плитку на стены и пол. Качество работы напрямую влияет на внешний вид интерьера, поэтому хорошие мастера очень ценятся.",
        "link": "https://postupi.online/professiya/plitochnik-oblicovshchik/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 334, "name": "Консьерж/Вахтер", "industry": "ЖКХ/Сервис", "university": "Не требуется",
        "description": "Следит за порядком в подъезде жилого дома или в холле организации. Спокойная работа, часто подходит для пенсионеров.",
        "link": "https://trudvsem.ru/professions/detail/13247", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 335, "name": "Водолаз", "industry": "Промышленность/Строительство/МЧС", "university": "Водолазные школы",
        "description": "Выполняет работы под водой: строит, ремонтирует, обследует объекты, участвует в спасательных операциях. Редкая, опасная и высокооплачиваемая профессия.",
        "link": "https://postupi.online/professiya/vodolaz/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 336, "name": "Контролер ОТК", "industry": "Промышленность/Производство", "university": "Технические колледжи",
        "description": "Проверяет качество готовой продукции на заводе, чтобы не допустить брака. Ответственная работа в отделе технического контроля.",
        "link": "https://postupi.online/professiya/kontroler-otk/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 337, "name": "Проводник поезда", "industry": "Транспорт/Сервис (РЖД)", "university": "Учебные центры РЖД",
        "description": "Обслуживает пассажиров в вагоне поезда дальнего следования. Работа связана с постоянными поездками по стране.",
        "link": "https://postupi.online/professiya/provodnik/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 338, "name": "Бетонщик", "industry": "Строительство", "university": "Строительные колледжи",
        "description": "Заливает бетонные конструкции на стройке. Одна из самых массовых и физически тяжелых строительных профессий.",
        "link": "https://postupi.online/professiya/betonshchik/", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 339, "name": "Стекольщик", "industry": "Строительство/Производство", "university": "Профессиональные училища",
        "description": "Режет стекло и устанавливает его в оконные рамы, двери, витрины. Работа, требующая большой аккуратности.",
        "link": "https://postupi.online/professiya/stekolshchik/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 340, "name": "Посудомойщица/Посудомойщик", "industry": "Общепит/HoReCa", "university": "Не требуется",
        "description": "Моет посуду на кухне ресторана или столовой. Стартовая позиция в сфере общественного питания.",
        "link": "https://postupi.online/professiya/mojshchik-posudy/", "junior_salary": 30000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 341, "name": "Наладчик станков с ЧПУ", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи, учебные центры",
        "description": "Настраивает станки с ЧПУ для производства деталей, пишет и корректирует программы. Высококвалифицированный рабочий, очень востребованный на производстве.",
        "link": "https://postupi.online/professiya/naladchik-stankov-s-chpu/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 342, "name": "Врач-стоматолог-терапевт", "industry": "Медицина/Стоматология", "university": "Медицинские ВУЗы (Стоматология)",
        "description": "Лечит кариес, пломбирует зубы, проводит профессиональную чистку. Самая распространенная и востребованная специализация в стоматологии.",
        "link": "https://postupi.online/professiya/stomatolog-terapevt/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 3}
    },
    {
        "id": 343, "name": "Домработница", "industry": "Сервис/Частные услуги", "university": "Не требуется, рекомендации",
        "description": "Поддерживает чистоту и порядок в частном доме или квартире. Работа в семьях, требует порядочности и трудолюбия.",
        "link": "https://postupi.online/professiya/domrabotnica/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 344, "name": "Юрисконсульт", "industry": "Юриспруденция/Бизнес", "university": "Юридические ВУЗы (МГЮА, МГУ)",
        "description": "Штатный юрист в компании, который занимается договорами, претензиями и консультирует руководство по правовым вопросам. Массовая юридическая профессия.",
        "link": "https://postupi.online/professiya/yuriskonsult/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 345, "name": "Тракторист-машинист", "industry": "Сельское хозяйство/Строительство", "university": "Аграрные и технические колледжи",
        "description": "Управляет трактором при выполнении сельскохозяйственных или строительных работ. Ключевая рабочая профессия на селе.",
        "link": "https://postupi.online/professiya/traktorist-mashinist/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 346, "name": "Врач-дерматолог", "industry": "Медицина/Красота", "university": "Медицинские ВУЗы + ординатура",
        "description": "Диагностирует и лечит заболевания кожи, волос и ногтей. Работает в поликлиниках и косметологических центрах.",
        "link": "https://postupi.online/professiya/dermatolog/", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 347, "name": "Торговый представитель", "industry": "Продажи/FMCG/Ритейл", "university": "Не требуется, тренинги",
        "description": "Представляет продукцию компании (например, продукты питания, напитки) в магазинах, договаривается о поставках и контролирует выкладку. Разъездная работа.",
        "link": "https://postupi.online/professiya/torgovyj-predstavitel/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 348, "name": "Музыкальный руководитель (в ДОУ)", "industry": "Образование/Искусство", "university": "Педагогические колледжи, консерватории, институты культуры",
        "description": "Проводит музыкальные занятия и организует утренники в детском саду. Творческая, но низкооплачиваемая работа.",
        "link": "https://postupi.online/professiya/muzykalnyj-rukovoditel/", "junior_salary": 30000, "avg_salary": 45000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 349, "name": "Арматурщик", "industry": "Строительство", "university": "Строительные колледжи",
        "description": "Вяжет каркасы из металлической арматуры для железобетонных конструкций. Важная и физически тяжелая работа на начальном этапе строительства.",
        "link": "https://postupi.online/professiya/armaturshchik/", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 350, "name": "Заведующий складом", "industry": "Логистика/Ритейл/Производство", "university": "Колледжи, ВУЗы (Логистика)",
        "description": "Руководит работой склада, организует прием, хранение и отгрузку товаров, управляет персоналом. Ответственная управленческая позиция.",
        "link": "https://postupi.online/professiya/zaveduyushchij-skladom/", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 351, "name": "Закройщик", "industry": "Легкая промышленность/Ателье", "university": "Колледжи легкой промышленности",
        "description": "Делает раскрой ткани по лекалам для последующего пошива одежды. Ответственная работа, от которой зависит качество всего изделия.",
        "link": "https://postupi.online/professiya/zakrojshchik/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 4}
    },
    {
        "id": 352, "name": "Оптометрист (специалист по подбору очков)", "industry": "Медицина/Ритейл/Сервис", "university": "Медицинские колледжи (оптика)",
        "description": "Проверяет зрение и подбирает очки и контактные линзы в салоне оптики. Медицинская специальность, востребованная в ритейле.",
        "link": "https://postupi.online/professiya/optometrist/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 353, "name": "Шахтер", "industry": "Добыча/Промышленность", "university": "Горные техникумы и ВУЗы",
        "description": "Добывает уголь и другие полезные ископаемые под землей. Одна из самых тяжелых и опасных, но и высокооплачиваемых рабочих профессий в России.",
        "link": "https://postupi.online/professiya/shahter/", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 354, "name": "Аппаратчик (химическое производство)", "industry": "Промышленность/Химия", "university": "Химико-технологические колледжи",
        "description": "Управляет химическим оборудованием на производстве, следит за ходом технологического процесса. Ответственная работа на химических заводах.",
        "link": "https://postupi.online/professiya/apparatchik/", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 355, "name": "Секретарь-референт", "industry": "Административная работа", "university": "Колледжи, курсы, ВУЗы (Документоведение)",
        "description": "Помощник руководителя, который планирует его график, организует встречи и ведет деловую переписку. Ответственная административная должность.",
        "link": "https://postupi.online/professiya/sekretar-referent/", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 356, "name": "Лифтер", "industry": "ЖКХ/Сервис", "university": "Курсы, инструктаж",
        "description": "Обслуживает лифты, следит за их исправностью, а в некоторых случаях сопровождает пассажиров. Профессия, которая постепенно исчезает.",
        "link": "https://trudvsem.ru/professions/detail/13524", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 357, "name": "Инженер-теплотехник", "industry": "Энергетика/ЖКХ/Промышленность", "university": "Энергетические ВУЗы (МЭИ)",
        "description": "Проектирует и обслуживает системы отопления, котельные и тепловые сети. Важный специалист для обеспечения теплом городов и предприятий.",
        "link": "https://postupi.online/professiya/inzhener-teplotehnik/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 358, "name": "Суши-повар (сушист)", "industry": "Общепит/HoReCa", "university": "Кулинарные курсы, обучение на месте",
        "description": "Готовит суши и роллы. Очень популярное направление в российском общепите, требующее аккуратности и скорости.",
        "link": "https://postupi.online/professiya/sushi-povar/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 4}
    },
    {
        "id": 359, "name": "Такелажник", "industry": "Промышленность/Строительство", "university": "Учебные центры",
        "description": "Перемещает очень тяжелые и крупногабаритные грузы (например, станки) с помощью специального оборудования. Редкая и высокооплачиваемая рабочая специальность.",
        "link": "https://trudvsem.ru/professions/detail/19129", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 360, "name": "Врач-невролог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Диагностирует и лечит заболевания нервной системы: от головных болей и остеохондроза до инсультов. Одна из самых востребованных врачебных специальностей.",
        "link": "https://postupi.online/professiya/nevrolog/", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 361, "name": "Водитель трамвая", "industry": "Транспорт/Госслужба", "university": "Учебно-курсовые комбинаты",
        "description": "Управляет трамваем на городских маршрутах. Стабильная работа в системе общественного транспорта, требующая высокой концентрации внимания.",
        "link": "https://trudvsem.ru/professions/detail/11190", "junior_salary": 55000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 362, "name": "Банщик", "industry": "Сервис/Здоровье", "university": "Курсы, школы банного мастерства",
        "description": "Проводит процедуры парения в русской бане. Профессия, переживающая возрождение на волне интереса к здоровому образу жизни.",
        "link": "https://trudvsem.ru/professions/detail/13702", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 363, "name": "Шлифовщик", "industry": "Промышленность/Металлообработка", "university": "Технические колледжи",
        "description": "Доводит детали до нужной чистоты и точности на шлифовальном станке. Квалифицированная рабочая профессия, требующая высокой точности.",
        "link": "https://postupi.online/professiya/shlifovshchik/", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 364, "name": "Школьный психолог", "industry": "Образование/Психология", "university": "Психологические и педагогические ВУЗы (МГУ, МПГУ)",
        "description": "Помогает ученикам справляться с трудностями в учебе и общении, проводит диагностику и консультации. Важная, но недооцененная роль в школьной системе.",
        "link": "https://postupi.online/professiya/shkolnyj-psiholog/", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 365, "name": "Работник мусоровоза", "industry": "ЖКХ", "university": "Не требуется",
        "description": "Загружает мусорные контейнеры в мусоровоз. Тяжелая и не самая престижная, но необходимая для города работа.",
        "link": "https://ru.wikipedia.org/wiki/Мусоровоз", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 366, "name": "Кальянщик", "industry": "Общепит/HoReCa/Сервис", "university": "Курсы, обучение на месте",
        "description": "Готовит и подает кальяны в ресторанах и специализированных заведениях. Популярная работа в сфере гостеприимства.",
        "link": "https://ru.wikipedia.org/wiki/Кальянщик", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 367, "name": "Врач-гинеколог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Занимается здоровьем женской репродуктивной системы, ведет беременность. Одна из ключевых врачебных специальностей.",
        "link": "https://postupi.online/professiya/ginekolog/", "junior_salary": 65000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 368, "name": "Изолировщик", "industry": "Строительство/Промышленность", "university": "Строительные колледжи",
        "description": "Наносит изоляционные материалы на трубы, стены, крыши для защиты от тепла, холода или влаги. Важная рабочая профессия в строительстве.",
        "link": "https://trudvsem.ru/professions/detail/12470", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 369, "name": "Репетитор", "industry": "Образование/Частные услуги", "university": "Педагогические и профильные ВУЗы",
        "description": "Готовит школьников к экзаменам (ЕГЭ, ОГЭ) или помогает подтянуть знания по предметам. Огромный рынок частных образовательных услуг в России.",
        "link": "https://postupi.online/professiya/repetitor/", "junior_salary": 40000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 370, "name": "Слесарь КИПиА", "industry": "Промышленность/Энергетика", "university": "Технические и политехнические колледжи",
        "description": "Обслуживает и ремонтирует контрольно-измерительные приборы и автоматику на производстве. 'Элита' рабочего класса, требующая глубоких технических знаний.",
        "link": "https://postupi.online/professiya/slesar-kipa/", "junior_salary": 70000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 371, "name": "Инспектор ДПС", "industry": "Госслужба/Право (МВД)", "university": "Учебные центры МВД, юридические ВУЗы",
        "description": "Обеспечивает безопасность дорожного движения, патрулирует дороги, оформляет ДТП. Государственная служба в структуре ГИБДД.",
        "link": "https://ru.wikipedia.org/wiki/Дорожно-патрульная_служба", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 372, "name": "Рамщик (пилорамщик)", "industry": "Деревообработка/Лесная промышленность", "university": "Лесотехнические колледжи",
        "description": "Работает на пилораме, распиливая бревна на доски и брус. Одна из основных профессий в лесоперерабатывающей отрасли.",
        "link": "https://trudvsem.ru/professions/detail/17709", "junior_salary": 50000, "avg_salary": 80000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 373, "name": "Мастер по ремонту обуви", "industry": "Сервис/Частные услуги", "university": "Колледжи, обучение у мастера",
        "description": "Ремонтирует обувь в мастерских. Спрос на услуги стабилен, хороший мастер может иметь постоянный поток клиентов.",
        "link": "https://trudvsem.ru/professions/detail/13765", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 4, 'routine': 5, 'art': 3}
    },
    {
        "id": 374, "name": "Инспектор по кадрам", "industry": "HR/Административная работа", "university": "Курсы, ВУЗы (Управление персоналом, Юриспруденция)",
        "description": "Оформляет кадровые документы, ведет трудовые книжки и личные дела сотрудников в строгом соответствии с ТК РФ.",
        "link": "https://trudvsem.ru/professions/detail/12837", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 375, "name": "Пчеловод", "industry": "Сельское хозяйство", "university": "Аграрные колледжи, курсы",
        "description": "Занимается разведением пчел и производством меда. Может быть как хобби, так и бизнесом, особенно в южных регионах России.",
        "link": "https://postupi.online/professiya/pchelovod/", "junior_salary": 40000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 376, "name": "Врач скорой помощи", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по скорой помощи",
        "description": "Оказывает экстренную медицинскую помощь на выездах. Динамичная и стрессовая работа на передовой здравоохранения.",
        "link": "https://postupi.online/professiya/vrach-skoroj-pomoshchi/", "junior_salary": 75000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 377, "name": "Пескоструйщик", "industry": "Промышленность/Строительство/Ремонт", "university": "Учебные центры",
        "description": "Очищает поверхности (металл, бетон) от ржавчины и старой краски с помощью пескоструйного аппарата. Востребован в судоремонте и строительстве.",
        "link": "https://trudvsem.ru/professions/detail/16479", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 378, "name": "Часовщик", "industry": "Сервис/Ремонт/Ритейл", "university": "Профильные колледжи, обучение у мастера",
        "description": "Ремонтирует механические и кварцевые часы. Редкая профессия, требующая огромной точности и усидчивости.",
        "link": "https://postupi.online/professiya/chasovshchik/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 3}
    },
    {
        "id": 379, "name": "Литейщик", "industry": "Промышленность/Металлургия", "university": "Металлургические колледжи",
        "description": "Заливает расплавленный металл в формы для получения деталей. Тяжелая и горячая работа на литейных производствах.",
        "link": "https://trudvsem.ru/professions/detail/13532", "junior_salary": 60000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 380, "name": "Заведующий хозяйством (Завхоз)", "industry": "Административная работа/Образование/Медицина", "university": "Не требуется специального",
        "description": "Отвечает за хозяйственное обеспечение учреждения: ремонт, закупку инвентаря, уборку. 'Мастер на все руки' в школе, больнице или офисе.",
        "link": "https://trudvsem.ru/professions/detail/12190", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 381, "name": "Машинист бульдозера", "industry": "Строительство/Добыча", "university": "Учебные центры, колледжи",
        "description": "Управляет бульдозером при строительстве дорог, разработке карьеров. Востребованная и хорошо оплачиваемая профессия оператора спецтехники.",
        "link": "https://postupi.online/professiya/mashinist-buldozera/", "junior_salary": 80000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 382, "name": "Врач-инфекционист", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Диагностирует и лечит инфекционные заболевания, от гриппа до гепатита и ВИЧ. Важность профессии особенно возросла в период пандемий.",
        "link": "https://postupi.online/professiya/infekcionist/", "junior_salary": 65000, "avg_salary": 125000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 383, "name": "Ювелир", "industry": "Производство/Ритейл/Искусство", "university": "Колледжи декоративно-прикладного искусства, курсы",
        "description": "Создает и ремонтирует украшения из драгоценных металлов и камней. Творческая профессия, требующая точности и художественного вкуса.",
        "link": "https://postupi.online/professiya/yuvelir/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 5, 'art': 5}
    },
    {
        "id": 384, "name": "Сталевар", "industry": "Промышленность/Металлургия", "university": "Металлургические техникумы и ВУЗы",
        "description": "Управляет процессом выплавки стали из чугуна. Ключевая, очень тяжелая и ответственная профессия в черной металлургии.",
        "link": "https://trudvsem.ru/professions/detail/18844", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 385, "name": "Воспитатель группы продленного дня", "industry": "Образование", "university": "Педагогические колледжи и ВУЗы",
        "description": "Присматривает за школьниками после уроков, помогает делать домашние задания, организует досуг. Работа в школе.",
        "link": "https://trudvsem.ru/professions/detail/11496", "junior_salary": 28000, "avg_salary": 40000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 3}
    },
    {
        "id": 386, "name": "Доярка/Оператор машинного доения", "industry": "Сельское хозяйство", "university": "Аграрные колледжи",
        "description": "Доит коров на молочных фермах с помощью доильных аппаратов. Одна из основных профессий в животноводстве.",
        "link": "https://trudvsem.ru/professions/detail/15860", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 387, "name": "Гардеробщик", "industry": "Сервис/Культура/Общепит", "university": "Не требуется",
        "description": "Принимает и выдает верхнюю одежду в театрах, ресторанах, поликлиниках. Работа, не требующая квалификации.",
        "link": "https://trudvsem.ru/professions/detail/11623", "junior_salary": 20000, "avg_salary": 28000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 388, "name": "Обвальщик мяса", "industry": "Производство/Ритейл", "university": "Колледжи пищевой промышленности",
        "description": "Отделяет мясо от костей на мясоперерабатывающих комбинатах или в супермаркетах. Профессия, требующая большой физической силы и сноровки.",
        "link": "https://trudvsem.ru/professions/detail/15394", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 389, "name": "Стекловар", "industry": "Промышленность/Производство", "university": "Химико-технологические колледжи",
        "description": "Управляет процессом варки стекла в печах на стекольных заводах. 'Горячая' и ответственная работа.",
        "link": "https://trudvsem.ru/professions/detail/18889", "junior_salary": 55000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 2}
    },
    {
        "id": 390, "name": "Младший воспитатель (помощник воспитателя)", "industry": "Образование", "university": "Педагогические колледжи, курсы",
        "description": "Помогает воспитателю в детском саду: кормит и одевает детей, поддерживает чистоту в группе. Часто называют 'нянечкой'.",
        "link": "https://trudvsem.ru/professions/detail/14418", "junior_salary": 25000, "avg_salary": 35000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 391, "name": "Обивщик мебели", "industry": "Производство/Сервис/Рабочие", "university": "Профессиональные училища, обучение на производстве",
        "description": "Обтягивает каркасы мягкой мебели тканью или кожей. Работает на мебельных фабриках или в мастерских по перетяжке.",
        "link": "https://trudvsem.ru/professions/detail/15403", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 392, "name": "Врач-УЗИст (специалист УЗИ)", "industry": "Медицина/Диагностика", "university": "Медицинские ВУЗы + курсы переподготовки",
        "description": "Проводит ультразвуковые исследования внутренних органов, помогая врачам ставить диагнозы. Одна из самых востребованных диагностических специальностей.",
        "link": "https://postupi.online/professiya/vrach-ultrazvukovoj-diagnostiki/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 393, "name": "Инженер-сметчик", "industry": "Строительство/Финансы", "university": "МГСУ, профильные курсы",
        "description": "Определяет стоимость строительства на основе проектной документации. Ключевой специалист, который связывает техническую и финансовую части проекта.",
        "link": "https://postupi.online/professiya/inzhener-smetchik/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 394, "name": "Чиновник / Государственный служащий", "industry": "Госслужба/Административная работа", "university": "РАНХиГС, МГУ (Гос. управление), профильные ВУЗы",
        "description": "Работает в органах государственной власти (министерствах, ведомствах), выполняя административные и управленческие функции.",
        "link": "https://postupi.online/professiya/gosudarstvennyj-sluzhashchij/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 395, "name": "Вулканизаторщик/Шиномонтажник", "industry": "Автосервис/Рабочие", "university": "Технические колледжи, курсы",
        "description": "Ремонтирует и меняет автомобильные шины. Сезонная работа с пиковыми нагрузками весной и осенью.",
        "link": "https://postupi.online/professiya/shinomontazhnik/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 396, "name": "Помощник юриста", "industry": "Юриспруденция", "university": "Юридические колледжи, студенты юрфаков",
        "description": "Помогает юристу или адвокату в подготовке документов, поиске информации. Отличный старт для карьеры в юриспруденции.",
        "link": "https://postupi.online/professiya/pomoshchnik-yurista/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 397, "name": "Рыбак (промысловик)", "industry": "Добыча/Сельское хозяйство", "university": "Морские и рыбопромышленные колледжи",
        "description": "Занимается промышленным выловом рыбы на судах в морях и океанах. Работа вахтовым методом, тяжелая и опасная.",
        "link": "https://trudvsem.ru/professions/detail/17926", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 398, "name": "Таможенный инспектор", "industry": "Госслужба/Логистика", "university": "РТА, РАНХиГС (Таможенное дело)",
        "description": "Проверяет грузы и документы на границе, обеспечивая соблюдение таможенного законодательства. Государственная служба в структуре ФТС.",
        "link": "https://postupi.online/professiya/tamozhennyj-inspektor/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 399, "name": "Стеклодув", "industry": "Производство/Искусство", "university": "Художественно-промышленные академии, колледжи",
        "description": "Создает изделия из расплавленного стекла. Редкая профессия на стыке ремесла и искусства, требующая мастерства и таланта.",
        "link": "https://postupi.online/professiya/stekloduv/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 1, 'routine': 4, 'art': 5}
    },
    {
        "id": 400, "name": "Врач-психиатр", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура по психиатрии",
        "description": "Лечит тяжелые психические расстройства. Работает в психоневрологических диспансерах и больницах. Очень сложная и ответственная врачебная специальность.",
        "link": "https://postupi.online/professiya/psihiatr/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 401, "name": "Обходчик железнодорожных путей", "industry": "Транспорт/РЖД", "university": "Железнодорожные колледжи и техникумы",
        "description": "Осматривает железнодорожные пути, выявляя неисправности для обеспечения безопасности движения поездов. Работа на открытом воздухе в любую погоду.",
        "link": "https://trudvsem.ru/professions/detail/15401", "junior_salary": 45000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 402, "name": "Оператор дробильной установки", "industry": "Добыча/Промышленность", "university": "Горные техникумы",
        "description": "Управляет оборудованием для измельчения горных пород на карьерах и обогатительных фабриках. Важная роль в добывающей промышленности.",
        "link": "https://trudvsem.ru/professions/detail/15694", "junior_salary": 65000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 403, "name": "Заточник инструментов", "industry": "Сервис/Рабочие", "university": "Профессиональные училища, курсы",
        "description": "Затачивает режущие инструменты: ножи, ножницы, пилы. Нишевая услуга, востребованная как у частных лиц, так и у организаций (например, салонов красоты).",
        "link": "https://trudvsem.ru/professions/detail/12270", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, "social": 3, "routine": 5, "art": 2}
    },
    {
        "id": 404, "name": "Учитель музыки", "industry": "Образование/Искусство", "university": "Консерватории, педагогические ВУЗы, институты культуры",
        "description": "Преподает музыку и пение в общеобразовательных или музыкальных школах. Творческая работа для тех, кто хочет делиться любовью к музыке.",
        "link": "https://postupi.online/professiya/uchitel-muzyki/", "junior_salary": 30000, "avg_salary": 50000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 4, 'art': 5}
    },
    {
        "id": 405, "name": "Сборщик урожая/Полевод", "industry": "Сельское хозяйство", "university": "Аграрные колледжи",
        "description": "Выполняет сезонные работы по сбору овощей, фруктов, ягод. Тяжелый физический труд, востребованный в аграрных регионах России.",
        "link": "https://trudvsem.ru/professions/detail/16608", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 1, 'creativity': 1, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 406, "name": "Работник химчистки", "industry": "Сервис", "university": "Колледжи, обучение на месте",
        "description": "Принимает, чистит и гладит одежду с помощью специального оборудования. Работа, требующая аккуратности и знания технологий чистки.",
        "link": "https://postupi.online/professiya/apparatchik-himchistki/", "junior_salary": 40000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 407, "name": "Дезинфектор", "industry": "Сервис/Медицина/ЖКХ", "university": "Профильные курсы, медицинские колледжи",
        "description": "Уничтожает грызунов, насекомых и болезнетворные микроорганизмы в помещениях и на открытых территориях.",
        "link": "https://postupi.online/professiya/dezinfektor/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 408, "name": "Сотрудник планетария", "industry": "Культура/Образование/Наука", "university": "Педагогические, физические, астрономические ВУЗы",
        "description": "Проводит экскурсии и читает лекции о космосе, управляет оборудованием для демонстрации звездного неба. Увлекательная работа для популяризаторов науки.",
        "link": "https://ru.wikipedia.org/wiki/Планетарий", "junior_salary": 35000, "avg_salary": 55000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 409, "name": "Мастер по изготовлению ключей", "industry": "Сервис", "university": "Обучение у мастера",
        "description": "Изготавливает дубликаты ключей в небольших мастерских. Простой и стабильный малый бизнес.",
        "link": "https://trudvsem.ru/professions/detail/12530", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 410, "name": "Врач-гастроэнтеролог", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Диагностирует и лечит заболевания желудочно-кишечного тракта. Очень востребованный специалист из-за особенностей современного питания и образа жизни.",
        "link": "https://postupi.online/professiya/gastroenterolog/", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    # --- НАЧАЛО: НОВЫЕ 30 ПРОФЕССИЙ ДЛЯ КОПИРОВАНИЯ ---
    {
        "id": 411, "name": "Пивовар", "industry": "Производство/HoReCa", "university": "МГУПП, Профильные курсы и школы (Siebel, VLB Berlin)",
        "description": "Создает пиво, разрабатывая рецептуры и контролируя все этапы производства: от выбора сырья до розлива. Востребован как на крупных заводах, так и в крафтовых пивоварнях, число которых в России растет.",
        "link": "https://postupi.online/professiya/pivovar/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 3}
    },
    {
        "id": 412, "name": "Судебный пристав", "industry": "Госслужба/Юриспруденция", "university": "ВГУЮ (РПА Минюста России), Юридические ВУЗы",
        "description": "Сотрудник Федеральной службы судебных приставов (ФССП), который обеспечивает исполнение решений судов, например, взыскание долгов. Государственная служба, требующая стрессоустойчивости.",
        "link": "https://postupi.online/professiya/sudebnyj-pristav/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 413, "name": "Сурдопереводчик", "industry": "Социальная сфера/Лингвистика", "university": "МГЛУ, РГСУ, Межрегиональный центр реабилитации лиц с проблемами слуха",
        "description": "Переводчик русского жестового языка, который помогает глухим и слабослышащим людям коммуницировать в судах, больницах, на телевидении. Социально значимая и редкая профессия.",
        "link": "https://postupi.online/professiya/surdoperevodchik/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 414, "name": "Врач-эпидемиолог", "industry": "Медицина/Госслужба", "university": "Первый МГМУ им. Сеченова (Медико-профилактический), СЗГМУ им. Мечникова",
        "description": "Изучает причины возникновения и распространения инфекционных болезней, разрабатывает меры профилактики. Работает в структурах Роспотребнадзора, больницах и научных центрах.",
        "link": "https://postupi.online/professiya/epidemiolog/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 415, "name": "Врач-аллерголог-иммунолог", "industry": "Медицина", "university": "РНИМУ им. Пирогова, Институт иммунологии ФМБА",
        "description": "Диагностирует и лечит аллергические заболевания и нарушения в работе иммунной системы. Востребованный специалист ввиду роста числа аллергиков в России.",
        "link": "https://postupi.online/professiya/allergolog-immunolog/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 416, "name": "Метролог", "industry": "Промышленность/Наука/Стандартизация", "university": "МГТУ им. Баумана, РХТУ им. Менделеева, ВНИИМ им. Менделеева",
        "description": "Специалист по единству измерений. Отвечает за точность и исправность измерительных приборов на производстве. Обязательная должность на любом высокотехнологичном предприятии.",
        "link": "https://postupi.online/professiya/metrolog/", "junior_salary": 55000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 417, "name": "Андеррайтер", "industry": "Страхование/Банки/Финансы", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Анализирует риски при принятии решения о страховании клиента или выдаче ему кредита. Ключевой аналитик в страховых компаниях и банках.",
        "link": "https://postupi.online/professiya/anderrajter/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 418, "name": "Риск-менеджер", "industry": "Финансы/Бизнес/Консалтинг", "university": "НИУ ВШЭ, Финансовый университет",
        "description": "Выявляет, оценивает и управляет потенциальными рисками (финансовыми, операционными), которые могут навредить компании. Работает в банках, корпорациях и на биржах.",
        "link": "https://postupi.online/professiya/risk-menedzher/", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 419, "name": "Food-стилист", "industry": "Медиа/Реклама/Общепит", "university": "Кулинарные школы, курсы фуд-фотографии",
        "description": "Создает 'аппетитный' вид еды для фотографий и видео в рекламе, меню, кулинарных книгах. Творческая профессия на стыке кулинарии и визуального искусства.",
        "link": "https://ru.wikipedia.org/wiki/Фуд-стилист", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 420, "name": "Саунд-дизайнер", "industry": "Кино/Геймдев/Медиа", "university": "ВГИК, СПбГИКиТ, Scream School",
        "description": "Создает и обрабатывает звуковые эффекты для фильмов, игр и приложений, формируя звуковую атмосферу. Творческая и техническая работа со звуком.",
        "link": "https://postupi.online/professiya/saund-dizajner/", "junior_salary": 60000, "avg_salary": 115000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 421, "name": "ASO-специалист", "industry": "Маркетинг/ИТ/Мобайл", "university": "Профильные онлайн-курсы",
        "description": "Оптимизирует страницы мобильных приложений в App Store и Google Play, чтобы они занимали высокие позиции в поиске и привлекали больше установок.",
        "link": "https://ru.wikipedia.org/wiki/Оптимизация_для_магазинов_приложений", "junior_salary": 65000, "avg_salary": 125000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 422, "name": "Growth Hacker (Маркетолог роста)", "industry": "Маркетинг/ИТ/Стартапы", "university": "НИУ ВШЭ, онлайн-курсы",
        "description": "Ищет нестандартные и быстрые способы для кратного роста пользовательской базы или доходов IT-продукта, постоянно тестируя гипотезы на стыке маркетинга, продукта и аналитики.",
        "link": "https://ru.wikipedia.org/wiki/Growth_Hacking", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 1}
    },
    {
        "id": 423, "name": "Тестировщик игр (Game QA)", "industry": "Геймдев/ИТ", "university": "Профильные курсы (XYZ School, Narwhal)",
        "description": "Ищет ошибки (баги) в компьютерных и мобильных играх перед их выпуском. Отличная стартовая позиция для начала карьеры в российской игровой индустрии.",
        "link": "https://synergy.ru/akademiya/karera/testirovshhik_igr_chto_eto_za_professiya_i_kak_nachat_svoj_put", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 424, "name": "Су-шеф", "industry": "Общепит/HoReCa", "university": "Кулинарные школы и колледжи, опыт работы",
        "description": "Второй человек на кухне после шеф-повара. Помогает в управлении кухней, контролирует работу поваров и качество блюд. Ключевая ступень в карьере повара.",
        "link": "https://ru.wikipedia.org/wiki/Су-шеф", "junior_salary": 70000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 4}
    },
    {
        "id": 425, "name": "Политолог", "industry": "Наука/Аналитика/Госслужба", "university": "МГУ (Политология), НИУ ВШЭ, МГИМО",
        "description": "Анализирует политические процессы в России и мире, работает в исследовательских центрах, органах власти или преподает в вузах. Экспертно-аналитическая работа.",
        "link": "https://postupi.online/professiya/politolog/", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 426, "name": "Востоковед", "industry": "Наука/Международные отношения/ВЭД", "university": "ИСАА МГУ, НИУ ВШЭ, СПбГУ (Восточный факультет)",
        "description": "Эксперт по странам Востока (Китай, арабские страны, Япония), знающий язык, культуру и экономику региона. Востребован в МИД, госкорпорациях и бизнесе, работающем с Азией.",
        "link": "https://postupi.online/professiya/vostokoved/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 427, "name": "Судебно-медицинский эксперт", "industry": "Медицина/Юриспруденция", "university": "Медицинские ВУЗы + ординатура по судмедэкспертизе",
        "description": "Проводит исследование тел умерших для установления причины смерти и помогает следствию в раскрытии преступлений. Работа в государственных бюро судмедэкспертизы.",
        "link": "https://postupi.online/professiya/sudebno-medicinskij-ekspert/", "junior_salary": 75000, "avg_salary": 125000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 428, "name": "Криминалист", "industry": "Юриспруденция/Госслужба (МВД, СК)", "university": "Университеты МВД РФ, МГЮА, юрфаки ВУЗов",
        "description": "Собирает и исследует улики на месте преступления (отпечатки пальцев, следы, ДНК), помогая следствию. Работа в экспертно-криминалистических центрах.",
        "link": "https://postupi.online/professiya/kriminalist/", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 429, "name": "Теолог", "industry": "Наука/Образование/Религия", "university": "МГУ, НИУ ВШЭ, Православный Свято-Тихоновский гуманитарный университет",
        "description": "Академический исследователь, изучающий богословие, историю и философию религии. Работает в вузах, научных институтах, может консультировать госорганы.",
        "link": "https://postupi.online/professiya/teolog/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 3}
    },
    {
        "id": 430, "name": "Керамист", "industry": "Искусство/Дизайн/Производство", "university": "МГХПА им. Строганова, 'Британка', частные школы",
        "description": "Создает изделия из глины — посуду, декор, арт-объекты. Творческая профессия с возможностью работать в мастерской, на производстве или открыть свое дело.",
        "link": "https://postupi.online/professiya/keramist/", "junior_salary": 45000, "avg_salary": 80000, "growth_rate": "Средние",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 431, "name": "Авиационный механик", "industry": "Транспорт/Авиация/Инженерия", "university": "МГТУ ГА, Самарский университет, авиационные технические колледжи",
        "description": "Обслуживает и ремонтирует самолеты и вертолеты, обеспечивая их летную годность. Крайне ответственная техническая работа в аэропортах и на авиазаводах.",
        "link": "https://postupi.online/professiya/aviatehnik/", "junior_salary": 80000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 432, "name": "Тренер по киберспорту", "industry": "Спорт/Геймдев/Образование", "university": "РГУФКСМиТ, профильные курсы",
        "description": "Готовит профессиональных киберспортсменов и команды, развивая их игровые навыки, тактику и психологическую устойчивость. Новая профессия в быстрорастущей индустрии.",
        "link": "https://postupi.online/professiya/trener-po-kibersportu/", "junior_salary": 55000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 433, "name": "Диджей (DJ)", "industry": "Развлечения/Музыка/HoReCa", "university": "Школы диджеинга (Action DJ, Umaker)",
        "description": "Подбирает и сводит музыкальные треки на мероприятиях, в клубах и барах, создавая нужную атмосферу. Творческая работа, требующая музыкального вкуса и технических навыков.",
        "link": "https://postupi.online/professiya/didzhej/", "junior_salary": 40000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 2, 'art': 5}
    },
    {
        "id": 434, "name": "Финансовый консультант", "industry": "Финансы/Консалтинг/Банки", "university": "Финансовый университет, НИУ ВШЭ",
        "description": "Помогает частным лицам управлять личными финансами: планировать бюджет, выбирать инструменты для инвестирования, достигать финансовых целей. Часто работает в банках или частным образом.",
        "link": "https://postupi.online/professiya/finansovyj-konsultant/", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 435, "name": "Актер театра и кино", "industry": "Искусство/Кино/Театр", "university": "ВГИК, ГИТИС, Школа-студия МХАТ, ВТУ им. Щепкина",
        "description": "Исполняет роли в спектаклях и фильмах, перевоплощаясь в разных персонажей. Творческая и очень конкурентная профессия, требующая таланта и упорства.",
        "link": "https://postupi.online/professiya/akter/", "junior_salary": 40000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 4, 'routine': 4, 'art': 5}
    },
    {
        "id": 436, "name": "Менеджер по внутренним коммуникациям", "industry": "HR/PR/Менеджмент", "university": "НИУ ВШЭ, МГУ (Журфак, Социология), РГГУ",
        "description": "Выстраивает коммуникацию внутри компании: информирует сотрудников о новостях, организует корпоративные мероприятия, развивает корпоративную культуру.",
        "link": "https://ru.wikipedia.org/wiki/Внутрикорпоративные_коммуникации", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 437, "name": "Методолог (в образовании и бизнесе)", "industry": "Образование/Консалтинг/ИТ", "university": "Педагогические ВУЗы, НИУ ВШЭ",
        "description": "Разрабатывает и описывает системы и методики. В EdTech — проектирует образовательные программы, в бизнесе — описывает и оптимизирует бизнес-процессы.",
        "link": "https://postupi.online/professiya/metodolog/", "junior_salary": 65000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 438, "name": "Специалист по сертификации", "industry": "Промышленность/Торговля/Госуслуги", "university": "Политехнические ВУЗы (Стандартизация и метрология)",
        "description": "Помогает компаниям получать сертификаты и декларации соответствия на их продукцию, подтверждая ее качество и безопасность согласно российским стандартам (ГОСТ).",
        "link": "https://postupi.online/professiya/specialist-po-sertifikacii/", "junior_salary": 60000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 439, "name": "Специалист по фармаконадзору", "industry": "Фармацевтика/Медицина", "university": "Медицинские и фармацевтические ВУЗы (Сеченовский, РХТУ)",
        "description": "Отслеживает и анализирует побочные эффекты лекарств, уже выпущенных на рынок, обеспечивая их безопасность. Критически важная роль в любой фармацевтической компании.",
        "link": "https://ru.wikipedia.org/wiki/Фармаконадзор", "junior_salary": 85000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 440, "name": "Медиапланер", "industry": "Маркетинг/Реклама", "university": "НИУ ВШЭ, РЭУ им. Плеханова",
        "description": "Планирует размещение рекламы в СМИ: на ТВ, радио, в интернете и наружной рекламе. Выбирает наиболее эффективные каналы для охвата целевой аудитории в рамках бюджета.",
        "link": "https://postupi.online/professiya/mediaplaner/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 441, "name": "Разработчик 1С", "industry": "ИТ/Бизнес-автоматизация", "university": "Технические ВУЗы + сертификация 1С",
        "description": "Автоматизирует бухгалтерский, управленческий и торговый учет в российских компаниях на платформе '1С:Предприятие'. Самая массовая и востребованная профессия на стыке программирования и экономики в России.",
        "link": "https://postupi.online/professiya/programmist-1s/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 442, "name": "Врач-диетолог", "industry": "Медицина/Wellness", "university": "Медицинские ВУЗы + ординатура по диетологии",
        "description": "Медицинский специалист, который разрабатывает лечебные планы питания при различных заболеваниях (ожирение, диабет, болезни ЖКТ). В отличие от нутрициолога, является врачом и работает в клиниках.",
        "link": "https://postupi.online/professiya/dietolog/", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 443, "name": "Инженер по автоматизации тестирования (QA Auto)", "industry": "ИТ", "university": "МГТУ им. Баумана, МИФИ, ИТМО",
        "description": "Пишет программы и скрипты, которые автоматически тестируют программное обеспечение, что ускоряет разработку и повышает качество. Продвинутая и высокооплачиваемая роль в QA.",
        "link": "https://education.yandex.ru/journal/chem-zanimaetsya-avtomatizator-testirovaniya-i-kak-im-stat", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 444, "name": "Менеджер по развитию бизнеса (Business Development Manager)", "industry": "Бизнес/Продажи/Менеджмент", "university": "НИУ ВШЭ, РАНХиГС",
        "description": "Ищет новые рынки, партнеров и возможности для роста компании. Работает на стыке продаж, маркетинга и стратегии, отвечая за долгосрочное развитие бизнеса.",
        "link": "https://postupi.online/professiya/menedzher-po-razvitiyu/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 445, "name": "Пентестер (Специалист по тестированию на проникновение)", "industry": "ИТ/Кибербезопасность", "university": "МИФИ, МГТУ им. Баумана (ИБ)",
        "description": "Легальный 'взломщик', который имитирует атаки хакеров на IT-системы компании, чтобы найти уязвимости до того, как их обнаружат злоумышленники. Элитное направление в кибербезопасности.",
        "link": "https://postupi.online/professiya/pentester/", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 446, "name": "Видеомонтажер (для соцсетей и блогов)", "industry": "Медиа/Маркетинг/Креатив", "university": "Онлайн-школы, курсы",
        "description": "Монтирует динамичные видео для YouTube, VK, Telegram и других платформ. Создает контент для блогеров и брендов. Огромный рынок фриланс-услуг.",
        "link": "https://postupi.online/professiya/videomontazher/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 447, "name": "Куратор выставок (Art Curator)", "industry": "Искусство/Культура", "university": "РГГУ, НИУ ВШЭ (История искусств), Школа 'Гараж'",
        "description": "Разрабатывает концепцию выставки, отбирает художников и произведения, организует пространство. Ключевая фигура в галерейном и музейном деле.",
        "link": "https://postupi.online/professiya/kurator/", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 448, "name": "Аналитик по противодействию мошенничеству (Anti-fraud)", "industry": "Финансы/Банки/ИТ", "university": "Финансовый университет, МИФИ",
        "description": "Разрабатывает и настраивает системы для выявления и предотвращения мошеннических операций (например, с банковскими картами). Работает в банках, финтехе и e-commerce.",
        "link": "https://finder.work/vacancies/3038954", "junior_salary": 85000, "avg_salary": 160000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 449, "name": "Врач-патологоанатом", "industry": "Медицина", "university": "Медицинские ВУЗы + ординатура",
        "description": "Исследует ткани и органы пациентов для постановки точного диагноза, особенно в онкологии. Вопреки стереотипам, в основном работает с живыми людьми через анализ биопсии.",
        "link": "https://postupi.online/professiya/patologoanatom/", "junior_salary": 65000, "avg_salary": 115000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 450, "name": "Лешмейкер / Бровист", "industry": "Красота/Сервис", "university": "Профильные школы и академии",
        "description": "Специалист по наращиванию ресниц и оформлению бровей. Одно из самых массовых и востребованных направлений в современной индустрии красоты в России.",
        "link": "https://postupi.online/professiya/leshmejker/", "junior_salary": 45000, "avg_salary": 90000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 5, 'art': 5}
    },
    {
        "id": 451, "name": "Игровой продюсер", "industry": "Геймдев/ИТ/Менеджмент", "university": "ВШБИ НИУ ВШЭ, Scream School",
        "description": "Руководит разработкой игры как бизнес-проекта. Отвечает за бюджет, сроки, команду и итоговый коммерческий успех. Связующее звено между разработчиками и издателем.",
        "link": "https://skillbox.ru/media/gamedev/kto-takoy-igrovoy-prodyuser/", "junior_salary": 90000, "avg_salary": 190000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 452, "name": "Мануальный терапевт", "industry": "Медицина/Wellness", "university": "Медицинский ВУЗ (неврология, травматология) + переподготовка",
        "description": "Врач, который лечит заболевания опорно-двигательного аппарата с помощью ручных техник. Очень востребованная медицинская услуга для лечения болей в спине и суставах.",
        "link": "https://postupi.online/professiya/manualnyj-terapevt/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 453, "name": "Художник-постановщик (в кино и театре)", "industry": "Кино/Театр/Искусство", "university": "ВГИК, Школа-студия МХАТ, СПбГАТИ",
        "description": "Отвечает за весь визуальный облик фильма или спектакля: создает эскизы декораций, руководит их постройкой. Ключевая творческая роль в создании мира произведения.",
        "link": "https://postupi.online/professiya/hudozhnik-postanovshchik/", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 454, "name": "Спичрайтер", "industry": "PR/Политика/Бизнес", "university": "МГУ (Журфак, Филологический), МГИМО",
        "description": "Пишет тексты публичных выступлений для политиков, топ-менеджеров и общественных деятелей. Непубличная работа, требующая мастерского владения словом и понимания психологии.",
        "link": "https://postupi.online/professiya/spichrajter/", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 4}
    },
    {
        "id": 455, "name": "Доула", "industry": "Сервис/Социальная сфера", "university": "Профильные курсы и ассоциации",
        "description": "Оказывает информационную, психологическую и бытовую поддержку женщине во время беременности, в родах и после них. Немедицинская профессия, популярность которой растет в России.",
        "link": "https://ru.wikipedia.org/wiki/Доула", "junior_salary": 40000, "avg_salary": 80000, "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 456, "name": "Кап-тестер (Q-грейдер)", "industry": "HoReCa/Ритейл/Производство", "university": "Профильные курсы и сертификация (SCA)",
        "description": "Профессиональный дегустатор кофе, который оценивает качество кофейных зерен. Работает у обжарщиков и крупных поставщиков кофе. Редкая и уважаемая профессия в кофейной индустрии.",
        "link": "https://ru.wikipedia.org/wiki/Каппинг_(дегустация_кофе)", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 3}
    },
    {
        "id": 457, "name": "Хранитель музейных фондов", "industry": "Культура/Искусство", "university": "РГГУ (Историко-архивный), ВУЗы культуры",
        "description": "Отвечает за учет, хранение и консервацию музейных экспонатов. Ключевая, но непубличная работа, обеспечивающая сохранность культурного наследия страны.",
        "link": "https://postupi.online/professiya/hranitel-muzejnyh-cennostej/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 3}
    },
    {
        "id": 458, "name": "Врач-трансплантолог", "industry": "Медицина", "university": "НМИЦ им. Шумакова, ведущие мед. ВУЗы",
        "description": "Врач-хирург, выполняющий операции по пересадке органов и тканей. Вершина хирургической карьеры, требующая высочайшей квалификации и самоотдачи.",
        "link": "https://postupi.online/professiya/transplantolog/", "junior_salary": 100000, "avg_salary": 300000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 459, "name": "Взрывник", "industry": "Добыча/Строительство", "university": "Горные ВУЗы и техникумы (МГРИ)",
        "description": "Проводит взрывные работы в карьерах, шахтах и при строительстве тоннелей для разрушения горных пород. Очень опасная, редкая и высокооплачиваемая рабочая профессия.",
        "link": "https://postupi.online/professiya/vzryvnik/", "junior_salary": 90000, "avg_salary": 170000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 460, "name": "Почвовед", "industry": "Наука/Экология/Сельское хозяйство", "university": "МГУ (Факультет почвоведения), РГАУ-МСХА",
        "description": "Изучает почвенный покров Земли. Оценивает плодородие земель для сельского хозяйства, проводит экологические экспертизы при строительстве. Работает в агрохолдингах и научных институтах.",
        "link": "https://postupi.online/professiya/pochvoved/", "junior_salary": 50000, "avg_salary": 85000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 461, "name": "Кредитный брокер", "industry": "Финансы/Консалтинг", "university": "Экономические ВУЗы, курсы",
        "description": "Посредник, который помогает физическим лицам и бизнесу получить кредит в банке на наиболее выгодных условиях. Анализирует предложения банков и готовит документы.",
        "link": "https://ru.wikipedia.org/wiki/Кредитный_брокер", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 462, "name": "Имиджмейкер", "industry": "Сервис/Консалтинг/Мода", "university": "Профильные школы, ВУЗы (PR, психология)",
        "description": "Создает и управляет персональным имиджем клиента (политика, бизнесмена, артиста), работая над его внешним видом, манерой речи и публичным поведением.",
        "link": "https://postupi.online/professiya/imidzhmejker/", "junior_salary": 55000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 463, "name": "Стример", "industry": "Медиа/Развлечения/Геймдев", "university": "Не требуется",
        "description": "Ведет прямые трансляции в интернете (например, на Twitch или VK Play), играя в игры, общаясь со зрителями или занимаясь творчеством. Доход зависит от популярности и донатов.",
        "link": "https://postupi.online/professiya/strimer/", "junior_salary": 30000, "avg_salary": 100000, "growth_rate": "Высокие",
        "score_vector": {'logic': 2, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 464, "name": "Агент по талантам (Talent Agent)", "industry": "Шоу-бизнес/Кино/Спорт", "university": "ВУЗы (Менеджмент, PR, Юриспруденция)",
        "description": "Представляет интересы актеров, музыкантов или спортсменов, ищет для них контракты и проекты. Работает в тесной связке со своим клиентом, получая процент от его гонораров.",
        "link": "https://ru.wikipedia.org/wiki/Агент_(шоу-бизнес)", "junior_salary": 70000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 465, "name": "Специалист по управлению знаниями (Knowledge Manager)", "industry": "ИТ/Консалтинг/Менеджмент", "university": "НИУ ВШЭ, РГГУ",
        "description": "Создает и поддерживает в компании систему, которая позволяет собирать, хранить и эффективно использовать знания и опыт сотрудников (например, корпоративные 'википедии', базы знаний).",
        "link": "https://ru.wikipedia.org/wiki/Управление_знаниями", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 466, "name": "Разработчик чат-ботов", "industry": "ИТ/Маркетинг/Сервис", "university": "Технические ВУЗы, онлайн-платформы",
        "description": "Проектирует и создает чат-ботов для бизнеса, которые консультируют клиентов, принимают заказы и автоматизируют общение в мессенджерах (Telegram, VK).",
        "link": "https://postupi.online/professiya/razrabotchik-chat-botov/", "junior_salary": 65000, "avg_salary": 130000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 467, "name": "Налоговый инспектор", "industry": "Госслужба/Финансы", "university": "Финансовый университет, РЭУ им. Плеханова",
        "description": "Сотрудник Федеральной налоговой службы (ФНС), который контролирует правильность уплаты налогов гражданами и организациями. Проводит проверки и консультации.",
        "link": "https://postupi.online/professiya/nalogovyj-inspektor/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 468, "name": "Орнитолог", "industry": "Наука/Экология", "university": "МГУ (Биофак), СПбГУ (Биофак)",
        "description": "Изучает птиц, их поведение, миграции и места обитания. Работает в заповедниках, научных институтах, участвует в экспедициях.",
        "link": "https://postupi.online/professiya/ornitolog/", "junior_salary": 45000, "avg_salary": 70000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 469, "name": "Хостес", "industry": "HoReCa/Общепит/Сервис", "university": "Не требуется, курсы ресторанного сервиса",
        "description": "Встречает гостей в ресторане, провожает их за столик, создает первое приятное впечатление о заведении. Стартовая позиция в ресторанном бизнесе.",
        "link": "https://postupi.online/professiya/hostes/", "junior_salary": 40000, "avg_salary": 65000, "growth_rate": "Низкие",
        "score_vector": {'logic': 2, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 470, "name": "Менеджер по e-mail маркетингу", "industry": "Маркетинг/ИТ", "university": "Онлайн-курсы, НИУ ВШЭ (Маркетинг)",
        "description": "Запускает и анализирует email-рассылки, чтобы превратить подписчиков в клиентов и удержать существующих. Специалист по прямому маркетингу в digital-среде.",
        "link": "https://postupi.online/professiya/email-marketolog/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    # --- НАЧАЛО: НОВЫЕ 30 ПРОФЕССИЙ ДЛЯ КОПИРОВАНИЯ (471-500) ---
    {
        "id": 471, "name": "Site Reliability Engineer (SRE)", "industry": "ИТ", "university": "МФТИ, МГТУ им. Баумана, ИТМО",
        "description": "Инженер по надежности сайтов, который применяет подходы из разработки ПО к задачам администрирования. Обеспечивает стабильность и производительность высоконагруженных сервисов (как в Яндексе или VK), автоматизируя рутинные задачи.",
        "link": "https://ru.wikipedia.org/wiki/Site_Reliability_Engineering", "junior_salary": 130000, "avg_salary": 260000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 472, "name": "ERP-консультант", "industry": "ИТ/Консалтинг", "university": "НИУ ВШЭ (Бизнес-информатика), РЭУ им. Плеханова",
        "description": "Внедряет и настраивает системы управления ресурсами предприятия (например, 1С:ERP, SAP) для оптимизации бизнес-процессов. Работает в IT-интеграторах и консалтинговых компаниях.",
        "link": "https://postupi.online/professiya/konsultant-erp/", "junior_salary": 80000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 473, "name": "Врач-флеболог", "industry": "Медицина", "university": "РНИМУ им. Пирогова + ординатура по сердечно-сосудистой хирургии",
        "description": "Диагностирует и лечит заболевания вен, в первую очередь — варикозное расширение вен. Востребованный узкий специалист, работающий в частных и государственных клиниках.",
        "link": "https://postupi.online/professiya/flebolog/", "junior_salary": 75000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 474, "name": "Врач-подолог", "industry": "Медицина/Сервис", "university": "Медицинские колледжи + спец. курсы (Институт Подологии)",
        "description": "Специалист по проблемам стопы: лечит вросшие ногти, мозоли, грибковые заболевания, работает с диабетической стопой. Профессия на стыке медицины и педикюра.",
        "link": "https://postupi.online/professiya/podolog/", "junior_salary": 60000, "avg_salary": 120000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 2}
    },
    {
        "id": 475, "name": "Винодел", "industry": "Сельское хозяйство/Производство", "university": "КубГАУ, МГУПП, профильные курсы",
        "description": "Создает вино, контролируя весь процесс: от выращивания винограда до розлива в бутылки. Перспективная профессия на фоне развития виноделия в южных регионах России (Краснодарский край, Крым).",
        "link": "https://postupi.online/professiya/vinodel/", "junior_salary": 65000, "avg_salary": 125000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 4}
    },
    {
        "id": 476, "name": "Литературный редактор", "industry": "Медиа/Издательское дело", "university": "МГУ (Филологический), Литературный институт им. Горького",
        "description": "Работает с текстом автора, улучшая его стиль, структуру и логику, но сохраняя авторский замысел. 'Серый кардинал' в любом издательстве, от которого зависит качество книги.",
        "link": "https://postupi.online/professiya/literaturnyj-redaktor/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 5, 'art': 4}
    },
    {
        "id": 477, "name": "Кастинг-директор", "industry": "Кино/ТВ/Реклама", "university": "ВГИК, ГИТИС, опыт работы в индустрии",
        "description": "Подбирает актеров на роли в кино, сериалах и рекламе. Проводит пробы и формирует актерский ансамбль проекта. Ключевая роль на подготовительном этапе производства.",
        "link": "https://postupi.online/professiya/kasting-direktor/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 478, "name": "Таможенный представитель (брокер)", "industry": "Логистика/ВЭД/Консалтинг", "university": "РТА, РАНХиГС",
        "description": "Посредник, который по поручению клиента (импортера или экспортера) занимается таможенным оформлением грузов. Глубоко знает законодательство и решает все вопросы с таможней.",
        "link": "https://ru.wikipedia.org/wiki/Таможенный_представитель", "junior_salary": 75000, "avg_salary": 140000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 479, "name": "Инвестиционный банкир", "industry": "Финансы/Инвестиции", "university": "РЭШ, НИУ ВШЭ (МИЭФ), МГУ (Экономфак)",
        "description": "Организует для крупных компаний сделки по слиянию и поглощению (M&A), выпуску акций (IPO) и облигаций. Работа в инвестбанках ('ВТБ Капитал', 'Sber CIB'), требующая высочайшей квалификации.",
        "link": "https://blog.sf.education/career-kto-takoj-investiczionnyj-bankir-i-kak-im-stat/", "junior_salary": 150000, "avg_salary": 400000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 480, "name": "Аукционист", "industry": "Искусство/Торговля", "university": "ВУЗы (искусствоведение), профильные курсы",
        "description": "Профессионально ведет торги на аукционах, продавая предметы искусства, антиквариат или недвижимость. Редкая профессия, требующая артистизма и отличной реакции.",
        "link": "https://postupi.online/professiya/aukcionist/", "junior_salary": 60000, "avg_salary": 125000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 481, "name": "Композитор (кино, игры)", "industry": "Искусство/Кино/Геймдев", "university": "Московская консерватория им. Чайковского, РАМ им. Гнесиных",
        "description": "Пишет оригинальную музыку для фильмов, сериалов и компьютерных игр, создавая эмоциональную атмосферу. Творческая и проектная работа.",
        "link": "https://postupi.online/professiya/kompozitor/", "junior_salary": 50000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 482, "name": "Врач-остеопат", "industry": "Медицина/Wellness", "university": "Медицинский ВУЗ + переподготовка (институты остеопатии)",
        "description": "Диагностирует и лечит нарушения в организме, рассматривая его как единую систему. Работает с помощью мягких ручных техник. Официально признанная в России врачебная специальность.",
        "link": "https://postupi.online/professiya/osteopat/", "junior_salary": 80000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 483, "name": "Музыкальный продюсер", "industry": "Музыка/Шоу-бизнес", "university": "Институты культуры, бизнес-школы (RMA)",
        "description": "Отвечает за весь процесс создания музыкального продукта, от поиска артиста и записи треков до их продвижения. Может быть как творческим, так и бизнес-партнером артиста.",
        "link": "https://ru.wikipedia.org/wiki/Музыкальный_продюсер", "junior_salary": 70000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 484, "name": "Event-декоратор", "industry": "Сервис/Дизайн", "university": "Школы дизайна и декора, курсы",
        "description": "Разрабатывает и реализует визуальное оформление мероприятий: свадеб, корпоративов, конференций. Работает с цветами, тканями, светом и мебелью, создавая атмосферу.",
        "link": "https://flatica.ru/statyi/novaya-professiya-ivent-dekorator-stsetivw-vs~158239061", "junior_salary": 50000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 485, "name": "Нарративный дизайнер", "industry": "Геймдев/Креатив", "university": "НИУ ВШЭ (Геймдизайн), Scream School",
        "description": "Проектирует историю в компьютерной игре, вплетая ее непосредственно в игровой процесс. Отвечает за то, как сюжет подается игроку через диалоги, окружение и геймплей.",
        "link": "https://postupi.online/professiya/narrativnyj-dizajner/", "junior_salary": 75000, "avg_salary": 145000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 486, "name": "Инженер-гидравлик", "industry": "Инженерия/Промышленность/Строительство", "university": "МГТУ им. Баумана, МГСУ",
        "description": "Проектирует и обслуживает гидравлические системы: от тормозов в автомобиле до гидроприводов на спецтехнике и промышленных прессах. Нишевая инженерная специальность.",
        "link": "https://postupi.online/professiya/inzhener-gidravlik/", "junior_salary": 70000, "avg_salary": 120000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 487, "name": "Agile Coach", "industry": "ИТ/Менеджмент/Консалтинг", "university": "Сертификация (ICAgile) + большой опыт в IT",
        "description": "Помогает целым компаниям или крупным отделам внедрять гибкие методологии (Agile). Работает на более высоком, стратегическом уровне, чем Scrum-мастер, меняя культуру и процессы.",
        "link": "https://ru.wikipedia.org/wiki/Agile-коучинг", "junior_salary": 150000, "avg_salary": 280000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 488, "name": "Шеф-кондитер", "industry": "HoReCa/Общепит", "university": "Кулинарные академии (Novikov School), опыт работы",
        "description": "Руководит кондитерским цехом в ресторане или отеле, разрабатывает десертное меню. Высшая ступень в карьере кондитера, требующая управленческих и творческих навыков.",
        "link": "https://ncpo.ru/blog/kak-stat-shef-konditerom/", "junior_salary": 90000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 489, "name": "Кинооператор", "industry": "Искусство/Кино/Медиа", "university": "ВГИК, СПбГИКиТ",
        "description": "Человек с камерой, который создает визуальный ряд фильма. Отвечает за композицию, свет и движение камеры, работая в тесной связке с режиссером. Ключевая творческая профессия в кино.",
        "link": "https://postupi.online/professiya/kinooperator/", "junior_salary": 60000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 490, "name": "Технический директор (CTO)", "industry": "ИТ/Менеджмент", "university": "Технические ВУЗы (МФТИ, МГУ) + большой опыт",
        "description": "Топ-менеджер, отвечающий за всю технологическую стратегию и разработку в IT-компании. Управляет командами разработчиков и принимает ключевые технические решения.",
        "link": "https://ru.wikipedia.org/wiki/Технический_директор", "junior_salary": 250000, "avg_salary": 500000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 491, "name": "Инженер по бурению", "industry": "Нефтегаз/Добыча", "university": "РГУ нефти и газа им. Губкина, УГНТУ, ТИУ",
        "description": "Проектирует и контролирует процесс строительства нефтяных и газовых скважин. Отвечает за выбор технологий, оборудования и траектории скважины. Высокооплачиваемая работа в нефтесервисе.",
        "link": "https://postupi.online/professiya/inzhener-po-bureniyu/", "junior_salary": 100000, "avg_salary": 220000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 492, "name": "Специалист по франчайзингу", "industry": "Бизнес/Продажи/Ритейл", "university": "Экономические и управленческие ВУЗы",
        "description": "Помогает компании упаковать свой бизнес во франшизу и продавать ее партнерам. Разрабатывает пакет документов, занимается поиском и обучением франчайзи.",
        "link": "https://www.rosbo.ru/blog/kak-stat-franchayzerom-s-nulya-chto-nuzhno-znat", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 493, "name": "Специалист по охране памятников (реставратор архитектуры)", "industry": "Культура/Строительство/Архитектура", "university": "МАРХИ, СПбГАСУ",
        "description": "Занимается сохранением и восстановлением объектов культурного наследия — старинных зданий и усадеб. Редкая профессия на стыке архитектуры, истории и строительства.",
        "link": "https://postupi.online/professiya/restavrator-pamyatnikov-arhitektury/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 5}
    },
    {
        "id": 494, "name": "Энтомолог", "industry": "Наука/Сельское хозяйство/Медицина", "university": "МГУ (Биофак), РГАУ-МСХА",
        "description": "Ученый, изучающий насекомых. Может заниматься защитой растений от вредителей, бороться с насекомыми-переносчиками болезней или исследовать биоразнообразие.",
        "link": "https://postupi.online/professiya/entomolog/", "junior_salary": 45000, "avg_salary": 75000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 1, 'routine': 5, 'art': 1}
    },
    {
        "id": 495, "name": "Специалист по международному праву", "industry": "Юриспруденция/Госслужба/Бизнес", "university": "МГИМО, МГЮА, НИУ ВШЭ",
        "description": "Юрист, который специализируется на отношениях между государствами и международными организациями. Работает в МИД, ООН, крупных корпорациях с зарубежными активами.",
        "link": "https://postupi.online/professiya/yurist-mezhdunarodnik/", "junior_salary": 80000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 496, "name": "Шоколатье", "industry": "HoReCa/Производство/Ритейл", "university": "Кулинарные школы (Academy of Chocolate, Barry Callebaut)",
        "description": "Мастер по изготовлению шоколада и изделий из него (конфет, фигур). Творческая и 'вкусная' профессия, востребованная на кондитерских фабриках и в бутиках.",
        "link": "https://postupi.online/professiya/shokolate/", "junior_salary": 55000, "avg_salary": 95000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 5}
    },
    {
        "id": 497, "name": "Мастер по ремонту стиральных машин", "industry": "Сервис/Рабочие", "university": "Технические колледжи, учебные центры",
        "description": "Диагностирует и устраняет неисправности в стиральных и посудомоечных машинах. Может работать в сервисном центре или как частный мастер, спрос на услуги стабильно высокий.",
        "link": "https://www.profguide.io/professions/master-po-remontu-stiralnyh-mashyn.html", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 498, "name": "Копирайтер UX-текстов (UX Writer)", "industry": "ИТ/Дизайн/Маркетинг", "university": "ВУЗы (филология, журналистика) + курсы",
        "description": "Пишет тексты для интерфейсов сайтов и приложений: названия кнопок, подсказки, сообщения об ошибках. Делает продукт понятным и дружелюбным для пользователя.",
        "link": "https://sdelaem.agency/blog/chto-takoe-ux-kopirajting-i-kak-nachat-rabotat-s-mikrotekstami/", "junior_salary": 70000, "avg_salary": 130000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 3}
    },
    {
        "id": 499, "name": "Лоббист", "industry": "Бизнес/Госуправление/Консалтинг", "university": "МГИМО, НИУ ВШЭ, РАНХиГС",
        "description": "Профессионал, который продвигает интересы определенной отрасли или крупной компании в органах государственной власти. В России эта деятельность не всегда формализована и часто является частью GR.",
        "link": "https://ru.wikipedia.org/wiki/Лоббизм", "junior_salary": 100000, "avg_salary": 250000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 500, "name": "Закупщик рекламы (Media Buyer)", "industry": "Маркетинг/Реклама/ИТ", "university": "Онлайн-курсы, ВУЗы (маркетинг, реклама)",
        "description": "Специалист, который покупает рекламные показы в различных системах (VK Реклама, Telegram Ads) с целью привлечения трафика и лидов. Часто работает с большими бюджетами в арбитраже трафика.",
        "link": "https://sky.pro/wiki/marketing/zakupshchik-reklamy-v-telegram-professiya-navyki-perspektivy/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 501, "name": "Go-разработчик (Golang)", "industry": "ИТ", "university": "МФТИ, МГУ (ВМК), ИТМО",
        "description": "Программист, который пишет высокопроизводительные и надежные серверные приложения на языке Go от Google. В России этот язык активно используется в Ozon, Avito и других высоконагруженных проектах.",
        "link": "https://habr.com/ru/articles/937760/", "junior_salary": 100000, "avg_salary": 210000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 502, "name": "Influence-менеджер", "industry": "Маркетинг/PR", "university": "НИУ ВШЭ (Коммуникации), РГГУ",
        "description": "Организует рекламные кампании у блогеров и инфлюенсеров в социальных сетях. Ищет подходящих лидеров мнений, договаривается об условиях и анализирует эффективность интеграций.",
        "link": "https://postupi.online/professiya/influence-menedzher/", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 503, "name": "Врач-ревматолог", "industry": "Медицина", "university": "НИИ ревматологии им. Насоновой, мед. ВУЗы",
        "description": "Диагностирует и лечит системные заболевания соединительной ткани и суставов, такие как ревматоидный артрит, системная красная волчанка. Узкий, но важный специалист.",
        "link": "https://postupi.online/professiya/revmatolog/", "junior_salary": 65000, "avg_salary": 135000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 504, "name": "Прокурор", "industry": "Госслужба/Юриспруденция", "university": "Университет прокуратуры РФ, МГЮА, МГУ (Юрфак)",
        "description": "Государственный обвинитель, который представляет сторону обвинения в суде по уголовным делам и надзирает за соблюдением законов. Высшая ступень в карьере юриста на госслужбе.",
        "link": "https://postupi.online/professiya/prokuror/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 505, "name": "Кузнец (художественная ковка)", "industry": "Искусство/Ремесло/Производство", "university": "МГХПА им. Строганова, колледжи ДПИ",
        "description": "Мастер, создающий из металла кованые изделия: от решеток и оград до эксклюзивной мебели и скульптур. Редкая профессия, сочетающая тяжелый физический труд и художественный талант.",
        "link": "https://postupi.online/professiya/kuznec/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 506, "name": "AML-специалист", "industry": "Финансы/Банки/Юриспруденция", "university": "МИФИ (Фин. безопасность), Финансовый университет",
        "description": "Специалист по противодействию отмыванию денег и финансированию терроризма (Anti-Money Laundering). Анализирует финансовые операции на предмет подозрительной активности. Обязательная должность в банках.",
        "link": "https://careerpath.pro/professions/spetsialist-po-finansovomu-monitoringu", "junior_salary": 85000, "avg_salary": 170000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 507, "name": "Спортивный врач", "industry": "Медицина/Спорт", "university": "Первый МГМУ им. Сеченова + ординатура по спортивной медицине",
        "description": "Отвечает за здоровье профессиональных спортсменов: проводит медосмотры, лечит травмы, контролирует допинг и восстановление. Работает в спортивных клубах, сборных и диспансерах.",
        "link": "https://postupi.online/professiya/sportivnyj-vrach/", "junior_salary": 70000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 508, "name": "Витражист", "industry": "Искусство/Дизайн/Ремесло", "university": "МГХПА им. Строганова, СПбГХПА им. Штиглица",
        "description": "Художник, который создает витражи — картины из цветного стекла. Работает над оформлением интерьеров церквей, ресторанов и частных домов. Редкая творческая профессия.",
        "link": "https://postupi.online/professiya/vitrazhist/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 509, "name": "Арт-терапевт", "industry": "Психология/Медицина/Искусство", "university": "Психологические ВУЗы + доп. образование",
        "description": "Психолог, который использует творчество (рисование, лепку, музыку) для помощи людям в решении психологических проблем и гармонизации эмоционального состояния.",
        "link": "https://postupi.online/professiya/art-terapevt/", "junior_salary": 45000, "avg_salary": 85000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 510, "name": "Release Manager", "industry": "ИТ/Менеджмент", "university": "Технические ВУЗы + опыт в разработке или QA",
        "description": "Управляет всем процессом выпуска новых версий программного обеспечения: планирует, координирует команды и контролирует развертывание. Обеспечивает, чтобы релиз прошел гладко.",
        "link": "https://ru.wikipedia.org/wiki/Управление_релизами", "junior_salary": 100000, "avg_salary": 190000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 511, "name": "Врач-гематолог", "industry": "Медицина", "university": "НМИЦ гематологии, мед. ВУЗы",
        "description": "Диагностирует и лечит заболевания крови и кроветворных органов, такие как анемия, лейкоз, лимфома. Сложная и ответственная врачебная специальность.",
        "link": "https://postupi.online/professiya/gematolog/", "junior_salary": 75000, "avg_salary": 160000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 512, "name": "Трейдер", "industry": "Финансы/Инвестиции", "university": "НИУ ВШЭ, РЭШ, Финансовый университет",
        "description": "Занимается куплей-продажей ценных бумаг, валют или других активов на бирже с целью получения прибыли. Может работать в банке, инвестфонде или на себя.",
        "link": "https://postupi.online/professiya/trejder/", "junior_salary": 100000, "avg_salary": 300000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 2, 'art': 1}
    },
    {
        "id": 513, "name": "Канистерапевт", "industry": "Социальная сфера/Медицина", "university": "Курсы и центры подготовки",
        "description": "Специалист, который использует специально обученных собак для реабилитации и абилитации людей с особенностями развития (ДЦП, аутизм). Направление пет-терапии.",
        "link": "https://ru.wikipedia.org/wiki/Канистерапия", "junior_salary": 40000, "avg_salary": 70000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 514, "name": "Менеджер по цепям поставок (Supply Chain Manager)", "industry": "Логистика/Производство/Ритейл", "university": "НИУ ВШЭ (Логистика), МАДИ",
        "description": "Управляет всем движением товара: от закупки сырья у поставщика до доставки готового продукта конечному потребителю. Оптимизирует запасы, транспорт и складские операции.",
        "link": "https://postupi.online/professiya/menedzher-po-cepyam-postavok/", "junior_salary": 90000, "avg_salary": 180000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 515, "name": "Стендап-комик", "industry": "Развлечения/Искусство", "university": "Не требуется, опыт выступлений",
        "description": "Автор и исполнитель юмористических монологов в жанре стендап. Выступает в клубах, на телевидении и YouTube. Профессия, требующая таланта, харизмы и постоянной работы над материалом.",
        "link": "https://ru.wikipedia.org/wiki/Стендап_(жанр)", "junior_salary": 35000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 516, "name": "Учитель русского языка и литературы", "industry": "Образование", "university": "Педагогические ВУЗы (МПГУ), МГУ (Филологический)",
        "description": "Преподает в школе родной язык и знакомит учеников с классической и современной литературой. Формирует грамотность и культурный код.",
        "link": "https://postupi.online/professiya/uchitel-russkogo-yazyka-i-literatury/", "junior_salary": 35000, "avg_salary": 60000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 4}
    },
    {
        "id": 517, "name": "Левел-дизайнер", "industry": "Геймдев", "university": "НИУ ВШЭ (Геймдизайн), Scream School",
        "description": "Проектирует и создает уровни в компьютерных играх: расставляет объекты, врагов, задает маршруты и события. Отвечает за то, чтобы на уровне было интересно играть.",
        "link": "https://postupi.online/professiya/level-dizajner/", "junior_salary": 70000, "avg_salary": 140000, "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 4}
    },
    {
        "id": 518, "name": "Врач-проктолог (колопроктолог)", "industry": "Медицина", "university": "НМИЦ колопроктологии им. Рыжих, мед. ВУЗы",
        "description": "Диагностирует и лечит заболевания толстой кишки, прямой кишки и заднего прохода. Деликатная, но очень востребованная хирургическая специальность.",
        "link": "https://postupi.online/professiya/proktolog/", "junior_salary": 80000, "avg_salary": 180000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 519, "name": "Полиграфолог", "industry": "Безопасность/HR/Юриспруденция", "university": "Профильные школы и курсы, ВУЗы (психология)",
        "description": "Специалист, который проводит психофизиологические исследования с использованием полиграфа ('детектора лжи'), чаще всего при приеме на работу или в ходе служебных расследований.",
        "link": "https://postupi.online/professiya/poligrafolog/", "junior_salary": 60000, "avg_salary": 110000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 520, "name": "Rust-разработчик", "industry": "ИТ/Блокчейн/Системное ПО", "university": "МФТИ, МГУ (ВМК), ИТМО",
        "description": "Программирует на языке Rust, который славится своей безопасностью и производительностью. Используется для создания системного ПО, в блокчейн-проектах и высоконагруженных системах.",
        "link": "https://ru.wikipedia.org/wiki/Rust_(язык_программирования)", "junior_salary": 110000, "avg_salary": 240000, "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 1, 'routine': 4, 'art': 1}
    },
    {
        "id": 521, "name": "Специалист по взысканию задолженности", "industry": "Финансы/Банки/Юриспруденция", "university": "Юридические и экономические колледжи, курсы",
        "description": "Ведет переговоры с должниками с целью возврата просроченной задолженности. Работает в банках, микрофинансовых организациях или коллекторских агентствах.",
        "link": "https://edwica.ru/professions/specialist-po-vzyskaniyu-4541", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 522, "name": "Гид-проводник (экстремальный туризм)", "industry": "Туризм/Спорт", "university": "Школы инструкторов, спортивные разряды",
        "description": "Организует и сопровождает туристические группы в походах, горах, на сплавах. Отвечает за безопасность и маршрут. Профессия для физически выносливых и ответственных людей.",
        "link": "https://postupi.online/professiya/instruktor-po-turizmu/", "junior_salary": 50000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 523, "name": "Астроном", "industry": "Наука", "university": "МГУ (ГАИШ), СПбГУ (Астрономическое отделение), КФУ",
        "description": "Ученый, который изучает небесные тела и Вселенную с помощью телескопов и анализа данных. Работает в обсерваториях и научно-исследовательских институтах.",
        "link": "https://postupi.online/professiya/astronom/", "junior_salary": 60000, "avg_salary": 100000, "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 524, "name": "Режиссер дубляжа", "industry": "Кино/Медиа/Искусство", "university": "ВГИК, СПбГИКиТ",
        "description": "Руководит процессом озвучивания зарубежных фильмов на русский язык. Подбирает актеров, следит за точностью перевода и попаданием в артикуляцию.",
        "link": "https://ru.wikipedia.org/wiki/Дублирование", "junior_salary": 65000, "avg_salary": 120000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 525, "name": "Генеалог", "industry": "Наука/Сервис/История", "university": "РГГУ (Историко-архивный), истфаки ВУЗов",
        "description": "Специалист по изучению родословных. Помогает людям восстановить историю своей семьи, работая с документами в государственных архивах. Растущий рынок частных услуг.",
        "link": "https://postupi.online/professiya/genealog/", "junior_salary": 50000, "avg_salary": 90000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 2}
    },
    {
        "id": 526, "name": "Печник", "industry": "Строительство/Ремесло", "university": "Профессиональные курсы, обучение у мастера",
        "description": "Мастер по кладке и ремонту печей и каминов. Редкая и востребованная профессия, особенно в загородном строительстве. Хороший печник ценится на вес золота.",
        "link": "https://postupi.online/professiya/pechnik/", "junior_salary": 60000, "avg_salary": 130000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 3}
    },
    {
        "id": 527, "name": "Спортивный комментатор", "industry": "Медиа/Спорт/Журналистика", "university": "МГУ (Журфак), профильные школы (школа комментаторов)",
        "description": "Ведет репортажи со спортивных соревнований в прямом эфире на ТВ или в интернете. Профессия, требующая глубокого знания спорта, хорошей дикции и быстрой реакции.",
        "link": "https://postupi.online/professiya/sportivnyj-kommentator/", "junior_salary": 50000, "avg_salary": 110000, "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 528, "name": "Специалист по этикету", "industry": "Консалтинг/Образование/Сервис", "university": "ВУЗы (международные отношения, лингвистика) + спец. школы",
        "description": "Консультирует по вопросам делового, светского и протокольного этикета. Обучает правилам поведения на официальных приемах, в бизнесе и обществе. Нишевая, но востребованная услуга.",
        "link": "https://arsvi.ru/news/how-to-become-a-trainer-27-09-2022.html", "junior_salary": 55000, "avg_salary": 100000, "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 3}
    },
    {
        "id": 529, "name": "Digital-стратег", "industry": "Маркетинг/Реклама/ИТ", "university": "НИУ ВШЭ, MADS, IKRA",
        "description": "Разрабатывает долгосрочную стратегию присутствия бренда в цифровой среде. Определяет, какие каналы и инструменты использовать для достижения бизнес-целей. Топ-позиция в digital-агентстве.",
        "link": "https://postupi.online/professiya/cifrovoj-strateg/", "junior_salary": 100000, "avg_salary": 200000, "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 530, "name": "Инженер-испытатель", "industry": "Промышленность/Инженерия/Авиакосмос", "university": "МАИ, МГТУ им. Баумана, технические ВУЗы",
        "description": "Проводит испытания новой техники — от автомобилей и самолетов до ракетных двигателей — чтобы проверить ее надежность, безопасность и соответствие характеристикам. Работа в КБ и на полигонах.",
        "link": "https://postupi.online/professiya/inzhener-ispytatel/", "junior_salary": 80000, "avg_salary": 150000, "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 531,
        "name": "Дата-журналист",
        "industry": "Медиа/ИТ/Аналитика",
        "university": "НИУ ВШЭ (Факультет коммуникаций, медиа и дизайна), МГУ (Журфак)",
        "description": "Специалист, который ищет истории в больших данных, анализирует их и представляет в виде понятных и увлекательных материалов: инфографики, интерактивных карт, расследований. Работает на стыке журналистики, программирования и дизайна в ведущих российских онлайн-СМИ.",
        "link": "https://postupi.online/professiya/data-zhurnalist/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 4}
    },
    {
        "id": 532,
        "name": "Агроинформатик (Агрокибернетик)",
        "industry": "Сельское хозяйство/ИТ",
        "university": "РГАУ-МСХА им. Тимирязева, КубГАУ, Ставропольский ГАУ",
        "description": "Внедряет IT-решения в сельское хозяйство: разрабатывает ПО для управления агропредприятием, настраивает системы мониторинга полей с помощью датчиков и дронов, анализирует данные для повышения урожайности. Ключевой специалист по цифровизации АПК.",
        "link": "https://postupi.online/professiya/agroinformatik/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 3, 'art': 1}
    },
    {
        "id": 533,
        "name": "Специалист по городской мобильности",
        "industry": "Транспорт/Госуправление/Консалтинг",
        "university": "МАДИ, НИУ ВШЭ (Высшая школа урбанистики)",
        "description": "Планирует и проектирует транспортные системы городов, делая их удобными, безопасными и экологичными. Анализирует пассажиропотоки, развивает общественный транспорт, велосипедную и пешеходную инфраструктуру.",
        "link": "https://sky.pro/wiki/profession/kakie-eshe-est-professii-polnyj-obzor-aktualnyh-specialnostej/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 3, 'art': 2}
    },
    {
        "id": 534,
        "name": "Инженер по солнечной энергетике",
        "industry": "Энергетика/Экология/Строительство",
        "university": "МЭИ, Сколтех, СПбПУ",
        "description": "Проектирует, устанавливает и обслуживает солнечные электростанции для промышленных предприятий и частных домов. Перспективная 'зеленая' профессия на фоне роста интереса к возобновляемой энергии в России.",
        "link": "https://postupi.online/professiya/specialist-po-vozobnovlyaemoj-energetike/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 535,
        "name": "Специалист по переработке вторсырья",
        "industry": "Экология/Промышленность",
        "university": "РХТУ им. Менделеева, РУДН (Экологический факультет)",
        "description": "Разрабатывает и контролирует технологические процессы по переработке отходов (пластика, стекла, бумаги) во вторичное сырье. Работает на мусоросортировочных комплексах и перерабатывающих заводах.",
        "link": "https://postupi.online/professiya/recikling-tehnolog/",
        "junior_salary": 60000,
        "avg_salary": 100000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 536,
        "name": "Аналитик цепей поставок",
        "industry": "Логистика/Ритейл/Аналитика",
        "university": "НИУ ВШЭ (Логистика и управление цепями поставок), Финансовый университет",
        "description": "Анализирует данные о движении товаров, чтобы оптимизировать логистические процессы, сократить издержки и ускорить доставку. Работает в крупных торговых и производственных компаниях.",
        "link": "https://postupi.online/professiya/menedzher-po-cepyam-postavok/",
        "junior_salary": 85000,
        "avg_salary": 160000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 537,
        "name": "Юрист по цифровому праву",
        "industry": "Юриспруденция/ИТ",
        "university": "НИУ ВШЭ (Факультет права), МГЮА, Сколково",
        "description": "Специализируется на правовом регулировании интернета, персональных данных, электронной коммерции, криптовалют и искусственного интеллекта. Сопровождает деятельность IT-компаний и стартапов.",
        "link": "https://postupi.online/professiya/cifrovoj-yurist/",
        "junior_salary": 80000,
        "avg_salary": 170000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 538,
        "name": "IT-рекрутер",
        "industry": "HR/ИТ",
        "university": "Онлайн-школы (Otus, Hedu), опыт в HR или IT",
        "description": "Специализируется на поиске и подборе IT-специалистов: от разработчиков до ML-инженеров. Глубоко понимает технологии, чтобы говорить с кандидатами на одном языке. Одна из самых востребованных и высокооплачиваемых ролей в HR.",
        "link": "https://postupi.online/professiya/it-rekruter/",
        "junior_salary": 75000,
        "avg_salary": 150000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 539,
        "name": "Нейропсихолог",
        "industry": "Психология/Медицина/Образование",
        "university": "МГУ (Психфак), НИУ ВШЭ",
        "description": "Диагностирует и корректирует нарушения высших психических функций (память, внимание, мышление) у детей и взрослых, связанные с работой мозга. Работает в медицинских и развивающих центрах.",
        "link": "https://postupi.online/professiya/nejropsiholog/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 540,
        "name": "Специалист по мультимодальным перевозкам",
        "industry": "Транспорт/Логистика",
        "university": "МАДИ, РУТ (МИИТ)",
        "description": "Организует перевозку грузов с использованием нескольких видов транспорта (например, море + ж/д + авто). Разрабатывает оптимальные маршруты и координирует всех участников процесса. ",
        "link": "https://glonass-std.ru/stati/kak-stat-logistom-multimodalnyh-perevozok-s-nulya/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 541,
        "name": "Менеджер по адаптации персонала (Onboarding Manager)",
        "industry": "HR/Управление персоналом",
        "university": "НИУ ВШЭ (Управление человеческими ресурсами), РГГУ",
        "description": "Разрабатывает и проводит программы для новых сотрудников, чтобы помочь им быстрее влиться в коллектив, понять свои задачи и начать эффективно работать. Снижает текучесть кадров на испытательном сроке.",
        "link": "https://www.rabota.ru/articles/career/onbording-spetsialist-chem-zanimaetsya-i-kak-im-stat-10499/",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 542,
        "name": "Аналитик углеродного рынка",
        "industry": "Экология/Финансы/Консалтинг",
        "university": "МГУ (Экономфак), НИУ ВШЭ, РЭУ им. Плеханова",
        "description": "Анализирует рынок углеродных единиц, помогает компаниям реализовывать климатические проекты и управлять своим углеродным следом в рамках российского и международного регулирования.",
        "link": "https://edwica.ru/professions/specialist-po-uglerodnomu-rynku-17044",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 543,
        "name": "Специалист по работе с отзывами (ORM-менеджер)",
        "industry": "Маркетинг/PR",
        "university": "НИУ ВШЭ (Реклама и связи с общественностью), онлайн-курсы",
        "description": "Управляет репутацией бренда в интернете (Online Reputation Management). Отслеживает упоминания компании на сайтах-отзовиках, в соцсетях и на форумах, отвечает на негатив и стимулирует позитивные отзывы.",
        "link": "https://postupi.online/professiya/orm-menedzher/",
        "junior_salary": 55000,
        "avg_salary": 95000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 544,
        "name": "Вертикальный фермер",
        "industry": "Сельское хозяйство/Технологии",
        "university": "РГАУ-МСХА им. Тимирязева, онлайн-платформы",
        "description": "Выращивает зелень, овощи и ягоды в закрытых помещениях на многоярусных установках (сити-фермах) с использованием гидропоники и искусственного освещения. Новое направление в городском сельском хозяйстве.",
        "link": "https://postupi.online/professiya/siti-fermer/",
        "junior_salary": 60000,
        "avg_salary": 100000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 545,
        "name": "3D-биопринтинг инженер",
        "industry": "Медицина/Биотехнологии/Наука",
        "university": "Первый МГМУ им. Сеченова, Сколтех, МИСиС",
        "description": "Специалист, который 'печатает' живые ткани и органы на 3D-биопринтере, используя клетки пациента. Футуристическая профессия на передовой регенеративной медицины в России.",
        "link": "https://postupi.online/professiya/inzhener-tkanevoj-inzhenerii/",
        "junior_salary": 100000,
        "avg_salary": 200000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 546,
        "name": "Менеджер по маркетплейс-маркетингу",
        "industry": "Маркетинг/E-commerce",
        "university": "НИУ ВШЭ (Маркетинг), профильные курсы (Marketplace Guru)",
        "description": "Специализируется на продвижении товаров внутри маркетплейсов (Ozon, Wildberries). Настраивает внутреннюю рекламу, работает с отзывами и вопросами, анализирует продажи для вывода карточек в ТОП.",
        "link": "https://practicum.yandex.ru/blog/professiya-menedzher-marketpleysov/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 547,
        "name": "Цифровой следователь (форензик-специалист)",
        "industry": "ИТ/Безопасность/Юриспруденция",
        "university": "МИФИ, МГТУ им. Баумана, Университеты МВД РФ",
        "description": "Специалист по компьютерной криминалистике. Расследует киберинциденты, восстанавливает удаленные данные с цифровых носителей и собирает доказательства для суда. Работает в правоохранительных органах и консалтинге.",
        "link": "https://postupi.online/professiya/kibersledovatel/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 548,
        "name": "Финтех-аналитик",
        "industry": "Финансы/ИТ/Аналитика",
        "university": "НИУ ВШЭ (МИЭФ), МФТИ, Финансовый университет",
        "description": "Анализирует и проектирует финансовые технологии и продукты на стыке банковского дела и IT. Работает в банках (Сбер, Тинькофф) и финтех-стартапах над созданием новых цифровых сервисов.",
        "link": "https://postupi.online/professiya/finansovyj-inzhener/",
        "junior_salary": 100000,
        "avg_salary": 190000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 3, 'art': 1}
    },
    {
        "id": 549,
        "name": "Специалист по работе с нейросетями",
        "industry": "ИТ/Дизайн/Медиа",
        "university": "Онлайн-курсы, технические ВУЗы",
        "description": "Профессионально использует генеративные нейросети (YandexGPT, Kandinsky, Midjourney) для создания текстов, изображений и другого контента. Объединяет творческие задачи с техническими навыками промпт-инжиниринга.",
        "link": "https://ru.wikipedia.org/wiki/Инженерия_подсказок",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 5}
    },
    {
        "id": 550,
        "name": "Облачный инженер (Cloud Engineer)",
        "industry": "ИТ",
        "university": "Технические ВУЗы + сертификации Yandex.Cloud",
        "description": "Администрирует и развивает IT-инфраструктуру компании в облачных сервисах. Настраивает виртуальные серверы, базы данных и сети, обеспечивая их надежность и масштабируемость. Одна из самых востребованных ролей в современном IT.",
        "link": "https://postupi.online/professiya/cloud-inzhener/",
        "junior_salary": 120000,
        "avg_salary": 230000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 551,
        "name": "Инженер по альтернативной энергетике",
        "industry": "Энергетика/Экология",
        "university": "МЭИ, Сколтех, СПбПУ",
        "description": "Разрабатывает и внедряет решения в области возобновляемых источников энергии, включая ветровую, геотермальную и водородную энергетику. Работает в научно-исследовательских институтах и инновационных компаниях.",
        "link": "https://postupi.online/professiya/inzhener-po-alternativnoj-energetike/",
        "junior_salary": 85000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 552,
        "name": "Клинический биоинформатик",
        "industry": "Медицина/Наука/ИТ",
        "university": "МГУ (Факультет биоинженерии и биоинформатики), РНИМУ им. Пирогова",
        "description": "Анализирует генетические данные пациентов для диагностики наследственных заболеваний, подбора персональной терапии и оценки рисков. Работает в медико-генетических центрах и лабораториях.",
        "link": "https://postupi.online/professiya/bioinformatik/",
        "junior_salary": 90000,
        "avg_salary": 170000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 553,
        "name": "Дизайнер образовательного опыта (LX Designer)",
        "industry": "Образование/EdTech/Дизайн",
        "university": "НИУ ВШЭ (Институт образования), онлайн-курсы",
        "description": "Проектирует образовательный процесс так, чтобы он был максимально увлекательным, понятным и эффективным для студента. Применяет принципы UX-дизайна к созданию онлайн-курсов и учебных программ.",
        "link": "https://postupi.online/professiya/pedagogicheskij-dizajner/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 3}
    },
    {
        "id": 554,
        "name": "Специалист по исламскому банкингу",
        "industry": "Финансы/Банки",
        "university": "МГИМО, СПбГУ (Восточный факультет), Финансовый университет",
        "description": "Консультирует и сопровождает финансовые операции в соответствии с нормами шариата (без ссудного процента, запрет на спекуляции). Востребован в банках, развивающих партнерский банкинг в России.",
        "link": "https://ru.wikipedia.org/wiki/Исламский_банкинг",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 555,
        "name": "Менеджер по устойчивому развитию (ESG-менеджер)",
        "industry": "Консалтинг/Менеджмент/Экология",
        "university": "МГИМО, РАНХиГС, НИУ ВШЭ",
        "description": "Разрабатывает и внедряет в компании стратегию устойчивого развития (Environmental, Social, Governance). Отвечает за снижение экологического следа, социальные проекты и прозрачность управления. Работает в крупных российских корпорациях.",
        "link": "https://postupi.online/professiya/specialist-po-ustojchivomu-razvitiyu/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 556,
        "name": "Биофармаколог",
        "industry": "Наука/Фармацевтика/Биотехнологии",
        "university": "МГУ (Биофак), РХТУ им. Менделеева",
        "description": "Разрабатывает лекарственные препараты нового поколения на основе биологических молекул (антитела, белки, генные конструкции). Работает в R&D-центрах ведущих фармацевтических компаний.",
        "link": "https://postupi.online/professiya/farmakolog/",
        "junior_salary": 85000,
        "avg_salary": 170000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 557,
        "name": "Цифровой антрополог",
        "industry": "Наука/Маркетинг/ИТ",
        "university": "НИУ ВШЭ (Социология), МГУ (Исторический факультет)",
        "description": "Изучает поведение людей в цифровой среде: как формируются онлайн-сообщества, как технологии меняют культуру и общение. Работает в исследовательских агентствах и IT-компаниях для лучшего понимания пользователей.",
        "link": "https://postupi.online/professiya/cifrovoj-antropolog/",
        "junior_salary": 65000,
        "avg_salary": 120000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 558,
        "name": "Инженер по композитным материалам",
        "industry": "Промышленность/Авиакосмос/Инженерия",
        "university": "МГТУ им. Баумана, МАИ, МИСиС",
        "description": "Разрабатывает и применяет композитные материалы (например, углепластик) для создания легких и прочных конструкций в авиастроении, автоспорте и других высокотехнологичных отраслях.",
        "link": "https://postupi.online/professiya/inzhener-po-kompozitnym-materialam/",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 559,
        "name": "Тренд-вотчер",
        "industry": "Маркетинг/Консалтинг/Дизайн",
        "university": "НИУ ВШЭ, Британская высшая школа дизайна",
        "description": "Профессиональный 'охотник за трендами'. Отслеживает и анализирует новые тенденции в обществе, технологиях и культуре, чтобы помочь компаниям создавать востребованные продукты и услуги. Работает в брендинговых и консалтинговых агентствах.",
        "link": "https://proforientator.ru/publications/articles/professiya-trendvotcher.html",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 4}
    },
    {
        "id": 560,
        "name": "Архитектор медицинского оборудования",
        "industry": "Медицина/Инженерия/ИТ",
        "university": "МГТУ им. Баумана (Биомедицинская техника), МИФИ",
        "description": "Проектирует и разрабатывает сложное медицинское оборудование: от томографов и аппаратов УЗИ до роботизированных хирургических комплексов. Работает в R&D-центрах производителей медтехники.",
        "link": "https://postupi.online/professiya/inzhener-medtehniki/",
        "junior_salary": 95000,
        "avg_salary": 190000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 561,
        "name": "Специалист по Legal Tech",
        "industry": "Юриспруденция/ИТ",
        "university": "НИУ ВШЭ, МГЮА, Сколково",
        "description": "Внедряет IT-решения (конструкторы документов, системы анализа судебной практики) в работу юристов для автоматизации рутинных задач и повышения эффективности. Работает в юридических фирмах и LegalTech-стартапах.",
        "link": "https://ru.wikipedia.org/wiki/LegalTech",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 3, 'art': 1}
    },
    {
        "id": 562,
        "name": "Партизанский маркетолог",
        "industry": "Маркетинг/Реклама",
        "university": "Онлайн-школы, ВУЗы (маркетинг)",
        "description": "Придумывает и реализует малобюджетные, но креативные и запоминающиеся рекламные акции, которые часто становятся вирусными. Специалист по нестандартному продвижению для стартапов и малого бизнеса.",
        "link": "https://ru.wikipedia.org/wiki/Партизанский_маркетинг",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 563,
        "name": "Проектировщик промышленных роботов",
        "industry": "Инженерия/Промышленность/ИТ",
        "university": "Университет Иннополис, ИТМО, МГТУ СТАНКИН",
        "description": "Разрабатывает роботизированные ячейки и линии для автоматизации производственных процессов на заводах. Подбирает роботов, проектирует оснастку и пишет управляющие программы.",
        "link": "https://postupi.online/professiya/robototehnik/",
        "junior_salary": 90000,
        "avg_salary": 170000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 2}
    },
    {
        "id": 564,
        "name": "Специалист по адаптивному спорту",
        "industry": "Спорт/Медицина/Образование",
        "university": "РГУФКСМиТ, НГУ им. Лесгафта",
        "description": "Тренер или инструктор, который проводит занятия по физической культуре и спорту для людей с ограниченными возможностями здоровья, помогая им в реабилитации и социализации. Работает в реабилитационных центрах и спортивных школах.",
        "link": "https://postupi.online/professiya/trener-po-adaptivnoj-fizkulture/",
        "junior_salary": 45000,
        "avg_salary": 80000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 565,
        "name": "Chief of Staff (Руководитель аппарата)",
        "industry": "Менеджмент/Бизнес",
        "university": "Ведущие ВУЗы (ВШЭ, МГУ, МГИМО) + опыт в консалтинге или управлении",
        "description": "'Правая рука' и стратегический партнер CEO в крупной компании. Помогает в принятии решений, управляет ключевыми проектами и оптимизирует работу топ-менеджмента. Редкая и влиятельная позиция.",
        "link": "https://ru.wikipedia.org/wiki/Руководитель_аппарата",
        "junior_salary": 200000,
        "avg_salary": 400000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 566,
        "name": "Инженер-атомщик (проектировщик АЭС)",
        "industry": "Энергетика/Промышленность/Инженерия",
        "university": "НИЯУ МИФИ, СПбПУ Петра Великого",
        "description": "Разрабатывает и проектирует ядерные реакторы и другое оборудование для атомных электростанций. Критически важный специалист для госкорпорации 'Росатом', работающий над проектами в России и за рубежом.",
        "link": "https://postupi.online/professiya/inzhener-atomshchik/",
        "junior_salary": 100000,
        "avg_salary": 200000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 567,
        "name": "Управляющий коммерческой недвижимостью",
        "industry": "Недвижимость/Менеджмент",
        "university": "ГУУ, РАНХиГС",
        "description": "Отвечает за эксплуатацию и получение прибыли от торговых центров, офисных зданий или складов. Ищет арендаторов, управляет техническими службами и бюджетом объекта.",
        "link": "https://postupi.online/professiya/menedzher-po-kommercheskoj-nedvizhimosti/",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 568,
        "name": "Спортивный аналитик (Data Scientist in sport)",
        "industry": "Спорт/Аналитика/ИТ",
        "university": "НИУ ВШЭ, МФТИ + спортивные ВУЗы",
        "description": "Анализирует большие данные (статистику матчей, данные с датчиков) для улучшения результатов спортсменов и команд. Работает в профессиональных клубах (футбол, хоккей) и букмекерских компаниях.",
        "link": "https://postupi.online/professiya/sportivnyj-analitik/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 569,
        "name": "Технолог по переработке сельхозпродукции",
        "industry": "Сельское хозяйство/Промышленность",
        "university": "МГУПП, КубГТУ",
        "description": "Разрабатывает и контролирует технологии переработки зерна, молока, мяса и овощей в готовые продукты питания. Ключевой специалист на пищевых комбинатах и агрохолдингах.",
        "link": "https://postupi.online/professiya/tehnolog-po-pererabotke-selhozprodukcii/",
        "junior_salary": 60000,
        "avg_salary": 100000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 570,
        "name": "Инженер по обогащению полезных ископаемых",
        "industry": "Добыча/Промышленность",
        "university": "НИТУ 'МИСиС', Санкт-Петербургский горный университет",
        "description": "Разрабатывает и управляет процессами отделения ценных минералов от пустой породы на обогатительных фабриках. Важнейший специалист в металлургии и горнодобывающей отрасли.",
        "link": "https://postupi.online/professiya/obogatitel-poleznyh-iskopaemyh/",
        "junior_salary": 85000,
        "avg_salary": 160000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 571,
        "name": "Специалист по антикризисным коммуникациям",
        "industry": "Коммуникации/PR/Менеджмент",
        "university": "МГИМО, НИУ ВШЭ",
        "description": "Разрабатывает и реализует коммуникационную стратегию компании в период кризиса (аварии, скандалы, санкции). Готовит заявления для СМИ и управляет репутационными рисками.",
        "link": "https://ru.wikipedia.org/wiki/Антикризисное_управление",
        "junior_salary": 90000,
        "avg_salary": 190000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 572,
        "name": "Банкетный менеджер",
        "industry": "HoReCa/Сервис",
        "university": "РГУТиС, ВУЗы гостиничного дела",
        "description": "Организует 'под ключ' банкеты, свадьбы, фуршеты и конференции в отелях и ресторанах. Отвечает за продажи, координацию всех служб и удовлетворенность клиента.",
        "link": "https://postupi.online/professiya/banketnyj-menedzher/",
        "junior_salary": 65000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 573,
        "name": "Художник по свету (светодизайнер)",
        "industry": "Искусство/Театр/Дизайн",
        "university": "Школа-студия МХАТ, СПбГАТИ, школы дизайна",
        "description": "Создает световую партитуру для спектаклей, концертов, архитектурных объектов и выставок. С помощью света управляет вниманием зрителя и создает нужную атмосферу.",
        "link": "https://postupi.online/professiya/hudozhnik-po-svetu/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 574,
        "name": "Инженер по промышленной безопасности",
        "industry": "Промышленность/Безопасность",
        "university": "РГУ нефти и газа им. Губкина, технические ВУЗы",
        "description": "Отвечает за предотвращение аварий на опасных производственных объектах (заводы, нефтепроводы). Контролирует соблюдение норм и проходит проверки Ростехнадзора. Обязательная должность на любом крупном производстве.",
        "link": "https://postupi.online/professiya/inzhener-po-promyshlennoj-bezopasnosti/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 575,
        "name": "Спортивный юрист",
        "industry": "Юриспруденция/Спорт",
        "university": "МГЮА, НИУ ВШЭ (совместно с ФИФА)",
        "description": "Сопровождает трансферы спортсменов, разрешает допинговые и контрактные споры, представляет интересы клубов и федераций в спортивных арбитражных судах. Элитная и узкая юридическая специализация.",
        "link": "https://postupi.online/professiya/sportivnyj-yurist/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 576,
        "name": "Эко-аудитор",
        "industry": "Экология/Консалтинг",
        "university": "РУДН (Экологический факультет), МГУ",
        "description": "Проводит независимую проверку деятельности компании на предмет ее соответствия экологическому законодательству и стандартам. Помогает бизнесу снижать негативное воздействие на природу и избегать штрафов.",
        "link": "https://vuzopedia.ru/professii/2005",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 577,
        "name": "Категорийный менеджер",
        "industry": "Ритейл/Продажи/Маркетинг",
        "university": "РЭУ им. Плеханова, НИУ ВШЭ",
        "description": "Управляет определенной категорией товаров в торговой сети (например, 'молочные продукты' или 'бытовая химия'). Отвечает за ассортимент, ценообразование, закупки и прибыльность своей категории.",
        "link": "https://postupi.online/professiya/kategorijnyj-menedzher/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 3, 'art': 1}
    },
    {
        "id": 578,
        "name": "Популяризатор науки (Science Communicator)",
        "industry": "Наука/Медиа/Образование",
        "university": "Университет ИТМО (Научная коммуникация), МГУ",
        "description": "Рассказывает о сложных научных открытиях простым и увлекательным языком. Ведет блоги, пишет книги, выступает с лекциями, работает в научных музеях и СМИ, делая науку доступной для всех.",
        "link": "https://postupi.online/professiya/nauchnyj-kommunikator/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 3}
    },
    {
        "id": 579,
        "name": "Телохранитель (Личный охранник)",
        "industry": "Безопасность",
        "university": "Школы телохранителей, опыт службы в спецподразделениях",
        "description": "Обеспечивает физическую безопасность клиента (бизнесмена, политика, звезды). Профессия, требующая отличной физической подготовки, навыков владения оружием и аналитического склада ума.",
        "link": "https://postupi.online/professiya/telohranitel/",
        "junior_salary": 90000,
        "avg_salary": 200000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 580,
        "name": "Дизайнер навигации (Wayfinding Designer)",
        "industry": "Дизайн/Архитектура",
        "university": "НИУ ВШЭ (Дизайн), МГХПА им. Строганова",
        "description": "Разрабатывает системы указателей и знаков для сложных пространств: аэропортов, вокзалов, торговых центров, парков. Помогает людям легко ориентироваться и находить путь.",
        "link": "https://ru.wikipedia.org/wiki/Навигационный_дизайн",
        "junior_salary": 65000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 4}
    },
    {
        "id": 581,
        "name": "Операционный директор (COO)",
        "industry": "Менеджмент/Бизнес",
        "university": "Ведущие ВУЗы + MBA (Сколково, ВШБ НИУ ВШЭ)",
        "description": "Второй человек в компании после генерального директора (CEO), который отвечает за всю операционную деятельность: производство, логистику, персонал. Налаживает и контролирует все внутренние бизнес-процессы.",
        "link": "https://ru.wikipedia.org/wiki/Операционный_директор",
        "junior_salary": 200000,
        "avg_salary": 500000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 582,
        "name": "Специалист по аквакультуре (Рыбовод)",
        "industry": "Сельское хозяйство/Промышленность",
        "university": "Астраханский ГТУ, Калининградский ГТУ",
        "description": "Занимается искусственным разведением рыбы (осетра, форели, лосося) и других водных организмов на специализированных фермах. Перспективное направление на фоне импортозамещения.",
        "link": "https://postupi.online/professiya/rybovod/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 583,
        "name": "Музейный педагог",
        "industry": "Образование/Культура/Искусство",
        "university": "РГГУ, МПГУ, институты культуры",
        "description": "Разрабатывает и проводит интерактивные занятия, квесты и мастер-классы для детей и взрослых в музеях, делая посещение выставки увлекательным образовательным опытом.",
        "link": "https://postupi.online/professiya/muzejnyj-pedagog/",
        "junior_salary": 40000,
        "avg_salary": 65000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 4}
    },
    {
        "id": 584,
        "name": "Геофизик",
        "industry": "Добыча/Наука/Геология",
        "university": "МГУ (Геологический), РГУ нефти и газа им. Губкина",
        "description": "Изучает строение Земли с помощью физических методов (сейсморазведка, гравиразведка) для поиска месторождений нефти, газа и других полезных ископаемых. Работает в 'поле' и в аналитических центрах.",
        "link": "https://postupi.online/professiya/geofizik/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 585,
        "name": "Инженер технического надзора (стройконтроль)",
        "industry": "Строительство",
        "university": "МГСУ, СПбГАСУ",
        "description": "Представляет интересы заказчика на стройке, контролируя качество работ, материалов и соблюдение проектных решений со стороны подрядчика. Обеспечивает, чтобы объект был построен без брака.",
        "link": "https://postupi.online/professiya/inzhener-tehnicheskogo-nadzora/",
        "junior_salary": 90000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 586,
        "name": "Семейный психолог",
        "industry": "Психология/Консалтинг/Сервис",
        "university": "МГУ (Психфак), НИУ ВШЭ (Психология)",
        "description": "Помогает парам и семьям разрешать конфликты, преодолевать кризисы в отношениях и выстраивать гармоничную коммуникацию. Ведет частную практику или работает в психологических центрах.",
        "link": "https://postupi.online/professiya/semejnyj-psiholog/",
        "junior_salary": 50000,
        "avg_salary": 100000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 587,
        "name": "F&B-менеджер (Food and Beverage Manager)",
        "industry": "HoReCa/Менеджмент",
        "university": "Российский международный олимпийский университет, бизнес-школы",
        "description": "Руководитель службы питания в крупном отеле или ресторанной сети. Отвечает за работу всех ресторанов, баров и рум-сервиса, контролирует закупки, бюджет и качество.",
        "link": "https://ru.wikipedia.org/wiki/F&B-менеджер",
        "junior_salary": 85000,
        "avg_salary": 170000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 588,
        "name": "Медиа-аналитик",
        "industry": "Коммуникации/PR/Маркетинг",
        "university": "НИУ ВШЭ (Социология), МГУ (Журфак)",
        "description": "Анализирует информационное поле вокруг бренда, персоны или события. Оценивает тональность публикаций в СМИ и соцсетях, эффективность PR-кампаний и составляет аналитические отчеты. Работает в PR-агентствах и крупных компаниях.",
        "link": "https://postupi.online/professiya/media-analitik/",
        "junior_salary": 65000,
        "avg_salary": 120000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 589,
        "name": "Аудитор энергоэффективности (Энергоаудитор)",
        "industry": "Энергетика/Экология/Консалтинг",
        "university": "МЭИ, технические ВУЗы",
        "description": "Проводит обследование зданий и промышленных предприятий, чтобы найти источники потерь энергии и разработать план по их сокращению. Помогает компаниям экономить на коммунальных платежах и снижать вред для экологии.",
        "link": "https://postupi.online/professiya/energoauditor/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 590,
        "name": "Менеджер девелоперских проектов",
        "industry": "Недвижимость/Строительство/Менеджмент",
        "university": "МГСУ, НИУ ВШЭ (Управление недвижимостью)",
        "description": "Управляет всем циклом создания объекта недвижимости: от покупки земельного участка и разработки концепции до строительства и продажи. Координирует архитекторов, строителей и маркетологов. ",
        "link": "https://postupi.online/professiya/menedzher-developerskih-proektov/",
        "junior_salary": 120000,
        "avg_salary": 250000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 591,
        "name": "Спортивный агент",
        "industry": "Спорт/Менеджмент/Юриспруденция",
        "university": "РГУФКСМиТ, юридические и экономические ВУЗы",
        "description": "Представляет интересы профессионального спортсмена. Ведет переговоры о контрактах с клубами и спонсорами, решает юридические и финансовые вопросы, строит карьеру своего клиента.",
        "link": "https://postupi.online/professiya/sportivnyj-agent/",
        "junior_salary": 70000,
        "avg_salary": 180000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 592,
        "name": "Леттерер-дизайнер",
        "industry": "Дизайн/Креатив/Искусство",
        "university": "Британская высшая школа дизайна, онлайн-школы",
        "description": "Художник, который рисует уникальные буквы и надписи. Создает логотипы, оформляет упаковку, постеры и обложки, делая текст главным элементом дизайна. Нишевое, но востребованное направление в брендинге.",
        "link": "https://ru.wikipedia.org/wiki/Леттеринг",
        "junior_salary": 50000,
        "avg_salary": 95000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 5}
    },
    {
        "id": 593,
        "name": "Игровой аналитик (Game Analyst)",
        "industry": "Геймдев/Аналитика/ИТ",
        "university": "НИУ ВШЭ, МФТИ",
        "description": "Анализирует поведение игроков внутри игры: какие уровни они проходят, где испытывают сложности, на что тратят деньги. Помогает геймдизайнерам улучшать баланс и монетизацию игры.",
        "link": "https://postupi.online/professiya/igrovoj-analitik/",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 594,
        "name": "Специалист по транспортной безопасности",
        "industry": "Безопасность/Транспорт/Госслужба",
        "university": "РУТ (МИИТ), СПбГУ ГА",
        "description": "Обеспечивает защиту объектов транспортной инфраструктуры (аэропортов, вокзалов, мостов) от актов незаконного вмешательства. Работает в соответствии с федеральным законом №16-ФЗ.",
        "link": "https://postupi.online/professiya/specialist-po-transportnoj-bezopasnosti/",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 595,
        "name": "Методист образовательных программ",
        "industry": "Образование/EdTech",
        "university": "МПГУ, НИУ ВШЭ (Институт образования)",
        "description": "Проектирует содержание и структуру образовательных программ, от школьных уроков до онлайн-курсов. Определяет цели обучения, подбирает форматы и оценивает результаты. Ключевой специалист по качеству образования.",
        "link": "https://postupi.online/professiya/metodist/",
        "junior_salary": 55000,
        "avg_salary": 95000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 2}
    },
    {
        "id": 596,
        "name": "Специалист по финансовому моделированию",
        "industry": "Финансы/Аналитика/Консалтинг",
        "university": "Финансовый университет, РЭШ, НИУ ВШЭ",
        "description": "Строит в Excel или специализированном ПО математические модели бизнеса для оценки инвестиционных проектов, планирования бюджета или прогнозирования финансовых показателей. Работает в инвестбанках, фондах и крупных корпорациях.",
        "link": "https://postupi.online/professiya/finansovyj-modelist/",
        "junior_salary": 95000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 597,
        "name": "Инженер-технолог (машиностроение)",
        "industry": "Промышленность/Инженерия",
        "university": "МГТУ им. Баумана, МГТУ 'СТАНКИН'",
        "description": "Разрабатывает технологический процесс изготовления деталей и сборки узлов на машиностроительном заводе. Определяет последовательность операций, подбирает оборудование и инструменты. Ключевой инженер на любом производстве.",
        "link": "https://postupi.online/professiya/inzhener-tehnolog/",
        "junior_salary": 70000,
        "avg_salary": 125000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 598,
        "name": "Промышленный клинер",
        "industry": "Сервис/Промышленность",
        "university": "Профильные учебные центры",
        "description": "Выполняет сложную уборку на промышленных объектах: чистку оборудования, удаление технических загрязнений, обеспыливание цехов. Работа, требующая специальных знаний и оборудования.",
        "link": "https://ru.wikipedia.org/wiki/Клининговая_компания",
        "junior_salary": 55000,
        "avg_salary": 90000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 599,
        "name": "Политический консультант",
        "industry": "Консалтинг/Политика",
        "university": "МГУ (Политология), НИУ ВШЭ, МГИМО",
        "description": "Консультирует политиков и государственные органы по широкому кругу вопросов: от разработки стратегии до анализа общественного мнения. В отличие от политтехнолога, больше сфокусирован на аналитике и консалтинге, а не на ведении кампаний.",
        "link": "https://postupi.online/professiya/politicheskij-konsultant/",
        "junior_salary": 80000,
        "avg_salary": 170000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 600,
        "name": "Технический дизайнер одежды",
        "industry": "Дизайн/Промышленность/Мода",
        "university": "РГУ им. Косыгина, профильные колледжи",
        "description": "Превращает эскизы дизайнера одежды в техническую документацию для фабрики. Разрабатывает лекала, подбирает материалы и контролирует пошив образцов. Связующее звено между творчеством и производством.",
        "link": "https://postupi.online/professiya/tehnicheskij-dizajner-odezhdy/",
        "junior_salary": 65000,
        "avg_salary": 115000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 4}
    },
    {
        "id": 601,
        "name": "Инженер по ветроэнергетике",
        "industry": "Энергетика/Экология/Инженерия",
        "university": "МЭИ, СПбПУ Петра Великого",
        "description": "Проектирует, строит и обслуживает ветроэнергетические установки (ВЭУ) и ветропарки. Рассчитывает эффективность, подбирает оборудование и контролирует работу станций. Востребованная 'зеленая' профессия в растущем секторе российской энергетики.",
        "link": "https://postupi.online/professiya/inzhener-vetroenergetiki/",
        "junior_salary": 85000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 602,
        "name": "Логист в e-commerce",
        "industry": "Логистика/Ритейл/Торговля",
        "university": "НИУ ВШЭ (Логистика), МАДИ",
        "description": "Организует всю цепочку движения товаров для интернет-магазинов и маркетплейсов: от управления складом (фулфилмент) до организации 'последней мили' — доставки курьером до клиента. Ключевой специалист в бурно растущем секторе онлайн-торговли.",
        "link": "https://postupi.online/professiya/logist-v-sfere-e-commerce/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 603,
        "name": "Литературный агент",
        "industry": "Медиа/Искусство/Консалтинг",
        "university": "Литературный институт им. Горького, НИУ ВШЭ (Медиакоммуникации)",
        "description": "Представляет интересы писателя: ищет издательство для рукописи, ведет переговоры о контракте, помогает с продвижением книги, занимается продажей прав на экранизацию. Профессия-мост между автором и книжным бизнесом.",
        "link": "https://ru.wikipedia.org/wiki/Литературный_агент",
        "junior_salary": 55000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 3}
    },
    {
        "id": 604,
        "name": "Реставратор антикварной мебели",
        "industry": "Искусство/Ремесло/Сервис",
        "university": "МГХПА им. Строганова, колледжи ДПИ",
        "description": "Восстанавливает старинную мебель, сохраняя ее историческую ценность и внешний вид. Работает с деревом, лаками, тканями. Редкая и кропотливая работа для частных коллекционеров, музеев и антикварных салонов.",
        "link": "https://postupi.online/professiya/restavrator-mebeli/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 5, 'art': 5}
    },
    {
        "id": 605,
        "name": "Спортивный скаут",
        "industry": "Спорт/Менеджмент",
        "university": "РГУФКСМиТ, онлайн-курсы",
        "description": "Занимается поиском талантливых молодых спортсменов для профессиональных клубов. Посещает матчи, анализирует статистику и потенциал игроков. 'Охотник за талантами' в мире большого спорта.",
        "link": "https://postupi.online/professiya/skaut/",
        "junior_salary": 65000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 606,
        "name": "Менеджер по внутреннему аудиту",
        "industry": "Финансы/Менеджмент",
        "university": "Финансовый университет, НИУ ВШЭ",
        "description": "Проверяет бизнес-процессы внутри компании на эффективность, соответствие законодательству и внутренним регламентам. Помогает руководству находить 'узкие места' и минимизировать риски. Работает в крупных корпорациях.",
        "link": "https://postupi.online/professiya/vnutrennij-auditor/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 607,
        "name": "Инженер-гидротехник",
        "industry": "Строительство/Энергетика/Инженерия",
        "university": "МГСУ, СПбГПУ Петра Великого",
        "description": "Проектирует, строит и эксплуатирует гидротехнические сооружения: плотины ГЭС, порты, каналы, системы мелиорации. Масштабная и ответственная инженерная профессия.",
        "link": "https://postupi.online/professiya/inzhener-gidrotehnik/",
        "junior_salary": 85000,
        "avg_salary": 150000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 608,
        "name": "Организационный психолог",
        "industry": "Психология/HR/Консалтинг",
        "university": "МГУ (Психфак), НИУ ВШЭ (Психология)",
        "description": "Изучает и улучшает психологический климат в компании. Помогает решать конфликты, повышать мотивацию сотрудников, проводить оценку персонала и адаптировать новичков. Работает в HR-отделах крупных компаний.",
        "link": "https://postupi.online/professiya/organizacionnyj-psiholog/",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 609,
        "name": "Специалист по беспилотной авиации",
        "industry": "Транспорт/Технологии/Сельское хозяйство",
        "university": "МАИ, Университет Иннополис",
        "description": "Проектирует, обслуживает и управляет беспилотными авиационными системами (БАС). Применяет дроны для аэрофотосъемки, мониторинга ЛЭП, доставки грузов и обработки полей.",
        "link": "https://postupi.online/professiya/inzhener-po-bespilotnym-aviacionnym-sistemam/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 2}
    },
    {
        "id": 610,
        "name": "Гример",
        "industry": "Искусство/Кино/Театр/Сервис",
        "university": "Театральные колледжи, школы визажа",
        "description": "Создает образ персонажа с помощью грима, париков и спецэффектов. Работает в кино, театре, на телевидении. Может создавать как простой макияж, так и сложный пластический грим.",
        "link": "https://postupi.online/professiya/grimer-pastizher/",
        "junior_salary": 50000,
        "avg_salary": 95000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 4, 'routine': 4, 'art': 5}
    },
    {
        "id": 611,
        "name": "Инженер железнодорожного транспорта",
        "industry": "Транспорт/Инженерия",
        "university": "РУТ (МИИТ), ПГУПС",
        "description": "Проектирует, строит и обслуживает объекты железнодорожной инфраструктуры: пути, мосты, станции, системы сигнализации и связи. Ключевой специалист для РЖД.",
        "link": "https://postupi.online/professiya/inzhener-putej-soobshcheniya/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 612,
        "name": "Специалист по тендерному сопровождению",
        "industry": "Продажи/Юриспруденция/Консалтинг",
        "university": "Профильные курсы (Академия Госзакупок)",
        "description": "Оказывает услуги компаниям по участию в государственных и коммерческих закупках (тендерах) 'под ключ': от поиска торгов и подготовки документации до участия в аукционе.",
        "link": "https://postupi.online/professiya/specialist-po-tenderam/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 613,
        "name": "Ландшафтный архитектор",
        "industry": "Архитектура/Дизайн/Экология",
        "university": "МАРХИ, РУДН, РГАУ-МСХА им. Тимирязева",
        "description": "Проектирует крупные общественные пространства: парки, набережные, городские площади. В отличие от ландшафтного дизайнера, работает с большими территориями и решает комплексные градостроительные задачи.",
        "link": "https://postupi.online/professiya/landshaftnyj-arhitektor/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 614,
        "name": "Спортивный менеджер",
        "industry": "Спорт/Менеджмент",
        "university": "РГУФКСМиТ, НИУ ВШЭ, МГУ (Высшая школа культурной политики и управления)",
        "description": "Управляет спортивным клубом, федерацией или спорткомплексом. Отвечает за финансы, маркетинг, организацию соревнований и развитие организации.",
        "link": "https://postupi.online/professiya/sportivnyj-menedzher/",
        "junior_salary": 75000,
        "avg_salary": 160000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 615,
        "name": "Эколог-проектировщик",
        "industry": "Экология/Строительство/Промышленность",
        "university": "РУДН (Экологический факультет), МГСУ",
        "description": "Разрабатывает природоохранную документацию для строящихся и действующих предприятий (проекты ПДВ, НДС, СЗЗ). Оценивает воздействие на окружающую среду и проходит государственную экспертизу.",
        "link": "https://postupi.online/professiya/ekolog-proektirovshchik/",
        "junior_salary": 65000,
        "avg_salary": 115000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 616,
        "name": "Менеджер по компенсациям и льготам (C&B Manager)",
        "industry": "HR/Менеджмент",
        "university": "НИУ ВШЭ, Финансовый университет",
        "description": "Разрабатывает и управляет системой оплаты труда, премирования и льгот в компании. Анализирует рынок зарплат, формирует грейды, отвечает за ДМС и другие бенефиты для сотрудников.",
        "link": "https://postupi.online/professiya/menedzher-po-kompensaciyam-i-lgotam/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 617,
        "name": "Технолог общественного питания",
        "industry": "HoReCa/Промышленность/Ритейл",
        "university": "МГУПП, РЭУ им. Плеханова",
        "description": "Разрабатывает рецептуры и технологические карты для блюд в ресторанах, столовых и на пищевых производствах. Контролирует качество сырья и соблюдение санитарных норм (ХАССП).",
        "link": "https://postupi.online/professiya/tehnolog-obshchestvennogo-pitaniya/",
        "junior_salary": 55000,
        "avg_salary": 90000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 5, 'art': 3}
    },
    {
        "id": 618,
        "name": "Оператор товарный (нефтепродукты)",
        "industry": "Энергетика/Транспорт/Промышленность",
        "university": "Профильные колледжи (нефтегазовые, транспортные)",
        "description": "Осуществляет прием, хранение и отгрузку нефти и нефтепродуктов на нефтебазах, терминалах и НПЗ. Ответственная рабочая профессия в нефтегазовом секторе.",
        "link": "https://postupi.online/professiya/operator-tovarnyj/",
        "junior_salary": 70000,
        "avg_salary": 110000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 1, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 619,
        "name": "Специалист по экономической безопасности",
        "industry": "Безопасность/Финансы/Юриспруденция",
        "university": "Экономические ВУЗы (специальность 'Экономическая безопасность'), Университеты МВД",
        "description": "Предотвращает и расследует экономические угрозы для компании: мошенничество, хищения, коммерческий шпионаж, проверяет контрагентов. Работает в службе безопасности крупных компаний.",
        "link": "https://postupi.online/professiya/specialist-po-ekonomicheskoj-bezopasnosti/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 620,
        "name": "Проектировщик автомобильных дорог",
        "industry": "Строительство/Транспорт/Инженерия",
        "university": "МАДИ, СибАДИ",
        "description": "Разрабатывает проекты строительства и реконструкции автомобильных дорог, развязок и мостов. Выполняет расчеты, чертежи и готовит документацию для прохождения экспертизы.",
        "link": "https://postupi.online/professiya/inzhener-proektirovshchik-avtomobilnyh-dorog/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 621,
        "name": "Драматург",
        "industry": "Искусство/Театр/Кино",
        "university": "Литературный институт им. Горького, ВГИК, РГИСИ",
        "description": "Пишет пьесы для театра, а также может работать над сценариями для кино и сериалов. Литературная профессия, требующая таланта создавать живые диалоги и захватывающие сюжеты.",
        "link": "https://postupi.online/professiya/dramaturg/",
        "junior_salary": 50000,
        "avg_salary": 100000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 3, 'routine': 2, 'art': 5}
    },
    {
        "id": 622,
        "name": "Инженер по лесному хозяйству (Лесопатолог)",
        "industry": "Сельское хозяйство/Экология",
        "university": "МГТУ им. Баумана (Мытищинский филиал), СПбГЛТУ",
        "description": "Занимается защитой лесов от вредителей и болезней. Обследует лесные массивы, назначает санитарные рубки и разрабатывает меры по сохранению здоровья леса.",
        "link": "https://postupi.online/professiya/inzhener-lesopatolog/",
        "junior_salary": 55000,
        "avg_salary": 90000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 623,
        "name": "Менеджер по работе с партнерами (Partner Manager)",
        "industry": "Продажи/Бизнес/ИТ",
        "university": "Экономические и управленческие ВУЗы",
        "description": "Развивает партнерскую сеть компании. Ищет новых партнеров (дилеров, агентов, интеграторов), обучает их и помогает им продавать продукты компании, достигая общих бизнес-целей.",
        "link": "https://postupi.online/professiya/menedzher-po-rabote-s-partnerami/",
        "junior_salary": 75000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 624,
        "name": "Тренер-аналитик (в спорте)",
        "industry": "Спорт/Аналитика",
        "university": "РГУФКСМиТ, технические ВУЗы",
        "description": "Член тренерского штаба, который занимается тактическим анализом своей команды и соперников. 'Разбирает' матчи, готовит видео-нарезки и статистические отчеты для главного тренера и игроков.",
        "link": "https://postupi.online/professiya/trener-analitik/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 625,
        "name": "Инженер по водоснабжению и водоотведению",
        "industry": "Строительство/ЖКХ/Инженерия",
        "university": "МГСУ, НИУ 'МЭИ'",
        "description": "Проектирует и обслуживает системы подачи воды и канализации для зданий и целых городов. Ключевой специалист в структурах 'Водоканала' и в строительных компаниях.",
        "link": "https://postupi.online/professiya/inzhener-po-vodosnabzheniyu-i-vodootvedeniyu/",
        "junior_salary": 70000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 626,
        "name": "Геммолог",
        "industry": "Ритейл/Наука/Искусство",
        "university": "МГУ (Геологический), РГГРУ, Геммологический центр МГУ",
        "description": "Эксперт по драгоценным камням. Определяет подлинность, качество и происхождение камней. Работает в ювелирных компаниях, ломбардах и экспертных лабораториях.",
        "link": "https://postupi.online/professiya/gemmolog/",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 4}
    },
    {
        "id": 627,
        "name": "Специалист по управлению автопарком",
        "industry": "Транспорт/Логистика",
        "university": "МАДИ, транспортные колледжи",
        "description": "Отвечает за эффективную эксплуатацию корпоративного автопарка. Организует техобслуживание и ремонт, контролирует расход топлива, управляет водителями. Работает в логистических и таксомоторных компаниях.",
        "link": "https://postupi.online/professiya/specialist-po-upravleniyu-avtoparkom/",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 628,
        "name": "PR-менеджер в IT",
        "industry": "Коммуникации/PR/ИТ",
        "university": "НИУ ВШЭ, МГИМО, технические ВУЗы",
        "description": "Продвигает IT-компании и их продукты в СМИ и профессиональном сообществе. Пишет статьи на Хабр, организует участие в конференциях, работает с IT-журналистами и блогерами.",
        "link": "https://postupi.online/professiya/pr-menedzher-v-it/",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 629,
        "name": "Инженер по охране окружающей среды (Эколог на предприятии)",
        "industry": "Экология/Промышленность",
        "university": "РХТУ им. Менделеева, РУДН",
        "description": "Отвечает за соблюдение природоохранного законодательства на заводе. Контролирует выбросы, сбросы и отходы, готовит отчетность для надзорных органов. Обязательная должность на любом промышленном предприятии.",
        "link": "https://postupi.online/professiya/inzhener-po-ohrane-okruzhayushchej-sredy/",
        "junior_salary": 60000,
        "avg_salary": 105000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 630,
        "name": "Концепт-художник",
        "industry": "Геймдев/Кино/Анимация",
        "university": "Британская высшая школа дизайна, Scream School",
        "description": "Создает визуальные образы персонажей, локаций и предметов на начальном этапе разработки игры или фильма. Задает стилистику и атмосферу будущего проекта. Ключевая роль в визуальном дизайне.",
        "link": "https://postupi.online/professiya/koncept-hudozhnik/",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 2, 'art': 5}
    },
    {
        "id": 631,
        "name": "Специалист по ипотечному кредитованию",
        "industry": "Финансы/Банки/Недвижимость",
        "university": "Финансовые ВУЗы и колледжи",
        "description": "Консультирует клиентов по ипотечным программам, помогает собрать документы и сопровождает сделку по покупке недвижимости с помощью кредита. Работает в банках и агентствах недвижимости.",
        "link": "https://postupi.online/professiya/specialist-po-ipotechnomu-kreditovaniyu/",
        "junior_salary": 60000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 5, 'art': 1}
    },
    {
        "id": 632,
        "name": "Директор по закупкам (Chief Procurement Officer)",
        "industry": "Менеджмент/Логистика/Ритейл",
        "university": "НИУ ВШЭ, экономические ВУЗы + MBA",
        "description": "Топ-менеджер, отвечающий за всю закупочную деятельность в крупной компании. Разрабатывает стратегию, управляет бюджетом и командой закупщиков, оптимизирует расходы.",
        "link": "https://ru.wikipedia.org/wiki/Директор_по_закупкам",
        "junior_salary": 180000,
        "avg_salary": 400000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 633,
        "name": "Конфликтолог-медиатор",
        "industry": "Психология/Юриспруденция/Консалтинг",
        "university": "СПбГУ (Факультет социологии), РГСУ, центры медиации",
        "description": "Нейтральный посредник, который помогает сторонам конфликта (в семье, бизнесе, организации) провести переговоры и найти взаимовыгодное решение без обращения в суд. Растущее направление в России.",
        "link": "https://postupi.online/professiya/mediator/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 634,
        "name": "Инженер-механик (сельскохозяйственная техника)",
        "industry": "Сельское хозяйство/Инженерия",
        "university": "РГАУ-МСХА им. Тимирязева, КубГАУ",
        "description": "Организует эксплуатацию, техническое обслуживание и ремонт тракторов, комбайнов и другой сельхозтехники. Ключевой технический специалист в любом агрохозяйстве.",
        "link": "https://postupi.online/professiya/agroinzhener/",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 635,
        "name": "Специалист по промышленному туризму",
        "industry": "Туризм/Промышленность/PR",
        "university": "РГУТиС, УрФУ",
        "description": "Разрабатывает и проводит экскурсии на действующие заводы и фабрики. Помогает предприятиям повышать свою открытость и привлекать новые кадры, а туристам — увидеть производственные процессы изнутри.",
        "link": "https://postupi.online/professiya/specialist-po-promyshlennomu-turizmu/",
        "junior_salary": 55000,
        "avg_salary": 95000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 636,
        "name": "Инженер-релейщик (специалист РЗиА)",
        "industry": "Энергетика/Промышленность",
        "university": "НИУ 'МЭИ', Новосибирский ГТУ, Ивановский ГЭУ",
        "description": "Инженер, отвечающий за релейную защиту и автоматику (РЗиА) на электростанциях и подстанциях. Настраивает 'мозг' энергосистемы, который отключает поврежденные участки и предотвращает крупные аварии. Элитная и крайне ответственная профессия в электроэнергетике.",
        "link": "https://postupi.online/professiya/inzhener-relejnoj-zashchity-i-avtomatiki/",
        "junior_salary": 90000,
        "avg_salary": 170000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 637,
        "name": "Технолог сварочного производства",
        "industry": "Промышленность/Строительство/Инженерия",
        "university": "МГТУ им. Баумана, СПбПУ Петра Великого",
        "description": "Разрабатывает и контролирует технологию сварки на производстве. Выбирает оборудование, материалы и режимы сварки, аттестует сварщиков. От его работы зависит прочность и надежность ответственных конструкций — от мостов до трубопроводов.",
        "link": "https://postupi.online/professiya/tehnolog-svarochnogo-proizvodstva/",
        "junior_salary": 80000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 638,
        "name": "Специалист по неразрушающему контролю (Дефектоскопист)",
        "industry": "Промышленность/Энергетика/Транспорт",
        "university": "НИТУ 'МИСиС', Томский политехнический университет, учебные центры",
        "description": "Проверяет качество сварных швов, деталей и конструкций, не разрушая их (с помощью ультразвука, рентгена и др.). 'Врач' для металла, который находит скрытые дефекты в самолетах, трубах и реакторах, обеспечивая их безопасность.",
        "link": "https://postupi.online/professiya/defektoskopist/",
        "junior_salary": 85000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 639,
        "name": "Инженер-кораблестроитель",
        "industry": "Промышленность/Инженерия/Транспорт",
        "university": "СПбГМТУ, Дальневосточный федеральный университет",
        "description": "Проектирует и строит корабли и суда — от гражданских танкеров до военных кораблей и подводных лодок. Работает в конструкторских бюро и на судостроительных верфях.",
        "link": "https://postupi.online/professiya/inzhener-korablestroitel/",
        "junior_salary": 90000,
        "avg_salary": 170000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 640,
        "name": "Диспетчер энергосистемы",
        "industry": "Энергетика",
        "university": "НИУ 'МЭИ', профильные технические ВУЗы",
        "description": "Управляет потоками электроэнергии в режиме реального времени в масштабах региона или всей страны. Обеспечивает баланс между производством и потреблением, предотвращая блэкауты. Работа в 'Системном операторе Единой энергетической системы'.",
        "link": "https://postupi.online/professiya/dispetcher-energosistemy/",
        "junior_salary": 100000,
        "avg_salary": 200000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 641,
        "name": "Инженер-организатор дорожного движения",
        "industry": "Транспорт/Строительство/Госуправление",
        "university": "МАДИ, СПбГАСУ",
        "description": "Проектирует схемы движения транспорта в городах: настраивает светофоры, рисует разметку, устанавливает знаки, чтобы увеличить пропускную способность улиц и уменьшить пробки.",
        "link": "https://postupi.online/professiya/inzhener-po-organizacii-dorozhnogo-dvizheniya/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 642,
        "name": "Специалист по органическому земледелию",
        "industry": "Сельское хозяйство/Экология",
        "university": "РГАУ-МСХА им. Тимирязева, аграрные ВУЗы",
        "description": "Внедряет и сертифицирует технологии ведения сельского хозяйства без использования синтетических пестицидов и удобрений. Помогает фермерам производить 'органические' продукты.",
        "link": "https://ru.wikipedia.org/wiki/Органическое_сельское_хозяйство",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 643,
        "name": "Ихтиолог",
        "industry": "Наука/Экология/Сельское хозяйство",
        "university": "МГУ (Биофак), Астраханский ГТУ, Дальрыбвтуз",
        "description": "Ученый, изучающий рыб. Оценивает запасы промысловых рыб в морях и реках, работает в НИИ рыбного хозяйства, а также может заниматься болезнями рыб в аквакультуре.",
        "link": "https://postupi.online/professiya/ihtiolog/",
        "junior_salary": 55000,
        "avg_salary": 95000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 644,
        "name": "Арборист (специалист по уходу за деревьями)",
        "industry": "Экология/Сервис/ЖКХ",
        "university": "Учебные центры, РГАУ-МСХА",
        "description": "'Хирург' для деревьев. Занимается лечением, обрезкой и удалением деревьев, в том числе в труднодоступных местах с использованием альпинистского снаряжения. Востребован в городском озеленении и частном секторе.",
        "link": "https://postupi.online/professiya/arborist/",
        "junior_salary": 60000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 3, 'routine': 4, 'art': 2}
    },
    {
        "id": 645,
        "name": "Колорист (кино и ТВ)",
        "industry": "Креатив/Кино/Медиа",
        "university": "Школы кино и телевидения, онлайн-курсы",
        "description": "Специалист по цветокоррекции видео. 'Раскрашивает' фильм или ролик на финальном этапе постпродакшна, создавая нужное настроение и добиваясь единого визуального стиля.",
        "link": "https://postupi.online/professiya/kolorist/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 646,
        "name": "Дизайнер выставочных стендов",
        "industry": "Дизайн/Маркетинг",
        "university": "МГХПА им. Строганова, Британская высшая школа дизайна",
        "description": "Проектирует и оформляет выставочные стенды для компаний, участвующих в отраслевых выставках. Создает креативные и функциональные пространства для привлечения клиентов.",
        "link": "https://postupi.online/professiya/dizajner-vystavochnyh-stendov/",
        "junior_salary": 65000,
        "avg_salary": 120000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 647,
        "name": "Спортивный диетолог",
        "industry": "Спорт/Медицина/Wellness",
        "university": "РГУФКСМиТ, мед. ВУЗы + курсы",
        "description": "Разрабатывает персональные планы питания для профессиональных спортсменов и любителей для достижения конкретных целей: набора мышечной массы, повышения выносливости, снижения веса.",
        "link": "https://postupi.online/professiya/sportivnyj-dietolog/",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 648,
        "name": "Зоопсихолог",
        "industry": "Психология/Сервис",
        "university": "МГУ (Психфак), аграрные ВУЗы (зоотехния) + курсы",
        "description": "Специалист по поведению животных. Помогает владельцам кошек и собак скорректировать нежелательное поведение питомцев (агрессия, страхи, нечистоплотность), находя его причины.",
        "link": "https://postupi.online/professiya/zoopsiholog/",
        "junior_salary": 50000,
        "avg_salary": 95000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 649,
        "name": "Иппотерапевт",
        "industry": "Медицина/Социальная сфера/Спорт",
        "university": "РГУФКСМиТ, мед. и пед. ВУЗы + курсы",
        "description": "Специалист по лечебной верховой езде. Проводит реабилитационные занятия с помощью лошадей для людей с нарушениями опорно-двигательного аппарата и особенностями ментального развития.",
        "link": "https://postupi.online/professiya/ippoterapevt/",
        "junior_salary": 45000,
        "avg_salary": 80000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 650,
        "name": "Отельер",
        "industry": "HoReCa/Менеджмент",
        "university": "Российский международный олимпийский университет, РЭУ им. Плеханова",
        "description": "Управляющий или владелец отеля. Отвечает за стратегию развития, финансовые результаты, качество сервиса и репутацию гостиницы. Вершина карьеры в гостиничном бизнесе.",
        "link": "https://postupi.online/professiya/oteler/",
        "junior_salary": 100000,
        "avg_salary": 250000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 2}
    },
    {
        "id": 651,
        "name": "Менеджер по управлению изменениями (Change Manager)",
        "industry": "Менеджмент/Консалтинг/HR",
        "university": "НИУ ВШЭ, РАНХиГС, бизнес-школы",
        "description": "Помогает компании успешно проводить крупные внутренние трансформации (внедрение нового ПО, слияние, реорганизация). Работает с сопротивлением сотрудников и выстраивает коммуникации.",
        "link": "https://ru.wikipedia.org/wiki/Управление_изменениями",
        "junior_salary": 120000,
        "avg_salary": 230000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 652,
        "name": "Антимонопольный юрист",
        "industry": "Юриспруденция/Консалтинг/Госслужба",
        "university": "МГЮА, МГУ (Юрфак), НИУ ВШЭ",
        "description": "Специализируется на законодательстве о защите конкуренции. Сопровождает сделки слияния и поглощения, представляет интересы компаний в Федеральной антимонопольной службе (ФАС).",
        "link": "https://postupi.online/professiya/antimonopolnyj-yurist/",
        "junior_salary": 90000,
        "avg_salary": 190000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 653,
        "name": "Краснодеревщик",
        "industry": "Ремесло/Производство/Дизайн",
        "university": "Колледжи ДПИ, художественно-промышленные академии",
        "description": "Мастер по изготовлению эксклюзивной мебели и предметов интерьера из ценных пород дерева. Сочетает навыки столяра, реставратора и художника. Редкая и престижная ремесленная профессия.",
        "link": "https://postupi.online/professiya/krasnoderevshchik/",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 5, 'art': 5}
    },
    {
        "id": 654,
        "name": "Наладчик промышленного оборудования",
        "industry": "Промышленность/Рабочие",
        "university": "Технические и политехнические колледжи",
        "description": "Настраивает, запускает и регулирует автоматические линии и станки на производстве. Высококвалифицированный рабочий, от которого зависит бесперебойная работа всего завода.",
        "link": "https://postupi.online/professiya/naladchik-promyshlennogo-oborudovaniya/",
        "junior_salary": 75000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 655,
        "name": "Специалист по водородной энергетике",
        "industry": "Энергетика/Наука/Инженерия",
        "university": "МЭИ, РХТУ им. Менделеева, Сколтех",
        "description": "Разрабатывает и внедряет технологии производства, хранения и использования водорода в качестве экологически чистого топлива. Профессия будущего, работа на переднем крае науки и энергетики.",
        "link": "https://postupi.online/professiya/specialist-po-vodorodnoj-energetike/",
        "junior_salary": 95000,
        "avg_salary": 190000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 3, 'art': 1}
    },
    {
        "id": 656,
        "name": "Сценограф",
        "industry": "Искусство/Театр/Дизайн",
        "university": "Школа-студия МХАТ, РГИСИ, ГИТИС",
        "description": "Художник, который создает визуальное пространство спектакля: декорации, костюмы, свет. Главный соавтор режиссера, отвечающий за материальный мир на сцене.",
        "link": "https://postupi.online/professiya/scenograf/",
        "junior_salary": 60000,
        "avg_salary": 120000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 4, 'routine': 3, 'art': 5}
    },
    {
        "id": 657,
        "name": "Персональный шоппер",
        "industry": "Сервис/Мода/Ритейл",
        "university": "Профильные школы стиля и имиджа",
        "description": "Помогает клиентам формировать гардероб: разбирает существующую одежду, сопровождает на шоппинге, подбирает образы в соответствии со стилем жизни и бюджетом клиента.",
        "link": "https://postupi.online/professiya/personalnyj-shopper/",
        "junior_salary": 50000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 5}
    },
    {
        "id": 658,
        "name": "Инженер-металлург",
        "industry": "Промышленность",
        "university": "НИТУ 'МИСиС', УрФУ, СПбПУ Петра Великого",
        "description": "Управляет процессами получения металлов из руды и создания сплавов с заданными свойствами. Фундаментальная профессия для черной и цветной металлургии.",
        "link": "https://postupi.online/professiya/metallurg/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 659,
        "name": "Продуктовый дизайнер (физические продукты)",
        "industry": "Дизайн/Промышленность",
        "university": "МГХПА им. Строганова, Британская высшая школа дизайна",
        "description": "Проектирует потребительские товары: от гаджетов и бытовой техники до мебели и посуды. Отвечает не только за внешний вид, но и за эргономику, функциональность и технологичность продукта.",
        "link": "https://postupi.online/professiya/promyshlennyj-dizajner/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 3, 'art': 5}
    },
    {
        "id": 660,
        "name": "Инженер-конструктор (авиастроение)",
        "industry": "Промышленность/Авиакосмос/Инженерия",
        "university": "МАИ, Казанский национальный исследовательский технический университет (КАИ)",
        "description": "Проектирует самолеты, вертолеты и их отдельные узлы (фюзеляж, крыло, шасси). Работает в конструкторских бюро, таких как 'Сухой' или 'Иркут'.",
        "link": "https://postupi.online/professiya/aviacionnyj-inzhener/",
        "junior_salary": 95000,
        "avg_salary": 190000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 661,
        "name": "Директор по логистике (Chief Logistics Officer)",
        "industry": "Менеджмент/Логистика/Транспорт",
        "university": "НИУ ВШЭ, МАДИ + MBA",
        "description": "Топ-менеджер, отвечающий за всю логистику и управление цепями поставок в компании. Разрабатывает стратегию, управляет бюджетом, складами и транспортными потоками.",
        "link": "https://postupi.online/professiya/direktor-po-logistike/",
        "junior_salary": 200000,
        "avg_salary": 450000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 662,
        "name": "Инженер по утилизации отходов",
        "industry": "Экология/Промышленность/ЖКХ",
        "university": "РХТУ им. Менделеева, МГСУ",
        "description": "Проектирует и эксплуатирует объекты по переработке и утилизации промышленных и бытовых отходов: полигоны, мусоросжигательные заводы, сортировочные комплексы.",
        "link": "https://postupi.online/professiya/ekolog-utilizator/",
        "junior_salary": 70000,
        "avg_salary": 125000,
        "growth_rate": "Очень высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 663,
        "name": "Бутафор",
        "industry": "Искусство/Театр/Кино",
        "university": "Театральные художественно-технические колледжи",
        "description": "Мастер, который изготавливает реквизит для спектаклей и фильмов: от 'драгоценностей' и оружия до еды и элементов декораций. Редкая и креативная профессия в закулисье.",
        "link": "https://postupi.online/professiya/butafor/",
        "junior_salary": 45000,
        "avg_salary": 75000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 3, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 5}
    },
    {
        "id": 664,
        "name": "Специалист по личной безопасности",
        "industry": "Безопасность/Консалтинг",
        "university": "Опыт в силовых структурах, профильные курсы",
        "description": "Анализирует угрозы и разрабатывает комплекс мер по защите жизни, здоровья и частной жизни клиента. В отличие от телохранителя, больше работает с информацией, планированием и превентивными мерами.",
        "link": "https://ru.wikipedia.org/wiki/Телохранитель",
        "junior_salary": 100000,
        "avg_salary": 220000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 665,
        "name": "Профайлер-верификатор",
        "industry": "Психология/Безопасность/HR",
        "university": "МГУ (Психфак), школы профайлинга",
        "description": "Специалист по 'чтению' людей. Анализирует невербальное поведение человека (мимику, жесты, речь) для выявления лжи, оценки его намерений и составления психологического портрета. Востребован в службах безопасности, HR и на переговорах.",
        "link": "https://postupi.online/professiya/profajler/",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 666,
        "name": "Спортивный директор",
        "industry": "Спорт/Менеджмент",
        "university": "РГУФКСМиТ, бизнес-школы (RMA)",
        "description": "Топ-менеджер в профессиональном спортивном клубе, отвечающий за всю спортивную составляющую: формирование команды, трансферную политику, назначение главного тренера и развитие академии.",
        "link": "https://postupi.online/professiya/sportivnyj-direktor/",
        "junior_salary": 150000,
        "avg_salary": 350000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 2, 'art': 1}
    },
    {
        "id": 667,
        "name": "Инженер-геотехник",
        "industry": "Строительство/Инженерия",
        "university": "МГСУ, СПбГАСУ",
        "description": "Специалист по фундаментам и основаниям зданий. Изучает свойства грунтов и проектирует фундаменты, подпорные стенки и подземные сооружения, обеспечивая их надежность и устойчивость.",
        "link": "https://postupi.online/professiya/inzhener-geotehnik/",
        "junior_salary": 85000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 1}
    },
    {
        "id": 668,
        "name": "Специалист по сертификации пищевой продукции",
        "industry": "Промышленность/Ритейл/Консалтинг",
        "university": "МГУПП, РГАУ-МСХА",
        "description": "Помогает производителям и импортерам продуктов питания получать необходимые декларации, сертификаты и проходить проверки на соответствие техническим регламентам (ТР ТС) и стандартам (ХАССП).",
        "link": "https://postupi.online/professiya/specialist-po-sertifikacii/",
        "junior_salary": 70000,
        "avg_salary": 120000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 669,
        "name": "Инженер БТИ (Кадастровый инженер)",
        "industry": "Недвижимость/Строительство/Госслужба",
        "university": "МИИГАиК, Государственный университет по землеустройству",
        "description": "Проводит техническую инвентаризацию объектов недвижимости: обмеряет квартиры и здания, составляет технические планы для постановки на кадастровый учет в Росреестре. ",
        "link": "https://postupi.online/professiya/kadastrovyj-inzhener/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 1, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 670,
        "name": "Байер (закупщик сырья и материалов)",
        "industry": "Промышленность/Производство/Логистика",
        "university": "Экономические и технические ВУЗы",
        "description": "Специалист отдела снабжения на производственном предприятии, который закупает сырье, комплектующие и оборудование. Ищет поставщиков, проводит переговоры и обеспечивает бесперебойность поставок.",
        "link": "https://postupi.online/professiya/menedzher-po-zakupkam/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 671,
        "name": "Инженер по надежности оборудования (Reliability Engineer)",
        "industry": "Промышленность/Энергетика/Инженерия",
        "university": "МГТУ им. Баумана, РГУ нефти и газа им. Губкина, технические ВУЗы",
        "description": "Анализирует причины отказов оборудования на производстве и разрабатывает программы по повышению его надежности и снижению простоев. Критически важный специалист для непрерывных производств, таких как НПЗ, металлургические и химические заводы.",
        "link": "https://postupi.online/professiya/inzhener-po-nadezhnosti/",
        "junior_salary": 95000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 3, 'routine': 4, 'art': 1}
    },
    {
        "id": 672,
        "name": "Инженер-гидролог",
        "industry": "Экология/Строительство/Наука",
        "university": "МГУ (Географический), РГГМУ",
        "description": "Изучает водные объекты (реки, озера) и водный режим территорий. Проводит расчеты для проектирования мостов, плотин и защиты от наводнений. Работает в проектных институтах и структурах Росгидромета.",
        "link": "https://postupi.online/professiya/gidrolog/",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 673,
        "name": "Планировщик маршрутной сети общественного транспорта",
        "industry": "Транспорт/Госуправление/Консалтинг",
        "university": "МАДИ, НИУ ВШЭ (Высшая школа урбанистики)",
        "description": "Анализирует пассажиропотоки и разрабатывает оптимальные маршруты и расписания для автобусов, трамваев и метро. Работает в городских департаментах транспорта и консалтинговых компаниях, чтобы сделать общественный транспорт быстрее и удобнее.",
        "link": "https://postupi.online/professiya/planirovshchik-marshrutnoj-seti-obshchestvennogo-transporta/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 674,
        "name": "Специалист по лесовосстановлению",
        "industry": "Экология/Сельское хозяйство",
        "university": "МГТУ им. Баумана (Мытищинский филиал), СПбГЛТУ",
        "description": "Разрабатывает и реализует проекты по восстановлению лесов после рубок, пожаров и болезней. Подбирает породы деревьев, организует посадку и уход за молодым лесом. Работает в лесничествах и лесопромышленных компаниях.",
        "link": "https://postupi.online/professiya/specialist-po-lesovosstanovleniyu/",
        "junior_salary": 60000,
        "avg_salary": 100000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 675,
        "name": "Технолог молочного производства",
        "industry": "Промышленность/Сельское хозяйство",
        "university": "МГУПП, Вологодская ГМХА",
        "description": "Отвечает за технологию производства молока, сыра, йогурта, творога и других молочных продуктов. Контролирует качество сырья, соблюдение рецептур и работу оборудования на молокозаводах.",
        "link": "https://postupi.online/professiya/tehnolog-molochnogo-proizvodstva/",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 676,
        "name": "Инженер-материаловед",
        "industry": "Промышленность/Наука/Инженерия",
        "university": "НИТУ 'МИСиС', МГТУ им. Баумана",
        "description": "Изучает строение и свойства материалов (металлов, керамики, полимеров) и создает новые материалы с заданными характеристиками. Работает в R&D-центрах авиационных, оборонных и металлургических компаний.",
        "link": "https://postupi.online/professiya/materialoved/",
        "junior_salary": 85000,
        "avg_salary": 160000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 2, 'routine': 4, 'art': 1}
    },
    {
        "id": 677,
        "name": "Креативный продюсер",
        "industry": "Креатив/Медиа/Реклама",
        "university": "НИУ ВШЭ (Медиакоммуникации), MADS, IKRA",
        "description": "Отвечает за творческую составляющую проекта (рекламного ролика, телешоу, YouTube-канала). Разрабатывает идею, подбирает команду (режиссера, сценариста) и контролирует, чтобы итоговый продукт соответствовал креативной концепции.",
        "link": "https://postupi.online/professiya/kreativnyj-prodyuser/",
        "junior_salary": 90000,
        "avg_salary": 180000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 678,
        "name": "Ветеринарно-санитарный врач",
        "industry": "Сельское хозяйство/Госслужба/Безопасность",
        "university": "МГАВМиБ им. Скрябина, СПбГУВМ",
        "description": "Контролирует качество и безопасность продуктов животного происхождения (мясо, молоко, яйца) на рынках, фермах и перерабатывающих предприятиях. Защищает людей от болезней, общих для человека и животных. Работает в структурах Россельхознадзора.",
        "link": "https://postupi.online/professiya/veterinarno-sanitarnyj-vrach/",
        "junior_salary": 60000,
        "avg_salary": 100000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 679,
        "name": "Музыкальный супервайзер",
        "industry": "Кино/Креатив/Медиа",
        "university": "Бизнес-школы (RMA), опыт в музыкальной индустрии",
        "description": "Подбирает и лицензирует музыку для фильмов, сериалов, рекламы и видеоигр. Ведет переговоры с правообладателями, формирует саундтрек и отвечает за музыкальный бюджет проекта.",
        "link": "https://ru.wikipedia.org/wiki/Музыкальный_супервайзер",
        "junior_salary": 70000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 3, 'art': 5}
    },
    {
        "id": 680,
        "name": "Специалист по системам менеджмента качества (ISO)",
        "industry": "Менеджмент/Промышленность/Консалтинг",
        "university": "Технические ВУЗы (специальность 'Управление качеством')",
        "description": "Внедряет и поддерживает на предприятии системы управления качеством в соответствии с международными стандартами (например, ISO 9001). Оптимизирует бизнес-процессы и готовит компанию к сертификационному аудиту.",
        "link": "https://postupi.online/professiya/menedzher-po-kachestvu/",
        "junior_salary": 75000,
        "avg_salary": 130000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 681,
        "name": "Управляющий логистическим терминалом",
        "industry": "Логистика/Транспорт/Менеджмент",
        "university": "МАДИ, НИУ ВШЭ (Логистика)",
        "description": "Руководит работой крупного складского или транспортного комплекса. Отвечает за операционную эффективность, бюджет, безопасность и управление персоналом терминала.",
        "link": "https://postupi.online/professiya/zaveduyushchij-skladom/",
        "junior_salary": 100000,
        "avg_salary": 200000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 682,
        "name": "Fashion-аналитик",
        "industry": "Мода/Ритейл/Аналитика",
        "university": "НИУ ВШЭ (Школа дизайна), Британская высшая школа дизайна",
        "description": "Анализирует продажи, рыночные тенденции и поведение потребителей в индустрии моды. Помогает брендам и ритейлерам прогнозировать спрос, формировать ассортимент и определять ценовую политику.",
        "link": "https://postupi.online/professiya/fashion-analitik/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 4}
    },
    {
        "id": 683,
        "name": "Административный директор (Head of Admin)",
        "industry": "Менеджмент/Административная работа",
        "university": "Управленческие и экономические ВУЗы",
        "description": "Топ-менеджер, отвечающий за всю административно-хозяйственную деятельность крупной компании: от управления офисом и автопарком до организации мероприятий и командировок. Обеспечивает комфортную и эффективную рабочую среду.",
        "link": "https://ru.wikipedia.org/wiki/Административный_директор",
        "junior_salary": 130000,
        "avg_salary": 250000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 684,
        "name": "Специалист по организации авиационных перевозок",
        "industry": "Транспорт/Логистика",
        "university": "МГТУ ГА, СПбГУ ГА",
        "description": "Организует грузовые и пассажирские авиаперевозки. Взаимодействует с авиакомпаниями, аэропортами, таможней, фрахтует рейсы и оформляет сопроводительную документацию.",
        "link": "https://postupi.online/professiya/specialist-po-organizacii-aviaperevozok/",
        "junior_salary": 75000,
        "avg_salary": 140000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 5, 'routine': 4, 'art': 1}
    },
    {
        "id": 685,
        "name": "Спортивный физиолог",
        "industry": "Спорт/Наука/Медицина",
        "university": "МГУ (Биофак), РГУФКСМиТ",
        "description": "Изучает, как физические нагрузки влияют на организм спортсмена. Разрабатывает программы тренировок и восстановления на основе данных о работе сердечно-сосудистой, дыхательной и мышечной систем. Работает в центрах спортивной медицины и профессиональных командах.",
        "link": "https://postupi.online/professiya/sportivnyj-fiziolog/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 4, 'routine': 4, 'art': 1}
    },
    {
        "id": 686,
        "name": "Ихтиопатолог",
        "industry": "Сельское хозяйство/Наука",
        "university": "МГАВМиБ им. Скрябина, Астраханский ГТУ",
        "description": "'Рыбий доктор'. Специалист по диагностике, лечению и профилактике болезней рыб, в первую очередь в аквакультуре (на рыбоводных хозяйствах). Обеспечивает здоровье и сохранность поголовья.",
        "link": "https://postupi.online/professiya/ihtiopatolog/",
        "junior_salary": 65000,
        "avg_salary": 110000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 687,
        "name": "Яхтенный брокер",
        "industry": "Продажи/Транспорт/Сервис",
        "university": "ВУЗы (менеджмент, международные отношения) + сертификация",
        "description": "Посредник при покупке, продаже и аренде дорогих яхт. Консультирует клиентов, подбирает суда, сопровождает сделки. Элитный сегмент продаж для состоятельных клиентов.",
        "link": "https://ru.wikipedia.org/wiki/Яхтенный_брокер",
        "junior_salary": 100000,
        "avg_salary": 300000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 3, 'art': 2}
    },
    {
        "id": 688,
        "name": "Горный инженер",
        "industry": "Добыча/Промышленность/Инженерия",
        "university": "НИТУ 'МИСиС', Санкт-Петербургский горный университет",
        "description": "Организует и контролирует процессы добычи полезных ископаемых открытым (карьеры) или подземным (шахты) способом. Отвечает за технологию, безопасность и эффективность горных работ.",
        "link": "https://postupi.online/professiya/gornyj-inzhener/",
        "junior_salary": 120000,
        "avg_salary": 250000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 4, 'routine': 5, 'art': 1}
    },
    {
        "id": 689,
        "name": "Книжный дизайнер (верстальщик)",
        "industry": "Дизайн/Медиа/Креатив",
        "university": "Высшая школа печати и медиаиндустрии (Политех), НИУ ВШЭ (Дизайн)",
        "description": "Разрабатывает дизайн и верстает макет книг, журналов и другой печатной продукции. Отвечает за внешний вид обложки, типографику, расположение текста и иллюстраций. ",
        "link": "https://postupi.online/professiya/dizajner-verstalshchik/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 4, 'art': 5}
    },
    {
        "id": 690,
        "name": "Инженер по стандартизации",
        "industry": "Промышленность/Менеджмент",
        "university": "Технические ВУЗы (специальность 'Стандартизация и метрология')",
        "description": "Разрабатывает и внедряет стандарты (ГОСТы, ТУ, стандарты организации) на предприятии. Контролирует, чтобы продукция и процессы соответствовали установленным требованиям.",
        "link": "https://postupi.online/professiya/inzhener-po-standartizacii-i-sertifikacii/",
        "junior_salary": 65000,
        "avg_salary": 115000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 2, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 691,
        "name": "Консультант по выходу на международные рынки",
        "industry": "Консалтинг/Бизнес/Продажи",
        "university": "МГИМО, РАНХиГС (ВШКУ), НИУ ВШЭ (МЭиМП)",
        "description": "Помогает российским компаниям начать экспорт своей продукции. Анализирует зарубежные рынки, разрабатывает стратегию, помогает с сертификацией, логистикой и поиском партнеров.",
        "link": "https://ru.wikipedia.org/wiki/Экспорт",
        "junior_salary": 100000,
        "avg_salary": 220000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 692,
        "name": "Арт-оценщик",
        "industry": "Искусство/Финансы/Консалтинг",
        "university": "МГУ (Истфак, отделение истории искусства), РГГУ",
        "description": "Эксперт, определяющий подлинность и рыночную стоимость произведений искусства. Работает в аукционных домах, галереях, страховых компаниях и банках (арт-банкинг).",
        "link": "https://postupi.online/professiya/art-ocenshchik/",
        "junior_salary": 80000,
        "avg_salary": 170000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 5, 'creativity': 5, 'social': 4, 'routine': 4, 'art': 5}
    },
    {
        "id": 693,
        "name": "Управляющий фитнес-клубом",
        "industry": "Менеджмент/Спорт/Сервис",
        "university": "РГУФКСМиТ, бизнес-школы",
        "description": "Руководит работой фитнес-клуба. Отвечает за финансовые показатели, продажи клубных карт, маркетинг, подбор персонала (тренеров, администраторов) и качество услуг.",
        "link": "https://postupi.online/professiya/upravlyayushchij-fitnes-klubom/",
        "junior_salary": 80000,
        "avg_salary": 160000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 4, 'social': 5, 'routine': 3, 'art': 1}
    },
    {
        "id": 694,
        "name": "Главный редактор",
        "industry": "Медиа/Креатив/Менеджмент",
        "university": "МГУ (Журфак), НИУ ВШЭ (Медиакоммуникации)",
        "description": "Руководит редакцией СМИ (журнала, сайта, телеканала). Определяет редакционную политику, отвечает за контент, управляет командой журналистов и редакторов. Ключевая фигура в медиабизнесе.",
        "link": "https://postupi.online/professiya/glavnyj-redaktor/",
        "junior_salary": 120000,
        "avg_salary": 250000,
        "growth_rate": "Средние",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 5, 'routine': 2, 'art': 4}
    },
    {
        "id": 695,
        "name": "Специалист по спортивным покрытиям (граундсмен)",
        "industry": "Спорт/Сервис/Агрономия",
        "university": "РГАУ-МСХА им. Тимирязева, профильные курсы",
        "description": "Отвечает за подготовку и уход за спортивными газонами на футбольных полях и полях для гольфа. Профессия на стыке агрономии и инженерии, от которой зависит качество игры.",
        "link": "https://ru.wikipedia.org/wiki/Граундсмен",
        "junior_salary": 70000,
        "avg_salary": 130000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 2, 'routine': 5, 'art': 2}
    },
    {
        "id": 696,
        "name": "Дворецкий (Батлер)",
        "industry": "Сервис/HoReCa",
        "university": "Международные школы батлеров, опыт в отелях класса люкс",
        "description": "Управляющий домашним хозяйством в богатом доме или персональный ассистент для VIP-гостей в отелях класса люкс. Организует быт, управляет персоналом, исполняет поручения. Элитная сервисная профессия.",
        "link": "https://ru.wikipedia.org/wiki/Дворецкий",
        "junior_salary": 150000,
        "avg_salary": 350000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 3, 'social': 5, 'routine': 4, 'art': 2}
    },
    {
        "id": 697,
        "name": "Инженер-электрик (проектировщик)",
        "industry": "Строительство/Энергетика/Инженерия",
        "university": "НИУ 'МЭИ', СПбПУ Петра Великого",
        "description": "Проектирует системы электроснабжения и освещения для зданий и промышленных объектов. Выполняет расчеты нагрузок, подбирает оборудование и чертит схемы в AutoCAD или Revit.",
        "link": "https://postupi.online/professiya/inzhener-elektrik/",
        "junior_salary": 80000,
        "avg_salary": 150000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 5, 'creativity': 3, 'social': 3, 'routine': 5, 'art': 1}
    },
    {
        "id": 698,
        "name": "Исторический костюмер",
        "industry": "Искусство/Кино/Театр",
        "university": "Школа-студия МХАТ, РГИСИ",
        "description": "Специалист по созданию исторических костюмов для кино и театра. Изучает крой, материалы и технологии пошива определенной эпохи, чтобы добиться максимальной достоверности.",
        "link": "https://postupi.online/professiya/hudozhnik-po-kostyumu/",
        "junior_salary": 60000,
        "avg_salary": 110000,
        "growth_rate": "Низкие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 3, 'routine': 5, 'art': 5}
    },
    {
        "id": 699,
        "name": "Переводчик-локализатор (игры, ПО)",
        "industry": "Креатив/ИТ/Медиа",
        "university": "МГЛУ, переводческие факультеты ВУЗов",
        "description": "Не просто переводит, а адаптирует текст и культурные реалии компьютерной игры или программы для российского рынка. Работает с юмором, идиомами и игровым сленгом.",
        "link": "https://dtf.ru/gamedev/2042179-kak-stat-perevodchikom-igr-instrukciya-dlya-novichkov",
        "junior_salary": 65000,
        "avg_salary": 120000,
        "growth_rate": "Высокие",
        "score_vector": {'logic': 4, 'creativity': 5, 'social': 2, 'routine': 4, 'art': 4}
    }
]


DB_NAME = 'careers.db'

def create_and_populate_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS careers")

    cursor.execute('''
        CREATE TABLE careers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT,
            university TEXT,
            description TEXT,
            link TEXT,
            junior_salary INTEGER,
            avg_salary INTEGER,
            growth_rate TEXT,
            score_vector TEXT
        )
    ''')

    for career in CAREER_DATA:
        score_vector_json = json.dumps(career['score_vector'], ensure_ascii=False)

        cursor.execute('''
            INSERT INTO careers (
                id, name, industry, university, description, link, junior_salary, avg_salary, growth_rate, score_vector
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            career['id'],
            career['name'],
            career['industry'],
            career['university'],
            career['description'],
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
    unique_careers = []
    seen_names = set()
    for career in CAREER_DATA:
        if career['name'] not in seen_names:
            unique_careers.append(career)
            seen_names.add(career['name'])
    
    for i, career in enumerate(unique_careers):
        career['id'] = i + 1
        
    CAREER_DATA = unique_careers

    create_and_populate_db()