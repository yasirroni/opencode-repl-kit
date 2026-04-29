# scripts/eda_spatial_network.jl
# Julia REPL EDA — Spatial Network Analysis
# Run: julia --project=julia/PackageName scripts/eda_spatial_network.jl
#
# Generated from iterative REPL exploration:
#   temp/eda_01_load.jl → temp/eda_06_plots.jl
# Consolidated: Phase A through F

using NCDatasets
using Arrow
using DataFrames
using Statistics
using Printf
using Plots

gr()
mkpath("data/figures")

# Helper: mean ignoring NaN
nanmean(a) = mean(a[.!isnan.(a)])
nanstd(a) = std(a[.!isnan.(a)])

# Nearest grid index helper
function nearest_grid_idx(val, arr)
    idx = searchsortedfirst(arr, val)
    return clamp(idx, 1, length(arr))
end

# =============================================================================
# PHASE A: DATA LOADING
# =============================================================================
println("=== PHASE A: DATA LOADING ===")

ds = NCDataset("data/grid_data.nc")
temperature = coalesce.(ds["temperature"][:,:,:], Float32(NaN))
pressure    = coalesce.(ds["pressure"][:,:,:], Float32(NaN))
humidity    = coalesce.(ds["humidity"][:,:,:], Float32(NaN))
elevation   = coalesce.(ds["elevation"][:,:], Float32(NaN))
lat = Float32.(ds["lat"][:])
lon = Float32.(ds["lon"][:])
alt = Float32.(ds["alt"][:])
close(ds)

nodes_df = DataFrame(Arrow.Table("data/nodes.arrow"))
edges_df = DataFrame(Arrow.Table("data/edges.arrow"))

println("Grid: $(size(temperature)) (lon×lat×alt)")
println("  lon: $(extrema(lon)) [$(length(lon)) levels]")
println("  lat: $(extrema(lat)) [$(length(lat)) levels]")
println("  alt: $alt [$(length(alt)) levels]")
println("  T: range=$(extrema(temperature)), NaN=$(count(isnan, temperature))")
println("  P: range=$(extrema(pressure)),    NaN=$(count(isnan, pressure))")
println("  H: range=$(extrema(humidity)),    NaN=$(count(isnan, humidity))")
println("  E: range=$(extrema(elevation)),   NaN=$(count(isnan, elevation))")
println("Nodes: $(size(nodes_df)) | $(names(nodes_df))")
println("Edges: $(size(edges_df)) | $(names(edges_df))")
println()

# =============================================================================
# PHASE B: GRID EXPLORATION
# =============================================================================
println("=== PHASE B: GRID EXPLORATION ===")

# Vertical profiles
println("\n--- Vertical Profiles ---")
for k in eachindex(alt)
    t_mean = nanmean(temperature[:,:,k])
    p_mean = nanmean(pressure[:,:,k])
    h_mean = nanmean(humidity[:,:,k])
    @printf("  alt=%2d: T=%8.2f K  P=%8.2f hPa  H=%6.2f%%\n", alt[k], t_mean, p_mean, h_mean)
end

# NaN distribution per altitude
println("\n--- NaN count per altitude ---")
for k in eachindex(alt)
    @printf("  alt=%2d: T=%4d  P=%4d  H=%4d\n", alt[k],
        count(isnan, temperature[:,:,k]),
        count(isnan, pressure[:,:,k]),
        count(isnan, humidity[:,:,k]))
end

# Figure 1: Vertical Profiles
temp_mean_per_alt = [nanmean(temperature[:,:,k]) for k in eachindex(alt)]
press_mean_per_alt = [nanmean(pressure[:,:,k]) for k in eachindex(alt)]
hum_mean_per_alt = [nanmean(humidity[:,:,k]) for k in eachindex(alt)]

p1 = plot(alt, temp_mean_per_alt, marker=:circle, xlabel="Altitude Level", ylabel="Mean Value",
    label="Temperature (K)", title="Vertical Profiles", linewidth=2)
plot!(alt, press_mean_per_alt ./ 100, marker=:square, label="Pressure/100", linewidth=2)
plot!(alt, hum_mean_per_alt, marker=:diamond, label="Humidity (%)", linewidth=2)
savefig(p1, "data/figures/vertical_profiles.png")
println("\nSaved: data/figures/vertical_profiles.png")

# Figure 2: Surface Temperature
surf_T = temperature[:,:,1]
p2 = heatmap(surf_T', xlabel="Longitude Index", ylabel="Latitude Index",
    title="Surface Temperature (alt=0)", colorbar=true, clim=(200, 260))
savefig(p2, "data/figures/surface_temp.png")
println("Saved: data/figures/surface_temp.png")

# Figure 3: Elevation Grid
p3 = heatmap(elevation', xlabel="Longitude Index", ylabel="Latitude Index",
    title="Grid Elevation (m)", colorbar=true)
savefig(p3, "data/figures/elevation_grid.png")
println("Saved: data/figures/elevation_grid.png")

# =============================================================================
# PHASE C: NETWORK TOPOLOGY
# =============================================================================
println("\n=== PHASE C: NETWORK TOPOLOGY ===")

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

