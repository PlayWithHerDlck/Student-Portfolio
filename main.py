from os import name

import psycopg2
from psycopg2.extras import DictCursor

# Конфигурация подключения
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "12345",  # <-- Укажите ваш настоящий пароль от Postgres
    "host": "localhost",
    "port": "5432",
}


# =====================================================================
# ФУНКЦИИ ВЫВОДА СТАТИСТИКИ (ЧТЕНИЕ)
# =====================================================================
def get_top_staff():
    print("\n📊 1. ТОП-5 МАСТЕРОВ ПО ВЫРУЧКЕ:")
    print("-" * 50)
    query = """
        SELECT s.full_name, COUNT(o.order_id) as total_orders, SUM(p.total_amount) as total_revenue
        FROM staff s
        JOIN orders o ON s.staff_id = o.staff_id
        JOIN payments p ON o.order_id = p.order_id
        WHERE o.status = 'Завершен'
        GROUP BY s.full_name
        ORDER BY total_revenue DESC
        LIMIT 5;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            for row in cur.fetchall():
                print(
                    f"Мастер: {row['full_name']:<18} | Заказов: {row['total_orders']:<3} | Выручка: {row['total_revenue']:.2f} руб."
                )


def get_popular_services():
    print("\n💆 2. САМЫЕ ПОПУЛЯРНЫЕ ПРОЦЕДУРЫ:")
    print("-" * 50)
    query = """
        SELECT s.title, COUNT(o.order_id) as times_booked, AVG(p.total_amount) as avg_check
        FROM orders o
        JOIN payments p ON o.order_id = p.order_id
        CROSS JOIN services s
        WHERE o.status = 'Завершен'
        GROUP BY s.title
        ORDER BY times_booked DESC
        LIMIT 3;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            for row in cur.fetchall():
                print(
                    f"Услуга: {row['title']:<38} | Записей: {row['times_booked']:<3} | Средний чек: {row['avg_check']:.2f} руб."
                )


def get_upcoming_appointments():
    print("\n📅 3. БЛИЖАЙШИЕ ЗАПИСИ НА СЕГОДНЯ И ЗАВТРА:")
    print("-" * 65)
    query = """
        SELECT o.order_id, c.first_name, c.phone, o.appointment_date, o.start_time
        FROM orders o
        JOIN clients c ON o.client_id = c.client_id
        WHERE o.status = 'Запланирован'
          AND o.appointment_date BETWEEN CURRENT_DATE AND CURRENT_DATE + 1
        ORDER BY o.appointment_date, o.start_time;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                print("На сегодня и завтра запланированных визитов не найдено.")
            for row in rows:
                print(
                    f"ID: {row['order_id']:<3} | Клиент: {row['first_name']:<10} | Тел: {row['phone']:<16} | Дата: {row['appointment_date']} в {row['start_time']}"
                )


def get_payment_stats():
    print("\n💳 4. СТАТИСТИКА ПО СПОСОБАМ ОПЛАТЫ:")
    print("-" * 50)
    query = """
        SELECT payment_method, COUNT(*) as tx_count, SUM(total_amount) as total_sum
        FROM payments
        GROUP BY payment_method
        ORDER BY tx_count DESC;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            for row in cur.fetchall():
                print(
                    f"Метод: {row['payment_method']:<10} | Транзакций: {row['tx_count']:<3} | Сумма: {row['total_sum']:.2f} руб."
                )


def get_vip_clients():
    print("\n👑 5. СПИСОК НАШИХ VIP-КЛИЕНТОВ (Ограничение 5 строк):")
    print("-" * 50)
    query = """
        SELECT DISTINCT c.client_id, c.first_name, c.phone, c.discount_percent
        FROM clients c
        JOIN orders o ON c.client_id = o.client_id
        WHERE c.discount_percent > 10 AND o.status = 'Завершен'
        ORDER BY c.discount_percent DESC
        LIMIT 5;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            for row in cur.fetchall():
                print(
                    f"ID: {row['client_id']:<4} | Имя: {row['first_name']:<12} | Тел: {row['phone']:<16} | Скидка: {row['discount_percent']}%"
                )


def get_all_clients():
    print("\n👥 6. СПИСОК ВСЕХ КЛИЕНТОВ САЛОНА (ТОП-50 новых):")
    print("-" * 60)
    query = """
        SELECT client_id, first_name, phone, discount_percent
        FROM clients
        ORDER BY client_id DESC
        LIMIT 999;
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()

                print(
                    f"{'ID':<6} | {'Имя клиента':<15} | {'Телефон':<20} | {'Скидка':<8}"
                )
                print("-" * 60)

                for row in rows:
                    print(
                        f"{row['client_id']:<6} | "
                        f"{row['first_name']:<15} | "
                        f"{row['phone']:<20} | "
                        f"{row['discount_percent']}%"
                    )
                print(f"\nВыведено записей: {len(rows)}")
    except Exception as e:
        print(f"❌ Ошибка при чтении клиентов: {e}")


