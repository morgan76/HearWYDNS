import click
from sound_module import *
from image_processing import *
import random


@click.command()
@click.argument("image_path", type=str, default='Images/preview.jpg')
@click.option("--samples-dir-1", type=str, default='Samples/Melodic/')
@click.option("--samples-dir-2", type=str, default='Samples/Voices/')
@click.option("--samples-dir-3", type=str, default='Samples/Aggressive/')
@click.option("--samples-dir-4", type=str, default='Samples/Beat/')
@click.option("--mask-size", type=int, default=100)
@click.option("--nb-grn", type=int, default=3)
@click.option("--nb-clouds", type=int, default=1)
@click.option("--MIDDLE", type=int, default=60)
@click.option("--STD", type=int, default=8)
@click.option("--shuffle", type=bool, default=True)
@click.option("--record",type=bool,default=False)
@click.option("--normalize",type=bool,default=True)
@click.option("--verbose", type=int, default=0)


def main(
    image_path,
    samples_dir_1,
    samples_dir_2,
    samples_dir_3,
    samples_dir_4,
    mask_size,
    nb_grn,
    nb_clouds,
    middle,
    std,
    shuffle,
    record,
    normalize,
    verbose
):
    # Image processing initialization
    image = pre_process(image_path)

    # Extraction of sub-regions and entropy values
    list_regions, nb_regions = moving_mask(image, mask_size)
    list_blocks = extract_from_mask(list_regions)
    # Random shuffling of the extracted values, you can comment or uncomment this following line
    # if you want the list to be shuffled or not
    if shuffle:
        list_blocks = random.sample(list(list_blocks), len(list_blocks))

    # Sound module initialization
    sound = Sound_Module([nb_grn, nb_clouds], samples_dir_1, samples_dir_2, samples_dir_3, samples_dir_4, list_blocks, middle, std, record, normalize)


    # Performance start
    print('Warming up ...')
    sound.start()
    print('Starting performance ...')
    for i in range(sound.TOTAL):
        print('----------------------------------------------')
        # printing the current iteration
        print('I=',i, '/', sound.TOTAL)
        # printing current value of entropy
        if i>0:
            print('Current entropy value :', sound.list_blocks[i-1])
        # printing instruments currently playing
        if verbose>0:
            sound.get_instruments_playing(i)
        # reading the conductor
        sound.read_conductor(i)
        # reading the melodic conductor
        sound.read_melodic_conductor(i)
        # updating the cloud instruments
        sound.update_cloud(i)
        # reading the granular conductor
        sound.read_grn_conductor(i)
        # pausing after next iteration
        time.sleep(sound.update_time(i))

    # Performance end
    sound.stop()
    
if __name__ == "__main__":
    main()
