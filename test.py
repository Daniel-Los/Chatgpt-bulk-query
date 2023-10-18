import sys

print(sys.argv)
# programme, project_name, folder_path, test_run, prompt_input, output_folder, arg_7, arg_8 = sys.argv
command=sys.argv
def test(arg):
    print('henlo', arg)
# arg1 = test_run

test(command[0])
