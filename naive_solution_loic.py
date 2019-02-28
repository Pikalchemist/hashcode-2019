#!/usr/bin/env python3

import numpy as np
from pakiwilib import *

def process(data):
    tags = set()
    for img in data.images:
        tags |= img[2]
    tags = list(tags)

    slides = [i for i in data.images if i[0] == 0]
    m_images = np.zeros((len(slides), len(tags), 2))
    for j, img, h in slides:
        for i, t in enumerate(tags):
            if t in img[2]:
                m_images[j, i, 0] = 1
                m_images[j, 0, 1] = img[1]

    result = []
    images = list(range(len(m_images)))
    N = 0
    img_id = np.random.randint(0, len(m_images))
    del images[img_id]
    result.append(img_id)
    while N < 10 and len(images) > 0:
        dists = np.zeros(len(images))
        for i, img2 in enumerate(images):
            dists[i] = np.sum(np.logical_xor(m_images[img_id,:,0], m_images[img2,:,0]))
        m = np.argmax(dists)
        result.append(images[m])
        del images[m]
        N += 1

    R = []
    for r in result:
        R.append((r,))
    return [result]

def process2(data):
    # 1. construct the slides
    v_imgs = [i for i in data.images[:] if i[1] ==1]
    p_slides = []
    while len(v_imgs) > 0:
        i1 = np.random.randint(0, len(v_imgs))
        i2 = i1
        while i2 == i1:
            i2 = np.random.randint(0, len(v_imgs))
        p_slides.append((v_imgs[i1], v_imgs[i2]))
        if i2 > i1:
            del v_imgs[i2]
            del v_imgs[i1]
        else:
            del v_imgs[i1]
            del v_imgs[i2]

    p_slides += [(i,) for i in data.images[:] if i[1] == 0]

    # 2. Populate slides
    slides = []
    i1 = np.random.randint(0, len(p_slides))
    s = p_slides[i1]
    slides.append(s)
    del p_slides[i1]

    # 3. prepare


    # 3. Random search
    K = 100
    while len(p_slides) > 0:
        last_slide = slides[-1]
        best_slide = -1
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
        del p_slides[best_slide]

    f_slides = [[i[0] for i in s] for s in slides]
    return f_slides

# s = Photoset("a_example")
# s = Photoset("c_memorable_moments")
s = Photoset("b_lovely_landscapes")
# s = Photoset("d_pet_pictures")
# s = Photoset("e_shiny_selfies")

r = process2(s)
slide = Slideshow(s, r)
print(s.score(slide))

slide.save()
