from enum import Enum
import pygame

class Form(Enum):
    BASE = 1
    BRUTE = 2
    SHRINKER = 3

FORM_IMAGES = {
    Form.BASE: "assets/player/Morph_Base.png",
    Form.BRUTE: "assets/player/Morph_Brute.png",
    Form.SHRINKER : "assets/player/Morph_Shrinker.png"
}

FORM_IMAGES_MULTIPLIER = {
    Form.BASE: 2.5,
    Form.BRUTE: 3,
    Form.SHRINKER : 1
}

FORM_LOADED_IMAGES = {}
def load_form_images():
    for form in Form:
        multiplier = FORM_IMAGES_MULTIPLIER[form]
        image = pygame.image.load(FORM_IMAGES[form]).convert()
        scaledImage = pygame.transform.scale(
            image,
            (
                image.get_width()*multiplier, 
                image.get_height()*multiplier
            )
        ).convert_alpha()
        FORM_LOADED_IMAGES[form] = scaledImage