import os
def uniquename(filename):

    base, ext = os.path.splitext(filename)
    i = 1
    new_filename = filename

    while os.path.exists(new_filename):
        new_filename = "{}({}){}".format(base, i, ext)
        i += 1

    return new_filename

if __name__ == '__main__':
    print(uniquename('poopie.txt'))