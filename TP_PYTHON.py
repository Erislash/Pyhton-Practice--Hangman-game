#TP PYTHON 1 - LCC - Programación 2 - 2020
#Integrantes:
    #Antonelli Tomás
    #Gimenez Erik

'''
En esta implementación del juego, se tomaron ciertas decisiones sobre las estructuras de datos a usar y el diseño. Se hace
entonces una descripción general de los puntos más relevantes.

* La palabra a adivinar se toma de un archivo externo cuya ruta de acceso se le pedirá al usuario cuando comience el juego.

* El estado de la palabra a adivinar es guardado en una lista de listas (lettersState) con la siguiente estructura. Y el booleano en la posición [1] de cada sublista cambia a True cuando se adivina una letra

EJEMPLO: Palabra "Python"
        [['P', True], ['y', True], ['t', False], ['h', True], ['o', False], ['n', False]]
        Las letras 'P', 'y'y 'h' fueron adivinadas. Las restantes no


        
* Un registro de las partidas se guarda en un archivo de texto externo en forma de lista, donde se coloca el nombre del jugador y debajo las partidas con un formato específico:

Federico                    Jugador
cohete,SI,5                 Primer palabra con la que jugó Federico, fue adivinada en 5 intentos
repasador,SI,9              Segunda palabra con la que jugó Federico, fue adivinada en 9 intentos
bolso,SI,6                  Tercera palabra con la que jugó Federico, fue adivinada en 6 intentos
Carlos                      Jugador
abecedario,NO,8             Primer palabra con la que jugó Carlos, no fue adivinada y en 8 intentos se acabaron sus vidas
juego,SI,6                  Segunda palabra con la que jugó Carlos, fue adivinada en 6 intentos
anima,SI,7                  Tercera palabra con la que jugó Federico, fue adivinada en 7 intentos

* Se obtienen los juegos anteriores y se guardan en un diccionario (previousGames), que posee el siguiente formato:
{
    'Federico': [("ropa","SI",6), ("botella","NO",10), ("batalla","SI",10)],
    'Juan': [("nuez","NO",6), ("puma","NO",10), ("estado","SI",7)]
}

FORMATO DE LOS VALORES:
[("palabra_1","SI"|"NO",NUMERO_INTENTOS), ("palabra_2","SI"|"NO",NUMERO_INTENTOS')]



* Se solicita el nombre del jugador (solo letras)

* En el caso de que el jugador ingresado ya haya jugado antes, se obtienen las palabras con las que ya jugó para no repetirlas (playerPreviousWords)

* Se imprime en consola el estado de la palabra cada vez que se ingrese una letra válida (un solo caracter no numérico y que no haya sido ingresado antes) pertenezca o no a la palabra a adivinar, gracias a la función (ShowWordProgress)

* Cuando se ingresa una letra válida, esta se guarda en una lista (oldLetters) para que no se pueda ingresar varias veces la misma letra y no se descuenten vidas por eso.

* La partida termina cuando se agotan las vidas o se adivinan todas las letras.

* Luego de cada juego se guardan las estadisticas del mismo en el archivo externo que lleva el registro de todas las partidas

* Al final se le pregunta al jugador si quiere volver a jugar

'''



#///////////////////////////////////////////////////////////////////////////////////
def DictKeys(p_dict):
    '''
        DictKeys: dict -> [Any]
            Devuelve una lista con las claves de un diccionario
        Args:
           p_dict: Un diccionario
        Returns:
           Una lista con elementos cuyo tipo depende de las claves usadas en el diccionario "dict"
    '''
    output = []
    for i in p_dict:
        output += [i]
    return output

