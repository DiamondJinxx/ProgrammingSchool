# 33. Встраивание

Встраивание -- это техника, когда мы не формируем полную структуру данных за один раз, при обращении к любому её элементу, а строим её постепенно, по мере запросов, как бы "встраивая" внутрь неё программный код, генерирующий нужные данные.

Например, если требуется список из миллиона линейно увеличивающихся чисел, и запрашивается самый первый элемент, то достаточно сгенерировать список только из этого одного элемента. Такая схема вычислений называется ленивой в противоположность жадной, когда сразу вычисляется всё.

# Абстракция цикла
Как мы видели, циклы в декларативной модели как правило многословны, потому что им нужны явные рекурсивные вызовы. Эти рекурсивные петли можно сделать более лаконичными и универсальными, определяя их в виде абстракций. Существует много различных видов циклов, которые мы можем определить в декларативной модели.

В этом разделе мы сначала определим простые циклы в духе классических "for" в императивном программировании -- для работы с целыми числами и списками, а затем добавим к ним аккумуляторы, чтобы сделать их более полезными.

# 33. Целочисленный цикл

Классический цикл For получает четыре параметра: начальное и конечное значения цикла и шаг, и процедуру P, которая должна быть применена к каждому значению условного "счётчика" цикла.
```
function For(A, B, S, P)
   if A > B
      return
   end 
   P(A)
   For(A+S, B, S, P)   
end

For(1,10,3,println) # печать значений 1,4,7,10
```
