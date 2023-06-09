Связанный (связный) список
Прочитайте обязательно:
Введение
Асимптотический анализ

Связанный (связный) список -- это набор "элементарных" данных (например, чисел или строк), каждое из которых связано с другим данным "связью", извините за тавтологию. Каждое элементарное данное вместе со своей "связью" называется узел.

В простейшем случае узел просто связывается со следующим узлом, получается цепочка узлов, по которой мы можем передвигаться от начала к концу (от конца к началу не можем, так как связь организована только в одну сторону). Конец списка обозначается так: связь последнего узла указывает на None.

Важное отступление про "указатели".

Общая идея, во многих языках программирования, что значение любого типа -- это объект, который хранится где-то в памяти, а переменная, в которую мы "записываем" этот объект, на самом деле хранит не его, а указатель на место в памяти, где реальный объект находится (адрес в памяти, номер ячейки памяти условно, ссылка). Поэтому когда мы записали в переменную x объект (экземпляр класса, список, ...):
x = Cat()
а потом делаем
y = x
то мы не копируем сам объект Cat, а копируем только его адрес в памяти. По сути, и x и y указывают на один и тот же объект! И при обращении к любой из них будет меняться один и тот же объект. Это так называемая передача значения по ссылке.

Исключение делается обычно для чисел и строк -- они действительно в присваивании полноценно копируются (это так называемая передача по значению).

Отличие связанного списка от массива, например, в том, что в связанном списке мы можем легко вычленить его часть, взяв за начало любой элемент списка. Кроме того, операции добавления и удаления элементов выполняются очень эффективно, всего за два шага. И в памяти связанный список хранится иначе, нежели массив: узлы списка могут быть разбросаны в памяти произвольно, а массив обычно занимает непрерывную область памяти.

Когда мы храним данные в обычном массиве, то они, как правило, располагаются в памяти сплошным блоком, каждое следующее значение вплотную после предыдущего. В таком случае, зная индекс элемента, мы можем получить его за O(1), просто взяв сдвиг в байтах i-го элемента относительно нулевого (зная, сколько байтов элемент соответствующего типа занимает в памяти). Но если массив очень большой, могут возникнуть серьёзные проблемы с его полноценным размещением в памяти одним блоком. Связные списки, с другой стороны, за счёт использования указателей допускают совершенно свободное размещение любого элемента где угодно в памяти, однако расплатой за это становится прямой доступ к элементам за O(N). Впрочем, на практике такой доступ и не требуется: обычно важно быстро получать лишь голову и хвост списка [CS106B].

Преимущества и недостатки связного списка:
1. Динамический размер. Связанный список -- это динамическая структура данных, которая может увеличиваться или уменьшаться в размере во время выполнения, в отличие от массива, который имеет фиксированный размер. Это происходит потому, что связанные списки выделяют память только тогда, когда это необходимо, а значит, могут эффективно обрабатывать такие операции, как вставка и удаление.
2. Непрерывная память: В отличие от массивов, связные списки не хранят данные в смежных областях памяти. Вместо этого связные списки используют указатели для хранения адреса следующего узла.
3. Вставка и удаление: Связные списки обеспечивают эффективные операции вставки и удаления, особенно в случае хранения больших наборов данных. Эти операции требуют только изменения указателей затронутых узлов, что делает их более быстрыми, чем в массивах, где эти операции требуют сдвига элементов.
4. Отсутствие прямого доступа: Связные списки не поддерживают прямой доступ к элементам по индексу. Это означает, что вы не можете получить прямой доступ к элементу в середине списка без предварительного просмотра всех элементов перед ним (за O(N) в наихудшем случае). Это недостаток по сравнению с массивами, которые позволяют осуществлять произвольный доступ за O(1).
[CS124].

Нам потребуется определить два класса: Node, который определяет узел, и LinkedList, который собственно и задаёт связанный список.

В классе Node будут два элемента: value (само данное) и next -- "связь", по сути указатель на следующий узел. Если данный узел финальный, поле next будет хранить None.

class Node:
    def __init__(self, v):
        self.value = v
        self.next = None
Класс LinkedList -- это по сути "обёртка", синтаксический сахар для узлов. Ведь мы уже можем работать с узлами напрямую:

n1 = Node(12)
n2 = Node(55)
n1.next = n2 # 12 -> 55
Давайте реализуем основные функции для работы с связанным списком.

class LinkedList:  
    def __init__(self):
        self.head = None
        self.tail = None
Поле head -- это по сути указатель на узел-голову списка, а поле tail -- это указатель на завершающий узел.

Добавим метод add_in_tail(), который добавляет новый узел в конец списка:

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item
Теперь для удобства создадим метод отладочного вывода списка:

def print_all_nodes(self):
        node = self.head
        while node is not None:
            print(node.value)
            node = node.next
Сформируем наш список из трёх элементов:

s_list = LinkedList()
s_list.add_in_tail(n1)
s_list.add_in_tail(n2)
s_list.add_in_tail(Node(128))
s_list.print_all_nodes()
Будет напечатано 12 55 128

Теперь нам надо найти нужный узел по заданному значению:

    def find(self, val):
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None
nf = s_list.find(55)
if nf is not None:
    print(nf.value)
Разрешать ли изменять значение некоторого узла в списке (менять значение его поля value)? В общем случае это нежелательно -- всегда лучше исходить из того, что наш связанный список иммутабелен, и любые операции над ним не меняют содержимое его узлов.

[ предыдущее занятие ]

Задание.
Пункты, помеченные * реализуйте отдельно.


1.1. Добавьте в класс LinkedList метод удаления одного узла по его значению
delete(val, all=False)

где флажок all=False по умолчанию -- удаляем только первый нашедшийся элемент.
1.2. Дополните этот метод удалением всех узлов по конкретному значению (флажок all=True).

1.3. Добавьте в класс LinkedList метод очистки всего содержимого (создание пустого списка) -- clean()

1.4. Добавьте в класс LinkedList метод поиска всех узлов по конкретному значению (возвращается стандартный питоновский список найденных узлов).

find_all(val)
1.5. Добавьте в класс LinkedList метод вычисления текущей длины списка -- len()

1.6. Добавьте в класс LinkedList метод вставки узла newNode после заданного узла afterNode (из списка)
insert(afterNode, newNode)

Если afterNode = None, добавьте новый элемент первым в списке.
Например, имеется список (a1,a2,a3,a4,a5) и новый узел a7;
вставляя узел a7 после узла a3, получаем список (a1,a2,a3,a7,a4,a5).

В целом, и этот метод, и другие -- слабая (уязвимая) версия интерфейса списка, она так сделана умышленно, а как правильно проектировать подобные классы, разбираем на треке по объектно-ориентированному анализу и проектированию на примерах из занятий данного курса.

1.7. Напишите проверочные тесты для каждого из предыдущих заданий.

* 1.8. Напишите функцию, которая получает на вход два связанных списка, состоящие из целых значений, и если их длины равны, возвращает список, каждый элемент которого равен сумме соответствующих элементов входных списков.

Рекомендации по тестированию.
Проверяйте случаи, когда список пустой, содержит много элементов и один элемент: как в таких ситуациях будет работать удаление одного и нескольких элементов, вставка, поиск. Особое внимание уделите корректности полей head и tail после всех этих операций.