# include() Workflow Template

# Write your Julia code here, then execute in REPL:
# pty_write(data="include(\"temp/this_file.jl\")\n")

function my_function(data)
    # Replace with your function
    return data .* 2
end

struct MyProcessor
    data::Vector{Float64}
end

function process(p::MyProcessor)
    return my_function(p.data)
end
