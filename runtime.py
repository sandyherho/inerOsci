import subprocess
import time
import pandas as pd

# Path to the source code files
fortran_source = 'iner_osci.f95'
python_script = 'iner_osci.py'
julia_script = 'iner_osci.jl'

# Name for the executable
fortran_executable = 'iner_osci'

# Function to measure execution time for any script
def measure_execution_time(command):
    start_time = time.time()  # Start time
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    end_time = time.time()  # End time
    
    execution_time = end_time - start_time  # Calculate execution time
    return execution_time, result.returncode, result.stdout, result.stderr

# Compile the Fortran program
compile_command = f'gfortran {fortran_source} -o {fortran_executable}'
compile_time, compile_return_code, compile_stdout, compile_stderr = measure_execution_time(compile_command)

# Prepare a list to collect data
data = []

if compile_return_code == 0:
    # Run each program 1000 times
    for i in range(1000):
        # Measure execution time for Fortran
        f_exec_time, f_return_code, f_stdout, f_stderr = measure_execution_time(f'./{fortran_executable}')
        
        # Measure execution time for Python
        p_exec_time, p_return_code, p_stdout, p_stderr = measure_execution_time(f'python {python_script}')
        
        # Measure execution time for Julia
        j_exec_time, j_return_code, j_stdout, j_stderr = measure_execution_time(f'julia {julia_script}')
        
        # Append each run's data to the list
        data.append({
            'Run': i + 1,
            'Fortran Execution Time': f_exec_time,
            'Python Execution Time': p_exec_time,
            'Julia Execution Time': j_exec_time,
            'Fortran Return Code': f_return_code,
            'Python Return Code': p_return_code,
            'Julia Return Code': j_return_code,
            'Fortran Output': f_stdout,
            'Python Output': p_stdout,
            'Julia Output': j_stdout,
            'Fortran Error': f_stderr,
            'Python Error': p_stderr,
            'Julia Error': j_stderr
        })
else:
    print("Compilation of Fortran program failed. No execution will be performed.")

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to CSV
csv_filename = 'multi_lang_execution_log.csv'
df.to_csv(csv_filename, index=False)

print(f'Data logged to {csv_filename} for 1000 runs across Fortran, Python, and Julia.')

