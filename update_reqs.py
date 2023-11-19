import subprocess
import time

from tqdm import tqdm

# Export Conda environment to environment.yml
print("Exporting Conda environment to environment.yml...")
for i in tqdm(range(100)):
    time.sleep(0.01)
subprocess.run(
    """conda env export | python -c "import sys; print(''.join(line for line in sys.stdin if 'prefix: ' not in line))" > environment.yml""",
    shell=True,
    check=True,
)

print("Exporting Conda list to requirements.txt...")
for i in tqdm(range(100)):
    time.sleep(0.01)
subprocess.run("conda list --export > requirements.txt", shell=True, check=True)

print("Done!")


# subprocess.run(
#     "poetry export --output requirements.txt", shell=True, check=True
# )
# msg(
#     "Updated [bright_yellow]requirements.txt[/bright_yellow] [green3]"
#     "successfully[/green3].",
#     "success",
# )