def test_DictKeys():
    testDictKeys = {
        "Metro 2033":"Ciencia Ficción",
        "1984":"Distopia",
        "DUNE":"Ciencia Ficción",
        "The Black Company":"Fantasía",
        "Rayuela":"Ficción"
    }
    assert DictKeys(testDictKeys) == ["Metro 2033","1984","DUNE","The Black Company","Rayuela"]
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def GetRoute():
    '''
        GetRoute: None -> String
            Pide que se ingrese la ruta de algún archivo por memoria y la valida leyendo dicho archivo. Hasta que no se ingrese un archivo válido no se saldrá de la función. Devuelve la rua validada
        Args:
           No toma parámetros
        Returns:
           Un string que indica la ruta completa de un archivo
    '''
    route = ""
    file = ""
    while route == "" or file == "":
        try:
            route = input('')
            file = open(route , 'r')
        except:
            print('La ruta ingresada no es correcta, vuelva a intentarlo\nRUTA:', end=" ")
            route = ""
            file = ""
            
    file.close()
    return route
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def GetWords(p_path):
    '''
        GetWords: String -> [String]
            Devuelve una lista con las palabras que serán usadas en el juego
        Args:
           p_path: La ruta donde se encuentran las palabras a usarse en el juego
        Returns:
           Una lista de Strings. Estos son las palabras a usarse en el juego
    '''
    words = []
    file = open(p_path , 'r')
    
    for word in file.readlines():
        processedWord = word.strip()
        words += [processedWord]

    file.close()
    return words
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def GetGames(p_path):
    '''
        DictKeys: String -> dict
            Devuelve un diccionario cuyas claves son los jugadores anteriores y los valores son listas de tuplas, donde cada tupla representa un juego. Ejemplo:

            EJEMPLO DE DICCIONARIO DEVUELTO
            {
                'Federico': [("ropa","SI",6), ("botella","NO",10), ("batalla","SI",10)],
                'Juan': [("nuez","NO",6), ("puma","NO",10), ("estado","SI",7)]
            }

            FORMATO DE LOS VALORES:
            [("palabra_1","SI"|"NO",NUMERO_INTENTOS), ("palabra_2","SI"|"NO",NUMERO_INTENTOS')]
 
        Args:
           p_path: La ruta del archivo donde se encuentran los juegos anteriores 
        Returns:
           Un diccionario donde se representan los juegos anteriores de cada jugador
    '''
    file = open(p_path , 'r')       #Archivo con los juegos anteriores
    player = ""                     #Jugador del que se recopilan los juegos
    players = {}                    #Variable que será devuelta, donde se ingresarán automaticamente los juegos anteriores

    for word in file.readlines():
        processedWord = word.strip()

        if not (processedWord[-1].isnumeric()):
            players[processedWord] = []
            player = processedWord
        else:
            processedWord = processedWord.split(',')
            processedWord = (processedWord[0], processedWord[1], processedWord[2])
            players[player] += [processedWord]
    
    file.close()
    return players
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def GetPreviousWords(p_player, p_games):
    '''
        GetPreviousWords: String -> dict
            Devuelve una lista con las palabras que ya jugó un determinado jugador (el cual es ingresado por primer parámetro) según el juego ingresado por segundo parámetro

            EJEMPLO DE DICCIONARIO DEVUELTO
            {
                'Federico': [("ropa","SI",6), ("botella","NO",10), ("batalla","SI",10)],
                'Juan': [("nuez","NO",6), ("puma","NO",10), ("estado","SI",7)]
            }
            FORMATO DE LOS VALORES:
            [("palabra_1","SI"|"NO",NUMERO_INTENTOS), ("palabra_2","SI"|"NO",NUMERO_INTENTOS')]

        Args:
           p_player: El nombre del jugador del que se quieren extraer las palabras ya jugadas
           p_games: Un diccionario donde se representan los juegos anteriores de cada jugador
        Returns:
           Una lista de Strings. Estos son las palabras con las que ya jugó el jugador ingresado por parámetro
    '''
    players = DictKeys(p_games)
    previousWords = []

    if(p_player in players):
        for game in p_games[p_player]:
            previousWords += [game[0]]

    return previousWords

