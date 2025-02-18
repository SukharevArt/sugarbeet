import tools
import numpy
import file_manager as fm
from scipy.optimize import linear_sum_assignment


def gen_p_matrix(size: int, sugar_divider: int,
                 min_start_sugar: float, max_start_sugar: float,
                 min_sugaring: float, max_sugaring: float,
                 min_degradation: float, max_degradation: float):
    """Возвращает матрицу P для решения задачи оптимизации, используя заданные интервалы разброса начальных условий.\n
    size - размер матрицы P, sugar_divider - знаменатель дроби дозаривания (если = 2, то дозаривание будет 1/2 и т.п)\n
    min_start_sugar, max_start_sugar - интервал разброса стартовых значений сахаристости (должны быть от 0 до 1!)\n
    min_sugaring, max_sugaring - интервал разброса значений увеличения сахаристости на этапах дозаривания (должны быть больше 1!)
    min_degradation, max_degradation - коэффициенты деградации будут от min_degradation до max_degradation (должны быть от 0 до 1!)."""

    sugar_cols = size // sugar_divider
    degradation_cols = size - sugar_cols
    a_vector = tools.gen_vector(size, min_start_sugar, max_start_sugar)
    sugar_matrix = tools.gen_matrix(size, sugar_cols, min_sugaring, max_sugaring)
    degradation_matrix = tools.gen_matrix(size, degradation_cols, min_degradation, max_degradation)
    b_matrix = tools.unite_matrix(sugar_matrix, degradation_matrix)
    p_matrix = tools.create_p_matrix(a_vector, b_matrix)

    if fm.file_print:
        fm.create()
        fm.write_start_conditions(a_vector, b_matrix)
        fm.write_sugar_matrix(p_matrix)

    return p_matrix


def hungarian_min(p_matrix):
    """Возвращает результат и список-перестановку целевой функции, поиск худшего результата с помощью венгерского алгоритма."""
    row_indices, col_indices = linear_sum_assignment(p_matrix)
    result = 0
    for i in range(len(row_indices)):
        result += p_matrix[row_indices[i]][col_indices[i]]

    for i in range(len(row_indices)):
        row_indices[col_indices[i]] = i

    if fm.file_print:
        fm.write_algorithm_res("Венгерский (min)", result, row_indices)

    return result, row_indices


def hungarian_max(p_matrix):
    """Возвращает результат и список-перестановку целевой функции, поиск лучшего результата с помощью венгерского алгоритма."""
    max_elem = numpy.max(p_matrix)
    reverse_p_matrix = numpy.copy(p_matrix)
    for i in range(len(p_matrix)):
        for j in range(len(p_matrix)):
            reverse_p_matrix[i][j] = -1 * p_matrix[i][j] + max_elem

    row_indices, col_indices = linear_sum_assignment(reverse_p_matrix)
    result = 0
    for i in range(len(row_indices)):
        result += p_matrix[row_indices[i]][col_indices[i]]

    for i in range(len(row_indices)):
        row_indices[col_indices[i]] = i

    if fm.file_print:
        fm.write_algorithm_res("Венгерский (max)", result, row_indices)

    return result, row_indices


def greedy(p_matrix: list):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью жадного алгоритма."""
    result = 0
    indices = []
    took = []

    for j in range(len(p_matrix)):
        col_max = 0
        col_max_index: int
        for i in range(len(p_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if p_matrix[i][j] > col_max:
                col_max = p_matrix[i][j]
                col_max_index = i
        result += col_max
        indices.append(col_max_index)
        took.append(col_max_index)

    if fm.file_print:
        fm.write_algorithm_res("Жадный", result, indices)

    return result, indices


def saving(p_matrix: list):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью бережливого алгоритма."""
    result = 0
    indices = []
    took = []

    for j in range(len(p_matrix)):
        col_min = 10
        col_min_index: int
        for i in range(len(p_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if p_matrix[i][j] < col_min:
                col_min = p_matrix[i][j]
                col_min_index = i
        result += col_min
        indices.append(col_min_index)
        took.append(col_min_index)

    if fm.file_print:
        fm.write_algorithm_res("Бережливый", result, indices)

    return result, indices


def saving_greedy(p_matrix: list, saving_steps: int):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью бережливо-жадного алгоритма.\n
    saving_steps - количество шагов в режиме сбережения, далее будет жадный режим."""
    result = 0
    indices = []
    took = []
    saving_steps_completed = 0

    for j in range(len(p_matrix)):

        col_min = 10
        col_min_index: int

        col_max = 0
        col_max_index: int

        saving_mode = saving_steps_completed < saving_steps

        for i in range(len(p_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if saving_mode and p_matrix[i][j] < col_min:
                col_min = p_matrix[i][j]
                col_min_index = i

            if not saving_mode and p_matrix[i][j] > col_max:
                col_max = p_matrix[i][j]
                col_max_index = i

        if saving_mode:
            result += col_min
            indices.append(col_min_index)
            took.append(col_min_index)

        else:
            result += col_max
            indices.append(col_max_index)
            took.append(col_max_index)

        saving_steps_completed += 1

    if fm.file_print:
        fm.write_algorithm_res("Бережливо-жадный", result, indices)

    return result, indices



def greedy_saving(p_matrix: list, greedy_steps: int):
    """Возвращает результат и список-перестановку целевой функции, поиск результата с помощью жадно-бережливого алгоритма.\n
    greedy_steps - количество шагов в режиме жадности, далее будет бережливый режим."""
    result = 0
    indices = []
    took = []
    greedy_steps_completed = 0

    for j in range(len(p_matrix)):

        col_min = 10
        col_min_index: int

        col_max = 0
        col_max_index: int

        greedy_mode = greedy_steps_completed < greedy_steps

        for i in range(len(p_matrix)):
            is_took = False

            for k in range(len(took)):
                if took[k] == i:
                    is_took = True
                    break

            if is_took:
                continue

            if not greedy_mode and p_matrix[i][j] < col_min:
                col_min = p_matrix[i][j]
                col_min_index = i

            if greedy_mode and p_matrix[i][j] > col_max:
                col_max = p_matrix[i][j]
                col_max_index = i

        if greedy_mode:
            result += col_max
            indices.append(col_max_index)
            took.append(col_max_index)

        else:
            result += col_min
            indices.append(col_min_index)
            took.append(col_min_index)

        greedy_steps_completed += 1

    if fm.file_print:
        fm.write_algorithm_res("Жадно-бережливый", result, indices)

    return result, indices



