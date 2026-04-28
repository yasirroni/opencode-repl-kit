function result = filterRange(data, column, min_val, max_val)
    % filterRange - Filter data by a range on a column.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or ignored (for numeric data).
    %   min_val: Minimum value (inclusive).
    %   max_val: Maximum value (inclusive).
    %
    % Returns:
    %   Filtered array (same type as input).

    if isempty(data)
        result = data;
        return;
    end

    if isstruct(data)
        values = [data.(column)];
    else
        values = data;
    end

    mask = ~isnan(values) & (values >= min_val) & (values <= max_val);
    result = data(mask);
end