def test_GetPreviousWords():
    testDict = {
        'Federico': [("ropa","SI",6), ("botella","NO",10), ("batalla","SI",10)],
        'Juan': [("nuez","NO",6), ("puma","NO",10), ("estado","SI",7)]
    }

    assert GetPreviousWords("Federico", testDict) == ["ropa","botella","batalla"]
    assert GetPreviousWords("Juan", testDict) == ["nuez","puma","estado"]
    assert GetPreviousWords("Marcos", testDict) == []
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def SavePlayer(p_player, p_currentGame, p_previousGames, p_previousGamesRoute):
    '''
        SavePlayer: String [tuple] dict String -> None
            Guarda el juego actual en el archivo donde están todos los juegos. Si el jugador ya había jugado antes, se agrega la palabra al final de la lista de palabras con las que ya jugo y si es un nuevo jugador se crea una nueva división
        Args:
           p_player: El nombre del jugador actual
           p_currentGame: Una lista de tuplas que contienen la información de los juegos de la sesión
           p_previousGames: Un diccionario que representa los juegos anteriores de cada jugador
           p_previousGamesRoute: La ruta donde se encuentran las estadísticas de los juegos previos 
        Returns:
           No regresa nada
    '''

    allGames = p_previousGames.copy()               #Diccionario que contiene todos los juegos
    players = DictKeys(allGames)                    #La lista de personas que ya han jugado
    file = open(p_previousGamesRoute, 'w')          #El archivo que guarda las estadísticas
    output = ""                                     #Esta variable se copiará en el archivo que guarda las estadísticas de los juegos
        
    #Si el jugador es nuevo se lo agrega al diccionario
    if not p_player in players:
        allGames[p_player] = []

    #Se agrega el juego nuevo al jugador
    allGames[p_player] += p_currentGame

    #En este ciclo crea la plantilla que se guardará en el archivo que guarda las estadísticas de los juegos anteriores teniendo en cuenta el formato acordado
    for player in allGames:
        output += player + "\n"
        for game in allGames[player]:
            output += str(game[0]) + ',' + str(game[1]) + ',' + str(game[2]) + "\n"

    file.write(output)
    file.close()  
#///////////////////////////////////////////////////////////////////////////////////


#///////////////////////////////////////////////////////////////////////////////////
def RandomFromList(p_list):
    '''
     RandomFromList: [Any] -> Any
        Toma un elemento aleatorio de una lista ingresada como parámetro
     Args:
        p_list: Una lista que contiene elementos de cualquier tipo
     Returns:
        Un elemento aleatorio de la lista
    '''

    import random
    return(p_list[random.randint(0, len(p_list) - 1)])

def test_RandomFromList():
    testRandomFromList = ['a', 'A', 'e', 'E', 'i', 'I']
    value = RandomFromList(testRandomFromList)

    assert value == 'a' or value == 'A' or value == 'e' or value == 'E' or value == 'i' or value == 'I'
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def ShowWordProgress(p_list):
    '''
     ShowWordProgress: [[String, Boolean]] -> None
        Recibe una lista de listas de dos valores, el primero es la letra de la palabra seleccionada y el segundo es un valor booleano que indica si se adivino esa letra (True) o no (False), con esos datos, imprime en consola la palabra donde se mostrarán las letras adivinadas y un guión (_) en el lugar donde están las letras no adivinadas

        EJEMPLO: Palabra "Python"
        [['P', True], ['y', True], ['t', False], ['h', True], ['o', False], ['n', False]]
        Las letras 'P', 'y'y 'h' fueron adivinadas. Las restantes no

     Args:
        p_list: Una lista que contiene elementos de cualquier tipo
     Returns:
        Un elemento aleatorio de la lista
    '''
    output = "///////////////\n\n"
    for letter in p_list:
        output += ' _ ' if not letter[1] else (" " + letter[0] + " ")
    output += "\n\n///////////////"

    print(output)
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def LetterExsists(p_letter, p_list):
    '''
     LetterExsists: String [[String, Boolean]] -> Boolean
        Recibe una letra representada por un string y una lista de listas de dos valores que lleva el estado de la palabra que se esta adivinando. El primero es la letra de la palabra seleccionada y el segundo es un valor booleano que indica si se adivino esa letra (True) o no (False), con esos datos, se indica si la letra introducida como primer parámetro es una de las letras a adivinar. 
        Si la letra ingresada se encuentra en algúna posicion de la palabra, se sustitye el booleano guardado junto a esa letra en la lista de listas
     Args:
        p_letter: La letra que ingresó el usuario
        p_list: Una lista que guarda el estado de la palabra a adivinar
     Returns:
        Un booleano indicando si esa letra era una de las letras a adivinar
    '''
    coincidence = False     #Indica si hay alguna coincidencia entre la letra introducida y la palabra a adivinar

    for letter in p_list:
        if(letter[0] == p_letter):
            letter[1] = True
            coincidence = True
    
    return coincidence

