# 18. Итеративные вычисления
Итак, мы добрались до практических ответов на вопрос "Как программировать в декларативной модели?".

Начнём с создания совсем простого вида программ: итеративные вычисления. Они начинаются с исходного состояния S0, и через серию последовательных трансформаций в S1, S2, ... достигают итогового состояния Sn.

Схема итеративных вычислений такая: имеется рекурсивная функция Iterate(Si), которая проверяет, является ли Si конечным состоянием Sn. Если это так, то она прекращает работу, иначе выполняет преобразование Si в Si+1, и вызывает саму себя с аргументом Si+1. На практике тут для удобства комбинируется несколько процедур.

Важная особенность такой схемы, что при итеративных вычислениях не формируется глубокий стек рекурсивных вызовов: по сути, этот стек вообще не нужен, так как никаких дополнительных вычислений над результатом работы не происходит, поэтому данная схема хорошо оптимизируется компилятором.

Например, классический факториал на Julia в декларативном формате запишется так:

```
function f(n, fin) 
  if fin == 1
     return n
  end 

  n = n * fin
  return f(n, fin-1)
end

println(f(1, 5)) # 120
```
Для наглядности в подобных случаях добавляют главную процедуру с одним параметром, которая выполняет начальные внутренние настройки и вызов рекурсивной функции с исходными аргументами.

# Абстракции управления

Далее полезно сделать следующий шаг и превратить нашу универсальную схему в абстракцию управления -- программный компонент, который может использоваться другими компонентами. Схема рекурсивного итеративного вычисления, как вы скорее всего заметили, очень похожа на классический оператор цикла while, только дополненный возвращаемым значением. Чтобы превратить схему в абстракцию управления, надо параметризовать её выделением частей, которые зависят друг от друга. В данном случае таких частей две: это проверка окончания вычислений и трансформация текущего состояния с получением следующего состояния. Каждую из частей можно представить как функцию с одним аргументом (сам аргумент в зависимости от задачи может быть достаточно сложной структурой данных).

Передача функций как аргументов в другие функции относится к группе техник в рамках программирования высшего порядка, рассматриваемых далее.

Получается следующая генерализованная функция нашей схемы -- по сути полноценный компонент, который теперь можно использовать в своих проектах.


```
function Iterate(S, IsDone, Transform) 
  if IsDone(S)
     return S
  end 

  S = Transform(S)
  return Iterate(S, IsDone, Transform) 
end
```
Первый параметр -- начальное состояние. Второй параметр -- функция IsDone, которая определяет, будет ли её аргумент (текущее состояние) результирующим. Функция Transform выполняет преобразование текущего состояния в следующее.

Например, для вычисления факториала по данной абстракции управления удобно будет использовать такое состояние, как список из двух элементов, где первый элемент -- текущее значение факториала, а второй -- понижающееся до 1 количество итераций, начиная с заданного (исходное число, факториал которого мы вычисляем).

```
function is_done(S)
  return S[end] == 1 
end

function transform(S)
  S1 = [S[1] * S[2], S[2] - 1] 
  return S1 
end
  
S = Iterate([1, 5], is_done, transform) # S = [120, 1]
```
В целом, это мощный способ структурировать программу, потому что он разделяет общие схемы управления и их конкретное использование. Программирование высшего порядка будет особенно полезно для такого структурирования.

Если подобная абстракция управления используется в проекте часто, то следующим шагом может стать предоставление её уже в качестве лингвистической абстракции (оператора языка).
