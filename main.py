import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

DATA_FILE = "data/tasks.json"

# --- Работа с данными ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "history": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        messagebox.showerror("Ошибка данных", f"Не удалось загрузить данные: {e}")
        return {"tasks": [], "history": []}

def save_data(data):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        messagebox.showerror("Ошибка записи", f"Не удалось сохранить данные: {e}")

# --- Логика приложения ---
class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        
        self.data = load_data()
        
        self.create_widgets()
        self.update_history_list()
        self.update_type_filter()

    def create_widgets(self):
        # Текущая задача
        tk.Label(self.root, text="Ваша задача:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.current_task_label = tk.Label(self.root, text="Нажмите 'Сгенерировать'", wraplength=400, justify="center")
        self.current_task_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Кнопка генерации
        tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task).grid(row=2, column=0, columnspan=3, pady=10)

        # Фильтрация по типу
        tk.Label(self.root, text="Фильтр по типу:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.combo_filter_type = ttk.Combobox(self.root, values=["Все"])
        self.combo_filter_type.current(0)
        self.combo_filter_type.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=3, column=2, padx=10, pady=5)

        # История задач
        tk.Label(self.root, text="История задач:", font=('Arial', 12, 'bold')).grid(row=4, column=0, padx=10, pady=(20, 5), sticky="w")
        
        # Прокрутка для списка истории
        history_frame = tk.Frame(self.root)
        history_frame.grid(row=5, column=0, columnspan=3, padx=10, sticky="nsew")
        
        yscroll = ttk.Scrollbar(history_frame)
        yscroll.pack(side="right", fill="y")
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=yscroll.set, height=15)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        yscroll.config(command=self.history_listbox.yview)

    def generate_task(self):
        if not self.data["tasks"]:
            messagebox.showwarning("Предупреждение", "Список задач пуст. Добавьте задачи в файл или через код.")
            return

        task = random.choice(self.data["tasks"])
        
        # Добавляем в историю (если не было такой задачи в истории сегодня/последней?)
        self.data["history"].insert(0, task) # Вставляем в начало
        
        save_data(self.data)
        
        self.current_task_label.config(text=f"✅ {task['name']} ({task['type']})")
        self.update_history_list()

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for task in self.data["history"]:
            self.history_listbox.insert(tk.END, f"{task['name']} ({task['type']})")

    def update_type_filter(self):
        types = sorted({x["type"] for x in self.data["tasks"]})
        self.combo_filter_type["values"] = ["Все"] + types

    def apply_filter(self):
         selected_type = self.combo_filter_type.get()
         filtered_tasks = [x for x in self.data["tasks"] if selected_type == "Все" or x["type"] == selected_type]
         
         if not filtered_tasks:
             messagebox.showinfo("Фильтр", f"Нет задач типа '{selected_type}'")
             return

         task = random.choice(filtered_tasks)
         self.current_task_label.config(text=f"✅ {task['name']} ({task['type']})")
