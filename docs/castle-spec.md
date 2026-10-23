# ТЗ: спрайти «Замку» (від квартири до замку)

Мета: 7 ізометричних картинок житла + 5 «прикрас». Той самий стиль, що й місто: піксель-арт, ізометрія 2:1 (SimCity 2000), Win3.1-палітра, без згладжування.

## Загальні правила (для всіх картинок)
- Фон: суцільний рожевий **#FF00FF**, без градієнтів і підлоги, яку не видно на карті. Я його виріжу.
- Формат 4:3 (наприклад 1600×1200). Об'єкт по центру, з відступом ~8% від країв.
- Ракурс: ізометрія 2:1, вид зверху-спереду, **світло зліва-зверху**, тінь падає вправо-вниз (як у місті).
- Кожна картинка стоїть на **ромбі-ділянці 3×3 «тайли»** (газон + бордюр), ромб одного розміру на всіх сходинках (ширина ~70% кадру), нижня вершина ромба на тому самому місці.
- Без тексту, без людей (родину малюю кодом), без логотипів, без реальних брендів.
- Піксельні краї, обмежена палітра (до ~32 кольорів), чорно-коричневий контур 1px.

## Базовий промпт (вставляти на початку кожного)
> Isometric pixel art, SimCity 2000 style, 2:1 dimetric view, light from top-left, crisp pixels no anti-aliasing, limited palette, 1px dark outline. Single building on a 3x3 tile diamond-shaped lawn plot, centered, solid flat magenta #FF00FF background, no text, no people, no shadows outside the plot.

## Сходинки (по одній картинці)
0. **Хрущовка** — `a drab five-storey Soviet panel block ("khrushchevka"), only one corner entrance with a cracked canopy, tiny balconies with laundry, bare patch lawn, a rusty bench`
1. **Новобудова** — `a modern 16-storey residential tower with a glass lobby and a covered parking entrance, neat small lawn, a shiny new car`
2. **Пентхаус** — `top of a stylish residential tower: a glass penthouse with a roof terrace, plants and a hot tub on the terrace, glass railings, warm lights`
3. **Будинок за містом** — `a two-storey brick country house with a tiled roof, a garage, a tall brick fence with a gate, a few fir trees, a well-kept lawn`
4. **Особняк** — `a large mansion with white columns, balconies, a pediment, a driveway with fountain, thuja hedge, wrought-iron gate, security booth`
5. **Маєток** — `a sprawling estate: a main palace-like house with side wings, stables, a gazebo, pier on a small pond, rooftop helipad marking, high fence with watch towers`
6. **Замок** — `a fairy-tale castle with a moat and drawbridge, four round towers, crenellated walls, a golden dome on the tallest tower, banners, golden lion statues at the gate`

## «Прикраси» (окремі спрайти на прозорому/рожевому фоні, на тому самому масштабі)
Розмір орієнтуємо на ділянку 3×3: басейн ≈ 1×1,2 тайла, вертоліт ≈ 1,2×1,2, леви ≈ 0,3 тайла, паркан = пряма секція 1 тайл.
- **fence** — `3-meter brick fence section with a pillar, isometric, one tile long`
- **pool** — `heated swimming pool, rectangular, light-blue water, white tiles around, a lounger, steam`
- **lions** — `two golden lion statues on grey stone pedestals, side by side`
- **toilet** — `a golden toilet on a red velvet pedestal under a glass dome, a joke luxury item`
- **heli** — `helipad with painted H circle and a small red helicopter on it`

## Конвеєр
1. Генеруй сходинки послідовно: першу — потім як референс стилю для інших («style reference»).
2. Одна картинка — один файл `castle_0.png … castle_6.png`, прикраси `ex_fence.png` тощо.
3. Я виріжу фон, вирівняю ромб по нижній вершині, підпишу в `assets/sp/manifest.json` і підключу до вкладки «Замок».
