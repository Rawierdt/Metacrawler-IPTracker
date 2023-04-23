import os
import pygame
from PIL import Image, ExifTags
import tkinter as tk
from tkinter import filedialog

# Metacrawler es un programa para borfrara m,etadatos, al cargar la imagen este borra los mertadatos EXIF,
# si la imagen no tiene ningun metadato tipo EXIF encontes la imagen quedara como simple y podra ser exportada
# si no cambio alguno
# Si la imagen tiene metadatos entoncess borrara sus metadatos y estara guardada en su lugar de origen

# Inicia pygame
pygame.init()

# Crea la ventana de pygame
width = 540
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Eliminador de Metadatos")

# Se definen las variables
filename = None
image_path = None

WHITE = (38, 255, 87)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('Tahoma', 30)
text = font.render('Borrar metadatos', True, BLACK)

# Imagen de fondo
background_image = pygame.image.load('fondo.jpg')

# Obtiene le tamaño de la imagen
text_rect = text.get_rect()

# Centrar texto y dibuja el texto
text_rect.center = (width // 2, height // 2)
screen.blit(text, text_rect)


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Se definen los botones
load_button = pygame.Rect(50, 410, 110, 50)
load_text = font.render('Cargar', True, BLACK)

save_button = pygame.Rect(200, 410, 130, 50)
save_text = font.render('Guardar', True, BLACK)

exit_button = pygame.Rect(360, 410, 110, 50)
exit_text = font.render('Salir', True, BLACK)

# Se eliminan los metadatos
def remove_exif():
    global image_path
    image = Image.open(image_path)
    try:
        for key in image.info:
            if key in ExifTags.TAGS:
                del image.info[key]
        image.save(image_path)
    except:
        pass

# Se carga la imagen
def load_image():
    global filename, image_path
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename()
    if image_path:
        filename = os.path.basename(image_path)
        image = pygame.image.load(image_path)
        screen.blit(image, (0, 0))
        remove_exif()

# Se remplaza el fondo por la imagen cargada sin los metadatos
if image_path:
    image = pygame.image.load(image_path)
    screen.blit(image, (0, 0))

# Funcion para guardar la imagen
def save_image():
    global image_path
    if image_path:
        root = tk.Tk()
        root.withdraw()
        new_path = filedialog.asksaveasfilename(defaultextension='.jpg')
        if new_path:
            try:
                os.rename(image_path, new_path)
                image_path = new_path
            except:
                pass

# Se crean los botones en pantalla
pygame.draw.rect(screen, WHITE, load_button)
pygame.draw.rect(screen, WHITE, save_button)
pygame.draw.rect(screen, WHITE, exit_button)
screen.blit(load_text, (60, 415))
screen.blit(save_text, (210, 415))
screen.blit(exit_text, (360, 415))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_image()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if load_button.collidepoint(pos):
                    load_image()
                elif save_button.collidepoint(pos):
                    save_image()
                elif exit_button.collidepoint(pos):
                    running = False
        elif event.type == pygame.DROPFILE:
            image_path = event.file
            load_image()

    # Aqui se dibuja el fondo
    screen.blit(background_image, (0, 0))
    if image_path:
        image = pygame.image.load(image_path)
        screen.blit(image, (0, 0))

    # Se crea el texto de los botones
    pygame.draw.rect(screen, WHITE, load_button)
    pygame.draw.rect(screen, WHITE, save_button)
    pygame.draw.rect(screen, WHITE, exit_button)
    screen.blit(load_text, (60, 415))
    screen.blit(save_text, (210, 415))
    screen.blit(exit_text, (390, 415))

    pygame.display.flip()

# Salir
pygame.quit()
