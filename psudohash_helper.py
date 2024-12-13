import subprocess
import os

def get_input(prompt, default=None):
    user_input = input(f"{prompt} [{default}]: " if default else f"{prompt}: ").strip()
    return user_input if user_input else default

def ask_yes_no(prompt):
    while True:
        choice = input(f"{prompt} (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please respond 'y' for yes or 'n' for no.")

def main():
    print("\n|-- Welcome to the Interactive Command Generator for psudohash.py --|\n")
    print(  "|   Keep in mind that each additional configuration you add,        |")
    print(  "|   will make the generated dictionary much larger.                 |\n")
    
    # Get the keywords
    keywords = []
    while True:
        word = get_input("Enter a keyword to mutate on (or press Enter to finish)")
        if word:
            keywords.append(word)
        else:
            break
    if not keywords:
        print("You must enter at least one keyword.")
        return
    
    # Join keywords
    words_option = ','.join(keywords)
    
    # Ask about numbering
    append_numbering = ask_yes_no("\nDo you want to add numbering to the end of the words?")
    numbering_level = ""
    numbering_limit = ""
    if append_numbering:
        numbering_level = get_input("\tNumbering level (example: 1 -ex.: 1-, 2 -ex.: 01-, or 3 -ex.: 001-)", "1")
        numbering_limit = get_input("\tNumbering limit (example: 50)", "50")
    
    # Ask about years
    append_years = ask_yes_no("\nDo you want to add years to the end of the words?")
    years_option = ""
    if append_years:
        years_option = get_input("\tEnter the years (example: 2020 or 1990-2022 or 2000,2022)")
    
    # Ask about paddings
    append_paddings = ask_yes_no("\nDo you want to add common symbols at the start or end of the words?")
    custom_paddings = ""
    if append_paddings:
        paddings_before = ask_yes_no("\tAdd symbols to the start of the words?")
        paddings_after = ask_yes_no("\tAdd symbols to the end of the words?")
        custom_paddings = get_input("\tEnter your own symbols separated by commas (optional)", "")
    
    # Output file
    output_file = get_input("\nOutput file name", "output.txt")
    
    # Generate command
    command = ["python3", "psudohash.py", "-w", words_option, "-o", output_file]
    
    if append_numbering:
        command += ["-an", numbering_level, "-nl", numbering_limit]
    if append_years and years_option:
        command += ["-y", years_option]
    if append_paddings:
        if paddings_before:
            command.append("-cpb")
        if paddings_after:
            command.append("-cpa")
        if custom_paddings:
            command += ["-ap", custom_paddings]
    
    # Show final command
    print("\nGenerated command:")
    print(" ".join(command))
    
    # Confirm execution
    execute = ask_yes_no("\nDo you want to execute this command now?")
    if execute:
        try:
            subprocess.run(command, check=True)
            print(f"\nExecution completed. The results are in {output_file}.")
        except subprocess.CalledProcessError as e:
            print(f"Error during command execution: {e}")
        except FileNotFoundError:
            print("Error: Make sure psudohash.py is in the same directory or the correct path.")
    else:
        print("\nExecution canceled. Copy and paste the command if you want to run it manually.")

if __name__ == "__main__":
    main()
