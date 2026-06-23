import math


# =====================================================
# PATH DIFFERENCE SCORE
# =====================================================

def path_difference(path1, path2):

    differences = 0

    for a, b in zip(path1, path2):

        if a != b:

            differences += 1

    return differences / max(len(path1), 1)


# =====================================================
# DIVERSITY PRESERVATION
# =====================================================

def preserve_diversity(
    results,
    diversity_threshold=0.3
):

    diverse_results = []

    for candidate in results:

        keep = True

        for existing in diverse_results:

            diff = path_difference(
                candidate["path"],
                existing["path"]
            )

            # Too similar
            if diff < diversity_threshold:

                keep = False

                break

        if keep:

            diverse_results.append(candidate)

    return diverse_results