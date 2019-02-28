#!/usr/bin/env python3

import numpy as np
from pakiwilib import *

# IMG = "a_example"
# IMG = "b_lovely_landscapes"
# IMG = "c_memorable_moments"
# IMG = "d_pet_pictures"
IMG = "e_shiny_selfies"


def process(data):
    # 1. construct the slides
    v_imgs = [i for i in data.images[:] if i[1] == 1]
    p_slides = []
    K = 100
    while len(v_imgs) > 0:
        best_img = -1
        best_t = -1
        i1 = np.random.randint(0, len(v_imgs))
        s1 = v_imgs[i1]
        for k in range(K):
            i2 = i1
            o = 0
            while i2 == i1:
                i2 = np.random.randint(0, len(v_imgs))
            s2 = v_imgs[i2]

            A = len(s1[2] | s2[2])
            if A > best_t:
                best_t = A
                best_img = i2
        p_slides.append((v_imgs[i1], v_imgs[best_img]))
        i2 = best_img
        if i2 > i1:
            del v_imgs[i2]
            del v_imgs[i1]
        else:
            del v_imgs[i1]
            del v_imgs[i2]

    p_slides += [(i,) for i in data.images[:] if i[1] == 0]
    print("Populate Slides")

    # 2. Populate slides
    slides = []
    i1 = np.random.randint(0, len(p_slides))
    s = p_slides[i1]
    slides.append(s)
    del p_slides[i1]

    # 3. Random search
    K = 5000
    AA = 0
    SCORE = 0
    while len(p_slides) > 1:
        last_slide = slides[-1]
        best_slide1 = -1
        best_score = -1
        ls_tags = set()
        for i in last_slide:
            ls_tags |= i[2]
        for k in range(K):
            i1 = np.random.randint(0, len(p_slides))
            S = p_slides[i1]

            s_tags = set()
            for i in S:
                s_tags |= i[2]

            A = len(s_tags & ls_tags)
            B = len(s_tags - ls_tags)
            C = len(ls_tags - s_tags)
            score = min(A, B, C)

            if score > best_score:
                best_score = score
                best_slide = i1

        s = p_slides[best_slide]
        slides.append(s)
        SCORE += best_score
        del p_slides[best_slide]
        AA += 1
        if AA % 1000 == 0:
            print(SCORE, len(slides), len(p_slides))

    f_slides = [[i[0] for i in s] for s in slides]
    return f_slides


def main():
    s = Photoset(IMG)
    print(IMG)

    r = process(s)
    slide = Slideshow(s, r)
    print(IMG, s.score(slide))

    slide.save()


if __name__ == "__main__":
    main()
