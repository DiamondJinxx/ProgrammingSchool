# 28. Категории наследования

## 1. Наследование подтипов (subtype inheritance)

Это классическая форма наследования, когда некоторая родительская категория естественно разделяется на достаточно очевидные и независимые подкатегории. Например, "Гоночный автомобиль", который будет применяться только в гонках, и "Такси", которое будет использоваться только для перевоза пассажиров в городе, удобно представить потомками класса "Автомобиль". Часто наследование подтипов напрямую отражает классические иерархии в естественных науках.

Однако даже в такой простой форме наследования практически всегда присутствует неопределённость: по каким критериям разделять классы-потомки? Эта тема более подробно рассматривается на следующем курсе по проектированию.

В данном виде наследования родительский АТД всегда представляется в форме либо абстрактного, либо частично реализованного класса.

Потомок всегда специализирует родительский тип какими-то уникальными характеристиками, и множество его экземпляров всегда будет подмножеством множества экземпляров предка. Кроме того, все потомки задают непересекающиеся друг с другом подмножества экземпляров.

## 2. Наследование с ограничением (restriction inheritance)

В данном случае экземпляры класса-потомка представляют собой частный, но важный случай класса-предка. Этот частный случай вытекает из дополнительного ограничения, накладываемого на родительские характеристики. Например, "Такси" можно разделить на "Пассажирское такси" и "Грузовое такси". При этом, важно, родительский класс не расширяется новыми возможностями, а наоборот ограничивается -- например, вводится ограничение на допустимую область применения (что не исключает появления новых атрибутов класса, например, количество пассажирских мест или грузовых мест, которые однако остаются только необходимым следствием такого ограничения).

Этот вид наследования весьма схож с базовым видом subtyping. Как правило, семантически он относится не к классам, а к экземплярам, физическим объектам, на которые наложены определённые измеряемые ограничения.

## 3. Наследование с расширением (extension inheritance)

Данный вид наследования, в противоположность наследованию с ограничением, нацелен на расширение уже самого класса-предка новыми возможностями, никак не применимыми к объектам родительского класса. В результате, в частности, множество объектов класса-потомка B перестаёт быть подмножеством множества экземпляров класса-предка А, хотя такое отношение сохраняется в обратном порядке -- применительно к множеству А как подмножеству множества B.

Наследование с расширением может быть похожим на наследование с ограничением, когда мы вроде бы "расширяем" родительский класс Такси спецификой грузовой или пассажирской перевозок, хотя на самом деле это всё же специализация. В то же время класс "Беспилотный автомобиль" будет скорее полноценным расширением класса "Автомобиль" -- для него становятся допустимыми операции наподобие "смена прошивки робота-водителя", никак не применимые к родительскому классу "Автомобиль".

Кроме того, часто наследование с расширением применяется в математике и computer science -- например, специализированные списки могут расширять родительский класс List качественно новыми операциями.

Один из прикладных критериев выбора между специализацией и расширением -- это добавление нескольких схожих классов в специализации, и как правило добавление единственного, но семантический более общего класса при расширении.
