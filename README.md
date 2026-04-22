# Calculator App (Stage 1-3)

Консольное приложение-калькулятор с поэтапной реализацией требований лабораторной работы.

## 1. Что умеет приложение
- Stage 1: `+`, `-`, `*`, `/`, целые и нецелые числа.
- Stage 2: научная нотация (`1.25e+09`), `^`, скобки.
- Stage 3: `sqrt`, `sin`, `cos`, `tg`, `ctg`, `ln`, `exp`, константы `pi`, `e`, флаг углов (`radian/degree`).

## 2. Безопасность
- Вычисление выполняется через собственный парсер и AST.
- `eval`/`exec` и выполнение произвольного кода не используются.

## 3. Структура проекта
- `task.md` — исходная формулировка задания.
- `spec.md` — спецификация требований.
- `calc.py` — CLI входная точка.
- `calculator/` — парсер, AST, вычислитель, API.
- `tests/` — unit/integration/functional/load тесты.
- `scripts/run_tests.py` — единый запуск тестов и генерация stage-отчетов.
- `reports/` — сохраненные отчеты:
  - `stageN_test_report.txt` — секции парсера/вычислителя/интеграции (и дополнительные секции для stage3);
  - `stage3_load_report.txt` — текстовый лог нагрузочных тестов с полным входом, выходом и временем.
- `benchmarks/benchmark.py` — benchmark-скрипт.
- `reports/benchmark_output.txt` — сохранённые результаты benchmark.

## 4. Запуск приложения
```bash
python calc.py "2 + 3 * 5"
python calc.py "3.375e+09^(1/3)"
python calc.py "sin(pi/2)"
python calc.py --angle-unit=degree "sin(90)"
```

## 5. Коды возврата
- `0` — успех.
- `1` — ошибка парсинга или вычисления.

## 6. Тесты (одной командой)
Текущий этап (по умолчанию stage3):
```bash
python scripts/run_tests.py
```

Явный запуск этапа:
```bash
python scripts/run_tests.py --stage stage1
python scripts/run_tests.py --stage stage2
python scripts/run_tests.py --stage stage3
```

Что делает команда:
- запускает все `unittest` тесты;
- формирует структурированный отчет по выбранному stage:
  - Stage 1: `парсер`, `вычислитель`, `интеграционные`;
  - Stage 2: `парсер`, `вычислитель`, `интеграционные`;
  - Stage 3: `парсер`, `вычислитель`, `интеграционные`, `функциональные CLI`, `единицы углов`;
- для Stage 3 дополнительно формирует отдельный текстовый нагрузочный отчет.

## 7. Benchmark
```bash
python benchmarks/benchmark.py
```
Результат печатается в консоль и сохраняется в `reports/benchmark_output.txt`.

## 8. Git stages
- `tag: stage1` — базовый калькулятор + `spec.md` + unit-тесты.
- `tag: stage2` — scientific notation + `^` + скобки + интеграционные тесты.
- `tag: stage3` — функции/константы/CLI angle-unit + functional/load + benchmark.

