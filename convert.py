import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Convert csv from tilastopalvelu.fi to a format that standings-simulator can understand. 1. Download schedule as Excel 2. Open in spreadsheet 3. export as csv. Tested with libreoffice 6.0.7.3')
    parser.add_argument('-i', '--input-file', required=True)
    parser.add_argument('-o', '--output-file', required=True)
    args = parser.parse_args()
    result_lines = []
    with open(args.input_file, 'r') as file:
        for line in file:
            strip = line.strip()
            if strip == '' or strip[0] == '#':
                continue
            items = strip.split(',')
            home = items[4].strip()
            away = items[5].strip()
            if len(items) > 6 and len(items[6]) > 0:
                split = items[6].split('-')
                home_goals = int(split[0].strip())
                away_goals = int(split[1].strip())
                result = '1' if home_goals > away_goals else '2'
                if len(items) > 7 and len(items[7]) > 0:
                    result = result + 'OT'
                result_lines.append((home, away, result))
            else:
                result_lines.append((home, away))

    file.close()
    file = open(args.output_file, 'w')
    for result_line in result_lines:
        file.write(','.join(result_line) + '\n')
    file.close()


main()
