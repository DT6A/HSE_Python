import numpy as np

from matrices import *

if __name__ == '__main__':
    # Easy
    np.random.seed(0)
    matrs = [np.random.randint(0, 10, (10, 10)) for _ in range(2)]
    my_matrs = list(map(lambda x: MyMatrix(x.tolist()), matrs))

    # `*` symbol is not supported on Windows in file names
    with open('artifacts/easy/matrix_plus.txt', 'w') as f:
        f.write(str(my_matrs[0] + my_matrs[1]))
    with open('artifacts/easy/matrix_star.txt', 'w') as f:
        f.write(str(my_matrs[0] * my_matrs[1]))
    with open('artifacts/easy/matrix_at.txt', 'w') as f:
        f.write(str(my_matrs[0] @ my_matrs[1]))

    # Medium
    mixin_matrs = list(map(lambda x: MixinMatrix(x.tolist()), matrs))
    (mixin_matrs[0] + mixin_matrs[1]).save_to_file('artifacts/medium/matrix_plus.txt')
    (mixin_matrs[0] * mixin_matrs[1]).save_to_file('artifacts/medium/matrix_star.txt')
    (mixin_matrs[0] @ mixin_matrs[1]).save_to_file('artifacts/medium/matrix_at.txt')

    # Hard
    np.random.seed(0)
    while True:
        A = np.random.randint(0, 3, (3, 3))
        B = np.random.randint(0, 3, (3, 3))
        C = np.random.randint(0, 3, (3, 3))
        D = np.array(B)
        if (hash(MyMatrix(A.tolist())) == hash(MyMatrix(C.tolist()))) and (A != C).any() and (B == D).all() and (
                A @ B != C @ D).any():
            break

    mA = MyMatrix(A.tolist())
    mB = MyMatrix(B.tolist())
    mC = MyMatrix(C.tolist())
    mD = MyMatrix(D.tolist())

    with open('artifacts/hard/A.txt', 'w') as f:
        f.write(str(mA))
    with open('artifacts/hard/B.txt', 'w') as f:
        f.write(str(mB))
    with open('artifacts/hard/C.txt', 'w') as f:
        f.write(str(mC))
    with open('artifacts/hard/D.txt', 'w') as f:
        f.write(str(mD))
    with open('artifacts/hard/AB.txt', 'w') as f:
        f.write(str(mA @ mB))
    with open('artifacts/hard/CD.txt', 'w') as f:
        f.write(str(MyMatrix((C @ D).tolist())))
    with open('artifacts/hard/hash.txt', 'w') as f:
        f.write(str(hash(mA @ mB)) + ' ' + str(hash(mC @ mD)))
