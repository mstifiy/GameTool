import imageio


def create_gif(image_list, gif_name, duration = 0.35):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration = duration)
    return


def main():
    image_list = ['img1.jpg', 'img2.jpg']
    gif_name = 'diff.gif'
    duration = 0.1
    create_gif(image_list, gif_name, duration)