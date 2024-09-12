# 6. Правильность/корректность кода (продолжение)
Конечно, программа, правильность которой доказана, всё равно может выдавать некорректные результаты, если например с ошибками реализована система, на которой она реализована и выполняется (компилятор, рантайм, ОС, процессор...).

Одна из классических форм доказательства правильности -- это математическая индукция. Сперва мы доказываем, что программа корректна для простого случая. Затем мы доказываем, что если программа корректна для некоторого данного случая, то она будет корректна и для следующего случая. Из этих двух моментов делается вывод, что программа корректна в целом.

Например, есть пустой список [] или список с одним или несколькими элементами, и из данного списка T следует его продолжение H|T -- мы получили корректное определение списка (иногда такой подход называют рекурсивным типом данных).
