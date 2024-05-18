
"""
    Добавление заметки:
python notes.py add --title "новая заметка" --body "тело новой заметки" --format json
    Редактирование заметки:
python notes.py edit --id 1 --title "обновленный заголовок" --body "обновленное тело заметки" --format json
    Удаление заметки:
python notes.py delete --id 1 --format json
    Просмотр всех заметок:
python notes.py view --format json
    Просмотр заметок с фильтрацией по дате:
python notes.py view --filter-date "2024-05-18" --format json
"""

import json
import csv
import argparse
import os
from datetime import datetime


class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.note_id,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Note(
            note_id=data["id"],
            title=data["title"],
            body=data["body"],
            timestamp=data["timestamp"]
        )


# Сохранение и загрузка заметок из файлов JSON и CSV
def save_notes_to_json(filename, notes):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump([note.to_dict() for note in notes], file, ensure_ascii=False, indent=4)


def load_notes_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        notes_data = json.load(file)
        return [Note.from_dict(note) for note in notes_data]


def save_notes_to_csv(filename, notes):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["id", "title", "body", "timestamp"])
        for note in notes:
            writer.writerow([note.note_id, note.title, note.body, note.timestamp])


def load_notes_from_csv(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        return [Note.from_dict(row) for row in reader]


# Добавление, Редактирование, Удаление и Просмотр заметок
def add_note(notes, title, body):
    """
    Добавление заметок
    :param notes:
    :param title:
    :param body:
    :return:
    """
    note_id = len(notes) + 1
    timestamp = datetime.now().isoformat()
    new_note = Note(note_id, title, body, timestamp)
    notes.append(new_note)
    return new_note


def edit_note(notes, note_id, title, body):
    """
    Редактирование заметок
    :param notes:
    :param note_id:
    :param title:
    :param body:
    :return:
    """
    for note in notes:
        if note.note_id == note_id:
            note.title = title
            note.body = body
            note.timestamp = datetime.now().isoformat()
            return note
    return None


def delete_note(notes, note_id):
    """
    Удаление заметок
    :param notes:
    :param note_id:
    :return:
    """
    for note in notes:
        if note.note_id == note_id:
            notes.remove(note)
            return note
    return None


def view_notes(notes, filter_date=None):
    """
    Просмотр заметок
    :param notes:
    :param filter_date:
    :return:
    """
    if filter_date:
        return [note for note in notes if note.timestamp.startswith(filter_date)]
    return notes


# Обработка аргументов командной строки
def main():
    parser = argparse.ArgumentParser(description='Приложение для заметок')
    parser.add_argument('command', choices=['add', 'edit', 'delete', 'view'], help='Команда для выполнения')
    parser.add_argument('--title', help='Название заметки')
    parser.add_argument('--body', help='Тело заметки')
    parser.add_argument('--id', type=int, help='Идентификатор заметки')
    parser.add_argument('--filter-date', help='Фильтровать заметки по дате (YYYY-MM-DD)')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Формат файла для хранения заметок')

    args = parser.parse_args()

    filename = 'notes.' + args.format

    if args.format == 'json':
        notes = load_notes_from_json(filename) if os.path.exists(filename) else []
    else:
        notes = load_notes_from_csv(filename) if os.path.exists(filename) else []

    if args.command == 'add':
        if args.title and args.body:
            new_note = add_note(notes, args.title, args.body)
            print(f'Примечание добавлено: {new_note.to_dict()}')
        else:
            print('Для добавления примечания необходимы заголовок и текст.')

    elif args.command == 'edit':
        if args.id and args.title and args.body:
            edited_note = edit_note(notes, args.id, args.title, args.body)
            if edited_note:
                print(f'Примечание изменено: {edited_note.to_dict()}')
            else:
                print('Примечание не найдено.')
        else:
            print('Для редактирования заметки необходимы идентификатор, заголовок и текст.')

    elif args.command == 'delete':
        if args.id:
            deleted_note = delete_note(notes, args.id)
            if deleted_note:
                print(f'Примечание удалено: {deleted_note.to_dict()}')
            else:
                print('Примечание не найдено.')
        else:
            print('Для удаления заметки необходим идентификатор.')

    elif args.command == 'view':
        filtered_notes = view_notes(notes, args.filter_date)
        for note in filtered_notes:
            print(note.to_dict())

    if args.format == 'json':
        save_notes_to_json(filename, notes)
    else:
        save_notes_to_csv(filename, notes)



if __name__ == '__main__':
    main()
