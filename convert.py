# load pandas
import pandas as pd
import datetime
import argparse

INPUT_FILE = 'input-statements.psv'
OUTPUT_FILE = 'output-sessions.psv'

def convert(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    # read file as pandas dataframe
    df = pd.read_csv(input_file,sep='|')

    df['HomeNo'] = df['HomeNo'].astype(str)

    df = df.sort_values(['HomeNo',"Starttime"])

    df['StarttimeConv'] =  pd.to_datetime(df['Starttime'], format='%Y%m%d%H%M%S')

    df['HomeNo_s'] = df['HomeNo'].shift(-1)

    df['StarttimeConv_s'] = df['StarttimeConv'].shift(-1)

    def end_time_conv (row):
        if row['HomeNo'] == row['HomeNo_s']:
            X=1
            end_date = row['StarttimeConv_s'] - datetime.timedelta(seconds=X)
            return end_date
        else:
            end_date = datetime.datetime(row['StarttimeConv'].year, row['StarttimeConv'].month, row['StarttimeConv'].day, 23, 59, 59) # .timestamp()
            return end_date
        
    df.apply (lambda row: end_time_conv(row), axis=1)

    df['EndTimeConv'] = df.apply (lambda row: end_time_conv(row), axis=1)

    def end_time (row):
        return row['EndTimeConv'].strftime('%Y%m%d%H%M%S')

    df['EndTime'] = df.apply (lambda row: end_time(row), axis=1)

    def duration (row):
        if row['HomeNo'] == row['HomeNo_s'] :
            ego = row['StarttimeConv_s'] - row['StarttimeConv']
            return ego.total_seconds()
        else:
            end_date = datetime.datetime(row['StarttimeConv'].year, row['StarttimeConv'].month, row['StarttimeConv'].day, 23, 59, 59) # .timestamp()
            ego = end_date - row['StarttimeConv']
            return ego.total_seconds()+1
        
    df.apply (lambda row: duration(row), axis=1)

    df['Duration'] = df.apply (lambda row: duration(row), axis=1)

    df = df.astype({'Duration': 'int64'})

    df = df.drop(columns=['StarttimeConv', 'HomeNo_s', 'StarttimeConv_s', 'EndTimeConv'])

    print(df)

    df.to_csv(output_file, sep='|', index=False)

    
if __name__ == "__main__":
    # execute only if run as a script

    parser = argparse.ArgumentParser(description='Get input and output files names')
    parser.add_argument('--input_file', type=str, default=INPUT_FILE,
                        help='an input file path')
    parser.add_argument('--output_file', type=str, default=OUTPUT_FILE,
                        help='an output file path)')

    args = parser.parse_args()

    convert(str(args.input_file), str(args.output_file))
