import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

target = input("Enter target URL: ")

headers = {
    "User-Agent": "Mozilla/5.0"
}

interesting = []

with open("params.txt") as file:
    params = file.read().splitlines()

print(Fore.CYAN + "\n[+] Starting Parameter Fuzzing...\n")


def fuzz(param):
    url = f"{target}?{param}=test"

    try:
        response = requests.get(url, headers=headers, timeout=3)

        length = len(response.text)

        result = f"[{response.status_code}] {url} | Length: {length}"

        print(Fore.GREEN + result)

        interesting.append(result)

    except requests.exceptions.RequestException:
        pass


with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(fuzz, params)

with open("results.txt", "w") as file:
    for item in interesting:
        file.write(item + "\n")

print(Fore.YELLOW + "\n[+] Fuzzing Completed")
print(Fore.YELLOW + "[+] Results saved to results.txt")