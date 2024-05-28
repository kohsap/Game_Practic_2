# Импортируем классы, используемые в игре
from data.classes.sprites import *
from sys import exit

class Game():
    '''Этот класс определяет основную игру'''

    def __init__(self):
        '''Этот инициализатор определяет заголовок и окна и запускает конфигурацию игрового движка'''
        
        # Запускает игру и аудио
        pg.init()
        pg.mixer.init()
        
        # Устанавливает заголовок и иконку
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        # Позволяет удерживать кнопки ввода
        pg.key.set_repeat(200, 175)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
    def loadData(self):
        '''Этот метод загружает данные из файлов за пределами Python'''
        self.playerSpriteSheet = Spritesheet(PLAYERSPRITE, PLAYERXML)
        self.waterSpriteSheet = Spritesheet(WATERSPRITE, WATERXML)
        self.keySpriteSheet = Spritesheet(KEYSPRITE, KEYXML)
        self.teleporterSpriteSheet = Spritesheet(TELEPORTERSPRITE, TELEPORTERXML)
        
        # Загружает фоновую музыку
        pg.mixer.music.load('data/sound/music.ogg')
        pg.mixer.music.set_volume(0.1)
        
        # Звуковой эффект, когда игрок движется
        self.moveSound = pg.mixer.Sound("data/sound/move.ogg")
        self.moveSound.set_volume(0.1)
        
        # Звуковой эффект, когда игрок полностью завершает уровень
        self.allTileComplete = pg.mixer.Sound("data/sound/allTileComplete.ogg")
        self.allTileComplete.set_volume(0.2)

        # Звуковой эффект, когда игрок умирает
        self.deadSound = pg.mixer.Sound("data/sound/dead.ogg")
        self.deadSound.set_volume(0.2)

        # Звуковой эффект, когда игрок касается сумки с сокровищами
        self.treasureSound = pg.mixer.Sound("data/sound/treasure.ogg")
        self.treasureSound.set_volume(0.2)

        # Звуковой эффект, когда игрок движется с ледяной плитки
        self.iceBreakSound = pg.mixer.Sound("data/sound/breakIce.ogg")
        self.iceBreakSound.set_volume(0.2)
        
        # Звуковой эффект, когда игрок касается ключа или разблокирует замок
        self.keyGet = pg.mixer.Sound("data/sound/keyGet.ogg")
        self.keyGet.set_volume(0.2)

        # Звуковой эффект, когда игрок возвращается на старт
        self.resetSound = pg.mixer.Sound("data/sound/reset.ogg")
        self.resetSound.set_volume(0.2)
        
        # Звуковой эффект, когда игрок касается движущегося блока
        self.movingBlockSound = pg.mixer.Sound("data/sound/movingBlockSound.ogg")
        self.movingBlockSound.set_volume(0.2)
        
        # Звуковой эффект, когда игрок телепортируется
        self.teleportSound = pg.mixer.Sound("data/sound/teleportSound.ogg")
        self.teleportSound.set_volume(0.2)
        
    def loadMap(self):
        '''Загружает текущий уровень, читая параметры'''
        
        # Сбрасывает переменные, связанные с картой
        mapData = []
        totalFree = 0
        
        # Открывает файл и добавляет все данные в mapData
        fileName = "data/maps/level%d.txt" % self.currentLevel
        currentMap = open(fileName, "r")
        for line in currentMap:
            mapData.append(line)
        
        # Генерирует карту на основе текстового файла
        for row, tiles in enumerate(mapData):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                elif tile == '0':
                    Unused(self, col, row)
                elif tile == 'F':
                    Free(self, col, row)
                    totalFree += 1
                elif tile == 'E':
                    self.endTile = End(self, col, row)
                elif tile == 'I':
                    Ice(self, col, row)
                    totalFree += 2
                elif tile == 'K':
                    Free(self, col, row)
                    self.key = GoldenKey(self, col, row)
                    totalFree += 1
                elif tile == 'B':
                    self.movingBlockTile = MovingBlockTile(self, col, row)
                elif tile == 'T':
                    Free(self, col, row)
                    self.movingBlock = MovingBlock(self, col, row)
                    totalFree += 1
                elif tile == '%':
                    # Эксклюзивная плитка, используемая только для уровня 14, 15, 16
                    Ice(self, col, row)
                    self.movingBlock = MovingBlock(self, col, row)
                    totalFree += 2
                elif tile == '&':
                    # Эксклюзивная плитка, используемая только для уровня 15
                    self.movingBlockTile = MovingBlockTile(self, col, row)
                    self.key = GoldenKey(self, col, row)
                elif tile == '!':
                    # Эксклюзивная плитка, используемая только для уровня 16
                    Ice(self, col, row)
                    self.key = GoldenKey(self, col, row)
                    totalFree += 2
                elif tile == '1':
                    # Телепорт 1
                    self.firstTeleporter = Teleporter(self, col, row)
                elif tile == '2':
                    # Телепорт 2
                    self.secondTeleporter = Teleporter(self, col, row)
                elif tile == 'H':
                    self.keyHole = KeyHole(self, col, row)
                    totalFree += 1
                elif tile == 'M':
                    Free(self, col, row)
                    if (self.lastLevelSolved):
                        self.treasureTile = Treasure(self, col, row)
                    totalFree += 1
                elif tile == 'P':
                    Free(self, col, row)
                    self.player.movetoCoordinate(col, row)
                    totalFree += 1
        
        # Вычитание верхнего и нижнего ряда свободных плиток, так как они предназначены для меню
        self.scoreKeeperTop.totalTiles = (totalFree - (2 * 19))
        self.scoreKeeperTop.completeTiles = 0
        # Обновление номера текущего уровня
        self.scoreKeeperTop.currentLevel = self.currentLevel
        

    def new(self):
        '''Этот метод инициализирует все переменные и настраивает игру'''
        
        # Загружает внешние данные
        self.loadData()
        
        # Создает группы, используемые для обработки событий позже
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.movable = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.iceSprites = pg.sprite.Group()
        self.scoreSprites = pg.sprite.Group()
        self.updatingBlockGroup = pg.sprite.Group()
        self.noWaterGroup = pg.sprite.Group()
        
        # Создает спрайт игрока до загрузки карты
        self.player = Player(self, 0, 0)
        
        # Часы для установки частоты кадров
        self.clock = pg.time.Clock()
        
        # Содержит конечную точку каждого уровня для обработки событий
        self.endTile = object()
        
        # Указывает, куда перемещать движущийся блок позже
        self.movingBlockTile = object()
        
        # Проверяет, может ли игрок открыть замок
        self.hasKey = False

        # Проверяет, сбрасывался ли игрок на карте
        self.resetOnce = False
        
        # Проверяет, смог ли игрок успешно передвинуться
        self.moved = False
        
        # Содержит текущий уровень игры
        self.currentLevel = 1
        
        # Позволяет игре помнить последний решенный уровень
        self.lastLevelSolved = True
        
        # Проверяет, движется ли движущийся блок
        self.blockIsMoving = False
        
        # Проверяет, может ли игрок телепортироваться
        self.canTeleport = True            
        
        self.scoreKeeperTop = ScoreKeeperTop(self)
        self.scoreKeeperBottom = ScoreKeeperBottom(self)
        self.resetButton = Button(self, "reset", 65, HEIGHT - 13, 72, 21)
        
        # Загружает карту
        self.loadMap()
        
        # Воспроизводит и бесконечно циклирует музыку
        pg.mixer.music.play(-1)
        

    def run(self):
        '''Этот метод является игровым циклом, который выполняет большую часть игры'''
        self.looping = True
        while self.looping:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        '''Этот метод обновляет все классы/объекты в рамках игрового цикла'''
        self.allSprites.update()
        self.scoreSprites.update()
    
    def deleteMap(self):
        '''Этот метод удаляет все плитки на текущем уровне'''
        for tiles in self.allSprites:
            tiles.kill()
            
    def playResetSounds(self):
        '''Этот метод воспроизводит соответствующие звуки при сбросе или смерти'''
        self.deadSound.play()
        self.resetSound.play()        
    
               
    def reset(self):
        '''Этот метод сбрасывает текущий уровень'''
        
        # Очищает карту и перезагружает карту
        self.deleteMap()
        self.loadMap()
        
        # Сбрасывает счет на 0 или до предыдущего уровня
        self.scoreKeeperBottom.score = self.scoreKeeperBottom.previousScore
        
        # Сбрасывает статус ключа
        self.hasKey = False
        
        # Сбрасывает статус телепорта
        self.canTeleport = True
        
        # Сообщает игре, что игрок сбросился один раз
        self.resetOnce = True
        
    
    def nextLevel(self):
        '''Этот метод перемещает игрока на следующий уровень'''
        
        # Обновляет переменные
        self.resetOnce = False
        self.currentLevel += 1
        
        if self.currentLevel == 20:
            # Показывает экран с результатами
            w = ScoreScreen(self.scoreKeeperTop, self.scoreKeeperBottom)
            w.new()
            w.run()
        
        # Очищает карту и загружает новую карту
        self.deleteMap()
        self.loadMap()
        
        # Сбрасывает статус ключа
        self.hasKey = False
        
        # Сбрасывает статус телепорта
        self.canTeleport = True
            
    def draw(self):
        '''Этот метод рисует все спрайты на экране'''
        self.allSprites.draw(self.screen)
        self.scoreSprites.draw(self.screen)
        self.updatingBlockGroup.draw(self.screen)
        pg.display.flip()
              

    def events(self):
        '''Этот метод обрабатывает события'''
        
        # УПРАВЛЕНИЕ
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.resetButton.rect.collidepoint(pg.mouse.get_pos()):
                    # Воспроизводит анимацию и звуки сброса и сбрасывает карту при нажатии кнопки
                    self.reset()
                    self.player.setFrame(RESETTING)
                    self.playResetSounds()
                                
            if event.type == pg.KEYDOWN:
                # Выходит из игры с помощью клавиши ESC
                # Стрелочные клавиши управляют движением
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.checkAndMove(dx=-1)
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.checkAndMove(dx=1)
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.checkAndMove(dy=-1)
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.checkAndMove(dy=1)
                        
               
        # Если игрок передвинулся, проверить, находится ли он на финишной линии
        if self.moved:
            # Обновить счетчики
            self.scoreKeeperTop.completeTiles += 1
            self.scoreKeeperBottom.score += 1
            
            # Проверить, коснулся ли игрок финишной линии
            if self.player.collideWithTile(self.endTile):
                # Проверить, можно ли применить бонусный счет
                if self.scoreKeeperTop.checkFinish():
                    # Позволяет игре помнить последний решенный уровень
                    self.lastLevelSolved = True
                    
                    # Воспроизводит бонусный звуковой эффект
                    self.allTileComplete.play()
                    
                    # Увеличивает количество решенных уровней на 1
                    self.scoreKeeperTop.solvedLevels += 1  
                    
                    # Дает x2 бонусные очки, если не было сброса/смерти, иначе дает нормальные очки
                    if not self.resetOnce:
                        self.scoreKeeperBottom.score += self.scoreKeeperTop.totalTiles * 2
                    else:
                        self.scoreKeeperBottom.score += self.scoreKeeperTop.totalTiles
                    
                # Напоминает игре, что игрок не решил последний уровень
                else:
                    self.lastLevelSolved = False
                
                # Устанавливает предыдущий счет для следующего уровня
                self.scoreKeeperBottom.previousScore = self.scoreKeeperBottom.score
                
                # Обновляет общее количество растаявших плиток за всю игру
                self.scoreKeeperTop.playerMelted += self.scoreKeeperTop.completeTiles
                
                # Переходит на следующий уровень
                self.nextLevel()
                
            # Если сумка с сокровищами существует, проверить, коснулся ли игрок сумки с сокровищами, сокровища появляются только после уровня 3 в оригинальной игре
            elif self.lastLevelSolved and self.currentLevel > TREASURELEVEL:
                if self.player.collideWithTile(self.treasureTile):
                    self.treasureTile.kill()
                    self.treasureSound.play()
                    self.scoreKeeperBottom.score += 100
            
            # Проверить, касается ли игрок ключа, появляется только после уровня 9 в оригинальной игре
            if self.currentLevel > KEYLEVEL:
                if self.player.collideWithTile(self.key):
                    # Позволяет игроку открывать замки
                    self.key.kill()
                    self.keyGet.play()
                    self.hasKey = True
            
            # Если у игрока есть ключ, проверить, находится ли он в радиусе замка
            if self.hasKey:
                if self.player.nearTile(self.keyHole) != 0:
                    # Удаляет замок и заменяет его на свободную плитку
                    Free(self, self.keyHole.x, self.keyHole.y)
                    self.keyGet.play()
                    self.keyHole.kill()
                    self.hasKey = False
                    
            # Проверяет, может ли игрок телепортироваться, только после уровня 16
            if self.currentLevel > TELEPORTLEVEL:
                    # Телепортирует к другому телепорту, убедитесь, что очки не добавляются
                    if self.player.collideWithTile(self.firstTeleporter):
                        self.scoreKeeperTop.completeTiles -= 1
                        self.scoreKeeperBottom.score -= 1
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.secondTeleporter.x, self.secondTeleporter.y)
                            self.canTeleport = False
                            self.teleportSound.play()
                        
                    elif self.player.collideWithTile(self.secondTeleporter):
                        self.scoreKeeperTop.completeTiles -= 1
                        self.scoreKeeperBottom.score -= 1
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.firstTeleporter.x, self.firstTeleporter.y)
                            self.canTeleport = False
                            self.teleportSound.play()
                                                    
            # Если игрок столкнулся с движущейся плиткой, очки не добавляются
            if self.currentLevel > MOVINGBLOCKLEVEL and self.player.collideWithTile(self.movingBlockTile):
                self.scoreKeeperTop.completeTiles -= 1
                self.scoreKeeperBottom.score -= 1        
            
            # Проверяет, не может ли игрок больше двигаться, продолжение
            # объяснение в классе Player
            if self.player.checkDeath():
                # Воспроизводит анимацию и звуки смерти и сбрасывает карту при нажатии кнопки
                self.player.setFrame(DYING)
                self.playResetSounds()            
                        
            # Сбрасывает переменную moved
            self.moved = False
    
    
