from pakiwilib import *
import numpy as np
import copy


class Pikaset(Photoset):
    def __init__(self, setname):
        super(Pikaset, self).__init__(setname)

    def random_vertical_combos(self):
        verticals = self.array[self.array[:, 1] == self.VERTICAL][:, 0]
        shuffled = np.random.permutation(verticals).reshape((verticals.shape[0] // 2, 2))
        return shuffled

    def process(self):
        combo_ids = self.random_vertical_combos()
        verticals = np.array([self.array[ida, 2] | self.array[idb, 2] for ida, idb in combo_ids])
        horizontals = self.array[self.array[:, 1] == self.HORIZONTAL][:, 2]

        newset = np.hstack([horizontals, verticals])

        horizontal_ids = (self.array[self.array[:, 1] == self.HORIZONTAL][:, 0])[:, np.newaxis]
        newset_ids = np.vstack([np.hstack([horizontal_ids, np.full_like(horizontal_ids, -1)]), combo_ids])
        # print(newset)
        # print(newset_ids)

        def score(tag1, tag2):
            return min(len(tag1 & tag2), len(tag1 - tag2), len(tag2 - tag1))

        ids_next = np.arange(newset.shape[0])
        score_matrix = np.array([[score(tag1, tag2) for tag2 in newset] for tag1 in newset])
        np.fill_diagonal(score_matrix, -100)
        slides = []

        current_score_matrix = copy.copy(score_matrix)

        # First couple
        maximum_ids = np.unravel_index(np.argmax(current_score_matrix), current_score_matrix.shape)
        maximum_id = maximum_ids[0]
        slides.append(ids_next[maximum_id])
        ids_next = np.delete(ids_next, maximum_id, axis=0)
        current_score_matrix = np.delete(current_score_matrix, maximum_id, axis=1)
        current_id = maximum_id

        # Others
        while True:
            # print('============')
            # print(current_id)
            # print(ids_next)
            # print(current_score_matrix)

            if current_score_matrix.shape[1] == 0:
                break

            maximum_id = np.argmax(current_score_matrix[current_id, :])
            # print('max')
            # print(ids_next[maximum_id])
            if ids_next[maximum_id] == current_id:
                break
            slides.append(ids_next[maximum_id])
            ids_next = np.delete(ids_next, maximum_id, axis=0)
            current_score_matrix = np.delete(current_score_matrix, maximum_id, axis=1)
            current_id = maximum_id
        # for i in range(score_matrix.shape[0]):
        #     maximum_ids = np.unravel_index(np.argmax(current_score_matrix), current_score_matrix.shape)
        #     if ids_first[maximum_ids[0]] == ids_second[maximum_ids[1]]:
        #         break
        #
        #     if first:
        #         first = False
        #         slides.append(ids_first[maximum_ids[0]])
        #     slides.append(ids_first[maximum_ids[1]])
        #
        #     # print()
        #     # print(current_score_matrix)
        #     # print(ids_first)
        #     # print(ids_second)
        #     # print(maximum_ids)
        #
        #     # Delete from available slide
        #     current_score_matrix = np.delete(current_score_matrix, maximum_ids[0], axis=0)
        #     ids_first = np.delete(ids_first, maximum_ids[0], axis=0)
        #     current_score_matrix = np.delete(current_score_matrix, maximum_ids[1], axis=1)
        #     ids_second = np.delete(ids_second, maximum_ids[1], axis=0)
        #     # if first:
        #     #     current_score_matrix = np.delete(current_score_matrix, maximum_ids[1], axis=1)
        #     #     ids_second = np.delete(ids_second, maximum_ids[1], axis=0)

        # print(slides)
        # print('hey')

        real_slides = newset_ids[np.array(slides)]
        real_slides = [(slide[0], ) if slide[1] == -1 else (slide[0], slide[1]) for slide in real_slides]

        return Slideshow(self, real_slides)