println("Nodes: $n_nodes | Edges: $(nrow(edges_df))")
println("In-degree:  min=$(minimum(in_degree)), max=$(maximum(in_degree)), mean=$(mean(in_degree))")
println("Out-degree: min=$(minimum(out_degree)), max=$(maximum(out_degree)), mean=$(mean(out_degree))")
println("Total:      min=$(minimum(total_degree)), max=$(maximum(total_degree)), mean=$(mean(total_degree))")
println("Isolated nodes: $(length(isolated)) of $n_nodes")

# Connected components (Union-Find)
parent = collect(0:n_nodes-1)
function find_root(x)
    while parent[x+1] != x
        parent[x+1] = parent[parent[x+1]+1]
        x = parent[x+1]
    end
    return x
end
function union_nodes!(a, b)
    ra, rb = find_root(a), find_root(b)
    if ra != rb
        parent[rb+1] = ra
    end
end

for row in eachrow(edges_df)
    union_nodes!(row.id_edge_from, row.id_edge_to)
end

component_sizes = Dict{Int, Int}()
for i in 0:n_nodes-1
    r = find_root(i)
    component_sizes[r] = get(component_sizes, r, 0) + 1
end

comp_sizes = sort(collect(values(component_sizes)), rev=true)
println("Components: $(length(comp_sizes)), Largest: $(maximum(comp_sizes))")
println("Top 5 sizes: $(comp_sizes[1:min(5,end)])")

# Node type breakdown
println("\n--- Node Type Breakdown ---")
for t in unique(skipmissing(nodes_df.node_type))
    subset = filter(r -> r.node_type == t, nodes_df)
    ids = subset.id_node
    degs = total_degree[ids .+ 1]
    @printf("  %-10s: count=%3d, mean_degree=%.1f\n", t, nrow(subset), mean(degs))
end

# Region breakdown
println("\n--- Region Breakdown ---")
for r in unique(skipmissing(nodes_df.region))
    subset = filter(rw -> rw.region == r, nodes_df)
    ids = subset.id_node
    degs = total_degree[ids .+ 1]
    @printf("  %-10s: count=%3d, mean_degree=%.1f\n", r, nrow(subset), mean(degs))
end

# Figure 4: Degree Distribution
p4 = histogram(total_degree, bins=0:maximum(total_degree), xlabel="Total Degree", ylabel="Count",
    title="Node Degree Distribution", color=:steelblue)
savefig(p4, "data/figures/degree_distribution.png")
println("\nSaved: data/figures/degree_distribution.png")

# Figure 5: In-Degree vs Out-Degree
p5 = scatter(in_degree, out_degree, xlabel="In-Degree", ylabel="Out-Degree",
    title="In-Degree vs Out-Degree", alpha=0.6, color=:teal, markersize=4)
savefig(p5, "data/figures/in_out_degree.png")
println("Saved: data/figures/in_out_degree.png")

# Figure 6: Component Sizes
p6 = histogram(comp_sizes, bins=20, xlabel="Component Size", ylabel="Count",
    title="Connected Component Sizes", color=:orange)
savefig(p6, "data/figures/component_sizes.png")
println("Saved: data/figures/component_sizes.png")

# =============================================================================
# PHASE D: NODE-GRID INTEGRATION
# =============================================================================
println("\n=== PHASE D: NODE-GRID INTEGRATION ===")

lats = nodes_df.latitude
lons = nodes_df.longitude

lat_idx = [nearest_grid_idx(l, lat) for l in lats]
lon_idx = [nearest_grid_idx(l, lon) for l in lons]

println("Grid index mapping: lat_idx=$(extrema(lat_idx)), lon_idx=$(extrema(lon_idx))")

# Elevation residual: node vs grid
# NOTE: NCDatasets uses FILE dimension order: (lon, lat) for 2D, (lon, lat, alt) for 3D
grid_elev_at_nodes = [elevation[lon_idx[i], lat_idx[i]] for i in eachindex(lats)]
node_elev = nodes_df.elevation
resid_elev = node_elev .- grid_elev_at_nodes

println("\n--- Elevation Residual (node - grid) ---")
println("  Mean bias: $(round(mean(resid_elev), digits=2)) m")
println("  RMSE: $(round(sqrt(mean(resid_elev.^2)), digits=2)) m")
println("  Std: $(round(std(resid_elev), digits=2)) m")

# Temperature residual: measured vs grid surface (alt level 9, index 10)
grid_temp_at_nodes = [temperature[lon_idx[i], lat_idx[i], 10] for i in eachindex(lats)]
node_temp = nodes_df.measured_temp
valid_temp = .!isnan.(node_temp) .& .!isnan.(grid_temp_at_nodes)
resid_temp = node_temp[valid_temp] .- grid_temp_at_nodes[valid_temp]

println("\n--- Temperature Residual (measured - grid_surface) ---")
println("  Valid pairs: $(count(valid_temp)) of $(length(node_temp))")
println("  Mean bias: $(round(mean(resid_temp), digits=2)) K")
println("  RMSE: $(round(sqrt(mean(resid_temp.^2)), digits=2)) K")
println("  Std: $(round(std(resid_temp), digits=2)) K")

