import random


words = ["долла́р", "долла́ра", "долла́ров"]


JOBS_NAMES = {
    "courier": "🚶 Курьер",
    "cleaner": "🧹 Уборщик",
    "fastfood": "🍔 Работник фастфуда",
    "loader": "📦 Грузчик",

    "artist": "🎨 Художник",
    "writer": "✍️ Писатель",
    "mechanic": "🔧 Механик",
    "programmer": "💻 Программист",
    "blogger": "📹 Видеоблогер",
}


JOBS_SALARIES = {
    "courier": 150,
    "cleaner": 120,
    "fastfood": 140,
    "loader": 170,

    "artist": 360,
    "writer": 370,
    "mechanic": 420,
    "programmer": 750,
    "blogger": 530,
}


JOBS_EVENTS = {
    "courier": [
        {"text": "⌛ Ты опоздал на заказ! Штраф составит ###{ammount} {word}###", "penalty_percent": 20},
        {"text": "🤝 Клиент дал тебе щедрые чаевые — ###+{amount} {word}###", "bonus_percent": random.randint(5, 7)},
        {"text": "💰 За эту смену тебе дали очень много чаевых — ###+{amount} {word}###", "bonus_percent": random.randint(12, 17)},
        {"text": "🤷 Ты потерял посылку! Штраф составит ###{ammount} {word}###", "penalty_percent": random.randint(30, 70)},
    ],
    "cleaner": [
        {"text": "✨ Выполнил уборку на отлично — получил премию ###+{amount} {word}###", "bonus_percent": random.randint(10, 15)},
        {"text": "🔧 Сломал дорогое оборудование — оплатил ремонт в размере ###{ammount} {word}###", "penalty_percent": random.randint(75, 90)},
        {"text": "💰 Нашёл забытые деньги во время уборки — получил ###+{amount} {word}###", "bonus_percent": random.randint(1, 100)},
    ],
    "fastfood": [
        {"text": "🍔 Впечатлил клиентов — бонус ###+{amount} {word}###", "bonus_percent": random.randint(10, 25)},
        {"text": "🍟 Уронил заказ — штраф в размере ###{ammount} {word}###", "penalty_percent": 15},
    ],
    "loader": [
        {"text": "📦 Перенёс дополнительный груз — получил бонус ###+{amount} {word}###", "bonus_percent": random.randint(10, 20)},
        {"text": "📉 Потерял коробку с товарами — штраф в размере ###{ammount} {word}###", "penalty_percent": random.randint(10, 30)},
        {"text": "🏥 Получил травму — оплатил лечение за ###{ammount} {word}###", "penalty_percent": random.randint(15, 35)},
        {"text": "🏥 Ты получил очень серьезную травму — оплатил лечение за ###{ammount} {word}###", "penalty_percent": random.randint(35, 70)},
    ],


    "artist": [
        {"text": "🎨 Продал картину — заработал ###+{amount} {word}###", "bonus_percent": random.randint(50, 1000)},
        {"text": "🖌️ Потерял кисть — купил новую за ###{ammount} {word}###", "penalty_percent": 20},
        {"text": "💡 Вдохновение пришло — создал шедевр, получил бонус ###+{amount} {word}###", "bonus_percent": random.randint(20, 50)},
        {"text": "😞 Неудачная выставка — доход снизился на ###{ammount} {word}###", "penalty_percent": random.randint(33, 70)},
        {"text": "🏆 Выиграл конкурс — получил приз ###+{amount} {word}###", "bonus_percent": random.randint(5, 15)},
    ],
    "writer": [
        {"text": "📚 Написал бестселлер — заработал ###+{amount} {word}###", "bonus_percent": random.randint(100, 1000)},
        {"text": "🗑️ Потерял черновики — потратил ###{ammount} {word}###", "penalty_percent": random.randint(5, 35)},
        {"text": "✍️ Получил гонорар за статью — ###+{amount} {word}###", "bonus_percent": random.randint(70, 300)},
        {"text": "😔 Писательский кризис — заработок уменьшился на ###{ammount} {word}###", "penalty_percent": random.randint(5, 35)},
    ],
    "mechanic": [
        {"text": "🚗 Быстрая работа — премия ###+{amount} {word}###", "bonus_percent": random.randint(7, 15)},
        {"text": "⚙️ Сломал инструмент — купил новый за ###{ammount} {word}###", "penalty_percent": random.randint(12, 40)},
        {"text": "❌ Поставил некачественную деталь — штраф ###{ammount} {word}###", "penalty_percent": random.randint(15, 42)},
    ],
    "programmer": [
        {"text": "🐞 Нашёл баг в коде — получил премию ###+{amount} {word}###", "bonus_percent": random.randint(5, 15)},
        {"text": "💻 Компьютер сломался — потратил ###{ammount} {word}### на ремонт", "penalty_percent": random.randint(25, 100)},
        {"text": "⏳ Пропустил дедлайн — штраф ###{ammount} {word}###", "penalty_percent": random.randint(15, 25)},
        {"text": "⚡ Оптимизировал код — бонус ###+{amount} {word}###", "bonus_percent": random.randint(10, 30)},
        {"text": "🚀 Сделал успешный релиз — заработал ###+{amount} {word}###", "bonus_percent": random.randint(80, 280)},
    ],
    "blogger": [
        {"text": "🎥 Успешный стрим — получил донаты на ###+{amount} {word}###", "bonus_percent": random.randint(40, 500)},
        {"text": "🔧 Проблемы с оборудованием — потратил ###{ammount} {word}### на ремонт", "penalty_percent": random.randint(30, 100)},
        {"text": "🏆 Популярное видео — премия ###+{amount} {word}###", "bonus_percent": random.randint(50, 250)},
        {"text": "👎 Увеличилось число хейтеров — потерял подписчиков, убыток ###{ammount} {word}###", "penalty_percent": random.randint(40, 100)},
    ]
}



def job_event(job_name, salary):
    if random.random() <= 0.3:
        event = random.choice(JOBS_EVENTS.get(job_name, []))
        if not event:
            return salary, None

        if "penalty_percent" in event:
            change = salary * event["penalty_percent"] / 100
            salary -= change
        elif "bonus_percent" in event:
            change = salary * event["bonus_percent"] / 100
            salary += change
        else:
            change = 0

        return salary, event["text"].format(ammount=int[change], word=plural(change, words))

    else:
        return salary, None



def plural(n, forms):
    n = abs(int(n)) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return forms[2]
    if 1 == n1:
        return forms[0]
    if 2 <= n1 <= 4:
        return forms[1]
    return forms[2]