# =====================================================================
# ФУНКЦИИ ДОБАВЛЕНИЯ ДАННЫХ (ЗАПИСЬ)
# =====================================================================
def add_new_client():
    print("\n👤 ДОБАВЛЕНИЕ НОВОГО КЛИЕНТА:")
    name = input("Введите имя клиента: ").strip()
    phone = input("Введите номер телефона: ").strip()
    try:
        discount = int(input("Введите процент скидки (0-100): ").strip() or 0)
    except ValueError:
        discount = 0

    if not name or not phone:
        print("❌ Ошибка: Имя и телефон не могут быть пустыми!")
        return

    query = (
        "INSERT INTO clients (first_name, phone, discount_percent) VALUES (%s, %s, %s);"
    )
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor() as cur:
            cur.execute(query, (name, phone, discount))
            conn.commit()
            print(f"✔️ Client '{name}' успешно добавлен в базу данных!")


def add_new_service():
    print("\n💅 ДОБАВЛЕНИЕ НОВОЙ СПА-УСЛУГИ:")
    title = input("Введите название процедуры: ").strip()
    try:
        duration = int(input("Длительность процедуры (в минутах): ").strip())
        price = float(input("Стоимость процедуры (руб.): ").strip())
    except ValueError:
        print("❌ Ошибка: Длительность и стоимость должны быть числами!")
        return

    if not title:
        print("❌ Ошибка: Название услуги не может быть пустым!")
        return

    query = "INSERT INTO services (title, duration_minutes, price) VALUES (%s, %s, %s);"
    with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
        with conn.cursor() as cur:
            cur.execute(query, (title, duration, price))
            conn.commit()
            print(f"✔️ Процедура '{title}' добавлена в прайс-лист!")


def add_new_order():
    print("\n📅 ЗАПИСЬ КЛИЕНТА НА СЕАНС (НОВЫЙ ЗАКАЗ):")
    try:
        client_id = int(input("Введите ID клиента: ").strip())
        staff_id = int(input("Введите ID мастера: ").strip())
        date = input("Введите дату визита (ГГГГ-ММ-ДД): ").strip()
        time = input("Введите время начала (ЧЧ:ММ): ").strip()
    except ValueError:
        print("❌ Ошибка: Неверный формат ID!")
        return

    query = """
        INSERT INTO orders (client_id, staff_id, appointment_date, start_time, status)
        VALUES (%s, %s, %s, %s, 'Запланирован');
    """
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:  # type: ignore
            with conn.cursor() as cur:
                cur.execute(query, (client_id, staff_id, date, time))
                conn.commit()
                print("✔️ Визит успешно запланирован в системе!")
    except psycopg2.errors.ForeignKeyViolation:  # type: ignore
        print("❌ Ошибка связи: Указанный ID клиента или мастера не существует в базе!")
    except Exception as e:
        print(f"❌ Ошибка при добавлении: {e}")


# Подменю добавления данных
def menu_insert_data():
    while True:
        print("\n" + "-" * 40)
        print("    📥 МЕНЮ ДОБАВЛЕНИЯ ЗАПИСЕЙ")
        print("-" * 40)
        print("1. Добавить нового клиента")
        print("2. Добавить новую спа-процедуру")
        print("3. Создать запись на визит (Заказ)")
        print("0. Вернуться назад")
        print("-" * 40)

        choice = input("👉 Выберите действие (0-3): ").strip()
        if choice == "1":
            add_new_client()
        elif choice == "2":
            add_new_service()
        elif choice == "3":
            add_new_order()
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод.")
        input("\nНажмите Enter, чтобы продолжить...")

        # =====================================================================
        # ГЛАВНЫЙ ИНТЕРФЕЙС
        # =====================================================================


def show_menu():
    while True:
        print("\n" + "=" * 50)
        print("    🏢 СИСТЕМА УПРАВЛЕНИЯ СПА-САЛОНОМ v1.2")
        print("=" * 50)
        print("1. Посмотреть ТОП-5 мастеров по выручке")
        print("2. Посмотреть самые популярные процедуры")
        print("3. Ближайшие записи клиентов (Сегодня / Завтра)")
        print("4. Статистика по способам оплаты")
        print("5. Список VIP-клиентов")
        print("6. Посмотреть список всех клиентов (ТОП-50)")
        print("7. 📥 ДОБАВИТЬ ДАННЫЕ В ТАБЛИЦЫ")
        print("0. Выход из программы")
        print("=" * 50)

        choice = input("👉 Выберите пункт меню (0-7): ").strip()

        if choice == "0":
            print("\n👋 Работа с базой данных завершена. До свидания!")
            break
        elif choice == "1":
            get_top_staff()
        elif choice == "2":
            get_popular_services()
        elif choice == "3":
            get_upcoming_appointments()
        elif choice == "4":
            get_payment_stats()
        elif choice == "5":
            get_vip_clients()
        elif choice == "6":
            get_all_clients()
        elif choice == "7":
            menu_insert_data()
            continue  # Возвращаемся в начало цикла, так как в подменю свой Enter
        else:
            print("\n❌ Некорректный ввод! Введите цифру от 0 до 7.")
            continue

        # Один общий Enter для всех пунктов просмотра (1-6)
        input("\nНажмите Enter для возврата в главное меню...")


if __name__ == "__main__":
    show_menu()
