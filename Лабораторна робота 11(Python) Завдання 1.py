import csv

def read_csv_file(file_path):
    #Зчитування даних з CSV файлу з обробкою помилок
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"Помилка: Файл {file_path} не знайдено.")
        return []
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        return []

def filter_data(data, year, min_value, max_value):
    #Фільтрація даних за роком та діапазоном значень.
    filtered_data = []
    for row in data:
        try:
            value = float(row[year]) if row[year] else None
            if value is not None and min_value <= value <= max_value:
                filtered_data.append(row)
        except ValueError:
            print(f"Неможливо обробити значення для країни {row['Country Name']}")
    return filtered_data

def save_to_csv(file_path, data, fields):
    #Збереження відфільтрованих даних у новий CSV файл.
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
        print(f"Дані успішно збережено у файл {file_path}")
    except Exception as e:
        print(f"Помилка при записі файлу: {e}")

def main():
    # Шлях до вхідного файлу з даними
    input_file_path = 'exports_data.csv'
    output_file_path = 'filtered_exports_data.csv'
    
    # Зчитування даних з файлу
    data = read_csv_file(input_file_path)
    if not data:
        return

    print("Вміст файлу:")
    for row in data:
        print(row)

    try:
        min_value = float(input("Введіть мінімальне значення для фільтрації: "))
        max_value = float(input("Введіть максимальне значення для фільтрації: "))
    except ValueError:
        print("Помилка: введіть числове значення для діапазону.")
        return

    # Фільтрація даних для 2015 та 2019 років
    filtered_data_2015 = filter_data(data, '2015', min_value, max_value)
    filtered_data_2019 = filter_data(data, '2019', min_value, max_value)

    # Збереження результатів, якщо дані відповідають обом рокам
    final_filtered_data = []
    for row in data:
        year_2015_valid = row['2015'] and min_value <= float(row['2015']) <= max_value
        year_2019_valid = row['2019'] and min_value <= float(row['2019']) <= max_value
        if year_2015_valid and year_2019_valid:
            final_filtered_data.append(row)

    # Збереження результатів у новий файл
    if final_filtered_data:
        save_to_csv(output_file_path, final_filtered_data, data[0].keys())
    else:
        print("Немає даних, що відповідають зазначеному діапазону.")

if __name__ == "__main__":
    main()