def test_LetterExsists():
    wordState = [['P', True], ['y', True], ['t', False], ['h', True], ['o', False], ['n', False]]

    assert LetterExsists('t', wordState) == True
    assert LetterExsists('f', wordState) == False
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def WinCondition(p_list):
    '''
    WinCondition: [[String, Boolean]] -> Boolean
        Recibe una lista de listas que lleva el estado de la palabra a adivinar. Si todas las letras de la palabra fueron adivinadas devuelve True y sino devuelve False
    Args:
        p_list: Una lista que guarda el estado de la palabra a adivinar
    Returns:
        Un booleano indicando si se adivinó la palabra o no
    '''
    for letter in p_list:
        if letter[1] == False:
            return False

    return True

def test_WinCondition():
    wordState = [['P', True], ['y', True], ['t', False], ['h', True], ['o', False], ['n', False]]
    wordStateWin = [['P', True], ['y', True], ['t', True], ['h', True], ['o', True], ['n', True]]

    assert WinCondition(wordState) == False
    assert WinCondition(wordStateWin) == True
#///////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////
def ValidateLetter(p_letter, p_oldLetters):
    '''
    ValidateLetter: Char [Char] -> Boolean
        Recibe un caracter y una lista con las letras que ya se usaron. Se comprueba que el caracter ingresado sea UNA sola letra y, además, se comprueba que esa letra no se haya introducido antes. Si se pasan todas estas pruebas se devuelve True, sino False
    Args:
        p_letter: Un caracter que deberá ser una letra, de lo contrario, no pasará la prueba
        p_oldLetters: Una lista que contiene las letras que se introdujeron previamente
    Returns:
        Un booleano indicando si se adivinó la palabra o no
    '''
    if(len(p_letter) > 1 or len(p_letter) < 1):
        return False

    asciiCode = ord(p_letter)
    isLetter = (asciiCode >= 97 and asciiCode <= 122) or (asciiCode == 241) #[97-122] = Letras minúsculas; 241 = ñ
    notInOldLetters = not p_letter in p_oldLetters

    return isLetter and notInOldLetters

def test_ValidateLetter():
    assert ValidateLetter('a', ['a', 'b', 'c']) == False
    assert ValidateLetter('a', ['b', 'c']) == True
    assert ValidateLetter('1', ['a', 'b', 'c']) == False
#///////////////////////////////////////////////////////////////////////////////////



