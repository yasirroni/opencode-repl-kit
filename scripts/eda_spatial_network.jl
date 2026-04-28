# scripts/eda_spatial_network.jl
# Julia REPL EDA — Spatial Network Analysis
# Run: julia --project=julia/PackageName scripts/eda_spatial_network.jl

using NCDatasets
using Arrow
using DataFrames
using Statistics
using LinearAlgebra
using Plots

gr()
mkpath("data/figures")

# === PHASE A: DATA LOADING ===
ds = NCDataset("data/grid_data.nc")
temperature = coalesce.(ds["temperature"][:,:,:], Float32(NaN))
pressure = coalesce.(ds["pressure"][:,:,:], Float32(NaN))
humidity = coalesce.(ds["humidity"][:,:,:], Float32(NaN))
elevation = coalesce.(ds["elevation"][:,:], Float32(NaN))
lat = Float32.(ds["lat"][:])
lon = Float32.(ds["lon"][:])
alt = Float32.(ds["alt"][:])
close(ds)

nodes_df = DataFrame(Arrow.Table("data/nodes.arrow"))
edges_df = DataFrame(Arrow.Table("data/edges.arrow"))

println("=== PHASE A: DATA LOADING ===")
println("Grid: $(size(temperature)) (lon=$(size(lon,1)) lon x lat=$(size(lat,1)) x alt=$(size(alt,1)))")
println("  alt: $alt")
println("  T range: $(extrema(temperature))")
println("  NaN in T: $(count(isnan, temperature))")
println("Nodes: $(size(nodes_df)) | $(names(nodes_df))")
println("Edges: $(size(edges_df)) | $(names(edges_df))")
println()

# === PHASE B: GRID EXPLORATION ===
temp_mean_per_alt = [mean(temperature[k,:,:]) for k in eachindex(alt)]
pressure_mean_per_alt = [mean(pressure[k,:,:]) for k in eachindex(alt)]
humidity_mean_per_alt = [mean(humidity[k,:,:]) for k in eachindex(alt)]

plot(alt, temp_mean_per_alt, xlabel="Altitude", ylabel="Mean Value", label="Temperature (K)", title="Vertical Profiles")
plot!(alt, pressure_mean_per_alt, label="Pressure (hPa)")
plot!(alt, humidity_mean_per_alt, label="Humidity (%)")
savefig("data/figures/vertical_profiles.png")
println("Saved: data/figures/vertical_profiles.png")

# === PHASE C: NETWORK TOPOLOGY ===
n_nodes = maximum(nodes_df.id_node) + 1
in_degree = zeros(Int, n_nodes)
out_degree = zeros(Int, n_nodes)

for row in eachrow(edges_df)
    src = row.id_edge_from + 1
    dst = row.id_edge_to + 1
    out_degree[src] += 1
    in_degree[dst] += 1
end

total_degree = in_degree .+ out_degree
isolated = findall(total_degree .== 0)
println("Isolated nodes: $(length(isolated)) of $n_nodes")
println("Degree: min=$(minimum(total_degree)), max=$(maximum(total_degree)), mean=$(round(mean(total_degree), digits=2))")

# Connected components (Union-Find)
parent = collect(0:n_nodes-1)
function find(x)
    while parent[x+1] != x
        parent[x+1] = parent[parent[x+1]+1]
        x = parent[x+1]
    end
    return x
end
function union!(a, b)
    ra, rb = find(a), find(b)
    if ra != rb
        parent[rb+1] = ra
    end
end

for row in eachrow(edges_df)
    union!(row.id_edge_from, row.id_edge_to)
end

component_sizes = Dict{Int, Int}()
for i in 0:n_nodes-1
    r = find(i)
    component_sizes[r] = get(component_sizes, r, 0) + 1
end

comp_sizes = sort(collect(values(component_sizes)), rev=true)
println("Components: $(length(comp_sizes)), Largest: $(maximum(comp_sizes))")
println("Sizes: $(comp_sizes[1:min(5,end)])")

scatter(in_degree, out_degree, xlabel="In-Degree", ylabel="Out-Degree", title="In-Degree vs Out-Degree", alpha=0.5)
savefig("data/figures/in_out_degree.png")
println("Saved: data/figures/in_out_degree.png")

