# WildParser

WildParser this is the parser of [wildberries](https://www.wildberries.ru/).

## Install

```
git clone https://github.com/zut3/WildParser.git
pip install -r requriments.txt
```

## Use

Import the class of parser from main python file and create instance.  
Parser have single public method - `collect`.
Method take infinity args - queries to the shop.



```python
from async_parser import WildParser

...

parser = WildParser()
parser.collect("some name of product", "la la la")
```

### Result exapmle
```json
{
            "name": "Смартфон iPhone 13 512GB",
            "images": [
                "https://images.wbstatic.net/c516x688/new/40650000/40654195-1.jpg",
                "https://images.wbstatic.net/c516x688/new/40650000/40654195-2.jpg"
            ],
            "prev_price": 109990,
            "price": 93491,
            "price_diff": 16499,
            "brand": "Apple",
            "photo_count": 3,
            "description": "iPhone 13. Самая совершенная система двух камер на iPhone. Режим \"Киноэффект\" делает из видео настоящее кино. Супербыстрый чип A15 Bionic. Неутомимый аккумулятор. Прочный корпус. И ещё более яркий дисплей Super Retina XDR."
        }
```