class TitleScreen():
    '''Этот класс определяет экран заголовка основной игры'''

    def __init__(self):
        '''Этот инициализатор принимает сцену главного меню в качестве параметра, инициализирует
        изображение и атрибуты прямоугольника, а также другие переменные, используемые для игрока'''
        
        # Запускает игру и аудио
        pg.init()
        pg.mixer.init()
        
        # Устанавливает заголовок и иконку
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

    def loadData(self):
        '''Этот метод загружает данные из файлов за пределами Python'''
        
        # Загружает фоновую музыку
        pg.mixer.music.load('data/sound/music.ogg')
        pg.mixer.music.set_volume(0.1)
        
        # Звуковой эффект при нажатии кнопки
        self.clickSound = pg.mixer.Sound("data/sound/move.ogg")
        self.clickSound.set_volume(0.2)
         
    def new(self):
        '''Этот метод инициализирует все переменные и настраивает игру'''
        
        # Загружает внешние данные
        self.loadData()
        
        # Создает группы, используемые для обработки событий позже
        self.scoreSprites = pg.sprite.Group()
        
        # Воспроизводит и бесконечно циклирует музыку
        pg.mixer.music.play(-1)
        
        # Часы для установки частоты кадров
        self.clock = pg.time.Clock()
        
        # Изображения главного меню
        self.mainMenu = BeginMenu(self)
        
        # Начальная картинка
        self.startButton = Button(self, "start", 237, 390, 108, 32)

    def run(self):
        '''Этот метод является игровым циклом, который выполняет большую часть игры'''
        self.looping = True
        while self.looping:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        '''Этот метод обновляет все классы/объекты в рамках игрового цикла'''
        self.scoreSprites.update()

    def events(self):
        '''Этот метод обрабатывает события'''
        
        # УПРАВЛЕНИЕ
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.startButton.rect.collidepoint(pg.mouse.get_pos()) and self.startButton.buttonType == "start":
                    # Когда игрок нажимает кнопку "Старт", показывается экран с инструкциями
                    self.startButton.__init__(self, "play", 237, 390, 108, 32)
                    self.clickSound.play()
                    
                elif event.button == 1 and self.startButton.rect.collidepoint(pg.mouse.get_pos()) and self.startButton.buttonType == "play":
                    self.clickSound.play()
                    # Запуск основной игры
                    x = Game()
                    x.new()
                    x.run()
                    
                    
    def draw(self):
        '''Этот метод рисует все спрайты на экране'''
        self.scoreSprites.draw(self.screen)
        pg.display.flip()

