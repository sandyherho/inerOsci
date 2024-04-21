using LinearAlgebra
using Printf

# Constants
const pi = π
const freq = -2 * pi / (24 * 3600)
const f = 2 * freq
const dt = 6 * 24 * 3600 / 120
const alpha = f * dt
const beta = 0.25 * alpha^2
const ntot = 120
const uzero = 0.05
const vzero = 0.05
const initial_conditions = [0.1, 0.0, 0.0, 0.0]  # [u, v, x, y]

function update_positions_and_velocities(u, v, du, dv)
    ustar = u + du
    vstar = v + dv
    un = (ustar * (1 - beta) + alpha * vstar) / (1 + beta)
    vn = (vstar * (1 - beta) - alpha * ustar) / (1 + beta)
    return un, vn
end

function write_outputs(file, x, y, time)
    @printf(file, "%.6f %.6f %.2f\n", x, y, time)
end

function simulate(mode::Int)
    conditions = copy(initial_conditions)
    filename = "output_jl_$(mode).txt"
    
    open(filename, "w") do file
        @printf(file, "%f %f %d\n", freq, dt, ntot)
        
        for n in 1:ntot
            time = n * dt
            du, dv = if n == 40
                (0.0, -0.3)
            elseif n == 80
                (0.0, 0.1)
            else
                (0.0, 0.0)
            end
            
            if mode == 1
                u, v = update_positions_and_velocities(conditions[1], conditions[2], du, dv)
            else
                u = cos(alpha) * conditions[1] + sin(alpha) * conditions[2] + du
                v = cos(alpha) * conditions[2] - sin(alpha) * conditions[1] + dv
            end
            
            x = conditions[3] + dt * (u + uzero) / 1000
            y = conditions[4] + dt * (v + vzero) / 1000
            conditions = [u, v, x, y]
            
            write_outputs(file, x, y, time)
        end
    end
end

function main()
    simulate(1)
    simulate(2)
end

main()

