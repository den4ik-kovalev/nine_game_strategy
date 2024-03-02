# Суть проекта
Это симуляция карточной игры "Девятка". Цель проекта - выяснить, имеет ли сложная стратегия в этой игре преимущество над стратегией случайного выбора (спойлер: да, имеет).
Приложение позволяет запускать симуляцию с разными настройками: размер колоды, количество игроков, количество игроков со сложной стратегией, количество игр.
В результате получается статистика выигрышей, по которой можно судить, насколько стратегия успешна.

# Правила игры
В игре может использоваться как колода из 36 карт, так и из 52. Участвуют от 3 до 6 игроков (в моей версии от 2 до 4). Цель игры — избавиться от карт на руках. 
Проигрывает тот, кто последний останется с картами. Старшинство карт — от 6 (либо от 2) до туза.

Все карты колоды сдаются по кругу по одной карте. Если игра ведется на деньги, перед раздачей карт все игроки ставят в банк 
оговоренную ставку. Игру начинает игрок, имеющий 9 бубен. Следующий игрок по часовой стрелке может положить 8 или 10 бубен, либо 
одну из трёх оставшихся 9. Если вышеназванных карт у него нет, то он пропускает ход, а при игре на деньги обязан поставить в банк 
определенную сумму, обычно равную начальной ставке. Также и в дальнейшем: при невозможности положить карту ход пропускается. Но 
игрок обязан выложить карту на кон, если он может сделать ход. Если не кидать карту при возможности ходить, то игрок исключается 
из игры. 

# Стратегии

## Простая стратегия (случайная)

### Алгоритм
1. Выбрать из карт на руке случайный ход из возможных

## Сложная стратегия
Эта стратегия основана на понятии расстояния.

### Расстояние
Расстояние можно расчитать для каждой карты на руке в зависимости от карт на столе. Объясню на примерах:
1. На столе нет пик -> Расстояние для 9 пик = 1
2. На столе нет пик -> Расстояние для 10 пик = 2
3. На столе от 8 до 10 пик -> Расстояние для 7 пик = 1
4. На столе от 8 до 10 пик -> Расстояние для 6 пик = 2
5. На столе от 8 до 10 пик -> Расстояние для валета пик = 1
6. На столе от 8 до 10 пик -> Расстояние для дамы пик = 2
7. На столе нет крестей -> Расстояние для 9 крестей = 1

Короче, расстояние для конкретной карты - это минимальное количество ходов, которое требуется чтобы сыграть эту карту

### Алгоритм
1. Расчитать расстояние для каждой на руке
2. Взять карту с максимальным расстоянием
3. Посмотреть, есть ли на руке карты, сыграв которые, расстояние для этой карты уменьшится
4. Если есть - сыграть такую карту
5. Если нет - вернуться к п.2 с другой картой

# Результат
Со сложной стратегией шанс выиграть больше, чем с простой.
