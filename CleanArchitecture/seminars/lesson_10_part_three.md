Для удобства хранения мутабельного состояния мы создали нашему API обёртку в виде класса.

Сам класс определён как callable с помощью специфичного для Python приёма -- когда с помощью внутренней функции __call__ класс можно вызывать как обычную функцию. А в функциональных языках такой способ обычно поддерживается естественным образом.

Наш интерфейс -- это единственная функция api(), которая на входе получает строку-команду. Внутри она настраивается методом setup, который получает список конкретных вызываемых функций, реализующих нужный интерфейс.

Метод make разбирает входную строку и вызывает соответствующую функцию, реализация которой настраивается независимо.

Смена реализации нашего интерфейса -- единственной функции api() -- выполняется так же прозрачно, одной строкой. Например, реализация, где перемещение происходит на вдвое большее расстояние, меняется одной строчкой.

Важно, что нашей api-функции не требуется конструктор. И ещё один серьёзный плюс -- возможность тестирования клиентской части путём подмены (техника mock) функции api на отладочную, что в нашем случае возможно одним оператором.

Далее рассмотрим второй вариант функциональной реализации.