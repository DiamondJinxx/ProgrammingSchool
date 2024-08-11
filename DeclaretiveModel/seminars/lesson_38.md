# 38. Filter

Другая универсальная операция над списками – это Filter, которая формирует новый список, в который включаются только те элементы исходного списка, которые соответствуют некоторому предикату. В Julia она называется filter().

Например, мы хотим выделить из исходного списка [1,2,3,4,5,6,7] только нечётные элементы; стандартная функция-предикат isodd() возвращает true, если её аргумент нечётный.

```
filter(isodd, [1,2,3,4,5,6,7]) # [1, 3, 5, 7]
```
Наша релизация Filter() может быть такой:
```
function Filter(Ls, F)

  function IterFilter(Rs, Ys, F)
    if Ys == []
        return Rs
    end

    head = Ys[1]
    tail = Ys[2:end]
    if F(head)
       return IterFilter(push!(Rs,head), tail, F)
    else
       return IterFilter(Rs, tail, F)
    end
  end

  return IterFilter([], Ls, F)
end

Filter([1,2,3,4,5,6,7], isodd) # [1, 3, 5, 7]
```