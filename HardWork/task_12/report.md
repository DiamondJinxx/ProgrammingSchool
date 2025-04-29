# Ясный код-2

## 2.1

```python
# Хоть класс и отвечает за загрузку данных, но загрузка в каждое конкретное облако это отдельная ответственность.
class DataUploader:

    def upload_to_google_cloud(self) -> None:
        ...

    def upload_to_mail_cloud(self) -> None:
        ...

    def upload_to_yandex_disk(self) -> None:
        ...

    def upload_to_vk_cloud(self) -> None:
        ...

    def upload_to_vk_cloud(self) -> None:
        ...
```

## 2.2

```python
# маленький класс, по сути сделанный ради того, чтобы быть сделаным.
# Подобную простую функциональность можно спокойно заменить форматированием строки, без оберток.
@dataclass(frozen=True)
class Formatter:
    template: str

    def format(self, **template_kwargs) -> str:
        return self.template.format(**template_kwargs)
```

## 2.3

```python

class HouseModel:
    ...

    # данный метод просится в отдельный класс сериализатора.
    def serialize(self) -> bytes:
        return json.dumps(self)
```

## 2.4

```python
@dataclass(frozen=True)
class LocalCache:
    data: dict[str, Any]

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key, default=None) -> Any:
        return self.data.get(key, default)

# Глобальная переменная
cache = LocalCache()

# в одном месте программы
cache.set("key1", "value1")

# в любом другом
cache.set("key2", "value2")
```

## 2.5

```python


class Mailman:
  def __init__(self, customer, sender):
    self.customer = customer
    self.sender = sender

  def deliver(self, subject, message):
    ...
    self.log(subject, message)


  def log(self, subject, message):
    sender_name = 'Unknown'


    if self.sender.__class__.__name__ == 'Order':
      sender_name = f'Order #{self.sender.id}'


    elif self.sender.__class__.__name__ == 'Chaser':
      sender_name = f'Chaser for Order #{self.sender.order.id}'


    LogEntry.objects.create(sender_name=sender_name, subject=subject, message=message)...
```

## 2.6

В питоне нигде каст не применяется, поэтому приведу базовй пример из C++ по приведению типов

```cpp
#include <iostream>

class Book      // класс книги
{
public:
    Book(std::string title, unsigned pages): title{title}, pages{pages}{}
    std::string getTitle() const {return title;}
    unsigned getPages() const {return pages;}
    virtual void print() const
    {
        std::cout << title << ". Pages: " << pages << std::endl;
    }
private:
    std::string title;  // название книги
    unsigned pages;     // количество страниц
};
class File  // класс электронного файла
{
public:
    File(unsigned size): size{size}{}
    unsigned getSize() const {return size;}
    virtual void print() const
    {
        std::cout << "Size: " << size << std::endl;
    }
private:
    unsigned size;     // размер в мегабайтах
};

class Ebook : public Book, public File     // класс электронной книги
{
public:
    Ebook(std::string title, unsigned pages, unsigned size): Book{title, pages}, File{size}{}
    void print() const override
    {
        std::cout << getTitle() << "\tPages: " << getPages() << "\tSize: " << getSize() << "Mb" << std::endl;
    }
};

int main()
{
    Ebook cppbook{"About C++", 350, 6};
    Book* book = &cppbook;  // указывает на объект Ebook
    // динамическое преобразование из Book в Ebook
    Ebook* ebook{dynamic_cast<Ebook*>(book)};
    ebook->print();  // About C++       Pages: 350      Size: 6Mb
}
```

## 2.7

```python
# Не то, чтобы я могу назвать это плохим примером проектирования. Видимо совсем плохие примеры в голову мне не лезут :)

# базовый класс клеинта к облачному хранилищу
class CloudClient(abc.ABC):
    ...

# класс использует клиента для облачного хранилища
class DataUploader(abc.ABC):
    cloud_client: CloudClient


    @abc.abstractmethod
    def upload(self) -> None:
        ...

class VKCloadClient(CloudClient):
    ...

# Для загрузчика в облако ВК нужен клиент для Облака ВК
class VKCloudUploader(DataUploader):

    def upload(self) -> None:
        ...

vk_cloud_uploader = VKCloudUploader(cloud_client=VKCloadClient())
```

## 2.8

```python
class FileReader:
    def read(file_path: Path) -> str:
        ...

# например вот такое корявенькое наследование
class JsonFileReader(FileReader):
    # мало того, что мы переопределяем метод, мы еще возвращаем другой тип
    def read(file_path: Path) -> dict:
        ...
```

## 3.1

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# модификация метода send объекта класса SendGridAPIClient приведет к измерению в нескольких классах
class Order:
  def ship(self):
    message = Mail(to_emails=self.customer.email, subject='Вот ваш курс', content='Удачи в прослушивании')

    sendgrid = SendgridAPIClient(settings.SENDGRID_API_KEY)
    sendgrid.send(message)

class Chaser:
  def chase(self):
    message = Mail(to_emails=self.customer.email, subject='Как вам курс?', content='Расскажите, что нам улучшить?')

    sendgrid = SendgridAPIClient(settings.SENDGRID_API_KEY)
    sendgrid.send(message)
```

## 3.2

```python
class BaseUserCheck:
    def verify(self, user) -> bool:
        ...

# Использование цепочки отвественности
class AccessController:
    checks: list[BaseUserCheck]

    def check_user_access_permisions(self, user) -> bool:
        return all(check.verify(user) for check in self.checks)

class CheckIsUserAdmin(BaseUserCheck):
    def verify(self, user) -> bool:
        return user.type == "admin"

# Вместо использование кода выше, можно сделать так:
if not user.is_admin:
    return
# Проверка всего одна, более не предвидится, городить цепочку ответсвенности не надо
```
