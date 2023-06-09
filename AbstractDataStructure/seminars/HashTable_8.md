# Хэширование
1. Хэш-таблицы и хэш-функции

Когда мы будем знакомиться с алгоритмами поиска, то узнаем, что в общем случае сложность поиска нужного элемента в упорядоченном массиве (когда есть возможность обращаться к произвольным элементам по индексу) можно снизить с O(n) до O(log n). Однако существуют структуры данных, которые ориентированы на максимально быстрый поиск нужной информации (проверку её наличия в хранилище), буквально за время O(1). Такие структуры называются хэш-таблицы.

Идея хэш-таблицы в том, что по значению содержимого i-го элемента таблицы мы можем быстро и однозначно определить сам индекс i (говорят - слот). Такое вычисление слота выполняет специальная хэш-функция.

Если диапазон значений, хранимых в таблице, не превышает её размер, то хэш-функция элементарна. Например, мы хотим хранить байты (значения от 0 до 255) в таблице размером 256 элемента. В таком случае хэш-функция f(x) = x : само значение элемента и есть его индекс в таблице. Мы просто смотрим, имеется ли значение N в таблице по индексу N.

Но идея хэш-таблиц в другом: мы хотим хранить значения потенциально очень широкого диапазона (например, строки) в таблице маленького размера (например, 128 элементов). При этом мы исходим из того, что и хранимые данные по своей уникальности примерно близки своим количеством размеру хэш-таблицы. Мы можем, например, суммировать байты каждой строки, брать остаток от деления суммы на 128, и таким образом получать уникальный индекс.

Простейшая реализация хэш-таблицы может быть создана с помощью связного списка, содержащего пары ключ-значение. Сложность нахождения ключа будет O(N), а добавление ключа вроде бы может быть выполнено за O(1), но т.к. надо проверить весь список (нету ли в нём уже такого ключа), добавление ключа тоже оказывается O(N).
Такую реализацию можно существенно ускорить, если хранить не одну, а множество коротких связных списков, каждый в отдельном элементе массива. Но в таком случае требуется хорошая хэш-функция, которая раскладывала бы ключи в индексы массива (диапазоны ключей в цепочках). В простейшем случае для простых случаев (например, хранение фамилий) массив может хранить 33 связных списка, а преобразование ключа-фамилии в его индекс прозрачно выполняется по первой букве фамилии (хотя в целом, очевидно, распределение фамилий по 33 буквам не будет равномерным) [B16].

