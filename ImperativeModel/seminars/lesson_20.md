# 20. Некоторые важные моменты
## Оператор break

Это известный во многих массовых императивных языках оператор немедленно прерывает некоторый блок кода (на концепции блока кода основаны Java, C#, C++...), передавая управление внешнему блоку. Проблема в контексте современных трендов движения в параллелизм в том, что break может выполняться внутри некоторой "нити", которая работает одновременно с другими. Например, break вызывается из тела цикла, которое в модели одновременного выполнения потенциально может выполняться "параллельно" с другими итерациями (пример на Julia мы разбирали в первом курсе "как понять в программировании всё"). В таком случае непонятно, что делать, если работа цикла в одной из нитей прерывается, однако другие итерации, другие "тела" цикла в других нитях ещё продолжают работу. Надо ли прерывать их работу?

Правильный ответ: нет, прерывать работу других нитей в таком случае нельзя, однако в целом такое неоднозначное выполнение цикла желательно завершать исключительной ситуацией.

## Декларативные объекты и идентичность

Мы рассматривали, как строить декларативный объект, который объединяет состояние и операции безопасным способом. Однако упущен такой аспект декларативных объектов, как их идентичность. Так как декларативные объекты иммутабельны -- после выполнения операции модификации каждый раз создаётся новый экземпляр, часто требуется понимать, что этот новый экземпляр -- фактически "тот же самый" по смыслу объект, который был и до этой операции. В императивном программировании с состояниями это реализуется прозрачно -- хранением ссылки на однократно созданный объект в переменной на протяжении всей программы. В случае декларативного подхода оказывается полезным добавлять в декларативные АТД операции, которые выдают некоторый уникальный идентификатор (число или строку) этого объекта.

## Эмуляция состояния в декларативной модели

Некоторые мутабельные структуры данных можно эмулировать в декларативной модели. Имеется обновляемый контейнер (например, список/массив ячеек, значения которых можно как считывать, так и менять). Считывание значения i-й ячейки декларативно реализуется прозрачно с помощью рекурсии. Обновление значения i-й ячейки декларативно реализуется также рекурсивно созданием новой копии списка, где вместо i-й ячейки создаётся и подставляется новая ячейка с новым значением.