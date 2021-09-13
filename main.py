import os
import subprocess
import sys
import time

import colorama

colorama.init()

print(
    f"---> {colorama.Back.MAGENTA}{colorama.Fore.WHITE}xxxcept{colorama.Style.RESET_ALL} | {colorama.Fore.MAGENTA}{colorama.Back.WHITE}check yo damn file's hashes{colorama.Style.RESET_ALL}"
)

if sys.argv[1:] == []:
    print(
        "---> You need to drag and drop file(s) onto the script!\n--> How am I going to check for hashes if there is nothing there?\n-> Who do you think I am?"
    )
    time.sleep(5)
    quit(1)

hash_algorithms = ["MD4", "MD5", "SHA1", "SHA256", "SHA512"]
hash_store = []
matched_hashes = 0
total_hashes = 0

idx: int
file: str
for idx, file in enumerate(sys.argv[1:]):
    hash_store.append([])
    print(f"--> [{colorama.Fore.YELLOW}{file}{colorama.Style.RESET_ALL}]")
    algo: str
    for algo in hash_algorithms:
        try:
            process = subprocess.Popen(
                ["Certutil", "-hashfile", file, algo],
                stdout=subprocess.PIPE,
                text=True,
            )
            out = process.communicate()

            if out:
                hash_store[idx].append(out[0].split()[4:][0])
            else:
                print(
                    "---> There has been an error. The program will quit in 5 seconds..."
                )
                time.sleep(5)
        except subprocess.CalledProcessError as err:
            print(err)
            time.sleep(5)
            quit(1)
    hash_store[idx].append(file)

    algo: str
    for algo in hash_algorithms:
        print(f"-> {algo}: {hash_store[idx][hash_algorithms.index(algo)]}")

if len(hash_store) > 1:  # If there is more than one file provided
    hash_group: list
    for hash_group in hash_store:  # For every file (hash group) in the hashes array
        match_type = []
        matched_hashes = 0
        total_hashes = len(hash_group) - 1
        hash_group2: list
        for hash_group2 in hash_store:
            matched_hashes = 0
            if hash_group == hash_group2:
                break
            hash: str
            for hash in hash_group:
                if hash in sys.argv[1:]:  # Excluding file path
                    break
                hash2: str
                for hash2 in hash_group2:
                    if hash2 in sys.argv[1:]:
                        break
                    if hash == hash2:
                        matched_hashes += 1
                        match_type.append(hash_algorithms[hash_group.index(hash)])
            if matched_hashes == total_hashes:  # If all the file's hashes match
                print(
                    f"---> {colorama.Fore.GREEN}[FILE_MATCH]{colorama.Style.RESET_ALL} "
                    + f"[{colorama.Fore.YELLOW}{hash_group[5]}{colorama.Style.RESET_ALL}] [{colorama.Fore.YELLOW}{hash_group2[5]}{colorama.Style.RESET_ALL}]"
                )

os.system("pause")