histogram(comp_sizes, bins=20, xlabel="Component Size", ylabel="Count", title="Connected Component Sizes")
savefig("data/figures/component_sizes.png")
println("Saved: data/figures/component_sizes.png")

# === PHASE D: NODE-GRID INTEGRATION ===
lats = nodes_df.latitude
lons = nodes_df.longitude

function nearest_grid_idx(val, arr)
    idx = searchsortedfirst(arr, val)
    idx = clamp(idx, 1, length(arr))
    return idx
end

lat_idx = [nearest_grid_idx(l, lat) for l in lats]
lon_idx = [nearest_grid_idx(l, lon) for l in lons]

grid_elev_at_nodes = [elevation[lat_idx[i], lon_idx[i]] for i in eachindex(lats)]
node_elev = nodes_df.elevation
resid_elev = node_elev .- grid_elev_at_nodes
rmse_elev = sqrt(mean(resid_elev.^2))
println("Elevation RMSE: $(round(rmse_elev, digits=3)) m")

grid_temp_at_nodes = Float32[temperature[lon_idx[i], lat_idx[i], 10] for i in eachindex(lats)]
node_temp = nodes_df.measured_temp
valid = .!(isnan.(node_temp)) .& isfinite.(grid_temp_at_nodes)
resid_temp = node_temp[valid] .- grid_temp_at_nodes[valid]
rmse_temp = sqrt(mean(resid_temp.^2))
println("Temperature RMSE: $(round(rmse_temp, digits=3)) K (n=$(count(valid)))")

scatter(node_elev, resid_elev, xlabel="Node Elevation (m)", ylabel="Elevation Residual (m)", title="Elevation Residual vs Node Elevation", alpha=0.5)
savefig("data/figures/elev_residual.png")
println("Saved: data/figures/elev_residual.png")

scatter(node_temp[valid], resid_temp, xlabel="Measured Temperature (K)", ylabel="Temperature Residual (K)", title="Temperature Residual vs Measured Temp", alpha=0.5)
savefig("data/figures/temp_residual.png")
println("Saved: data/figures/temp_residual.png")

# === PHASE E: EDGE ANALYSIS ===
dist = edges_df.distance_km
weight = edges_df.weight
elev_change = edges_df.elevation_change

println("Distance: min=$(round(minimum(dist),digits=2)), max=$(round(maximum(dist),digits=2)), mean=$(round(mean(dist),digits=2)) km")
println("Weight: min=$(round(minimum(weight),digits=2)), max=$(round(maximum(weight),digits=2)), mean=$(round(mean(weight),digits=2))")
println("Uphill: $(count(elev_change.>0)), Downhill: $(count(elev_change.<0)), Flat: $(count(elev_change.==0))")
corr_dw = cor(dist, weight)
println("Corr(distance, weight): $(round(corr_dw, digits=3))")

scatter(dist, weight, xlabel="Distance (km)", ylabel="Weight", title="Weight vs Distance (r=$(round(corr_dw, digits=2)))", alpha=0.4)
savefig("data/figures/weight_vs_distance.png")
println("Saved: data/figures/weight_vs_distance.png")

histogram(dist, bins=30, xlabel="Distance (km)", ylabel="Count", title="Edge Distance Distribution")
savefig("data/figures/distance_distribution.png")
println("Saved: data/figures/distance_distribution.png")

# === PHASE F: NODE MAPS ===
scatter(lons, lats, marker_z=resid_elev, xlabel="Longitude", ylabel="Latitude", title="Nodes Colored by Elevation Residual", colorbar=true)
savefig("data/figures/node_map_elevation_residual.png")
println("Saved: data/figures/node_map_elevation_residual.png")

scatter(lons, lats, marker_z=node_elev, xlabel="Longitude", ylabel="Latitude", title="Nodes Colored by Elevation", colorbar=true)
savefig("data/figures/node_map_elevation.png")
println("Saved: data/figures/node_map_elevation.png")

println("\n=== ALL PHASES COMPLETE ===")
println("Figures saved to data/figures/")