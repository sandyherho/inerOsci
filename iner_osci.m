%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% iner_osci.m                                              %
%                                                          %
% 2D Idealized Inertial Oscillation Solver                 %
%                                                          %
% Sandy Herho <sandy.herho@email.ucr.edu>                  %
%                                                          %
% 04/21/2024                                               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Constants defined globally
pi = 3.141592653589793;
freq = -2 * pi / (24 * 3600);
f = 2 * freq;
dt = 6 * 24 * 3600 / 120;
alpha = f * dt;
beta = 0.25 * alpha^2;
ntot = 120;
uzero = 0.05;
vzero = 0.05;
initial_conditions = [0.1, 0.0, 0.0, 0.0];  % [u, v, x, y]

function [un, vn] = update_positions_and_velocities(u, v, du, dv, alpha, beta)
    ustar = u + du;
    vstar = v + dv;
    un = (ustar * (1 - beta) + alpha * vstar) / (1 + beta);
    vn = (vstar * (1 - beta) - alpha * ustar) / (1 + beta);
endfunction

function write_outputs(file_id, x, y, time)
    fprintf(file_id, '%.6f %.6f %.2f\n', x, y, time);
endfunction

function simulate(mode, initial_conditions, alpha, beta, uzero, vzero, ntot, dt, freq)
    conditions = initial_conditions;
    filename = sprintf('output_octave_%d.txt', mode);
    file_id = fopen(filename, 'w');
    fprintf(file_id, '%f %f %d\n', freq, dt, ntot);
    
    for n = 1:ntot
        time = n * dt;
        if n == 40
            du = 0.0;
            dv = -0.3;
        elseif n == 80
            du = 0.0;
            dv = 0.1;
        else
            du = 0.0;
            dv = 0.0;
        endif
        
        if mode == 1
            [u, v] = update_positions_and_velocities(conditions(1), conditions(2), du, dv, alpha, beta);
        else
            u = cos(alpha) * conditions(1) + sin(alpha) * conditions(2) + du;
            v = cos(alpha) * conditions(2) - sin(alpha) * conditions(1) + dv;
        endif
        
        x = conditions(3) + dt * (u + uzero) / 1000;
        y = conditions(4) + dt * (v + vzero) / 1000;
        conditions = [u, v, x, y];
        
        write_outputs(file_id, x, y, time);
    endfor
    
    fclose(file_id);
endfunction

% Main function to run simulations
simulate(1, initial_conditions, alpha, beta, uzero, vzero, ntot, dt, freq);
simulate(2, initial_conditions, alpha, beta, uzero, vzero, ntot, dt, freq);

