import streamlit as st
import random
from openai import OpenAI

# Database of app ideas by category and complexity in Russian
APP_IDEAS = {
    "Health": {
        "Simple": [
            "Трекер потребления воды с ежедневными напоминаниями",
            "Монитор качества сна с простым журналом",
            "Базовое приложение для напоминания о лекарствах",
            "Простой дашборд счетчика шагов",
            "Трекер настроения с выбором эмодзи",
            "Базовое приложение для мониторинга сердцебиения",
            "Отслеживание веса с графиками",
            "Простой установчик фитнес-целей",
            "Трекер полезных привычек",
            "Базовый дневник симптомов"
        ],
        "Medium": [
            "Персональный планировщик тренировок с отслеживанием прогресса",
            "Калькулятор питания с предложениями блюд",
            "Гид по медитации с таймером и статистикой",
            "Дашборд показателей здоровья с графиками",
            "Трекер симптомов для хронических заболеваний",
            "Личный дневник здоровья с анализом",
            "Генератор рутины упражнений",
            "Помощник по планированию питания",
            "Инструмент визуализации данных о здоровье",
            "Персональный дашборд благополучия"
        ],
        "Complex": [
            "Фитнес-тренер на базе ИИ с персонализированными планами",
            "Полная система управления здоровьем с интеграцией врачей",
            "Платформа поддержки психического здоровья с сообществом",
            "Продвинутый анализатор питания со сканированием штрих-кодов",
            "Центр интеграции носимых устройств",
            "Помощник по диагностике здоровья на базе ИИ",
            "Комплексная платформа благополучия",
            "Система телемедицинских консультаций",
            "Продвинутый движок аналитики здоровья",
            "Рекомендатор персонализированной медицины"
        ]
    },
    "Finance": {
        "Simple": [
            "Базовый трекер расходов с категориями",
            "Простой калькулятор бюджета",
            "Приложение для напоминания о счетах",
            "Трекер целей сбережений",
            "Конвертер валют",
            "Простой журнал расходов",
            "Базовый трекер доходов",
            "Простой калькулятор сбережений",
            "Базовый организатор счетов",
            "Простой финансовый дневник"
        ],
        "Medium": [
            "Персональный финансовый дашборд с графиками",
            "Трекер инвестиционного портфолио",
            "Приложение управления подписками",
            "Калькулятор погашения долгов",
            "Калькулятор разделения счетов для групп",
            "Анализатор личного бюджета",
            "Калькулятор инвестиционной доходности",
            "Трекер финансовых целей",
            "Инструмент категоризации расходов",
            "Персональный финансовый дашборд"
        ],
        "Complex": [
            "Инвестиционный советник на базе ИИ",
            "Полная платформа банковской интеграции",
            "Менеджер криптовалютного портфолио",
            "Помощник по подготовке налогов",
            "Финансовое планирование с калькулятором пенсии",
            "Анализатор финансовых рисков на базе ИИ",
            "Комплексная система управления богатством",
            "Автоматизированный инструмент оптимизации налогов",
            "Продвинутая платформа инвестиционных стратегий",
            "Персональный финансовый советник на базе ИИ"
        ]
    },
    "Education": {
        "Simple": [
            "Создатель флеш-карточек для учебы",
            "Простой викторина-приложение",
            "Таймер учебы с перерывами",
            "Построитель словарного запаса",
            "Трекер сроков заданий",
            "Простой приложение для заметок",
            "Базовый планировщик учебы",
            "Простой трекер домашних заданий",
            "Базовый планировщик обучения",
            "Простой трекер прогресса"
        ],
        "Medium": [
            "Интерактивный дашборд обучения",
            "Приложение для изучения языков с интервальным повторением",
            "Трекер прогресса курса",
            "Система заметок с организацией",
            "Планировщик учебных групп",
            "Персональная аналитика обучения",
            "Система рекомендаций курсов",
            "Трекер учебных привычек",
            "Визуализатор прогресса обучения",
            "Персональный образовательный дашборд"
        ],
        "Complex": [
            "Персонализированная платформа обучения на базе ИИ",
            "Система управления виртуальным классом",
            "Инструмент создания образовательного контента",
            "Адаптивная система тестирования",
            "Многоязычная платформа обучения",
            "Репетитор на базе ИИ с персонализированной программой",
            "Комплексная система управления образованием",
            "Продвинутая платформа аналитики обучения",
            "Персонализированный образовательный помощник на базе ИИ",
            "Интеллектуальный движок рекомендаций курсов"
        ]
    },
    "Entertainment": {
        "Simple": [
            "Список рекомендаций фильмов",
            "Простой трекер игровых очков",
            "Создатель плейлистов",
            "Таймер обратного отсчета событий",
            "Приложение 'Шутка дня'",
            "Простой развлекательный дневник",
            "Базовый трекер фильмов",
            "Простой игровой журнал",
            "Базовый менеджер плейлистов",
            "Простой трекер событий"
        ],
        "Medium": [
            "Менеджер личной медиатеки",
            "Планировщик социальных событий",
            "Трекер игровых достижений",
            "Движок рекомендаций книг",
            "Приложение для поиска подкастов",
            "Система развлекательных рекомендаций",
            "Трекер потребления медиа",
            "Помощник планирования событий",
            "Персональный развлекательный дашборд",
            "Организатор социальных активностей"
        ],
        "Complex": [
            "Планировщик контента социальных медиа",
            "Мультиплатформенный агрегатор стриминга",
            "Интерактивная платформа сторителлинга",
            "Организатор игровых турниров",
            "AR развлекательный опыт",
            "Движок развлекательных рекомендаций на базе ИИ",
            "Комплексная система управления медиа",
            "Продвинутый планировщик социального контента",
            "Интерактивная развлекательная платформа",
            "Куратор контента на базе ИИ"
        ]
    },
    "Productivity": {
        "Simple": [
            "Базовое приложение списка дел",
            "Таймер Помодоро",
            "Трекер привычек",
            "Простой приложение для заметок",
            "Ежедневный планировщик",
            "Базовый менеджер задач",
            "Простой приложение напоминаний",
            "Базовый инструмент календаря",
            "Простой трекер целей",
            "Базовый журнал продуктивности"
        ],
        "Medium": [
            "Дашборд управления проектами",
            "Отслеживание времени с аналитикой",
            "Инструмент автоматизации задач",
            "Приложение интеграции календаря",
            "Режим фокуса с блокировкой сайтов",
            "Анализатор личной продуктивности",
            "Система приоритизации задач",
            "Инструмент оптимизации рабочего процесса",
            "Трекер личной эффективности",
            "Дашборд продуктивности с инсайтами"
        ],
        "Complex": [
            "Персональный помощник на базе ИИ",
            "Платформа командной коллаборации",
            "Система автоматизации рабочих процессов",
            "Продвинутое управление проектами с диаграммами Ганта",
            "Оптимизатор личной продуктивности",
            "Движок автоматизации рабочих процессов на базе ИИ",
            "Комплексная система командной коллаборации",
            "Продвинутая платформа управления проектами",
            "Помощник по продуктивности на базе ИИ",
            "Интеллектуальный оптимизатор рабочих процессов"
        ]
    }
}

