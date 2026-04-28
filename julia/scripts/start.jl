using Pkg

cd("opencode/opencode-cli-repl-demo/julia/PackageName")

Pkg.activate(".")
Pkg.instantiate()
Pkg.update()
Pkg.precompile()

println("Base.active_project(): ", Base.active_project())
