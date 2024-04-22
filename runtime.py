#!/usr/bin/env python

"""
runtime.py

Record the Execution Time

Sandy Herho <sandy.herho@email.ucr.edu>
04/22/2024
"""

import subprocess
import time
import pandas as pd

# File names for all scripts
file_names = ['iner_osci.f95', 'iner_osci.py', 'iner_osci.jl', 'iner_osci.m', 'iner_osci.R']
# Name for the executable
fortran_executable = 'iner_osci'

# Function to compile the Fortran program and measure the compilation time
def compile_fortran_program(source_path, output_executable):
    compile_command = ['gfortran', '-o', output_executable, source_path]
    start_time = time.time()  # Start time
    result = subprocess.run(compile_command, capture_output=True, text=True)
    end_time = time.time()  # End time
    
    compile_time = end_time - start_time  # Calculate compile time
    return compile_time, result.returncode, result.stdout, result.stderr

# Function to measure execution time for any script
def measure_execution_time(command):
    start_time = time.time()  # Start time
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    end_time = time.time()  # End time
    
    execution_time = end_time - start_time  # Calculate execution time
    return execution_time, result.returncode, result.stdout, result.stderr

if __name__ == "__main__":
    # Prepare a list to collect data
    data = []

    # Compile the Fortran program
    compile_time, compile_return_code, compile_stdout, compile_stderr = compile_fortran_program(file_names[0], fortran_executable)

    if compile_return_code == 0:
        # Run each program 1000 times
        for filename in file_names:
            if filename == 'iner_osci.f95':
                # Execute Fortran program
                for i in range(1000):
                    exec_time, return_code, stdout, stderr = measure_execution_time(f'./{fortran_executable}')
                    data.append({
                        'Script': filename,
                        'Execution Time': exec_time,
                        'Return Code': return_code,
                        'Output': stdout,
                        'Error': stderr
                    })
            elif filename.endswith('.py'):
                # Execute Python script
                for i in range(1000):
                    exec_time, return_code, stdout, stderr = measure_execution_time(f'python {filename}')
                    data.append({
                        'Script': filename,
                        'Execution Time': exec_time,
                        'Return Code': return_code,
                        'Output': stdout,
                        'Error': stderr
                    })
            elif filename.endswith('.jl'):
                # Execute Julia script
                for i in range(1000):
                    exec_time, return_code, stdout, stderr = measure_execution_time(f'julia {filename}')
                    data.append({
                        'Script': filename,
                        'Execution Time': exec_time,
                        'Return Code': return_code,
                        'Output': stdout,
                        'Error': stderr
                    })
            elif filename.endswith('.m'):
                # Execute Octave script
                for i in range(1000):
                    exec_time, return_code, stdout, stderr = measure_execution_time(f'octave-cli {filename}')
                    data.append({
                        'Script': filename,
                        'Execution Time': exec_time,
                        'Return Code': return_code,
                        'Output': stdout,
                        'Error': stderr
                    })
            elif filename.endswith('.R'):
                # Execute R script
                for i in range(1000):
                    exec_time, return_code, stdout, stderr = measure_execution_time(f'Rscript {filename}')
                    data.append({
                        'Script': filename,
                        'Execution Time': exec_time,
                        'Return Code': return_code,
                        'Output': stdout,
                        'Error': stderr
                    })
    else:
        print("Compilation of Fortran program failed. No execution will be performed.")

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to CSV
    csv_filename = 'multi_lang_execution_log_1000_runs.csv'
    df.to_csv(csv_filename, index=False)

    print(f'Data logged to {csv_filename} for 1000 runs across multiple languages.')

