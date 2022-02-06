import os
from os import path, mkdir
from PIL import Image
import pandas as pd
import numpy as np

output_folder = "generated"
if not path.exists(output_folder):
    mkdir(output_folder)

characters = []
backgrounds = []

for count, filename in enumerate(os.listdir("backgrounds")):
    backgrounds.append(filename)

for count, filename in enumerate(os.listdir('characters')):
    characters.append(filename)


def renaming_files(folder_name):
    """
    Rename the files in the given folder name
    For example foldername is characters it will rename all the files in the folder as characters_1, characters_2 and soon
    Args:
        folder_name: Name of the folder
    """
    folder = folder_name

    for count, filename in enumerate(os.listdir(folder)):
        dst = f"{folder_name}_{str(count)}.png"
        src = f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
        dst = f"{folder}/{dst}"

        # rename() function will
        # rename all the files
        os.rename(src, dst)
        backgrounds.append(dst)


def generate_image(background, character, file_name):
    """
    Generate image with given background, given character and given object and save it with the given file name
    Args:
        background (str): background name
        character (str): character name
        file_name (str): file name
    """
    background_file = path.join("backgrounds", f"{background}")
    background_image = Image.open(background_file)

    # Create character
    character_file = path.join("characters", f"{character}")
    character_image = Image.open(character_file)

    coordinates = (int(1920 / 2 - character_image.width / 2), int(1000 - character_image.height))  # x, y
    background_image.paste(character_image, coordinates, mask=character_image)

    output_file = path.join(output_folder, f"{file_name}.png")
    background_image.save(output_file)


def generate_all_imgs():
    """
    Generate all possible combination of images
    """
    num = 0
    df = pd.DataFrame(columns=["background", "character", "generated image"])
    for background in backgrounds:
        for character in characters:
            generate_image(background, character, f"generated{num}")
            data = [background, character, f"generated{num}"]
            s = pd.Series(data, index=df.columns)
            df = df.append(s, ignore_index=True)
            num += 1
    df.to_csv('data.csv', index=False)


def generate_random_imgs(total_imgs):
    """Generates a given number of random images according to predefined probabilities

    Args:
        total_imgs (int): total number of images to generate
    """
    df = pd.DataFrame(columns=["background", "character", "generated image"])

    for num in range(total_imgs):
        background = np.random.choice(len(backgrounds))
        background = backgrounds[background]

        character = np.random.choice(len(characters))
        character = characters[character]

        generate_image(background, character, f"generated{num}")
        data = [background, character, f"generated{num}"]
        s = pd.Series(data, index=df.columns)
        df = df.append(s, ignore_index=True)

    df.to_csv('data.csv', index=False)


if __name__ == "__main__":
    """
    Based on the requirements we need to uncomment the below functions and utilize
    """
    # generate_all_imgs()
    # renaming_files(folder_name="characters")
    generate_random_imgs(5)
