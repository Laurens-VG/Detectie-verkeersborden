import argparse
import glob
from testbench import *


"""
main.py wordt gebruikt om de testbench te starten
argumenten: --method: naam van de te testen methode (gebruik videos of images)
            --dataset: naam van de dataset (gebruik vb: dag, nacht, schemering)
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Testbench verkeersborddetectie')
    parser.add_argument("--method",
                        help="method name (images, videos)",
                        default="videos")
    parser.add_argument('--dataset', help='dataset name (example: dag)', default="nacht")
    args = parser.parse_args()
    if args.method == "images":
        testbench_images(args.dataset)
    elif args.method == "videos":
        start = 0
        while True:
            vidname = glob.glob('videos/' + args.dataset + '/*.mp4')
            iterate_video(vidname[start])
            start += 1
    else:
        print("bad method name")
        exit()
