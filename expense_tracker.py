import flet as ft
import datetime
import json
import os
from collections import defaultdict

def format_rupiah(amount):
    return "Rp{:,.2f}".format(amount).replace(",", ".").replace(".", ",", 1)

expenses = []
selected_month = "All"
months = ["All", "January", "February", "March","April","May","June","July","August","September","October","November","December"]
DATA_FILE = "expenses.json"

def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump([
            {
                "title": e["title"],
                "amount": e["amount"],
                "category": e["category"],
                "date": e["date"].strftime('%Y-%m-%d')
            } for e in expenses
        ], f)

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                expenses.append({
                    "title": item["title"],
                    "amount": item["amount"],
                    "category": item["category"],
                    "date": datetime.datetime.strptime(item["date"], '%Y-%m-%d').date()
                })

def main(page: ft.Page):
    page.title = "💸 Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    load_expenses()

    title = ft.Text("💰 Expense Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN)

    dropdown = ft.Dropdown(
        label="Filter by Month",
        options=[ft.dropdown.Option(month) for month in months],
        value="All",
        on_change=lambda e: [refresh_ui(), update_pie_chart()]
    )

    amount_input = ft.TextField(label="Amount", keyboard_type="number", width=120)
    title_input = ft.TextField(label="Title", width=160)
    category_input = ft.TextField(label="Category", width=140)
    date_picker = ft.DatePicker(first_date=datetime.date(2023, 1, 1), last_date=datetime.date.today())
    page.overlay.append(date_picker)
    
    # Inisialisasi SnackBar di awal
    snack_bar = ft.SnackBar(
        content=ft.Text(""),
        action="OK",
        on_action=lambda e: setattr(page.snack_bar, "open", True)
    )
    page.snack_bar = snack_bar

    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True
    )

    def show_notification(message, duration=4000, bgcolor=None):
        page.snack_bar.content = ft.Text(message)
        page.snack_bar.bgcolor = bgcolor or ft.Colors.BLUE_GREY
        page.snack_bar.duration = duration
        page.snack_bar.open = True
        page.update()

    def update_pie_chart():
        month = dropdown.value
        category_totals = defaultdict(float)

        for exp in expenses:
            exp_month = exp["date"].strftime('%B')
            if month == "All" or exp_month == month:
                cat = exp["category"]
                amt = exp["amount"]
                category_totals[cat] += amt

        pie_chart.sections = [
            ft.PieChartSection(
                value=amt,
                title=f"{cat}\n{format_rupiah(amt)}",
                color=ft.Colors.CYAN if i % 2 == 0 else ft.Colors.TEAL
            )
            for i, (cat, amt) in enumerate(category_totals.items())
        ]

        pie_chart.update()

    def add_expense(e):
        if not amount_input.value or not title_input.value or not category_input.value or not date_picker.value:
            show_notification("❗ Please fill in all fields!", bgcolor=ft.Colors.AMBER)
            return

        try:
            expenses.append({
                "title": title_input.value,
                "amount": float(amount_input.value),
                "category": category_input.value,
                "date": date_picker.value
            })
            save_expenses()
            amount_input.value = title_input.value = category_input.value = ""
            refresh_ui()
            update_pie_chart()
            show_notification("✅ Expense added successfully!", bgcolor=ft.Colors.GREEN)
        except Exception as e:
            show_notification(f"❌ Error: {str(e)}", bgcolor=ft.Colors.RED)

    def delete_expense(index):
        try:
            deleted_expense = expenses.pop(index)
            save_expenses()
            refresh_ui()
            update_pie_chart()
            show_notification(f"🗑️ Deleted: {deleted_expense['title']}", bgcolor=ft.Colors.GREY)
        except Exception as e:
            show_notification(f"❌ Error deleting: {str(e)}", bgcolor=ft.Colors.RED)

    add_button = ft.ElevatedButton("➕ Add", on_click=add_expense, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
    input_row = ft.ResponsiveRow([
        title_input,
        amount_input,
        category_input,
        ft.ElevatedButton("📅 Pick Date", on_click=lambda _: [setattr(date_picker, "open", True), page.update()]),
        add_button
    ], spacing=10, run_spacing=10)

    total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER)
    expense_list = ft.Column()
    category_bars = ft.Column()

    def refresh_ui():
        month = dropdown.value
        filtered = []
        total = 0
        chart_data = defaultdict(float)
        for idx, exp in enumerate(expenses):
            exp_month = exp["date"].strftime('%B')
            if month == "All" or exp_month == month:
                filtered.append((idx, exp))
                total += exp["amount"]
                chart_data[exp["category"]] += exp["amount"]

        category_bars.controls.clear()
        for cat, amount in chart_data.items():
            percent = (amount / total) if total else 0
            category_bars.controls.append(
                ft.Column([
                    ft.Text(f"{cat} - {format_rupiah(amount)} ({percent*100:.1f}%)"),
                    ft.ProgressBar(value=percent, color=ft.Colors.LIGHT_BLUE_ACCENT)
                ])
            )

        expense_list.controls.clear()
        for idx, exp in filtered:
            card = ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(exp["title"], weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text(f"{format_rupiah(exp['amount'])} | {exp['category']} | {exp['date'].strftime('%d %b %Y')}", color=ft.Colors.GREY_400)
                        ], spacing=5),
                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e, i=idx: delete_expense(i), icon_color=ft.Colors.RED_ACCENT)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=15
                ),
                elevation=3,
                color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                shape=ft.RoundedRectangleBorder(radius=10)
            )
            expense_list.controls.append(card)

        total_text.value = f"Total untuk {month}: {format_rupiah(total)}"
        page.update()

    # Final layout
    page.add(
        ft.Column([
            title,
            dropdown,
            input_row,
            total_text,
            ft.Container(content=pie_chart, width=400, height=400),
            ft.Divider(),
            category_bars,
            ft.Divider(),
            expense_list
        ])
    )

    refresh_ui()
    update_pie_chart()

ft.app(target=main)
