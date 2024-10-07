# 15. Сопровождение
Когда система создана и хорошо работает, мы должны убедиться, что она будет долго продолжать работать хорошо. Процесс поддержания качественной работоспособности системы после ее развёртывания называется сопровождением.

Как лучше всего структурировать системы, чтобы они были пригодны для продуктивного обслуживания?

**Проектирование компонентов.**

Существуют хорошие и плохие способы проектирования компонентов. Плохой способ, например, создать визуальную диаграмму, и декомпозировать её на кусочки, где каждый кусочек -- компонент. Гораздо лучше думать о компоненте как об абстракции.

Например, предположим, что мы пишем программу, которая использует списки. Тогда почти всегда хорошей идеей будет собрать все операции со списками в компонент, который задаёт абстракцию списка. В такой конструкции списки можно реализовывать, отлаживать, изменять и расширять, не затрагивая остальную часть программы. Если потом мы будем делать прикладную программу для работы со списками, которые слишком велики и не умещаются в оперативной памяти, достаточно будет изменить лишь сам компонент-список, чтобы хранить данные в файлах, а не в оперативной памяти.

**Инкапсуляция проектных решений.**

В более общем смысле можно сказать, что компонент должен инкапсулировать некоторое проектное требование (фичу). Таким образом, при изменении соответствующего проектного требования изменится только этот компонент. Это очень мощная форма модульности.
Полезность компонента можно оценить, посмотрев, какие изменения он позволяет внести. Например, если программа выполняет обработку текста, то решение о том, какую кодировку символов использовать, надо выделить в отдельный компонент, что упростит переход от одного текстового формата к другому.

**Избегайте изменения интерфейсов компонентов.**

Изменение интерфейса компонента всегда проблематично, поскольку все компоненты, которые зависят от измененного интерфейса, должны быть переписаны или перекомпилированы. Поэтому изменения интерфейса всегда следует избегать, однако на практике это практически невозможно -- как минимум, на фазе проектирования компонента. Всё, что мы можем сделать -- это минимизировать частоту таких изменений. Точнее говоря, интерфейсы часто используемых компонентов должны быть разработаны как можно более тщательнее с самого начала.