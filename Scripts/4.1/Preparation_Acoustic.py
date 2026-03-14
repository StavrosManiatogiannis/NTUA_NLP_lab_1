import os
import subprocess

# The directory KALDI is installed in
kaldi_directory = os.path.expanduser("~/kaldi/")

# The directory WSJ files are in
wsj_s5_directory = kaldi_directory + "/egs/wsj/s5"

# The directory USC files should be in
usc_directory = kaldi_directory + "/egs/usc"


# Copy path.sh
subprocess.run(["cp", f"{wsj_s5_directory}/path.sh", f"{usc_directory}/path.sh"])

# Copy cmd.sh
subprocess.run(["cp", f"{wsj_s5_directory}/cmd.sh", f"{usc_directory}/cmd.sh"])


# Change KALDI_ROOT in path.sh to kaldi_directory
path_file_lines = []
with open(f"{usc_directory}/path.sh", "r") as path_file:
    path_file_lines = path_file.readlines()

path_file_lines[0] = f"export KALDI_ROOT={kaldi_directory}\n"

with open(f"{usc_directory}/path.sh", "w") as path_file:
    path_file.writelines(path_file_lines)



# Change "queue.pl" to "run.pl" in cmd.sh

cmd_file_lines = []
with open(f"{usc_directory}/cmd.sh", "r") as cmd_file:
    cmd_file_lines = cmd_file.readlines()

cmd_file_lines[12] = "export train_cmd = run.pl\n"
cmd_file_lines[13] = "export decode_cmd=\"run.pl\" --mem 2G\n"
cmd_file_lines[15] = "export cuda_cmd=\"run.pl --gpu 1\"\n"


with open(f"{usc_directory}/cmd.sh", "w") as cmd_file:
    cmd_file.writelines(cmd_file_lines)



# Create soft link to "steps"
subprocess.run(["ln","-s", f"{wsj_s5_directory}/steps", f"{usc_directory}/steps"])

# Create soft link to "utils"
subprocess.run(["ln","-s", f"{wsj_s5_directory}/utils", f"{usc_directory}/utils"])

# Create "local" directory
subprocess.run(["mkdir", f"{usc_directory}/local"])

# Create soft link to "_kaldi.sh"
subprocess.run(["ln", "-s", f"{usc_directory}/steps/_kaldi.sh", f"{usc_directory}/local/_kaldi.sh"])

# Create the conf folder
subprocess.run(["mkdir", f"{usc_directory}/conf",])

# Copy mfcc.conf
subprocess.run(["cp", f"{wsj_s5_directory}/conf/mfcc.conf", f"{usc_directory}/conf/mfcc.conf"])

# Create directories inside data
dir_to_create = ["lang", "local", "local/dict", "local/lm_tmp", "local/nist_lm"]
dir_to_create = [f"{usc_directory}/data/{dir}" for dir in dir_to_create]
subprocess.run(["mkdir", *dir_to_create])