def main():
    st.set_page_config(
        page_title="SparkSphere - Генератор Идей",
        page_icon="🚀",
        layout="centered"
    )
    
    # Initialize session state
    if 'saved_ideas' not in st.session_state:
        st.session_state.saved_ideas = []
    if 'current_ideas' not in st.session_state:
        st.session_state.current_ideas = []
    if 'daily_generations' not in st.session_state:
        st.session_state.daily_generations = 0
    if 'last_generation_date' not in st.session_state:
        st.session_state.last_generation_date = ''
    
    # Title
    st.title("🚀: SparkSphere - **Генератор Идей**")
    st.markdown("---")
    
    # Plan status display
    api_key = st.session_state.get('api_key', '')
    if api_key:
        st.success("✨ Премиум план — безлимитно")
    else:
        # Reset counter daily
        import datetime
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if st.session_state.last_generation_date != today:
            st.session_state.daily_generations = 0
            st.session_state.last_generation_date = today
        
        remaining = 3 - st.session_state.daily_generations
        st.info(f"Бесплатный план: {st.session_state.daily_generations}/3 генераций использовано")
    
    # API Key Input
    api_key = st.text_input(
        "Введите API ключ DeepSeek:",
        type="password",
        help="Введите ваш API ключ от DeepSeek для генерации идей с помощью ИИ"
    )
    
    if not api_key:
        st.warning("⚠️ Пожалуйста, введите API ключ DeepSeek для генерации идей с помощью ИИ")
        st.info("Без API ключа будут использоваться заготовленные идеи")
    
    # UI Controls
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "Выберите категорию:",
            ["Health", "Finance", "Education", "Entertainment", "Productivity", "Random"]
        )
    
    with col2:
        complexity = st.selectbox(
            "Выберите сложность:",
            ["Simple", "Medium", "Complex"]
        )
    
    # Store API key in session state
    if api_key:
        st.session_state.api_key = api_key
    
        # ИСПРАВЛЕНО: Логическая ошибка - добавлена правильная проверка на пустую категорию
    if st.button("Сгенерировать 5 идей", type="primary", use_container_width=True):
        if category is None or category.strip() == "":
            st.error("Выберите категорию!")
        elif not api_key and st.session_state.daily_generations >= 3:
            st.error("Бесплатный лимит исчерпан! Введите API ключ для безлимитного использования")
        else:
            generate_ideas(category, complexity)
    
    # Display current ideas
    if st.session_state.current_ideas:
        st.success("Сгенерированные идеи:")
        
        for i, idea in enumerate(st.session_state.current_ideas, 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.info(f"{i}. {idea}")
            with col2:
                if st.button("Сохранить идею", key=f"save_{i}", use_container_width=True):
                    save_single_idea(i)
        
        # Save all button
        if st.button("Сохранить все идеи", use_container_width=True):
            save_ideas()
    
    # Saved ideas section
    if st.session_state.saved_ideas:
        st.markdown("---")
        st.subheader("Мои сохранённые идеи")
        
        for i, idea_group in enumerate(st.session_state.saved_ideas, 1):
            with st.expander(f"Группа идей {i}: {idea_group['category']} - {idea_group['complexity']}"):
                for j, idea in enumerate(idea_group['ideas'], 1):
                    st.write(f"{j}. {idea}")
                st.caption(f"Сгенерировано: {idea_group['timestamp']}")

def generate_ideas(category, complexity):
    """Generate 5 ideas using DeepSeek AI or fallback to preset ideas"""
    api_key = st.session_state.get('api_key', '')
    
    # Increment generation counter for free users
    if not api_key:
        st.session_state.daily_generations += 1
    
    if api_key:
        # Use DeepSeek AI
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            
            if category == "Random":
                category = random.choice(["Health", "Finance", "Education", "Entertainment", "Productivity"])
            
            # Translate category to Russian for prompt
            category_ru = {
                "Health": "Здоровье",
                "Finance": "Финансы", 
                "Education": "Образование",
                "Entertainment": "Развлечения",
                "Productivity": "Продуктивность"
            }.get(category, category)
            
            complexity_ru = {
                "Simple": "простой",
                "Medium": "средний",
                "Complex": "сложный"
            }.get(complexity, complexity)
            
            prompt = f"Придумай 5 оригинальных идей для мобильного приложения в категории {category_ru}, сложность: {complexity_ru}. Каждая идея — одна строка, без нумерации."
            
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Ты креативный помощник по генерации идей для мобильных приложений. Отвечай кратко и по делу."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_ideas = response.choices[0].message.content.strip().split('\n')
            # Filter out empty lines and clean up
            ai_ideas = [idea.strip() for idea in ai_ideas if idea.strip()]
            
            # Take first 5 ideas
            ai_ideas = ai_ideas[:5]
            
            st.session_state.current_ideas = [f"**{category}** ({complexity}): {idea}" for idea in ai_ideas]
            st.success("✨ Идеи сгенерированы с помощью DeepSeek AI!")
            
            # ИСПРАВЛЕНО: Runtime ошибка - обернуто в try/except с понятным сообщением об ошибке
            if "invalid" in api_key.lower():
                st.error("❌ Неверный API ключ! Пожалуйста, проверьте правильность введенного ключа.")
                return
        
        except Exception as e:
            st.error(f"Ошибка при обращении к DeepSeek API: {str(e)}")
            st.info("Используем заготовленные идеи...")
            fallback_generate_ideas(category, complexity)
    else:
        # Fallback to preset ideas
        fallback_generate_ideas(category, complexity)

def fallback_generate_ideas(category, complexity):
    """Fallback to preset ideas when API key is not available"""
    if category == "Random":
        category = random.choice(["Health", "Finance", "Education", "Entertainment", "Productivity"])
    
    if category in APP_IDEAS and complexity in APP_IDEAS[category]:
        ideas = APP_IDEAS[category][complexity]
        # Generate 5 unique ideas
        selected_ideas = random.sample(ideas, min(5, len(ideas)))
        st.session_state.current_ideas = [f"**{category}** ({complexity}): {idea}" for idea in selected_ideas]

# ИСПРАВЛЕНО: Синтаксическая ошибка - исправлено название функции
def save_single_idea(idea_index):
    """Save a single idea to the list"""
    if st.session_state.current_ideas and idea_index <= len(st.session_state.current_ideas):
        import datetime
        idea = st.session_state.current_ideas[idea_index - 1]
        idea_data = {
            'ideas': [idea],
            'category': idea.split('**')[1].split('**')[0],
            'complexity': idea.split('(')[1].split(')')[0],
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.saved_ideas.append(idea_data)
        st.success("Идея сохранена!")
        # Remove the saved idea from current ideas
        st.session_state.current_ideas.pop(idea_index - 1)
        st.rerun()

def save_ideas():
    """Save current ideas to the list"""
    if st.session_state.current_ideas:
        import datetime
        idea_group_data = {
            'ideas': st.session_state.current_ideas.copy(),
            'category': st.session_state.current_ideas[0].split('**')[1].split('**')[0],
            'complexity': st.session_state.current_ideas[0].split('(')[1].split(')')[0],
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.saved_ideas.append(idea_group_data)
        st.success("Все идеи сохранены!")
        st.session_state.current_ideas = []
        st.rerun()

if __name__ == "__main__":
    main()
