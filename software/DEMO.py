import cv2
from testbench import *


def main():
    iterate_video("videos/dag/signs_2.mp4")
    iterate_video("videos/schemering/S_signs.mp4")
    iterate_video("videos/nacht/N_signs_3.mp4")

    iterate_video("videos/dag/signs_5.mp4")
    iterate_video("videos/schemering/S_signs_2.mp4")
    iterate_video("videos/nacht/N_signs_2.mp4")

    iterate_video("videos/dag/no_sign_3.mp4")
    iterate_video("videos/schemering/S_no_sign_4.mp4")
    iterate_video("videos/nacht/N_no_sign_4.mp4")


if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
