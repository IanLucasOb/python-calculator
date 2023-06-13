# TODO FIX
import pygame
import sympy

# PyGame Initial config
pygame.init()
pygame.display.set_caption("Calculadora 🤙️🥶️")
screen = pygame.display.set_mode((320, 300))
clock = pygame.time.Clock()
running = True
# Colors:
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
red = (255, 0, 0)

inputValue = ""
result = 0
operators = ["0", "+", "-", "*", "//", "%", "**"]  # Operators and 0
haveSomeOperator = False
endsWithOperator = False
expressionIsInvalid = ""

# Generate a text configuration with a font and text
def textConfig(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# Create an text element in screen
def drawText(text, positionX, positionY, width, height, fontSize=20, color=black):
    smallText = pygame.font.Font("freesansbold.ttf", fontSize)
    textSurf, textRect = textConfig(text, smallText, color)
    textRect.center = ((positionX + (width / 2)), (positionY + (height / 2)))
    screen.blit(textSurf, textRect)


# Draw value input
def drawValueTextBox():
    global inputValue
    global result
    value = str(result) if result else inputValue
    drawText(value, 0, -10, 320, 60)


# Creates a button element in screen
def drawButton(color, positionX, positionY, width, height):
    global button
    global buttonNumber
    pygame.draw.rect(screen, color, (positionX, positionY, width, height))


# Create buttons and verify if mouse is over it
def createButton(text, width, height, positionX, positionY, activeColor, inactiveColor):
    mouse = pygame.mouse.get_pos()
    if (
        positionX + width > mouse[0] > positionX
        and positionY + height > mouse[1] > positionY
    ):
        drawButton(activeColor, positionX, positionY, width, height)
    else:
        drawButton(inactiveColor, positionX, positionY, width, height)
    drawText(text, positionX, positionY, width, height)


# Find the button that was clicked based in x and y
def whichButtonWasClicked(position):
    x, y = position
    rows = [80, 120, 160, 200, 240, 280]
    cols = [106, 212, 318]

    if 60 < y <= rows[0]:
        if x <= cols[0]:
            setValue(1)
        elif x <= cols[1]:
            setValue(2)
        elif x <= cols[2]:
            setValue(3)
    elif rows[0] < y <= rows[1]:
        if x <= cols[0]:
            setValue(4)
        elif x <= cols[1]:
            setValue(5)
        elif x <= cols[2]:
            setValue(6)
    elif rows[1] < y <= rows[2]:
        if x <= cols[0]:
            setValue(7)
        elif x <= cols[1]:
            setValue(8)
        elif x <= cols[2]:
            setValue(9)
    elif rows[2] < y <= rows[3]:
        if x <= cols[0]:
            setValue(0)
        elif x <= cols[1]:
            setValue(" + ")
        elif x <= cols[2]:
            setValue(" - ")
    elif rows[3] < y <= rows[4]:
        if x <= cols[0]:
            setValue(" * ")
        elif x <= cols[1]:
            setValue(" // ")
        elif x <= cols[2]:
            setValue(" % ")
    elif rows[4] < y <= rows[5]:
        if x <= cols[0]:
            setValue(" ** ")
        elif x <= cols[2]:
            # '=' button
            calculateResult()


def setValue(value):
    global inputValue
    global result
    if result:
        result = ""
    _value = str(value)
    trimValue = _value.strip()
    valueIsOperator = trimValue in operators
    if (
        (inputValue.endswith(_value) and valueIsOperator)
        or (inputValue == "" and valueIsOperator)
        or (valueIsOperator and str(inputValue)[len(str(inputValue)) - 2] in operators)
    ):
        return
    inputValue = inputValue + _value


# Calculate result :D
def calculateResult():
    global inputValue
    global result
    global haveSomeOperator
    global expressionIsInvalid
    global endsWithOperator
    endsWithOperator = False
    if inputValue == "":
        expressionIsInvalid = False
        return
    for i in operators:
        if not endsWithOperator and i != 0:
            endsWithOperator = inputValue.endswith(f"{i} ")
        if not haveSomeOperator:
            haveSomeOperator = inputValue.find(i) > 0
    if haveSomeOperator and not endsWithOperator:
        result = sympy.sympify(inputValue)
        if result != "":
            inputValue = ""
            haveSomeOperator = False
            expressionIsInvalid = False
        else:
            expressionIsInvalid = True
    else:
        expressionIsInvalid = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                whichButtonWasClicked(event.pos)
    # print('o py ta on')
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE'

    # Draw the input that show the values and operations
    drawValueTextBox()
    # If expression is invalid, show a message
    if expressionIsInvalid:
        drawText("Expressão inválida!", 0, -10, 320, 85, 14, red)

    # Create 1-9 buttons
    for i in reversed(range(1, 10)):
        if i <= 3:
            positionY = 40
            positionX = 107 * (i - 1)
        elif i <= 6:
            positionY = 80
            positionX = 107 * (i - 4)
        else:
            positionY = 120
            positionX = 107 * (i - 7)
        createButton(str(i), 106.3, 40, positionX, positionY, grey, white)
    for idx, operator in enumerate(operators, start=1):
        if idx <= 3:
            positionY = 160
            positionX = 107 * (idx - 1)
        elif idx <= 6:
            positionY = 200
            positionX = 107 * (idx - 4)
        else:
            positionY = 240
            positionX = 107 * (idx - 7)
        createButton(str(operator), 106.3, 40, positionX, positionY, grey, white)

        createButton("=", 212, 40, 107, 240, grey, white)
        # createButton(str('+'),106.3,40,107,160,grey,white)
    drawText("v1.0.0 - Ianzin", 15, 250, 40, 85, 10)
    pygame.display.update()
    clock.tick(15)  # limits FPS to 60


pygame.quit()
