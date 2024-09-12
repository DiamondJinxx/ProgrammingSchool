# 46. Правильная организация программы

Что такое правильная организация программы? Можно написать программу как один большой монолит, но по мере роста объёма он начинает стремительно запутываться. Лучший способ борьбы с растущей сложностью – разделить (декомпозировать) программу на логические единицы, каждая из которых реализует набор операций, каким-то образом связанный в одно целое (хороший подход – через абстрактные типы данных).

Каждая логическая единица имеет две части: интерфейс и реализацию. Только один интерфейс «виден» снаружи логического блока, а реализации могут свободно заменяться.

При таком подходе программа представляется направленным графом без циклов, где ребро между двумя логическими единицами означает, что первая нуждается во второй для своей реализации. В мэйнстриме такие логические единицы называют "модули" или "компоненты", хотя точных определений этих слов обычно не даётся. На данном курсе мы выясняем, какие тут существуют основные понятия и как их можно применять для создания небольших декларативных программ. Аналогичная тема в разрезе programming in large рассматривается на следующих курсах.

## Модули и функторы

Мы называем модулем часть программы, которая группирует связанные по смыслу операции в одну сущность, которая имеет интерфейс и реализацию. В декларативной модели модули могут быть внедрены простым способом:
- Интерфейс модуля представляет собой запись, которая группирует связанные сущности (как правило, процедуры и функции, но в целом разрешено всё, включая классы, объекты, и тому подобное);
- Реализация модуля представляет собой набор языковых сущностей, которые доступны через интерфейс, а всё остальное снаружи недоступно. Реализация скрыта с помощью лексической видимости.

Спецификации модулей будем рассматривать как сущности, отличные от самих модулей. Спецификация модуля -- это вид шаблона, который создает новый модуль (как класс «создаёт» объект в ООП). Спецификация модуля иногда называется программным компонентом, но к сожалению, термин " программный компонент" широко используется в программировании для обозначения множества самых разнообразных понятий. Поэтому спецификацию модуля мы будем называть функтор.
Функтор – это функция, получающая на вход набор модулей, которые требуются для создания нового модуля, и возвращает новый созданный модуль.

Строго говоря, функтор получает на вход интерфейсы модулей как аргументы, создаёт новый модуль и возвращает его интерфейс.

Функтор состоит из трёх частей:
- импорт, задающий перечень требуемых модулей;
- экспорт, определяющий интерфейс итогового модуля;
- реализация, включающая код инициализации функтора.

В терминах программной инженерии, программный компонент – это элемент для независимого развёртывания (не требующий ничего дополнительного для своей установки и использования, кроме, возможно, перечня стандартных библиотек). Главное, что программный компонент не имеет внутреннего состояния, поэтому хорошо укладывается в декларативную модель.

Функторы можно считать одним из видов программных компонентов; тогда модулем будет экземпляр программного компонента – результат инсталляции функтора в конкретном рабочем окружении. Такое окружение включает множество модулей, каждый из которых может иметь внутреннее состояние.

Приложение называется автономным (standalone), если оно не подразумевает активного взаимодействия с пользователем, как правило, через GUI. Оно состоит из главного функтора, который вычисляется при старте приложения и импортирует нужные модули, что в свою очередь приводит к вызову других функторов.

Вычисление, или «инсталляция» функтора выполняется в три шага.

Во-первых, идентифицируются модули, которые будут требоваться для его работы.

Во-вторых, выполняется код инициализации.

В-третьих, загружаются модули, которые непосредственно востребованы во время работы.

Вычисление не главных функторов может происходить в самое разное время работы программы, непосредственно в те моменты, когда в коде запрашивается некоторый ресурс из пока невычисленного функтора.

Это так называемое динамическое связывание, в противоположность статическому связыванию, когда все модули загружаются сразу в момент старта приложения.

В любой момент множество инсталлированных модулей называется рабочим модульным окружением.

# Поддержка модулей в Julia

В Julia поддерживается концепция модулей, весьма близкая к вышеописанной декларативной модели: docs.julialang.org/en/v1/manual/modules/

В качестве примера определим модуль MyList, содержащий функции для работы со списками.

Создадим файл MyList.jl, и обозначим его как модуль с соответствующим названием с помощью ключевого слова module, заканчивающегося end:

```
module MyList
 # ...
end
```
Мы определим в модуле три функции:
- Append(), которая добавляет новый элемент в хвост списку;
- Is(), которая проверяет, присутствует ли элемент в списке;
- Sort(), которая сортирует список.

Экспортируемые из модуля функции, типы и другие сущности (имена) задаются в разделе экспорта, после ключевого слова export.

Добавим для простоты стандартные реализации.

```
module MyList

export Append, Is, Sort, x, y

function Append(Ls, Elem)
  return vcat(Elem, Ls)
end

function Is(Ls, Elem)
  return Elem in Ls
end

function Sort(Ls)
  return sort(Ls)
end

x() = "x"
y = "y"
z() = "z"

end
```
Мы также добавили две функции x() и z(), одна из которых x() экспортируется из модуля, а другая z() доступна только внутри него. Кроме того, в модуль добавлена экспортируемая переменная y.


Как использовать модуль в своей программе? Это правильнее делать с помощью инструкции using или import, но они подразумевают, что модуль установлен в системе Julia с помощью менеджера пакетов. Поэтому для простоты воспользуемся такой схемой:
```
include("MyList.jl")

import .MyList: x

print( x() )
```
Сперва мы включаем с помощью include код модуля из файла MyList.jl, находящегося в текущем каталоге, в файл с данным кодом, который расположен в одном каталоге с MyList.jl.
Затем мы импортируем модуль MyList, что называется, in place – непосредственно из текущего файла, для чего ставим точку перед именем импортируемого модуля:

import .MyList
Наконец, после имени импортируемого модуля через двоеточие задаётся перечень импортируемых из этого модуля имён:

import .MyList: x
Выполняя import или using, мы вызываем функтор MyList, который создаёт и возвращает «экземпляр» модуля MyList со всем его физическим содержимым. Например, выполнив

import .MyList: x, y
мы получим в нашей программе полноценную переменную y, проинициализированную значением "y1".

Как видно, модуль как функтор вычисляется в реальном времени. Он вполне может содержать данные, рассчитываемые в момент вызова. Функтор может быть размещён в отдельном файле, и при этом он может быть совсем «лёгким» -- например, хранить один объект или класс.

Фактически функторы – это значения, однако в Julia модули позиционируются прежде всего как синтаксические единицы, как пространства имён для инкапсуляции и разграничения видимости. В любом случае, модули сегодня присутствуют практически в любом языке программирования и поддерживают схему компонентно-ориентированного программирования, которая особенно продуктивна в языках с динамической типизацией: компоненты (модули) создаются и гибко связываются в реальном времени. При этом полезная возможность, поддерживаемая в Julia – это предварительная компиляция модулей для их быстрой загрузки, если они не требуют ввода данных из внешнего мира.

Но следует помнить и о типичных проблемах иерархий модулей, когда потенциально возможны, например, закольцованные ссылки. Чем больше модулей в системе, тем тщательнее надо продумывать взаимосвязи между ними.
