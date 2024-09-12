# 9. Dependency injection (разделяем интерфейс и реализацию)

Теперь вернёмся немного назад, к ООП, и посмотрим, какие есть хорошие способы для разделения интерфейсов (которые не следует путать с API) и их реализации. До сих пор мы напрямую работали непосредственно с реализацией, теперь попробуем её изолировать. Для этого воспользуемся классическим паттерном Dependency injection (внедрение/инъекция зависимостей).

Идея этого паттерна -- максимальное по возможности разделение исполнительских функций между объектами, чтобы каждый занимался исключительно собственной работой. При этом внутренняя реализация этой работы скрывается за интерфейсом. По сути, мы пытаемся развязать все возможные связки в системе через такие интерфейсы, ну а побочным эффектом этого паттерна часто становится не упрощение, а усложнение самого кода (хотя формально сложность связей в системе действительно снижается).