def HangedGame():
    '''
    HangedGame: None -> None
        Esta es la función principal, la cual inicia y lleva adelante el juego hasta el final.
    Args:
        No toma argumentos
    Returns:
        No devuelve nada
    '''


    wordList = []                   #La lista de palabras a escoger
    previousGames = {}              #Un diccionario que representa los juegos anteriores, según cada jugador
    previousGamesRoute = ""         #La ruta del archivo que guarda las estadísticas de los juegos anteriores
    wordListRoute = ""              #La ruta del archivo que guarda las letras con las que se podrá jugar
    playerPreviousWords = []        #Las palabras que ya jugó el jugador indicado por Input

    player = ""                     #El nombre del jugador. Se introducirá por Input
    currentGame = []                #Una lista de tuplas, cada tupla representa las estadísticas de un juego terminado



    print('//////////Bienvenido al juego del AHORCADO!//////////')
    print('\tAntes de comenzar, es necesario realizar algunas configuraciones')
    print('\tPrimero, ingrese la ruta completa (incluyendo extensión) del archivo donde se encuentran las palabras a utilizar: ')
    print('RUTA:', end=' ')
    wordListRoute = GetRoute()



    print('\tAhora, ingrese la ruta completa (incluyendo extensión) del archivo dondee se encuentra el registro de los juegos anteriores: ')
    print('RUTA:', end=' ')
    previousGamesRoute = GetRoute()
    previousGames = GetGames(previousGamesRoute)



    print('\tPor último, ingrese su nombre:', end=' ')
    player = input()
   

    playAgain = True        #La variable que indica si volver a jugar o no

    #Se le pregunta al jugador si quiere jugar
    playAgain = True if (input("¿Querés jugar " + player + "?\n\t1-SI\n\t2-NO\nRespuesta: "))== "1" else False

    #Mientras el jugador indique que quiere seguir jugando después de cada juego, se seguirán iniciando juegos con palabras nuevas
    while(playAgain):
        
        playerPreviousWords = GetPreviousWords(player, previousGames)   #Se obtienen las palabras con las que ya jugó ese jugador
                                                                        #en el caso de ya haber jugado



        wordList = GetWords(wordListRoute)
        currentWord = RandomFromList(wordList)          #Se selecciona aleatoriamente la palabra

        while currentWord == "" or currentWord in playerPreviousWords:
            currentWord = RandomFromList(wordList)



        lettersState = []       #La lista que contiene el estado de cada una de las letras de la palabra
        lives = 7               #La cantidad de vidas que tenemos
        oldLetters = []         #La lista que contiene las letras ya usadas
        tries = 0               #Los intentos que llevamos. No se cuentan aquellos donde se introduce una letra inválida



        #Se crea y estructura la lista con el estado de las letras. Si alguna letra está en mayúsculas, pasará a estar en minúsculas
        for letter in currentWord:
            lettersState += [[letter.lower(), False]]

        # print('Bienvenidos al juego del ahorcado: La palabra es: ' + str(currentWord) + ' (se muestra con motivos de testeo)')
        print('Ahora si ' + player + ', la palabra ya ha sido seleccionada. COMENZAMOS!!!')
        print('La palabra consta de: ' + str(len(currentWord)) + ' letras')


        #Es un ciclo infinito que será roto cuando el jugador gane o pierda
        while True:
            validLetter = False
            choseLetter = ""

            #Se pide que se introduzca una letra, la cual es convertida a minúscula para que el tipo de letra no afecte a la validación
            while(validLetter == False):
                choseLetter = input('\nIngrese una letra: ')
                choseLetter = choseLetter.lower()

                #Si lo introducido por consola no es válido, se seguirá pidiendo una letra válida, sino se agrega la letra a la lista de letras ya usadas y se continúa con el programa fuera del ciclo
                if not ValidateLetter(choseLetter, oldLetters):
                    print('LETRA INVÁLIDA')
                    validLetter = False
                    continue
                else:
                    validLetter = True
                    oldLetters += [choseLetter]
            


            #Luego que se valide la letra se comprueba si esa letra es o no parte de la palabra a adivinar. Si no lo es se resta una vida
            if LetterExsists(choseLetter, lettersState):
                print('LETRA HALLADA!!!')
            else:
                print('Seguí intentando!')
                lives -= 1

            tries += 1     #Se suma un intento



            #Se muestra el estado del juego y de la palabra
            print('VIDAS: ' + str(lives) + '\nINTENTOS: ' + str(tries))
            ShowWordProgress(lettersState)


            #Si todas las letras fueron adivinadas se muestra un mensaje indicando eso junto con las estadísticas del juego
            if(WinCondition(lettersState)):
                print('GANASTE!!!!!!!!')
                print('TUS ESTADÍSTICAS: \n\tVIDAS: ' + str(lives) + '\n\tINTENTOS: ' + str(tries))
                print("///////////////\n\n")
                break
            
            #Si ya no quedan más vidas, el juego está perdido. Se indica lo anterior y se muestran las estadísticas
            if(lives <= 0):
                print('PERDISTE :( La palabra era: ' + currentWord)
                print('TUS ESTADÍSTICAS: \n\tVIDAS: ' + str(lives) + '\n\tINTENTOS: ' + str(tries))
                print("///////////////\n\n")
                break



        currentGame += [(currentWord, ("SI" if lives > 0 else "NO"), tries)]    #Se añade un juego nuevo 
                                                                                #(representado por una tupla) a esta sesión de juego

        #Se pregunta si se quierte volver a jugar
        playAgain = True if (input("¿Quiere jugar otra vez?\n\t1-SI\n\t2-NO\nRespuesta: "))== "1" else False

        #La sesión de juego se guarda en el archivo de registro
        SavePlayer(player, currentGame, previousGames, previousGamesRoute) 

    
    print('//////////\nJUEGO TERMINADO\nGracias por jugar!\n//////////')

HangedGame()