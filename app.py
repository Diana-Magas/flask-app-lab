from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key"

@app.route('/')
@app.route("/resume")

def resume():
    profile = {
        "name": "Діана Магас",
        "position": "Junior Full-Stack Developer / Студентка",
        "summary": "Студентка спеціальності «Інженерія програмного забезпечення». "
                   "Захоплююся розробкою вебдодатків на Laravel. Створюю сучасні та зручні вебрішення , прагну розвиватися, вчитися новому та втіпювати цікаві ідеї в реальність",
    }

    personal = [
        ("Місто", "Івано-Франківськ, Україна"),
        ("Мови", "Українська (рідна), Англійська (B2), Італійська (А2)"),
        ("Курс", "3-й курс"),
        ("Інтереси", "Веброзробка, open-source, UX/UI дизайн"),
    ]

    education = [
        {"title": "Прикладна математика", "period": "2021 — 2025",
         "place": "Івано-Франківський фаховий коледж Карпатського національного університету ім. Василя Стефаника",
         "text": "Кваліфікація: технік-програміст, веб-програміст."},

        {"title": "Інженерія програмного забезпечення", "period": "2025 - теперішній час",
         "place": "Карпатського національного університет ім. Василя Стефаника",
         "text": "Розробка вебзастосунків, програмування, робота з базами даних сучасними вебтехнологіями.."},
         
         
        {"title": "Pre-Junior Program", "period": "01.03.2024-10.05.2024",
         "place": "EPAM",
         "text": "Веброзробка: HTML, CSS, JavaScript та Bootstrap. Практика створення адаптивних вебсторінок."},

        {"title": "Meta Social Media Marketing Professional","period": "24.09.2022-16.01.2023",
         "place": "Meta",
         "text": "SMM, створення контенту, стратегія просування в соціальних мережах, робота з аудиторією та аналіз ефективності."}
    ]

    technologies = ["Laravel", "Filament", "InertiaJs", "Docker", "Bootstrap 5",
                    "React", "PostgreSQL", "Git / GitHub/GitLab"]

    skills = ["Креативність", "Відповідальність", "Адаптивний дизайн",
              "Робота в команді", "Git workflow"]

    projects = [
    {
        "title": "FinLex Alliance — юридично-бухгалтерський вебсайт", "period": "2025 - теперішній час",
        "type": "Комерційний проєкт",
        "text": "Розробка вебсайту для юридичних та бухгалтерських послуг з адміністративною панеллю, керуванням послугами, контентом і контактними заявками.",
        "tags": ["Laravel", "PHP", "React", "Inertia.js", "PostgreSQL", "Filament"]
    },
    {
        "title": "Travel.Pro — туристичний вебсайт","period": " серпень 2026 - теперішній час",
        "type": "Комерційний проєкт",
        "text": "Розробка вебсайту туристичної агенції з каталогом турів, категоріями, інформаційними сторінками та адміністративною панеллю для керування контентом.",
        "tags": ["Laravel", "PHP", "React", "Inertia.js", "PostgreSQL", "Filament"]
    },
    {
        "title": "Практика / стажування",
        "type": "Практичний досвід",
        "text": "Виконання практичних завдань з веброзробки, робота з існуючим кодом, Git та командна взаємодія під час розробки вебпроєктів.",
        "tags": ["PHP", "Laravel", "Git", "Web Development"]
    }
]
    return render_template("resume.html", title="Резюме", profile=profile,
                           personal=personal, education=education,
                           technologies=technologies, skills=skills,
                           projects=projects)


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        flash("Дякуємо! Ваше повідомлення прийнято.", "success")
        return redirect(url_for("contacts"))
    return render_template("contacts.html", title="Контакти")


if __name__ == '__main__':
    app.run(debug=True)