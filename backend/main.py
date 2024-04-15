# main.py
import subprocess

def main():
    abbr = input("Enter the NBA team abbreviation: ")
    season_year = input("Enter the season year (e.g., 2023): ")
    
    # Call the other Python script and pass the inputs as arguments
    subprocess.run(['python', 'team_stats.py', abbr, season_year], check=True)

if __name__ == "__main__":
    main()