Хэш-таблицы активно используются, например, в базах данных, но при этом к ним предъявляются повышенные требования в плане консистентности, т.к. сразу несколько потоков могут получать доступ к ключам-значениям и их модификацию. Для этого вводится поддержка транзакций, что позволяет объединять несколько операций в одну атомарную транзакцию, которая либо выполняется полностью, либо не выполняется вообще (что делать в случаях, когда несколько транзакций п

Большая проблема в том, что идеальную хэш-функцию придумать подчас очень трудно или невозможно. В нашем случае самые разные строки могут выдавать один и тот же слот -- такая ситуация называется коллизией. Решается эта проблема, во-первых, подбором оптимальной хэш-функции, которая минимизирует количество коллизий, и во-вторых, так называемым разрешением коллизий, когда несколько разных значений претендуют на один слот.

2. Методы разрешения коллизий

Существует довольно много методов разрешения коллизий. Один из самых простых, не требующих дополнительного объёма памяти -- это метод линейного разрешения, частным случаем которого считается метод последовательных проб.

Значение, попадающее в слот, который уже занят, перемещается к следующему слоту (в общем случае, "перепрыгивает" через N слотов), где проверяется, свободен ли он. Такой поиск продолжается циклически, и желательно продумывать размер хэш-таблицы и размер шага такими, чтобы при длительном поиске в конечном итоге охватывалось бы всё её пространство -- с неоднократным прохождением по таблице. Или как минимум, чтобы индекс, дойдя до конца таблицы, продолжал бы с её начала, пока не превысил бы исходно выбранный слот. Шаг N может быть не фиксированным, а например, растёт квадратично: 1,2,4,8,...

Недостаток данного метода в том, что подчас эффективность поиска может быть очень плохой, когда коллизий много и приходится многократно пробегать по всей таблице, которая сильно заполнена. А когда в ней вообще нету свободных слотов, добавление элемента становится невозможным, в таких случаях обычно используют динамические массивы. Кроме того, в линейном разрешении нередко проявляется проблема кластеризации -- занятые слоты группируются в кластеры, которые замедляют поиск свободных ячеек.

Полностью снимает эти проблемы метод цепочек. Он подразумевает хранение в каждом слоте не одного значения, а целого списка значений. В него записываются все значения, для которых хэш-функция его выбрала. Недостаток -- необходимость ведения таких списков и ощутимое замедление работы, если коллизии возникают часто, и приходится дополнительно сканировать длинные списки. Более того, если все значения будут попадать в одну ячейку, мы получим среднее время выборки, пропорциональное O(N). В таком случае использование хэш-таблицы вообще теряет смысл, можно просто задействовать связанные списки например.

Существуют также подходы, когда для разных диапазонов ключей больше подходят разные хэш-функции, и в таких случаях создаются массивы хэш-таблиц, каждая со своей хэш-функцией. Это т.н. Locality-Sensitive Hashing, когда похожие объекты с высокой вероятностью группируются в своих таблицах. Но как выявлять похожесть, тоже проблема. На практике она решается например так, что когда ключи попадают в один слот таблицы, коллизия разрешается добавлением связного списка (или ещё одной хэш-таблицы), хранящего все ключи-значения в данном слоте [B16].

В 2001-м был также разработан алгоритм кукушкиного хэширования для разрешения коллизий, когда используется несколько хэш-функций. Он особенно хорош для случаев, когда используется большое число ключей. Каждому ключу находится уже не одна, а несколько позиций в таблице. Если все они заняты, то соответствующим ключам подыскиваются альтернативные места, и т. д. В редких случаях, когда возникают бесконечные циклы, вся таблица перестраивается с новыми хэш-функциями. Такой подход на практике весьма эффективен: он позволяет избежать довольно накладных разрешений коллизий с помощью связных списков, однако в наихудшем случае он работает за O(N), т.к. перестраивается вся таблица [CS124].

В качестве компромиссного был придуман метод двойного хэширования, когда используются две совершенно разные хэш-функции h1() и h2(). Если слот k = h1(v) занят, тогда вычисляется h1(v) + i * h2(v) по модулю длины таблицы, где i принимает значения от 1 до длины таблицы - 1. Особое требование к h2(), чтобы она возвращала индексы слотов, взаимно простые с длиной таблицы. Например, эту длину можно взять простым числом, тогда h2() будет возвращать натуральные числа, меньшие этой длины.

Ещё один вариант разрешения коллизий -- хэширование Робин Гуда, ориентированная на минимизацию разброса элементов по таблице (когда более "богатые" в плане близости к идеальному месту элементы немного жертвуют своей позицией в пользу слишком далёких "бедных") [CS 124].

Хэш-таблицы иногда также реализуются способом, похожим на динамический "массиво-список": вычисляется слот, где хранится не один элемент, а целый блок, массив фиксированного размера, или динамический массив. Эта реализация напоминает разрешение коллизий с помощью цепочек, только здесь мы не разрешаем коллизии, а наоборот, пытаемся избавиться от их возникновения, оптимизируя структуру под работу хэш-функций. Этот подход похож на случай, когда вы ищете в словаре нужное слово, и не занимаетесь линейным поиском с самого начала, а сразу пропускаете много страниц и переходите к "примерно" нужному месту, где начинаете искать уже по конкретным страницам (например, двоичным поиском).
В частности, такая схема хорошо подойдёт, когда такая хэш-таблица должна хранить типы-генерики (значения разных типов), и сперва выбирается хранилище для конкретного типа, вычисляя "хэш" по самому типу, а затем уже внутри нужного блока применяем наиболее подходящий элемент с учётом специфики хэширования значений конкретного типа.

3. Реализация

В классе хэш-таблицы потребуются два параметра: размер хэш-таблицы (желательно простое число, для экспериментов можно например брать 17 или 19), и длину шага (количество слотов) для поиска следующего свободного слота (например, 3).

```
class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size
```
      
В этом классе требуется реализовать четыре метода:

- хэш-функцию hash_fun(value), которая по входному значению вычисляет индекс слота;

- функцию поиска слота seek_slot(value), которая по входному значению сперва рассчитывает индекс хэш-функцией, а затем отыскивает подходящий слот для него с учётом коллизий, или возвращает None, если это не удалось;

- put(value), который помещает значение value в слот, вычисляемый с помощью функции поиска;

- find(value), который проверяет, имеется ли в слотах указанное значение, и возвращает либо слот, либо None.

Напишите тесты, которые проверяют работу этих четырёх методов.