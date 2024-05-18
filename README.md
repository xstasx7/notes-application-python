    
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