# Residual by region
println("\n--- Residual by Region ---")
for r in unique(skipmissing(nodes_df.region))
    idx_r = findall(==(r), nodes_df.region)
    valid_r = valid_temp[idx_r]
    if count(valid_r) > 0
        rt = resid_temp[findall(valid_r)]
        @printf("  %-10s: n=%3d, mean_resid=%6.2f K, RMSE=%6.2f K\n",
            r, count(valid_r), mean(rt), sqrt(mean(rt.^2)))
    end
end

# Figure 7: Elevation Distribution (residual is 0 for synthetic data)
p7 = histogram(nodes_df.elevation, bins=30, xlabel="Node Elevation (m)", ylabel="Count",
    title="Node Elevation Distribution", color=:purple)
savefig(p7, "data/figures/elev_residual_hist.png")
println("\nSaved: data/figures/elev_residual_hist.png")

# Figure 8: Temperature Residual Histogram
p8 = histogram(resid_temp, bins=30, xlabel="Temperature Residual (K)", ylabel="Count",
    title="Temperature Residual (measured - grid)", color=:orange)
vline!([mean(resid_temp)], label="Mean=$(round(mean(resid_temp), digits=1)) K", linewidth=2, color=:red)
savefig(p8, "data/figures/temp_residual_hist.png")
println("Saved: data/figures/temp_residual_hist.png")

# Figure 9: Node Map
p9 = scatter(lons, lats, marker_z=node_elev,
    xlabel="Longitude", ylabel="Latitude", title="Nodes Colored by Elevation",
    colorbar=true, markersize=5, color=:viridis)
savefig(p9, "data/figures/node_map.png")
println("Saved: data/figures/node_map.png")

# =============================================================================
# PHASE E: EDGE ANALYSIS
# =============================================================================
println("\n=== PHASE E: EDGE ANALYSIS ===")

dist = edges_df.distance_km
weight = edges_df.weight
elev_change = edges_df.elevation_change
terrain_factor = edges_df.terrain_factor

println("--- Distance ---")
println("  Min: $(round(minimum(dist), digits=2)) | Max: $(round(maximum(dist), digits=2)) | Mean: $(round(mean(dist), digits=2)) km")

println("\n--- Weight ---")
println("  Min: $(round(minimum(weight), digits=2)) | Max: $(round(maximum(weight), digits=2)) | Mean: $(round(mean(weight), digits=2))")

corr_dw = cor(dist, weight)
println("\n--- Weight vs Distance ---")
println("  Correlation: $(round(corr_dw, digits=4))")
println("  Edges with weight == distance: $(count(==(0), dist .- weight)) of $(nrow(edges_df))")

# Elevation change
uphill = count(>(0), elev_change)
downhill = count(<(0), elev_change)
flat = count(==(0), elev_change)
println("\n--- Elevation Change ---")
println("  Uphill: $uphill ($(round(100*uphill/nrow(edges_df), digits=1))%)")
println("  Downhill: $downhill ($(round(100*downhill/nrow(edges_df), digits=1))%)")
println("  Flat: $flat ($(round(100*flat/nrow(edges_df), digits=1))%)")

# Terrain factor
println("\n--- Terrain Factor ---")
println("  Min: $(round(minimum(terrain_factor), digits=3)) | Max: $(round(maximum(terrain_factor), digits=3))")
println("  Mean: $(round(mean(terrain_factor), digits=3))")
println("  Flat (==1.0): $(count(==(1.0), terrain_factor))")

# Weight = distance × terrain_factor (verified: correlation = 1.0)
nonzero = dist .> 0
ratio = weight[nonzero] ./ dist[nonzero]
corr_tf = cor(terrain_factor[nonzero], ratio)
println("\n--- Weight = Distance × Terrain Factor ---")
println("  Corr(terrain_factor, weight/distance): $(round(corr_tf, digits=4))")

# Figure 10: Weight vs Distance
p10 = scatter(dist, weight, xlabel="Distance (km)", ylabel="Weight",
    title="Weight vs Distance (r=$(round(corr_dw, digits=2)))", alpha=0.4, color=:coral, markersize=3)
savefig(p10, "data/figures/weight_vs_distance.png")
println("\nSaved: data/figures/weight_vs_distance.png")

# Figure 11: Terrain Factor Distribution (log scale)
tf = edges_df.terrain_factor
p11 = histogram(log10.(tf[tf .> 0]), bins=30, xlabel="log10(Terrain Factor)", ylabel="Count",
    title="Terrain Factor Distribution (log scale)", color=:green)
savefig(p11, "data/figures/terrain_factor_dist.png")
println("Saved: data/figures/terrain_factor_dist.png")

# =============================================================================
# SUMMARY
# =============================================================================
println("\n=== ALL PHASES COMPLETE ===")
println("Figures saved to data/figures/:")
for f in readdir("data/figures", join=true)
    println("  $f ($(round(stat(f).size / 1024, digits=0)) KB)")
end