class ScoreScreen():
    '''Этот класс отображает ваши общие статистические данные после завершения всех 19 уровней'''
    
    def __init__(self, scoreBoardTop, scoreBoardBottom):
        '''Этот инициализатор принимает сцену главного меню в качестве параметра, инициализирует
        изображение и атрибуты прямоугольника, а также другие переменные, используемые для игрока'''
        
        # Запускает игру и аудио
        pg.init()
        pg.mixer.init()
        
        # Устанавливает заголовок и иконку
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        
        # Статистика игрока
        self.levelSolved = scoreBoardTop.solvedLevels
        self.iceMelted = scoreBoardTop.playerMelted
        self.totalScore = scoreBoardBottom.score
          
    def loadData(self):
        '''Этот метод загружает данные из файлов за пределами Python'''
        
        # Загружает фоновую музыку
        pg.mixer.music.load('data/sound/winner.ogg')
        pg.mixer.music.set_volume(0.1)

        # Инициализирует шрифт, используемый в игре
        self.font = pg.font.Font("data/font/arcade.ttf", 18) 
        
        # Изображение пингвина
        self.puffle= pg.image.load("data/images/puffle.png")
        
        # Звуковой эффект при загрузке линии
        self.lineSound = pg.mixer.Sound("data/sound/move.ogg")
        self.lineSound.set_volume(0.2)
               
        # Звуковой эффект при загрузке пингвина
        self.puffleSound = pg.mixer.Sound("data/sound/allTileComplete.ogg")
        self.puffleSound.set_volume(0.2)

    def new(self):
        '''Этот метод инициализирует все переменные и настраивает игру'''
        
        # Загружает внешние данные
        self.loadData()
        
        # Создает группы, используемые для обработки событий позже
        self.scoreSprites = pg.sprite.Group()
        
        # Воспроизводит и бесконечно циклирует музыку
        pg.mixer.music.play(-1)
        
        # Часы для установки частоты кадров
        self.clock = pg.time.Clock()
        
        # Счетчик, используемый для отображения текста с течением времени
        self.counter = 0
                
        # Кнопка для завершения игры
        self.finishButton = Button(self, "finish", 237, 390, 108, 32)
        
        self.levelSolvedText = self.font.render("Всего решено уровней:%21d" % self.levelSolved, 1 , (0,0,0))
        self.iceMeltedText = self.font.render("Всего растоплено льда:%25d" % self.iceMelted, 1 , (0,0,0))
        self.totalScoreText = self.font.render("Общее количество очков:%32d" % self.totalScore, 1, (0,0,0))
        
        # Светло-голубой фон
        self.screen.fill((217,241, 255))
               
    def run(self): 
        '''Этот метод является игровым циклом, который выполняет большую часть игры'''
        self.looping = True
        while self.looping:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
            
    def update(self):
        '''Этот метод обновляет все классы/объекты в рамках игрового цикла'''
        self.scoreSprites.update()
        
        # Выводит каждую строку статистики каждые 0,75 секунды
        if self.counter == 1:
            self.screen.blit(self.levelSolvedText, (75,25))
            pg.time.delay(750)
            self.lineSound.play()
        elif self.counter == 2:
            self.screen.blit(self.iceMeltedText, (75,75))
            pg.time.delay(750)
            self.lineSound.play()
        elif self.counter == 3:
            self.screen.blit(self.totalScoreText, (75,125))
            pg.time.delay(750)
            self.lineSound.play()
        elif self.counter == 4:
            self.screen.blit(self.puffle, (170,150))
            pg.time.delay(750)
            self.puffleSound.play()
        self.counter += 1 
        
    def events(self):
        '''Этот метод обрабатывает события'''
        
        # УПРАВЛЕНИЕ
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.finishButton.rect.collidepoint(pg.mouse.get_pos()) and self.finishButton.buttonType == "finish":
                    pg.quit()
                    exit()
                    
                    
    def draw(self):
        '''Этот метод рисует все спрайты на экране'''
        self.scoreSprites.draw(self.screen)       
        pg.display.flip()

# Создаем объект класса TitleScreen и запускаем игру
g = TitleScreen()

while True:
    g.new()
    g.run()
