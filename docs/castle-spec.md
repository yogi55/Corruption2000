# ТЗ: «Замок» — шість планів житла й «багатства» до них

## Ідея
Кожне житло — це **ізометричний план-розріз** (як у The Sims чи SimCity-інтер'єрах): видно підлогу й дві задні стіни, кімнати порожні. Гроші йдуть на «багатства» — меблі й розкіш, які з'являються на плані. Коли накопичив достатньо, переїжджаєш у наступне житло: новий план, більший, і там купуєш далі. Останній план — замок. Перемога: замок заповнений.

## Сходинки і їхні «багатства» (чернетка цін, тис.)
| # | План | Переїзд | Багатства (5 на план) |
|---|------|---------|------------------------|
| 0 | Хрущовка 2к | старт | євроремонт (стіни й підлога), плазма, кондиціонер, шуба на вішаку, імпортний холодильник |
| 1 | Новобудова 3к | 300 | кухня з островом, домашній кінотеатр, шафа-купе з дзеркалом, акваріум, тренажер |
| 2 | Пентхаус | 900 | джакузі на терасі, бар, рояль, камін, панорамне вікно |
| 3 | Будинок за містом | 2 000 | гараж із двома авто, сауна, мангал і альтанка, басейн, кабінет із глобусом |
| 4 | Маєток | 5 000 | стайня, вертолітний майданчик, фонтан, кінозал, винний льох |
| 5 | Замок | 12 000 | леви біля брами, золотий унітаз, тронна зала, ров із крокодилами, **трон** |

Кожне багатство 10–20% від ціни переїзду, додає підозри (життя «не за зарплатою») і дає нову репліку родини. «Переїзд» відкривається, коли куплено 3 з 5 багатств і є гроші. Нинішні 5 покупок замку (паркан, басейн, леви, унітаз, вертоліт) стають багатствами на відповідних планах.

## Що малювати
**А. Шість планів** (`plan_0.png … plan_5.png`): порожнє житло, однакова камера, один формат.
**Б. Шість листів багатств** (`items_0.png … items_5.png`): 5 предметів у ряд на фоні #FF00FF, кожен окремо, у масштабі свого плану, без підлоги.

### Правила для всіх
- Піксель-арт, ізометрія 2:1, світло зліва-зверху, чіткі пікселі, 1px темний контур, палітра до ~32 кольорів. Така сама естетика, як у місті.
- Фон суцільний **#FF00FF**. Без тексту й людей.
- План: 4:3 (напр. 1600×1200), розріз по центру, видно підлогу й дві задні стіни, видимі кімнати й двері, порожні.
- Листи предметів: 4:3, 5 предметів у рівному ряду, між ними порожні проміжки, масштаб однаковий.

### Базовий промпт плану
> Isometric pixel art cutaway floor plan, SimCity 2000 / The Sims style, 2:1 dimetric view, light from top-left, crisp pixels, 1px dark outline, limited palette. Empty <житло>, two back walls and the floor visible, no furniture, no people, no text, solid flat magenta #FF00FF background.

Замінюй `<житло>`:
0. `Soviet 2-room khrushchevka apartment, small rooms, cheap wallpaper, linoleum floor, tiny kitchen and bathroom`
1. `modern 3-room apartment in a new tower, open kitchen-living room, parquet, bedrooms, large window`
2. `penthouse with a large open living area and a roof terrace, glass walls, marble floor`
3. `two-storey country house cutaway, big living room, kitchen, staircase, garage on one side`
4. `huge mansion estate cutaway with a great hall, wings, courtyard, stables and a helipad outside`
5. `castle interior cutaway: great hall, stone walls, a throne dais, towers, drawbridge gate`

### Базовий промпт листа багатств
> Isometric pixel art item sheet, same style and scale as the floor plan, 5 separate objects in a row on solid flat magenta #FF00FF, each object isolated with room around it, no floor, no text, no people.

Додай перелік: `1) euro-renovated wall and floor panel, 2) plasma TV on a stand, 3) split air-conditioner, 4) fur coat on a coat rack, 5) big imported fridge` (для листа 0; для інших — стовпчик «Багатства» вище).

## Що роблю я
Вирізаю фон, вирівнюю плани по одній точці, у коді розставляю предмети в слоти плану, роблю кнопку «Переїхати», ціни й підозру, нові репліки родини. Старий код-малюнок будинку прибираю.
